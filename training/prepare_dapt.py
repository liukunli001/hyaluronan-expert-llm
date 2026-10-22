#!/usr/bin/env python3
"""Build the DAPT (continued pretraining) corpus from corpus_v1.jsonl.

- Excludes the bench hold-out papers (eval/holdout_pmcids.txt).
- Core-set selection (default): rank papers by subfield relevance
  (keyword hits in title/first 4k chars + review bonus), then take papers
  until the estimated-token budget is hit. --all uses every non-holdout paper.
- General replay is NOT baked in here; dapt.py mixes a FineWeb-Edu
  sample at load time (--replay-frac), so ratios stay adjustable.
- MinHash near-duplicate removal (word 5-gram shingles over the first
  20k chars; pairs with estimated Jaccard >= --dup-threshold lose the
  lower-scored paper). --no-dedup skips it.
Outputs: data/processed/dapt_corpus.jsonl {pmcid, year, text} and
  data/processed/dapt_anneal.jsonl - the high-quality subset (reviews and
  top-scored papers, ~--anneal-frac of the budget) that dapt.py appends
  at the tail of training as the annealing phase.
"""
import json, pathlib, re, argparse, collections, zlib
import numpy as np

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

# --- MinHash near-duplicate detection -------------------------------------
_PERMS = 64
_rng = np.random.default_rng(42)
_A = _rng.integers(1, 2**62, size=_PERMS, dtype=np.uint64) | np.uint64(1)
_B = _rng.integers(0, 2**62, size=_PERMS, dtype=np.uint64)
_POW = np.uint64(1099511628211) ** np.arange(5, dtype=np.uint64)
_word_hash_cache = {}

def _signature(text):
    words = re.findall(r"[a-z0-9]+", text[:20000].lower())
    if len(words) < 5:
        return None
    h = []
    for w in words:
        v = _word_hash_cache.get(w)
        if v is None:
            v = zlib.crc32(w.encode())
            _word_hash_cache[w] = v
        h.append(v)
    w = np.array(h, dtype=np.uint64)
    from numpy.lib.stride_tricks import sliding_window_view
    shingles = (sliding_window_view(w, 5) * _POW).sum(axis=1)
    return (shingles[:, None] * _A[None, :] + _B[None, :]).min(axis=0)

def near_dup_drops(rows, scores, threshold=0.8, bands=16):
    sigs = [_signature(r["text"]) for r in rows]
    rows_per_band = _PERMS // bands
    buckets = collections.defaultdict(list)
    for i, s in enumerate(sigs):
        if s is None:
            continue
        for b in range(bands):
            key = (b, s[b * rows_per_band:(b + 1) * rows_per_band].tobytes())
            buckets[key].append(i)
    dropped = set()
    for idxs in buckets.values():
        for x in range(len(idxs)):
            for y in range(x + 1, len(idxs)):
                i, j = idxs[x], idxs[y]
                if i in dropped or j in dropped:
                    continue
                if float((sigs[i] == sigs[j]).mean()) >= threshold:
                    dropped.add(i if scores[i] < scores[j] else j)
    return dropped

ANNEAL_OUT = ROOT / "data" / "processed" / "dapt_anneal.jsonl"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token-budget", type=float, default=60e6, help="est tokens (chars/3.5)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no-dedup", action="store_true")
    ap.add_argument("--dup-threshold", type=float, default=0.8)
    ap.add_argument("--anneal-frac", type=float, default=0.15,
                    help="share of the token budget reserved for the anneal subset")
    a = ap.parse_args()
    holdout = set(HOLDOUT.read_text().split()) if HOLDOUT.exists() else set()
    rows, n_hold = [], 0
    with open(CORPUS, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r["pmcid"] in holdout:
                n_hold += 1; continue
            rows.append(r)
    if not a.no_dedup:
        dropped = near_dup_drops(rows, [score(r) for r in rows], a.dup_threshold)
        rows = [r for i, r in enumerate(rows) if i not in dropped]
        print(f"near-dup removed: {len(dropped)}")
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
    # Anneal subset: reviews first, then top scores, up to anneal-frac of budget.
    anneal, a_chars = [], 0
    anneal_budget = chars * a.anneal_frac
    for r in picked:  # picked is already score-sorted, reviews boosted in score
        if a_chars >= anneal_budget:
            break
        if "review" in (r["title"] or "").lower() or score(r) >= 5:
            anneal.append(r); a_chars += r["n_chars"]
    with open(ANNEAL_OUT, "w", encoding="utf-8") as fh:
        for r in anneal:
            fh.write(json.dumps({"pmcid": r["pmcid"], "year": r["year"], "text": r["text"]},
                                ensure_ascii=False) + "\n")
    print(f"holdout excluded: {n_hold} | papers picked: {len(picked)} / {len(rows)}")
    print(f"chars: {chars:,} | est tokens: {chars/3.5:,.0f} -> {OUT}")
    print(f"anneal subset: {len(anneal)} papers | est tokens: {a_chars/3.5:,.0f} -> {ANNEAL_OUT}")

if __name__ == "__main__":
    main()
