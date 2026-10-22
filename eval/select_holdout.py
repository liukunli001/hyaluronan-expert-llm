#!/usr/bin/env python3
"""Select ~30 hold-out papers from the cleaned corpus.

These papers are reserved for paper-grounded bench items and are EXCLUDED from
DAPT training data, the SFT generation pool, and the closed-book RAG index.
Selection: review-type papers (title/journal heuristics) spread across the six
subfields and across decades, deterministic (sorted by pmcid, evenly spaced).
Output: eval/holdout_pmcids.txt (one PMCID per line) + prints a summary.
"""
import json, pathlib, re, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "processed" / "corpus_v1.jsonl"
OUT = ROOT / "eval" / "holdout_pmcids.txt"
SUB = {"synthesis_modification": r"synthes|modif|conjugat|derivati|methacrylat|crosslink",
       "cd44_signaling": r"CD44|RHAMM|LYVE-1|receptor",
       "nano_delivery": r"nanoparticle|drug delivery|micelle|liposom|targeted delivery",
       "hydrogel_scaffold": r"hydrogel|scaffold|tissue engineer|wound",
       "cancer": r"cancer|tumor|tumour|carcinoma|metastas",
       "mol_weight": r"molecular weight|low molecular|high molecular|oligosaccharide"}

def main():
    rows = []
    with open(CORPUS, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            t = (r["title"] or "").lower()
            if "hyalur" in t and ("review" in t or "overview" in t or "advances in" in t or "progress in" in t):
                rows.append(r)
    print("review-type candidates:", len(rows))
    picked, per = [], collections.Counter()
    # round-robin across subfields so the hold-out covers the domain
    buckets = collections.defaultdict(list)
    for r in sorted(rows, key=lambda x: x["pmcid"]):
        head = (r["title"] + " " + r["text"][:2000])
        for name, pat in SUB.items():
            if re.search(pat, head, re.I):
                buckets[name].append(r); break
    names = list(SUB)
    i = 0
    seen = set()
    while len(picked) < 30 and any(buckets[n] for n in names):
        n = names[i % len(names)]; i += 1
        if buckets[n]:
            r = buckets[n].pop(0)
            if r["pmcid"] not in seen:
                seen.add(r["pmcid"]); picked.append(r); per[n] += 1
    OUT.write_text("\n".join(r["pmcid"] for r in picked) + "\n", encoding="utf-8")
    print("picked:", len(picked), dict(per))
    for r in picked:
        print(r["pmcid"], r["year"], r["title"][:90])

if __name__ == "__main__":
    main()
