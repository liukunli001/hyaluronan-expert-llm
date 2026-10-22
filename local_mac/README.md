# Local Mac route (Apple Silicon, MLX)

Alternative to renting a GPU: train and evaluate on your own Mac with
[mlx-lm](https://github.com/ml-explore/mlx-lm). Read the trade-offs first -
this route changes the recipe, it does not just move it.

## What changes vs the GPU route
- **LoRA instead of full-parameter training.** Full FT of an 8B does not
  fit a Mac's unified memory with optimizer states; LoRA (rank 64, all
  layers) is the practical ceiling. Domain uptake is somewhat weaker and
  the honest label is "LoRA domain adaptation", not the plan's headline
  full-parameter continued pretraining.
- **Smaller DAPT budget.** At Mac training speeds (~100-400 tok/s for
  LoRA on an 8B, chip-dependent), the full 60M-token x 2-epoch run would
  take weeks. The local converter defaults to a **12M-token** set
  (anneal papers first, then the top-scored core) - still several
  overnight runs. SFT (25k short examples) is a few hours to overnight.
- **Eval is slower** (per-question generation, ~20-60 min for 240 items)
  but uses the identical grading code as the vLLM runner.

## Memory tiers (unified memory)
| RAM | Route |
|---|---|
| 16GB | Inference of the 4-bit model + demo only; training not recommended |
| 32GB | QLoRA on the 4-bit base (mlx-community/Qwen3-8B-Base-4bit) |
| 64GB | bf16 LoRA workable; 4-bit comfortable and faster |
| 128GB | bf16 LoRA with large batches; full FT still not advised here |

## Setup & commands (from the repo root)
```bash
# Step 0 - preflight: detects chip + unified memory itself, picks the
# tier below, and writes local_mac/resolved_config.json with the exact
# model id / batch / commands for this machine (read-only, no installs)
python3 local_mac/preflight_mac.py

pip install mlx-lm
python3 local_mac/prepare_local_data.py            # -> data/dapt_mlx/, data/sft_mlx/

# S1 baseline (base model, no training yet)
python3 local_mac/run_eval_mlx.py --model Qwen/Qwen3-8B-Base --tag base-mac

# S2 DAPT-LoRA (bf16 base on 64GB+; swap in the 4bit repo id on 32GB)
mlx_lm.lora --model Qwen/Qwen3-8B-Base --data data/dapt_mlx --train \
  --fine-tune-type lora --config local_mac/lora_config.yaml \
  --batch-size 1 --grad-accumulation-steps 16 --learning-rate 1e-4 \
  --iters 4000 --save-every 500 --adapter-path runs/dapt-lora-mac

# S3 SFT-LoRA on top (after the teacher step produced sft_train.jsonl)
mlx_lm.lora --model Qwen/Qwen3-8B-Base --data data/sft_mlx --train \
  --fine-tune-type lora --config local_mac/lora_config.yaml \
  --adapter-path runs/sft-lora-mac --iters 1500 --learning-rate 1e-4

# Eval a trained adapter
python3 local_mac/run_eval_mlx.py --model Qwen/Qwen3-8B-Base \
  --adapter-path runs/dapt-lora-mac --tag dapt-lora-mac
```

## The hybrid (keeps the original headline recipe)
Rent the 96GB card only for DAPT full FT (~3.5 h, ~$9) and do baseline
eval prep, SFT data generation, RAG and all analysis locally. If the
application story ("full-parameter continued pretraining with TRL")
matters more than ~$10, this is the better trade.
