#!/usr/bin/env python3
"""HA-Expert-Bench runner (S1 baseline + S6 ablation).

Grading policy (saves judge budget, keeps numbers defensible):
- mcq / quantitative: graded automatically (exact letter / numeric match).
- open / trap: graded by an LLM judge against the verified answer key.
  Requires JUDGE_API_KEY (or TEACHER_API_KEY); without a key those items
  are written out as "ungraded" instead of being silently scored.
- Iteration uses --split dev (a stratified 25%); reported numbers should
  come from --split final or all on the Kunli-verified bench file.

Ablation cells (S6): base | base+rag | dapt+sft | dapt+sft+rag
  python3 run_eval.py --model Qwen/Qwen3-8B-Base --tag base
  python3 run_eval.py --model Qwen/Qwen3-8B-Base --tag base+rag --rag
  python3 run_eval.py --model ../training/runs/sft-v1/final --tag sft
  python3 run_eval.py --model ../training/runs/sft-v1/final --tag sft+rag --rag

Runs on the GPU box (vLLM). Results land in eval/results/<tag>.jsonl with
a printed summary (overall + per category)."""
import argparse, json, os, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent

def pick_split(items, split):
    if split == "all":
        return items
    by_cat = {}
    for it in items:
        by_cat.setdefault(it["category"], []).append(it)
    dev, final = [], []
    for cat in sorted(by_cat):
        for i, it in enumerate(sorted(by_cat[cat], key=lambda x: x["id"])):
            (dev if i % 4 == 0 else final).append(it)
    return dev if split == "dev" else final

def numbers(text):
    out = []
    for m in re.findall(r"-?\d[\d,]*\.?\d*", text.replace(",", "")):
        try:
            out.append(float(m))
        except ValueError:
            pass
    return out

def grade_auto(item, resp):
    exp = item["draft_answer"]
    if item["type"] == "mcq":
        m = re.match(r"\s*([A-D])", exp)
        want = m.group(1) if m else None
        got = re.search(r"\b([A-D])\b", resp)
        return want is not None and got is not None and got.group(1) == want
    if item["type"] == "quantitative":
        rng = re.search(r"(\d[\d,]*\.?\d*)\s*[-–~]\s*(\d[\d,]*\.?\d*)", exp)
        got = numbers(resp)
        if not got:
            return False
        if rng:
            lo, hi = float(rng.group(1).replace(",", "")), float(rng.group(2).replace(",", ""))
            return any(lo * 0.95 <= g <= hi * 1.05 for g in got)
        want = numbers(exp)
        if not want:
            return None  # cannot auto-grade; defer to judge
        w = want[0]
        return any(abs(g - w) <= 0.05 * max(1.0, abs(w)) for g in got)
    return None

JUDGE_PROMPT = """You grade a candidate answer against the reference answer for a hyaluronan research question.
Question: {q}
Reference answer: {ref}
Candidate answer: {cand}
Reply with strict JSON {{"verdict": "correct"|"partial"|"wrong"}}.
"correct" = matches the reference on all key facts. "partial" = right direction, missing or imprecise on a key fact. "wrong" = contradicts the reference, affirms a false premise, or misses the point."""

def judge(item, resp):
    key = os.environ.get("JUDGE_API_KEY") or os.environ.get("TEACHER_API_KEY", "")
    if not key:
        return "ungraded"
    base = os.environ.get("TEACHER_API_BASE", "https://api.openai.com/v1")
    model = os.environ.get("JUDGE_MODEL", os.environ.get("TEACHER_MODEL", "gpt-5"))
    body = json.dumps({"model": model, "messages": [
        {"role": "user", "content": JUDGE_PROMPT.format(
            q=item["question"], ref=item["draft_answer"], cand=resp[:2000])}],
        "temperature": 0}).encode()
    req = urllib.request.Request(base + "/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + key,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            txt = json.loads(r.read())["choices"][0]["message"]["content"]
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0))["verdict"] if m else "ungraded"
    except Exception as e:
        print("judge error:", e, file=sys.stderr)
        return "ungraded"

def build_prompt(item, rag_ctx=""):
    q = item["question"]
    if item["type"] == "mcq" and item.get("options"):
        q += "\n" + "\n".join(item["options"]) + "\nAnswer with the letter (A, B, C, or D) first."
    if rag_ctx:
        q = ("Use the following literature excerpts, and cite them as [1], [2], ... "
             f"in your answer.\n\n{rag_ctx}\n\nQuestion: {q}")
    return q

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True, help="result file name, e.g. base, sft+rag")
    ap.add_argument("--bench", default=str(ROOT / "eval" / "bench_v1_draft.jsonl"))
    ap.add_argument("--split", choices=["all", "dev", "final"], default="all")
    ap.add_argument("--rag", action="store_true", help="prepend retrieved corpus context")
    ap.add_argument("--chat", action="store_true", help="use the model chat template")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-tokens", type=int, default=512)
    a = ap.parse_args()

    items = [json.loads(l) for l in open(a.bench, encoding="utf-8") if l.strip()]
    items = pick_split(items, a.split)
    if a.limit:
        items = items[:a.limit]
    print(f"bench items: {len(items)} (split={a.split})")

    retrieve = None
    if a.rag:
        sys.path.insert(0, str(ROOT / "rag"))
        try:
            from qa import retrieve  # S5 deliverable (rag/qa.py)
        except Exception:
            raise SystemExit("--rag needs rag/qa.py with retrieve() - built in S5.")

    from vllm import LLM, SamplingParams
    llm = LLM(model=a.model, dtype="bfloat16", gpu_memory_utilization=0.90)
    tok = llm.get_tokenizer()
    prompts = []
    for it in items:
        ctx = ""
        if retrieve is not None:
            hits = retrieve(it["question"], k=4)
            ctx = "\n\n".join(f"[{i+1}] {h}" for i, h in enumerate(hits))
        p = build_prompt(it, ctx)
        if a.chat:
            p = tok.apply_chat_template([{"role": "user", "content": p}],
                                        tokenize=False, add_generation_prompt=True)
        prompts.append(p)
    outs = llm.generate(prompts, SamplingParams(temperature=0.0,
                                                max_tokens=a.max_tokens))

    out_dir = ROOT / "eval" / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{a.tag}.jsonl"
    score = {"correct": 1.0, "partial": 0.5, "wrong": 0.0}
    tot, n_scored, by_cat = 0.0, 0, {}
    with open(out_path, "w", encoding="utf-8") as fh:
        for it, o in zip(items, outs):
            resp = o.outputs[0].text.strip()
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
