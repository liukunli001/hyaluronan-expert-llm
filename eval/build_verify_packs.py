#!/usr/bin/env python3
"""Build evidence packs for LLM verification of HA-Expert-Bench draft answers.

For each bench question, attach source evidence from the local corpus:
- if the question has source_pmcid: windows from that exact paper around the
  most question-relevant sentences;
- else: top passages from the whole corpus by keyword overlap (BM25-lite).

Output: eval/verify_packs.jsonl with {id, question, type, draft_answer,
options?, evidence: [{pmcid, text}], evidence_source}.
Verification itself is done by an LLM reading these packs - never from memory.
"""
import json, math, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "eval" / "bench_v1_draft.jsonl"
CORPUS = ROOT / "data" / "processed" / "corpus_v1.jsonl"
OUT = ROOT / "eval" / "verify_packs.jsonl"

STOP = set("what which how does do is are was were the a an of in on for to and or "
           "with without by at from as it its this that these those be been has have "
           "had can could should would may might than then so such into about".split())

def toks(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2 and w not in STOP]

def sentences(text):
    return re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))

def windows(text, qtoks, n=3, width=700):
    """Top-n text windows around the sentences most overlapping the question."""
    sents = sentences(text)
    scored = []
    for i, s in enumerate(sents):
        st = set(toks(s))
        scored.append((len(st & qtoks), i))
    scored.sort(reverse=True)
    picks = sorted(i for sc, i in scored[:n] if sc > 0)
    out = []
    for i in picks:
        seg = " ".join(sents[max(0, i - 1): i + 2])
        out.append(seg[:width])
    return out

def main():
    bench = [json.loads(l) for l in open(BENCH)]
    corpus = {}
    df = Counter()
    doc_toks = {}
    print("loading corpus...", file=sys.stderr)
    for l in open(CORPUS):
        r = json.loads(l)
        corpus[r["pmcid"]] = r
        t = toks(r["title"] + " " + r["text"][:4000])
        doc_toks[r["pmcid"]] = Counter(t)
        for w in set(t):
            df[w] += 1
    N = len(corpus)
    idf = {w: math.log(N / (c + 1)) + 1.0 for w, c in df.items()}

    packs = []
    for q in bench:
        qt = set(toks(q["question"] + " " + str(q.get("draft_answer", ""))))
        ev, src = [], ""
        sp = q.get("source_pmcid")
        if sp and sp in corpus:
            for w in windows(corpus[sp]["text"], qt):
                ev.append({"pmcid": sp, "text": w})
            src = "source_paper"
        if not ev:  # BM25-lite over title+lead of every paper
            scores = []
            for pm, cnt in doc_toks.items():
                s = sum(cnt[w] * idf.get(w, 1.0) for w in qt if w in cnt)
                if s > 0:
                    scores.append((s, pm))
            scores.sort(reverse=True)
            for _, pm in scores[:3]:
                for w in windows(corpus[pm]["text"], qt, n=2):
                    ev.append({"pmcid": pm, "text": w})
            src = "retrieved"
        packs.append({
            "id": q["id"], "category": q["category"], "type": q["type"],
            "question": q["question"], "draft_answer": q["draft_answer"],
            "options": q.get("options"), "evidence": ev[:5],
            "evidence_source": src,
        })
    with open(OUT, "w") as f:
        for p in packs:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    n_src = sum(1 for p in packs if p["evidence_source"] == "source_paper")
    n_noev = sum(1 for p in packs if not p["evidence"])
    print(f"packs: {len(packs)} | from source paper: {n_src} | no evidence: {n_noev}")

if __name__ == "__main__":
    main()
