# Training runbook (S1-S4, optimized recipe 2026-10-22)

Order: `prepare_dapt.py` -> `dapt.py` -> `build_sft_data.py` -> `sft.py` -> eval (`../eval/run_eval.py`).
SFT data generation and the RAG index build do not need the GPU - run them
in parallel with DAPT so the GPU never idles.

## Hardware recipe
- **Pod**: 1x RTX PRO 6000 (96GB, Runpod ~$2.49-2.59/h), container disk
  100GB (a full checkpoint is ~32GB; 50GB cannot hold two).
- Full FT of an 8B in bf16: weights 16GB + grads 16GB + **8-bit AdamW
  states ~16GB** + activations. With FA2 varlen flattening and gradient
  checkpointing OFF this fits in 96GB (and in 80GB with `--grad-ckpt`).
  `--optim adamw_torch_fused` needs ~64GB of optimizer states alone -
  only on multi-GPU/FSDP or bigger cards.
- LoRA path (`sft.py --lora`) also runs on a 24GB consumer card for debugging.
- Estimated wall time (8B, optimized recipe): DAPT ~3-3.5 h for
  2 epochs over the 60M-token core + 12% replay + anneal tail; SFT 25k
  examples ~1 h; vLLM eval ~0.5 h per model variant.

## Steps
```bash
pip install -r requirements.txt
python3 prepare_dapt.py                 # -> dapt_corpus.jsonl (60M core) + dapt_anneal.jsonl
python3 dapt.py --data ../data/processed/dapt_corpus.jsonl \
                --anneal-data ../data/processed/dapt_anneal.jsonl --out runs/dapt-v1
TEACHER_API_KEY=... python3 build_sft_data.py --n 15000   # -> data/processed/sft_train.jsonl
python3 sft.py --base runs/dapt-v1/final --data ../data/processed/sft_train.jsonl --out runs/sft-v1
```

## What the optimized recipe does differently
- `prepare_dapt.py`: MinHash near-duplicate removal (Jaccard >= 0.8 on
  word 5-grams) before core selection; writes the anneal subset
  (reviews + top-scored papers, ~15% of budget) separately.
- `dapt.py`: document-boundary chunking + FlashAttention-2 varlen
  flattening (no cross-document attention); epochs materialized in
  dataset order with a sequential sampler; anneal set appended last so
  the cosine tail trains on the best data; replay 12%; checkpoints
  every ~15M tokens (bench the mid-run checkpoint before spending the
  full budget); `--packing` restores the legacy block-packing path.
- `build_sft_data.py --type-weights quantitative=2,mechanism=1.5`:
  oversample the question types the S1 baseline is weakest on.
- `sft.py`: NEFTune noise on by default (`--neftune 5.0`, 0 disables);
  max_length 2048; gradient checkpointing off unless `--grad-ckpt`.

## Notes
- Hold-out papers (eval/holdout_pmcids.txt) are excluded from DAPT data
  and from the SFT passage pool by construction.
- Chat template: Qwen3 official template from the base repo; SFT uses
  assistant-only loss. Do not hand-edit the template - eval/serving reuse it.
- Every run saves to runs/<name>/final with the tokenizer; HF Space demo
  and vLLM eval load exactly that directory.
- Pod hygiene: checkpoints land on the container disk - copy
  runs/*/final (or push to HF Hub) before stopping the pod, and stop the
  pod as soon as a stage finishes; billing is per second of runtime.
