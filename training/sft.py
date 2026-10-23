#!/usr/bin/env python3
"""S3: SFT with TRL SFTTrainer on build_sft_data.py output.

  full FT : python3 sft.py --base runs/dapt-v1/final --data ../data/processed/sft_train.jsonl
  LoRA    : python3 sft.py --lora --base Qwen/Qwen3-8B-Base --data ...
Loss is computed on assistant responses only (assistant_only_loss with the
Qwen chat template)."""
import argparse
import torch
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="runs/sft-v1")
    ap.add_argument("--lora", action="store_true")
    ap.add_argument("--epochs", type=float, default=2.0)
    ap.add_argument("--lr", type=float, default=0.0, help="default: 1e-5 full FT, 1e-4 LoRA")
    ap.add_argument("--bsz", type=int, default=4)
    ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--neftune", type=float, default=5.0,
                    help="NEFTune noise alpha (0 disables); cheap SFT quality boost on small data")
    ap.add_argument("--grad-ckpt", action="store_true",
                    help="enable gradient checkpointing (smaller cards); off by default on 96GB")
    a = ap.parse_args()
    lr = a.lr or (1e-4 if a.lora else 1e-5)

    ds = load_dataset("json", data_files=a.data, split="train")
    import math
    total_steps = math.ceil(len(ds) / (a.bsz * a.accum)) * max(1, round(a.epochs))
    cfg = SFTConfig(
        output_dir=a.out,
        num_train_epochs=a.epochs,
        per_device_train_batch_size=a.bsz,
        gradient_accumulation_steps=a.accum,
        learning_rate=lr,
        lr_scheduler_type="cosine",
        warmup_steps=max(3, int(0.03 * total_steps)),  # transformers v5 dropped warmup_ratio
        bf16=True,
        gradient_checkpointing=a.grad_ckpt,
        gradient_checkpointing_kwargs={"use_reentrant": False} if a.grad_ckpt else None,
        neftune_noise_alpha=a.neftune if a.neftune > 0 else None,
        optim="adamw_bnb_8bit" if not a.lora else "adamw_torch",
        logging_steps=20,
        save_strategy="epoch",
        save_total_limit=2,
        report_to=[],
        seed=42,
        max_length=2048,
        assistant_only_loss=True,
        model_init_kwargs={"dtype": torch.bfloat16,
                           "attn_implementation": "flash_attention_2"},
    )
    peft_cfg = None
    if a.lora:
        peft_cfg = LoraConfig(r=64, lora_alpha=128, lora_dropout=0.05, bias="none",
                              task_type="CAUSAL_LM",
                              target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                              "gate_proj", "up_proj", "down_proj"])
    trainer = SFTTrainer(model=a.base, args=cfg, train_dataset=ds, peft_config=peft_cfg)
    trainer.train()
    trainer.save_model(a.out + "/final")
    print("saved:", a.out + "/final")

if __name__ == "__main__":
    main()
