#!/usr/bin/env python3
"""Second-pass judge grading for a run_eval.py results file.

run_eval grades mcq/quantitative automatically and leaves open/trap items
'ungraded' when no judge is reachable during generation (the generation
engine owns the GPU then). This pass grades the leftovers against the bench
answer key via an OpenAI-compatible judge endpoint (env: TEACHER_API_BASE,
TEACHER_API_KEY, JUDGE_MODEL) and writes <results>.graded.jsonl + a summary.

Scoring mirrors run_eval: correct=1.0, partial=0.5, wrong=0.0.
"""
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eval"))
from run_eval import judge  # noqa: E402  (anchored JUDGE_PROMPT, env-configured)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--bench", required=True)
    a = ap.parse_args()

    bench = {json.loads(l)["id"]: json.loads(l) for l in open(a.bench, encoding="utf-8") if l.strip()}
    rows = [json.loads(l) for l in open(a.results, encoding="utf-8") if l.strip()]
    score = {"correct": 1.0, "partial": 0.5, "wrong": 0.0}
    n_judged = 0
    for r in rows:
        if r["verdict"] == "ungraded":
            r["verdict"] = judge(bench[r["id"]], r["response"])
            n_judged += 1
            if n_judged % 50 == 0:
                print("judged", n_judged, flush=True)
    out = a.results.replace(".jsonl", ".graded.jsonl")
    with open(out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    tot, n, by_cat, by_type = 0.0, 0, {}, {}
    for r in rows:
        if r["verdict"] in score:
            tot += score[r["verdict"]]; n += 1
            for d, k in ((by_cat, r["category"]), (by_type, r["type"])):
                s = d.setdefault(k, [0.0, 0]); s[0] += score[r["verdict"]]; s[1] += 1
    print(f"== graded {a.results} (judge calls: {n_judged}) ==")
    if n:
        print(f"overall: {tot / n:.3f} over {n} graded items")
        for k in sorted(by_type):
            s, c = by_type[k]; print(f"  type {k}: {s / c:.3f} (n={c})")
        for k in sorted(by_cat):
            s, c = by_cat[k]; print(f"  cat {k}: {s / c:.3f} (n={c})")
    print("still ungraded:", len(rows) - n, "| results ->", out)


if __name__ == "__main__":
    main()
