#!/usr/bin/env python3
"""Mac preflight for the local MLX route: detect chip + unified memory,
pick the right precision/tier, and print copy-paste commands.

Why: the local route's only open question was "how much unified memory
does your Mac have?" - this script answers it by itself, so nobody has
to look it up. It changes nothing on the machine: read-only sysctl
queries plus one small JSON report written next to this script
(local_mac/resolved_config.json, or --out).

Run from the repo root:
    python3 local_mac/preflight_mac.py
Testing / manual override (e.g. detection failed):
    python3 local_mac/preflight_mac.py --mem-gb 64
"""
import argparse, json, pathlib, platform, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent

TIERS = [
    # (min_gb, name, model, precision, batch, grad_accum, tok/s range, verdict)
    (120, "128GB", "Qwen/Qwen3-8B-Base", "bf16 LoRA", 2, 8, (300, 500),
     "bf16 LoRA with larger batches; full FT still not advised."),
    (56, "64GB", "Qwen/Qwen3-8B-Base", "bf16 LoRA", 1, 16, (200, 400),
     "bf16 LoRA workable; 4-bit also fine and faster."),
    (24, "32GB", "mlx-community/Qwen3-8B-Base-4bit", "4-bit QLoRA", 1, 16, (100, 250),
     "QLoRA on the 4-bit base; bf16 will not fit comfortably."),
    (0, "16GB or less", "mlx-community/Qwen3-8B-Base-4bit", "4-bit inference only",
     1, 16, (0, 0),
     "Training not recommended at this size; use this Mac for inference/demo "
     "and the hybrid route (rent ~3.5h of GPU for DAPT, ~$9) for training."),
]


def sysctl(key):
    try:
        out = subprocess.run(["sysctl", "-n", key], capture_output=True,
                             text=True, timeout=10)
        return out.stdout.strip() or None
    except Exception:
        return None


def detect_mem_gb():
    raw = sysctl("hw.memsize")
    if raw and raw.isdigit():
        return round(int(raw) / (1024 ** 3))
    return None


def pick_tier(mem_gb):
    for tier in TIERS:
        if mem_gb >= tier[0]:
            return tier
    return TIERS[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mem-gb", type=float, default=None,
                    help="override detected unified memory (GB)")
    ap.add_argument("--out", default=str(HERE / "resolved_config.json"))
    ap.add_argument("--token-budget", type=float, default=12e6,
                    help="local DAPT token budget (default 12M, as in "
                         "prepare_local_data.py)")
    args = ap.parse_args()

    is_mac = sys.platform == "darwin"
    chip = sysctl("machdep.cpu.brand_string") if is_mac else None
    mem_gb = args.mem_gb if args.mem_gb is not None else detect_mem_gb()
    free_gb = round(shutil.disk_usage(str(HERE)).free / (1024 ** 3), 1)

    if mem_gb is None:
        print("Could not detect unified memory automatically.")
        print("Check: Apple menu > About This Mac > Memory, then re-run with")
        print("  python3 local_mac/preflight_mac.py --mem-gb <16|32|64|128>")
        return 1

    _, tier_name, model, precision, batch, accum, (lo, hi), verdict = pick_tier(mem_gb)
    trainable = lo > 0
    est = None
    if trainable:
        est = (round(args.token_budget / hi / 3600, 1),
               round(args.token_budget / lo / 3600, 1))

    report = {
        "platform": platform.platform(),
        "is_macos": is_mac,
        "chip": chip,
        "unified_memory_gb": mem_gb,
        "free_disk_gb_here": free_gb,
        "tier": tier_name,
        "model": model,
        "precision": precision,
        "batch_size": batch,
        "grad_accumulation_steps": accum,
        "trainable_locally": trainable,
        "dapt_token_budget": args.token_budget,
        "est_dapt_hours_range": est,
        "commands": {
            "setup": "pip install mlx-lm",
            "prepare_data": "python3 local_mac/prepare_local_data.py",
            "s1_baseline_eval": (
                "python3 local_mac/run_eval_mlx.py "
                f"--model {model} --tag base-mac"),
            "s2_dapt_lora": (
                f"mlx_lm.lora --model {model} --data data/dapt_mlx --train "
                "--fine-tune-type lora --config local_mac/lora_config.yaml "
                f"--batch-size {batch} --grad-accumulation-steps {accum} "
                "--learning-rate 1e-4 --iters 4000 --save-every 500 "
                "--adapter-path runs/dapt-lora-mac") if trainable else None,
        },
    }
    pathlib.Path(args.out).write_text(json.dumps(report, indent=2) + "\n")

    print(f"Chip:            {chip or 'unknown (not read on this OS)'}")
    print(f"Unified memory:  {mem_gb} GB  -> tier: {tier_name}")
    print(f"Free disk here:  {free_gb} GB"
          + ("  [warn: model + data need roughly 25 GB free]" if free_gb < 25 else ""))
    print(f"Route:           {precision} on {model}")
    print(f"Verdict:         {verdict}")
    if est:
        print(f"DAPT estimate:   {args.token_budget/1e6:.0f}M tokens at "
              f"{lo}-{hi} tok/s = about {est[0]}-{est[1]} hours "
              "(split across overnight runs; checkpoints every 500 iters)")
    print(f"\nReport written:  {args.out}")
    print("\nNext commands (from the repo root):")
    for k, v in report["commands"].items():
        if v:
            print(f"  # {k}\n  {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
