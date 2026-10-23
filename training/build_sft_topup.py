#!/usr/bin/env python3
"""Top-up pass for SFT data: more paragraphs per paper + rotated question
kinds, deduped against the existing sft_train.jsonl. Uses the fixed
first-JSON-object parser from build_sft_data (imported, not copied).
Output: data/processed/sft_topup.jsonl (same chat-messages format)."""
import json, re, random, argparse, pathlib, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_sft_data import teacher, grounded, TYPES, SYSTEM, CORPUS, HOLDOUT, ROOT

OUT = ROOT / "data" / "processed" / "sft_topup.jsonl"
MAIN = ROOT / "data" / "processed" / "sft_train.jsonl"

def passages4():
    holdout = set(HOLDOUT.read_text().split()) if HOLDOUT.exists() else set()
    with open(CORPUS, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r["pmcid"] in holdout:
                continue
            paras = [p.strip() for p in r["text"].split("\n") if 400 <= len(p.strip()) <= 2200]
            random.shuffle(paras)
            for p in paras[:4]:
                yield p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6600, help="additional pairs to add")
    ap.add_argument("--workers", type=int, default=48)
    a = ap.parse_args()
    random.seed(123)
    seen_q = set()
    for l in open(MAIN, encoding="utf-8"):
        q = json.loads(l)["messages"][1]["content"]
        seen_q.add(re.sub(r"[^a-z0-9]+", " ", q.lower()).strip()[:80])
    kinds = list(TYPES)
    tasks = []
    for i, p in enumerate(passages4()):
        # two kinds per passage, rotated away from a plain round-robin
        tasks.append((p, kinds[i % len(kinds)]))
        tasks.append((p, kinds[(i + 3) % len(kinds)]))
    random.shuffle(tasks)
    print("topup tasks:", len(tasks), "existing questions:", len(seen_q), flush=True)
    kept = 0
    out_fh = open(OUT, "w", encoding="utf-8")
    idx, window = 0, a.workers * 4
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        while idx < len(tasks) and kept < a.n:
            chunk = tasks[idx:idx + window]
            idx += len(chunk)
            futs = {ex.submit(teacher, p, k): p for p, k in chunk}
            for f in as_completed(futs):
                if kept >= a.n:
                    break
                try:
                    qa = f.result()
                except Exception as e:
                    print("teacher error:", e, flush=True); continue
                if not qa or not qa.get("question") or not qa.get("answer"):
                    continue
                key = re.sub(r"[^a-z0-9]+", " ", qa["question"].lower()).strip()[:80]
                if key in seen_q or not grounded(qa["answer"], futs[f]):
                    continue
                seen_q.add(key)
                rec = {"messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": qa["question"]},
                                    {"role": "assistant", "content": qa["answer"]}]}
                out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                out_fh.flush()
                kept += 1
                if kept % 500 == 0:
                    print("kept", kept, flush=True)
    out_fh.close()
    print("topup kept:", kept, "->", OUT)

if __name__ == "__main__":
    main()
