#!/usr/bin/env python3
"""Convert the pipeline data into mlx-lm format for local Mac training.

- DAPT (continued pretraining, LoRA): emits data/dapt_mlx/{train,valid}.jsonl
  in {"text": ...} format. Anneal papers come first, then the core corpus
  in score order, chunked to ~6k chars, until --token-budget is reached
  (default 12M est tokens - a realistic overnight-runs budget on a Mac;
  raise it if you have the patience / a faster chip).
- SFT: if data/processed/sft_train.jsonl exists (needs the teacher step),
  emits data/sft_mlx/{train,valid}.jsonl in {"messages": ...} format.

Run from the repo root:  python3 local_mac/prepare_local_data.py
"""
import argparse, json, pathlib, random

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"

def write_split(rows, out_dir, valid_frac=0.02, seed=42):
    rows = rows[:]
    random.Random(seed).shuffle(rows)
    n_valid = max(1, int(len(rows) * valid_frac))
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "train.jsonl", "w", encoding="utf-8") as fh:
        for r in rows[n_valid:]:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(out_dir / "valid.jsonl", "w", encoding="utf-8") as fh:
        for r in rows[:n_valid]:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{out_dir}: {len(rows) - n_valid} train / {n_valid} valid")

def chunks(text, size=6000):
    for i in range(0, len(text), size):
        piece = text[i:i + size].strip()
        if len(piece) >= 800:
            yield piece

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token-budget", type=float, default=12e6,
                    help="est tokens for the local DAPT set (anneal first)")
    a = ap.parse_args()
    budget_chars = a.token_budget * 3.5
    rows, chars = [], 0
    seen = set()  # anneal papers are a subset of the corpus - dedupe across files
    for name in ["dapt_anneal.jsonl", "dapt_corpus.jsonl"]:
        path = PROC / name
        if not path.exists():
            print("missing", path, "- run training/prepare_dapt.py first")
            return
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                if r["pmcid"] in seen:
                    continue
                seen.add(r["pmcid"])
                for piece in chunks(r["text"]):
                    if chars >= budget_chars:
                        break
                    rows.append({"text": piece})
                    chars += len(piece)
                if chars >= budget_chars:
                    break
        if chars >= budget_chars:
            break
    print(f"DAPT local set: {len(rows)} chunks, ~{chars / 3.5:,.0f} est tokens")
    write_split(rows, ROOT / "data" / "dapt_mlx")

    sft = PROC / "sft_train.jsonl"
    if sft.exists():
        rows = [json.loads(l) for l in open(sft, encoding="utf-8") if l.strip()]
        write_split(rows, ROOT / "data" / "sft_mlx")
    else:
        print("sft_train.jsonl not found yet (teacher step pending) - SFT data skipped")

if __name__ == "__main__":
    main()
