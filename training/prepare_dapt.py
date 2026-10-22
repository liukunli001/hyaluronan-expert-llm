#!/usr/bin/env python3
"""Build the DAPT (continued pretraining) corpus from corpus_v1.jsonl.

- Excludes the bench hold-out papers (eval/holdout_pmcids.txt).
- Core-set selection (default): rank papers by subfield relevance
  (keyword hits in title/first 4k chars + review bonus), then take papers
  until the estimated-token budget is hit. --all uses every non-holdout paper.
- 20% general replay is NOT baked in here; dapt.py mixes a FineWeb-Edu
  sample at load time (--replay-frac), so ratios stay adjustable.
Output: data/processed/dapt_corpus.jsonl {pmcid, year, text} + printed stats.
"""
import json, pathlib, re, argparse, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "processed" / "corpus_v1.jsonl"
HOLDOUT = ROOT / "eval" / "holdout_pmcids.txt"
OUT = ROOT / "data" / "processed" / "dapt_corpus.jsonl"
SUB = [r"synthes|modif|conjugat|derivati|methacrylat|crosslink",
       r"CD44|RHAMM|LYVE-1|receptor",
       r"nanoparticle|drug delivery|micelle|liposom|targeted delivery",
       r"hydrogel|scaffold|tissue engineer|wound",
       r"cancer|tumor|tumour|carcinoma|metastas",
       r"molecular weight|low molecular|high molecular|oligosaccharide"]
RX = [re.compile(p, re.I) for p in SUB]

def score(r):
    head = (r["title"] or "") + " " + r["text"][:4000]
    s = sum(1 for rx in RX if rx.search(head))
    if "review" in (r["title"] or "").lower():
        s += 1
    return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token-budget", type=float, default=60e6, help="est tokens (chars/3.5)")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    holdout = set(HOLDOUT.read_text().split()) if HOLDOUT.exists() else set()
    rows, n_hold = [], 0
    with open(CORPUS, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r["pmcid"] in holdout:
                n_hold += 1; continue
            rows.append(r)
    rows.sort(key=lambda r: (-score(r), r["pmcid"]))
    picked, chars = [], 0
    budget_chars = a.token_budget * 3.5
    for r in rows:
        if not a.all and chars >= budget_chars:
            break
        picked.append(r); chars += r["n_chars"]
    with open(OUT, "w", encoding="utf-8") as fh:
        for r in picked:
            fh.write(json.dumps({"pmcid": r["pmcid"], "year": r["year"], "text": r["text"]},
                                ensure_ascii=False) + "\n")
    print(f"holdout excluded: {n_hold} | papers picked: {len(picked)} / {len(rows)}")
    print(f"chars: {chars:,} | est tokens: {chars/3.5:,.0f} -> {OUT}")

if __name__ == "__main__":
    main()
