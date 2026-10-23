# Bench verification round 3 (S5b) — vector-index re-check of the 103 uncertain keys

Method (same evidence-anchored protocol as v2, better retrieval): for each of
the 103 questions whose v2 key stayed `uncertain`, an evidence pack of the
top-6 semantically retrieved corpus passages (Qwen3-Embedding-0.6B + FAISS
index, 636,959 chunks) was assembled (`rag/build_packs_v3.py`), and an LLM
verifier judged the draft key strictly against that pack — verified /
corrected (with the decisive evidence quoted) / still uncertain. Six parallel
verifier batches, 103/103 judged.

## Outcome

| v2 status | n | → v3 |
|---|---|---|
| verified | 118 | unchanged |
| corrected | 19 | unchanged |
| uncertain | 103 | **72 verified, 3 corrected, 28 still uncertain** |

Bench v3 totals (240 questions): **190 verified + 22 corrected = 212 keys
evidence-settled (88.3%)**; 28 remain uncertain drafts (11.7%).

Only **3 answer keys changed** in v3: **B22** and **F07** (quantitative) and
**G14** (trap). Re-scoring impact on the S6 results was checked explicitly:
B22/F07 auto-grades are identical under the v3 keys in all four cells;
G14's four saved responses were re-judged against the corrected key
(see `eval/results/s6-full-report.md` addendum).

Files: `eval/bench_v3.jsonl` (authoritative key set going forward),
`eval/verify_packs_v3.jsonl`, `eval/verify_out_v3/batch{1..6}.jsonl`.
