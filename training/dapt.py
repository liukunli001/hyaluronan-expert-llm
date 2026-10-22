#!/usr/bin/env python3
"""S2: domain-adaptive continued pretraining (DAPT) of Qwen3-8B-Base.

Optimized recipe (2026-10-22):
- Documents are tokenized into <=seq-len chunks (document boundaries kept);
  chunks are flattened into single rows with DataCollatorWithFlattening
  (FlashAttention-2 varlen), so no attention crosses document boundaries.
- Epochs are materialized into the dataset order (main corpus shuffled per
  epoch), then the ANNEAL set (prepare_dapt.py's high-quality subset) is
  appended UNSHUFFLED at the tail: the last steps of the cosine schedule
  train on the best data while LR decays to zero (annealing).
- A SequentialSampler preserves that order (no Trainer shuffle).
- Gradient checkpointing defaults OFF (fits on the 96GB RTX PRO 6000 /
  80GB H100 with 8-bit AdamW); --grad-ckpt re-enables it for smaller cards.
- Checkpoints are saved every --ckpt-tokens (default 15M) so a mid-run
  checkpoint can be bench-evaluated before the budget is spent.
- FineWeb-Edu replay fraction defaults to 0.12 (was 0.20).

  python3 dapt.py --data ../data/processed/dapt_corpus.jsonl \
                  --anneal-data ../data/processed/dapt_anneal.jsonl \
                  --out runs/dapt-v1
"""
import argparse
import torch
from datasets import Dataset, concatenate_datasets, load_dataset
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          DataCollatorWithFlattening, Trainer, TrainingArguments)
from torch.utils.data import SequentialSampler


class OrderedTrainer(Trainer):
    """Trainer that preserves dataset order (anneal tail must stay last)."""
    def _get_train_sampler(self, *args, **kwargs):
        return SequentialSampler(self.train_dataset)


def chunk_dataset(ds, tok, seq_len, num_proc=8):
    """Tokenize a text dataset and split documents into <=seq_len chunks."""
    def tok_fn(batch):
        return tok(batch["text"])
    ds = ds.map(tok_fn, batched=True, num_proc=num_proc,
                remove_columns=ds.column_names)

    def split(batch):
        out = []
        for ids in batch["input_ids"]:
            for i in range(0, len(ids), seq_len):
                piece = ids[i:i + seq_len]
                if len(piece) >= 128:
                    out.append(piece)
        return {"input_ids": out}
    return ds.map(split, batched=True, num_proc=num_proc,
                  remove_columns=ds.column_names)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen3-8B-Base")
    ap.add_argument("--data", required=True)
    ap.add_argument("--anneal-data", default="",
                    help="high-quality subset appended at the tail (annealing)")
    ap.add_argument("--out", default="runs/dapt-v1")
    ap.add_argument("--replay-frac", type=float, default=0.12,
                    help="fraction of FineWeb-Edu replay chunks mixed in")
    ap.add_argument("--seq-len", type=int, default=4096)
    ap.add_argument("--epochs", type=int, default=2,
                    help="epochs over the main corpus (anneal tail runs once)")
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--bsz", type=int, default=8, help="chunks per device step")
    ap.add_argument("--accum", type=int, default=16)
    ap.add_argument("--optim", default="adamw_bnb_8bit")
    ap.add_argument("--grad-ckpt", action="store_true",
                    help="enable gradient checkpointing (smaller cards)")
    ap.add_argument("--compile", action="store_true",
                    help="torch.compile (helps the --packing path most)")
    ap.add_argument("--packing", action="store_true",
                    help="legacy block packing instead of flattening")
    ap.add_argument("--ckpt-tokens", type=float, default=15e6,
                    help="save a checkpoint roughly every N tokens")
    ap.add_argument("--save-limit", type=int, default=3)
    ap.add_argument("--max-steps", type=int, default=-1)
    a = ap.parse_args()

    import importlib.util
    if importlib.util.find_spec("flash_attn") is None and not a.packing:
        print("flash_attn not installed -> fallback: --packing + SDPA attention")
        a.packing = True

    tok = AutoTokenizer.from_pretrained(a.base)
    raw = load_dataset("json", data_files=a.data, split="train")
    domain = chunk_dataset(raw, tok, a.seq_len)
    n_domain_chunks = len(domain)
    print(f"domain chunks: {n_domain_chunks}")

    parts = []
    if a.replay_frac > 0:
        target = int(n_domain_chunks * a.replay_frac / (1 - a.replay_frac))
        stream = load_dataset("HuggingFaceFW/fineweb-edu", name="sample-10BT",
                              split="train", streaming=True).shuffle(seed=42)
        texts, got = [], 0
        for x in stream:
            texts.append({"text": x["text"]})
            got += max(1, len(x["text"]) // (a.seq_len * 4))
            if got >= target:
                break
        replay = chunk_dataset(Dataset.from_list(texts), tok, a.seq_len,
                               num_proc=4)
        replay = replay.select(range(min(target, len(replay))))
        parts.append(replay)
        print(f"replay chunks: +{len(replay)}")

    main_ds = concatenate_datasets(parts + [domain]) if parts else domain
    epochs_ds = []
    for e in range(a.epochs):
        epochs_ds.append(main_ds.shuffle(seed=42 + e))
    train_ds = concatenate_datasets(epochs_ds)

    if a.anneal_data:
        anneal_raw = load_dataset("json", data_files=a.anneal_data, split="train")
        anneal = chunk_dataset(anneal_raw, tok, a.seq_len)
        train_ds = concatenate_datasets([train_ds, anneal])
        print(f"anneal chunks appended: +{len(anneal)}")

    if a.packing:  # legacy: regroup token stream into fixed blocks with labels
        def group(batch):
            concat = {k: sum(batch[k], []) for k in batch}
            total = (len(concat["input_ids"]) // a.seq_len) * a.seq_len
            out = {k: [v[i:i + a.seq_len] for i in range(0, total, a.seq_len)]
                   for k, v in concat.items()}
            out["labels"] = out["input_ids"].copy()
            return out
        train_ds = train_ds.map(group, batched=True, num_proc=8)
        collator = None
    else:
        collator = DataCollatorWithFlattening()

    tokens_per_step = a.bsz * a.accum * a.seq_len
    save_steps = max(50, int(a.ckpt_tokens / tokens_per_step))
    print(f"total chunks: {len(train_ds)} | ~tokens/step {tokens_per_step} "
          f"| save every {save_steps} steps")

    attn = ("flash_attention_2" if importlib.util.find_spec("flash_attn")
            else "sdpa")
    model = AutoModelForCausalLM.from_pretrained(
        a.base, dtype=torch.bfloat16, attn_implementation=attn)
    model.config.use_cache = False

    args = TrainingArguments(
        output_dir=a.out,
        num_train_epochs=1,  # epochs are materialized in the dataset order
        max_steps=a.max_steps,
        per_device_train_batch_size=a.bsz,
        gradient_accumulation_steps=a.accum,
        learning_rate=a.lr,
        lr_scheduler_type="cosine",
        warmup_steps=10,  # transformers v5 dropped warmup_ratio (~3% of ~290 steps)
        weight_decay=0.0,
        bf16=True,
        gradient_checkpointing=a.grad_ckpt,
        gradient_checkpointing_kwargs={"use_reentrant": False} if a.grad_ckpt else None,
        torch_compile=a.compile,
        use_liger_kernel=importlib.util.find_spec("liger_kernel") is not None,
        optim=a.optim,
        logging_steps=20,
        save_strategy="steps",
        save_steps=save_steps,
        save_total_limit=a.save_limit,
        report_to=[],
        seed=42,
        dataloader_num_workers=4,
    )
    trainer = OrderedTrainer(model=model, args=args, train_dataset=train_ds,
                             data_collator=collator)
    trainer.train()
    model.config.use_cache = True
    trainer.save_model(a.out + "/final")
    tok.save_pretrained(a.out + "/final")
    print("saved:", a.out + "/final")


if __name__ == "__main__":
    main()
