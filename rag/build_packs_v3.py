#!/usr/bin/env python3
"""S5b: build evidence packs for the 103 bench questions whose v2 answer key
stayed 'uncertain' (keyword retrieval had failed to surface decisive
evidence). Uses the FAISS vector index (top-6 chunks per question).
Output: eval/verify_packs_v3.jsonl {id, question, type, category,
draft_answer, evidence[6]}.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "rag"))
from qa import retrieve  # noqa: E402


def main():
    bench = [json.loads(l) for l in open(ROOT / "eval/bench_v2_verified.jsonl", encoding="utf-8") if l.strip()]
    todo = [r for r in bench if r.get("verify_status") == "uncertain"]
    print(f"uncertain questions: {len(todo)}", flush=True)
    out = open(ROOT / "eval/verify_packs_v3.jsonl", "w", encoding="utf-8")
    for i, r in enumerate(todo):
        hits = retrieve(r["question"], k=6)
        out.write(json.dumps({"id": r["id"], "question": r["question"],
                              "type": r["type"], "category": r["category"],
                              "draft_answer": r["answer"], "evidence": hits},
                             ensure_ascii=False) + "\n")
        out.flush()
        if (i + 1) % 20 == 0:
            print("packed", i + 1, flush=True)
    out.close()
    print("done ->", ROOT / "eval/verify_packs_v3.jsonl")


if __name__ == "__main__":
    main()
