#!/usr/bin/env python3
"""Build SFT data: teacher-generated HA Q&A grounded in corpus passages.

Requires a teacher API (OpenAI-compatible):
  TEACHER_API_KEY=...  TEACHER_MODEL=gpt-5 (default)  TEACHER_API_BASE=https://api.openai.com/v1
Passages come from the DAPT core corpus minus bench hold-out papers.
Grounding filter: an answer is kept only if enough of its content words
appear in the source passage (cheap hallucination screen; Kunli also
spot-checks 100 pairs). Output: data/processed/sft_train.jsonl in
chat-messages format {"messages": [system, user, assistant]}.
Optionally mix general instruction data: --general path/to/messages.jsonl --general-n 10000
"""
import json, os, re, random, argparse, urllib.request, pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "processed" / "dapt_corpus.jsonl"
HOLDOUT = ROOT / "eval" / "holdout_pmcids.txt"
OUT = ROOT / "data" / "processed" / "sft_train.jsonl"
BASE = os.environ.get("TEACHER_API_BASE", "https://api.openai.com/v1")
KEY = os.environ.get("TEACHER_API_KEY", "")
MODEL = os.environ.get("TEACHER_MODEL", "gpt-5")
SYSTEM = "You are a hyaluronan (hyaluronic acid) research expert. Answer accurately and concisely, grounded in the literature."
TYPES = {
    "factual": "Ask one specific factual question answerable only from this passage (a definition, an entity, a reported value).",
    "mechanism": "Ask one question about a mechanism or pathway described in this passage.",
    "comparison": "Ask one question contrasting two things the passage compares (e.g., high- vs low-molecular-weight HA).",
    "methods": "Ask one question about an experimental or synthesis method used in this passage.",
    "application": "Ask one question about a biomedical application described in this passage.",
    "quantitative": "Ask one question whose answer is a number or quantity stated in this passage.",
}
STOP = set("the a an of in on for and or to is are was were with by from as at it its this that be been has have had not no".split())

def teacher(passage, kind):
    prompt = (f"Passage from a hyaluronan research paper:\n\"\"\"\n{passage}\n\"\"\"\n\n"
              f"{TYPES[kind]} Then answer it using ONLY the passage. "
              "Reply with strict JSON: {\"question\": \"...\", \"answer\": \"...\"}. "
              "The answer must be self-contained (no 'the passage says').")
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0.7, "max_tokens": 700}).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + KEY,
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        txt = json.loads(r.read())["choices"][0]["message"]["content"]
    # Parse the FIRST complete JSON object and ignore any trailing text the
    # teacher appends (the old greedy-regex + json.loads died on 'Extra data').
    i = txt.find("{")
    if i < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(txt[i:])
        return obj
    except Exception:
        return None

def grounded(answer, passage):
    words = [w for w in re.findall(r"[a-z0-9][a-z0-9\-]+", answer.lower()) if w not in STOP]
    if not words:
        return False
    hit = sum(1 for w in words if w in passage.lower())
    return hit / len(words) >= 0.55

def passages():
    holdout = set(HOLDOUT.read_text().split()) if HOLDOUT.exists() else set()
    with open(CORPUS, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r["pmcid"] in holdout:
                continue
            paras = [p.strip() for p in r["text"].split("\n") if 400 <= len(p.strip()) <= 2200]
            random.shuffle(paras)
            for p in paras[:2]:
                yield p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=15000, help="target HA Q&A pairs")
    ap.add_argument("--general", default="", help="optional general messages jsonl to mix in")
    ap.add_argument("--general-n", type=int, default=10000)
    ap.add_argument("--type-weights", default="",
                    help="e.g. 'quantitative=2,mechanism=1.5' - oversample question types "
                         "the base model is weak on (from the S1 baseline breakdown)")
    ap.add_argument("--workers", type=int, default=48,
                    help="concurrent teacher calls (the teacher server batches them)")
    a = ap.parse_args()
    if not KEY:
        raise SystemExit("TEACHER_API_KEY not set - cannot call the teacher model.")
    random.seed(42)
    kept, seen_q = [], set()
    weights = {}
    for kv in a.type_weights.split(","):
        if "=" in kv:
            k, v = kv.split("=", 1)
            weights[k.strip()] = float(v)
    bag = []
    for k in TYPES:
        bag += [k] * max(1, round(weights.get(k, 1.0) * 10))
    # Materialize tasks in the same order/kind assignment as the sequential version.
    tasks = [(p, bag[i % len(bag)]) for i, p in enumerate(passages())]
    print("passage tasks:", len(tasks), flush=True)
    out_fh = open(OUT, "w", encoding="utf-8")

    def accept(qa, p):
        if not qa or not qa.get("question") or not qa.get("answer"):
            return
        key = re.sub(r"[^a-z0-9]+", " ", qa["question"].lower()).strip()[:80]
        if key in seen_q or not grounded(qa["answer"], p):
            return
        seen_q.add(key)
        rec = {"messages": [{"role": "system", "content": SYSTEM},
                            {"role": "user", "content": qa["question"]},
                            {"role": "assistant", "content": qa["answer"]}]}
        kept.append(rec)
        out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out_fh.flush()
        if len(kept) % 500 == 0:
            print("kept", len(kept), flush=True)

    # Bounded in-flight window: submit in chunks, harvest as calls complete,
    # stop as soon as the target is reached (surplus results are discarded).
    idx = 0
    window = a.workers * 4
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        while idx < len(tasks) and len(kept) < a.n:
            chunk = tasks[idx:idx + window]
            idx += len(chunk)
            futs = {ex.submit(teacher, p, k): p for p, k in chunk}
            for f in as_completed(futs):
                if len(kept) >= a.n:
                    break
                try:
                    accept(f.result(), futs[f])
                except Exception as e:
                    print("teacher error:", e, flush=True)
    out_fh.close()
    print("kept total:", len(kept), flush=True)
    if a.general:
        gen = [json.loads(l) for l in open(a.general, encoding="utf-8")][:a.general_n]
        kept += gen
        print("mixed general:", len(gen))
    random.shuffle(kept)
    with open(OUT, "w", encoding="utf-8") as fh:
        for r in kept:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("wrote", len(kept), "->", OUT)

if __name__ == "__main__":
    main()
