# S6 Full-Bench Report — HA-Expert-Bench (240 questions)

Run: 2026-10-22 night (PT), RunPod RTX PRO 6000. Four ablation cells,
greedy decoding (temperature 0, max 512 tokens).

## Protocol

- **Bench**: `bench_v2_verified.jsonl` — 240 questions (open 195, quantitative 20,
  trap 15, mcq 10), answer key evidence-verified against the corpus
  (118 verified, 19 corrected, 103 draft answers retained as uncertain).
- **Cells**: base = Qwen3-8B-Base; sft = DAPT (continued pretraining on 60M
  tokens of HA literature) + full-parameter SFT on 12,003 self-generated QA
  pairs; rag = FAISS retrieval (Qwen3-Embedding-0.6B, 636,959 chunks from
  12,306 papers, top-4 excerpts with citation markers). Holdout papers are
  excluded from training data and from the retrieval index.
- **Grading**: mcq/quantitative auto-graded (exact letter / numeric tolerance);
  open/trap graded by an LLM judge anchored to the verified reference answer
  (verdicts correct / partial / wrong = 1.0 / 0.5 / 0.0). Judge = the SFT
  model itself served locally ($0 API, per project decision) — a known
  limitation: the judge is one of the contestants. Anchoring to a fixed
  reference key (not free preference) mitigates but does not eliminate this.
- A retry pass re-judged items whose first-pass judge output was unparseable;
  overall scores moved by ≤0.004 (final values below).

## Results (final, after retry pass)

| Cell | Overall | n graded | MCQ (10) | Quantitative (20) | Open (195) | Trap (15) |
|---|---|---|---|---|---|---|
| base | **0.300** | 227 | 0.800 | 0.250 | 0.282 | 0.267 |
| DAPT+SFT | **0.601** | 217 | 0.900 | 0.300 | 0.631 | 0.500 |
| base+RAG | **0.710** | 238 | 0.900 | 0.450 | 0.719 | 0.867 |
| DAPT+SFT+RAG | **0.662** | 219 | 0.700 | 0.550 | 0.676 | 0.633 |

(Per-type scores from the first grading pass; retry pass changed only the
handful of previously ungraded items. Residual ungraded after retry:
base 13, sft 23, base+rag 2, sft+rag 21 — judge JSON failures.)

Auto-graded objective subset only (30 items): base 0.433, sft 0.500,
base+rag 0.600, sft+rag 0.600.

## Findings

1. **SFT doubles the base model** (0.300 → 0.601). The base model's signature
   failure — inventing follow-up questions instead of answering — disappears;
   open-question score rises 0.282 → 0.631.
2. **Retrieval is the largest single lever**, especially where parametric
   knowledge is unreliable: traps 0.267 → 0.867 on the base model. Both
   long-standing trap failures (G01 "HA is a protein polymer", G13 "HA
   solutions are Newtonian fluids") are corrected by **both** RAG cells.
3. **SFT and RAG are not additive here**: DAPT+SFT+RAG (0.662) trails
   base+RAG (0.710) on open and trap questions, despite winning quantitative
   (0.550, the best of any cell). Mechanism, visible in the outputs:
   - The SFT model never saw retrieved-context prompts in training. In
     5/240 sft+rag responses it collapses into citation-marker loops
     (e.g. G09: "[1] [4] [2] [3] …" repeated to the token limit) where the
     SFT-only and base+RAG answers are correct.
   - Self-distillation inherited the teacher's repetition habit: heavy
     repetition (a 30-char block repeated ≥5×) appears in 35/240 sft
     responses vs 10/240 base, 7/240 base+rag, 22/240 sft+rag.
   The fix is concrete future work: include RAG-format examples (question +
   retrieved excerpts + cited answer) in SFT data, filter repetitive teacher
   outputs before training, and/or decode with a repetition penalty.

## Trap detail (verdicts)

| ID | base | sft | base+rag | sft+rag |
|---|---|---|---|---|
| G01 | wrong | wrong | correct | correct |
| G02 | wrong | wrong | correct | wrong |
| G03 | wrong | wrong | correct | partial |
| G04 | partial | correct | correct | correct |
| G05 | partial | correct | correct | correct |
| G06 | partial | correct | correct | wrong |
| G07 | partial | correct | partial | partial |
| G08 | partial | correct | correct | correct |
| G09 | wrong | correct | partial | wrong |
| G10 | wrong | ungraded | partial | partial |
| G11 | wrong | wrong | correct | correct |
| G12 | correct | ungraded | correct | wrong |
| G13 | wrong | wrong | correct | correct |
| G14 | wrong | wrong | correct | correct |
| G15 | partial | partial | partial | correct |

## Samples

**G13 — "HA solutions are simple Newtonian fluids, so their viscosity is a
single constant, correct?"**
- sft: "Yes, HA solutions are simple Newtonian fluids, so their viscosity is
  a single constant." (then repeats the sentence) — wrong
- sft+rag: "No, HA solutions are not simple Newtonian fluids. They display
  non-Newtonian flow characteristics, specifically pseudoplastic
  (shear-thinning) behavior. This means that their viscosity decreases as
  shear rate increases." — correct

**G09 — "For joint injections, the highest-MW HA is always the best
choice, correct?"**
- sft: "No, the highest-MW HA is not always the best choice for joint
  injections. The choice of HA depends on the specific condition being
  treated…" — correct
- sft+rag: "[1] [4] [2] [3] [1] [4] [2] [3] …" (citation loop to the token
  limit) — wrong

## Caveats

- Judge = SFT model (self-judging), anchored to verified keys; treat
  cross-cell gaps of <0.02 as noise.
- MCQ n=10 — the sft+rag 0.700 vs 0.900 gap is two questions.
- 103 of 240 reference answers are evidence-uncertain drafts (bench v3
  re-verification with the vector index is the next step); scores against
  those items carry key risk.
- Greedy decoding throughout; repetition behavior is decode-sensitive.

## Addendum (2026-10-23): bench v3 re-verification — S6 scores unaffected

The 103 `uncertain` v2 keys were re-verified against top-6 vector-retrieved
evidence packs (S5b): 72 verified, 3 corrected, 28 remain uncertain; bench v3
has 212/240 keys evidence-settled. Only 3 keys changed (B22, F07, G14).
Re-scoring check: B22/F07 auto-grades identical under v3 keys in all 4 cells;
G14 re-judged against the corrected key in all 4 cells — verdicts unchanged
(wrong/wrong/correct/correct). **All headline scores in this report stand.**
