#!/usr/bin/env python3
"""S2: domain-adaptive continued pretraining (DAPT) of Qwen3-8B-Base.

Standard causal-LM training on the HA corpus (prepare_dapt.py output),
optionally mixed with a FineWeb-Edu replay slice to limit forgetting.
Runs on the GPU box (see training/README.md for the 1xH100-80GB recipe).

  python3 dapt.py --data ../data/processed/dapt_corpus.jsonl --out runs/dapt-v1
"""
import argparse, os
import torch
from datasets import load_dataset
from transformers import (AutoModelForCausalLM, AutoTokenizer, Trainer,
                          TrainingArguments)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen3-8B-Base")
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="runs/dapt-v1")
    ap.add_argument("--replay-frac", type=float, default=0.20,
                    help="fraction of FineWeb-Edu replay examples mixed in")
    ap.add_argument("--seq-len", type=int, default=4096)
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--bsz", type=int, default=4)
    ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--optim", default="adamw_bnb_8bit",
                    help="8-bit AdamW keeps full FT of 8B inside 80GB; use adamw_torch_fused on multi-GPU")
    a = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(a.base)
    ds = load_dataset("json", data_files=a.data, split="train")
    if a.replay_frac > 0:
        n_replay = int(len(ds) * a.replay_frac / (1 - a.replay_frac))
        replay = load_dataset("HuggingFaceFW/fineweb-edu", name="sample-10BT",
                              split="train", streaming=True)
        replay = replay.shuffle(seed=42).take(n_replay)
        from datasets import Dataset
        replay = Dataset.from_list([{"text": x["text"]} for x in replay])
        from datasets import concatenate_datasets
        ds = concatenate_datasets([ds, replay]).shuffle(seed=42)
        print(f"mixed replay: +{n_replay} general examples -> {len(ds)} total")

    def tokenize(batch):
        return tok(batch["text"])
    ds = ds.map(tokenize, batched=True, num_proc=8, remove_columns=ds.column_names)

    def group(batch):  # pack into seq-len blocks (standard HF recipe)
        concat = {k: sum(batch[k], []) for k in batch}
        total = (len(concat["input_ids"]) // a.seq_len) * a.seq_len
        out = {k: [v[i:i + a.seq_len] for i in range(0, total, a.seq_len)]
               for k, v in concat.items()}
        out["labels"] = out["input_ids"].copy()
        return out
    ds = ds.map(group, batched=True, num_proc=8)

    model = AutoModelForCausalLM.from_pretrained(
        a.base, torch_dtype=torch.bfloat16, attn_implementation="flash_attention_2")
    model.config.use_cache = False

    args = TrainingArguments(
        output_dir=a.out,
        num_train_epochs=a.epochs,
        per_device_train_batch_size=a.bsz,
        gradient_accumulation_steps=a.accum,
        learning_rate=a.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        weight_decay=0.0,
        bf16=True,
        gradient_checkpointing=True,
        optim=a.optim,
        logging_steps=20,
        save_strategy="epoch",
        save_total_limit=2,
        report_to=[],
        seed=42,
    )
    Trainer(model=model, args=args, train_dataset=ds).train()
    model.config.use_cache = True
    Trainer(model=model, args=args).save_model(a.out + "/final")
    tok.save_pretrained(a.out + "/final")
    print("saved:", a.out + "/final")

if __name__ == "__main__":
    main()
