#!/usr/bin/env python3
"""HA-Expert-Bench on a Mac (MLX backend) - same grading as eval/run_eval.py.

  python3 local_mac/run_eval_mlx.py --model Qwen/Qwen3-8B-Base --tag base-mac
  python3 local_mac/run_eval_mlx.py --model Qwen/Qwen3-8B-Base \
      --adapter-path runs/dapt-lora-mac --tag dapt-lora-mac

MCQ/quantitative items are auto-graded; open/trap items use the LLM judge
when JUDGE_API_KEY / TEACHER_API_KEY is set, else they are left "ungraded".
Results land in eval/results/<tag>.jsonl, identical schema to the vLLM runner.
"""
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eval"))
from run_eval import build_prompt, grade_auto, judge, pick_split  # noqa: E402

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--adapter-path", default="")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--bench", default=str(ROOT / "eval" / "bench_v1_draft.jsonl"))
    ap.add_argument("--split", choices=["all", "dev", "final"], default="all")
    ap.add_argument("--chat", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-tokens", type=int, default=512)
    a = ap.parse_args()

    items = [json.loads(l) for l in open(a.bench, encoding="utf-8") if l.strip()]
    items = pick_split(items, a.split)
    if a.limit:
        items = items[:a.limit]
    print(f"bench items: {len(items)} (split={a.split})")

    from mlx_lm import generate, load
    model, tok = load(a.model, adapter_path=a.adapter_path or None)

    out_dir = ROOT / "eval" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{a.tag}.jsonl"
    score = {"correct": 1.0, "partial": 0.5, "wrong": 0.0}
    tot, n_scored, by_cat = 0.0, 0, {}
    with open(out_path, "w", encoding="utf-8") as fh:
        for it in items:
            p = build_prompt(it)
            if a.chat and hasattr(tok, "apply_chat_template"):
                p = tok.apply_chat_template([{"role": "user", "content": p}],
                                            tokenize=False, add_generation_prompt=True)
            resp = generate(model, tok, prompt=p, max_tokens=a.max_tokens,
                            verbose=False).strip()
            auto = grade_auto(it, resp)
            if auto is True:
                verdict = "correct"
            elif auto is False:
                verdict = "wrong"
            else:
                verdict = judge(it, resp)
            fh.write(json.dumps({"id": it["id"], "category": it["category"],
                                 "type": it["type"], "verdict": verdict,
                                 "response": resp}, ensure_ascii=False) + "\n")
            fh.flush()
            if verdict in score:
                tot += score[verdict]; n_scored += 1
                c = by_cat.setdefault(it["category"], [0.0, 0])
                c[0] += score[verdict]; c[1] += 1
    print(f"== {a.tag} ({a.model}) ==")
    if n_scored:
        print(f"overall: {tot / n_scored:.3f} over {n_scored} graded items")
        for cat in sorted(by_cat):
            s, n = by_cat[cat]
            print(f"  {cat}: {s / n:.3f} (n={n})")
    print("ungraded:", len(items) - n_scored, "| results ->", out_path)

if __name__ == "__main__":
    main()
