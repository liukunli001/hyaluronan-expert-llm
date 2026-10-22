# HA-Expert-Bench — protocol

Goal: 240 questions whose answers are **100% verified by Kunli** (domain PhD).
Until an item is verified it stays `"status": "draft"` and is never used in a reported score.

## Composition (target)
| Category | n | Focus |
|---|---|---|
| A basics | 40 | structure, biosynthesis, degradation, sources |
| B receptors_signaling | 40 | CD44, RHAMM, HARE/Stabilin-2, LYVE-1, TLR |
| C mw_biology | 40 | HMW vs LMW signaling, tumor stroma, synthesis inhibitors |
| D chemistry_modification | 40 | EDC/NHS, methacrylation, thiolation, oxidation, crosslinkers |
| E nano_delivery | 40 | self-assembled HA NPs, CD44 targeting, conjugates, clearance |
| F clinical_quant | 25 | viscosupplementation, fillers, turnover numbers, MW measurement |
| G traps | 15 | plausible false premises the model must correct, not answer |

Types: open (majority), mcq, quantitative. Scoring: MCQ exact match; open answers
graded by a GPT-5-class judge against the verified answer key with a fixed rubric,
plus Kunli spot-checks of judge decisions on a 50-item sample.

## Anti-contamination rule
Items grounded in a specific paper record that paper's PMCID in `source_pmcid`;
those papers (~30) are excluded from the DAPT corpus, the SFT generation pool and
the RAG index used in the "closed-book" eval runs. Textbook-level items (batch 1,
`bench_draft.jsonl`) need no exclusion.

## Kunli's verification pass (est. 2-3 h total)
For each item: confirm the draft answer, fix it, or delete the item.
Only then does `status` become `"verified"`.

## Running the bench (`run_eval.py`)
- MCQ and quantitative items are auto-graded (no judge cost); open and
  trap items go to an LLM judge against the verified key
  (`JUDGE_API_KEY` or `TEACHER_API_KEY`).
- `--split dev` is a stratified 25% for iteration; reported numbers come
  from the verified file with `--split final` / `all`.
- S6 ablation cells: base, base+rag, dapt+sft, dapt+sft+rag (see the
  script header for the four commands).
