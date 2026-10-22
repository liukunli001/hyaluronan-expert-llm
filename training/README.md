# Training runbook (S1-S4)

Order: `prepare_dapt.py` -> `dapt.py` -> `build_sft_data.py` -> `sft.py` -> eval (../eval).

## Hardware recipe
- **DAPT / SFT full FT**: 1x H100 80GB (RunPod/Lambda ~$2.89-3.99/h).
  Full FT of an 8B in bf16: weights 16GB + grads 16GB + **8-bit AdamW states ~16GB**
  + activations (grad ckpt on) fits in 80GB. `--optim adamw_torch_fused` needs
  ~64GB of optimizer states alone - only on multi-GPU/FSDP or bigger cards.
- LoRA path (`sft.py --lora`) also runs on a 24GB consumer card for debugging.
- Estimated wall time (8B, seq 4096): DAPT 60M-token core set ~3-4 h; SFT 25k
  examples ~1 h. Eval with vLLM adds ~0.5 h per model variant.

## Steps
```bash
pip install -r requirements.txt
python3 prepare_dapt.py                 # -> data/processed/dapt_corpus.jsonl (holdout excluded)
python3 dapt.py --data ../data/processed/dapt_corpus.jsonl --out runs/dapt-v1
TEACHER_API_KEY=... python3 build_sft_data.py --n 15000   # -> data/processed/sft_train.jsonl
python3 sft.py --base runs/dapt-v1/final --data ../data/processed/sft_train.jsonl --out runs/sft-v1
```

## Notes
- Hold-out papers (eval/holdout_pmcids.txt) are excluded from DAPT data and
  from the SFT passage pool by construction.
- Chat template: Qwen3 official template from the base repo; SFT uses
  assistant-only loss. Do not hand-edit the template - eval/serving reuse it.
- Every run saves to runs/<name>/final with the tokenizer; HF Space demo and
  vLLM eval load exactly that directory.
