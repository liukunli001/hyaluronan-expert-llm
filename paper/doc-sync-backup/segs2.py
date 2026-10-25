# Round-2 sync: replacement segments per paragraph element index (current Doc).
# Each value: list of (style, text); style '' plain, 'B' bold, 'I' italic.
S = {}

S[4] = [
 ('', 'General-purpose LLMs handle specialized fields\' literatures unreliably: fluent answers, often wrong on quantitative details and confident even when a premise is false. We study one such field — hyaluronan (hyaluronic acid, HA) — and ask how far a single researcher can go, on under USD 50 of cloud compute, toward a '),
 ('I', 'trustworthy'),
 ('', ' domain model. We release (i) a corpus of 12,306 HA papers (~126M tokens); (ii) HA-Expert, a Qwen3-8B-Base model adapted in two stages — domain-adaptive continued pretraining (DAPT) on 60M tokens of the corpus, then full-parameter supervised fine-tuning (SFT) on 12,003 question–answer pairs it generated itself — optionally grounded at inference by retrieval over a 636,959-passage FAISS index; and (iii) HA-Expert-Bench: 240 questions whose reference answers evidence-restricted LLM verifiers confirmed or corrected (212 of 240), including 15 adversarial "trap" questions. In a four-cell ablation, SFT doubles the base model (0.300 → 0.601); retrieval is the largest single lever (base+RAG 0.710; traps 0.267 → 0.867); and SFT and RAG do '),
 ('B', 'not'),
 ('', ' compose additively (0.662): a model never trained on retrieved context collapses into citation-marker loops (5 of 240 responses) and inherits its teacher\'s repetition habit.'),
]

S[6] = [
 ('', 'Hyaluronan is a linear glycosaminoglycan of repeating β-1,4-glucuronic-acid / β-1,3-N-acetylglucosamine disaccharides. Practitioners\' knowledge — molecular-weight-dependent biology, receptor interactions, chemical modification, production, clinical dosing — is spread across thousands of chemistry, materials, and medical papers.'),
]

S[7] = [
 ('', 'General-purpose LLMs promise an interface to such a literature, but our probes found three systematic failures: '),
 ('I', 'behavior'),
 ('', ' (base model continued prompts with invented follow-up questions), '),
 ('I', 'epistemic stance'),
 ('', ' (assent to false premises — HA is a protein polymer; HA solutions are Newtonian fluids), and '),
 ('I', 'verifiability'),
 ('', ' (quantitative claims with no checkable source).'),
]

S[8] = [
 ('', 'We address them with the standard toolkit (continued pretraining, instruction tuning, retrieval) under three small-lab constraints: (1) one rented GPU, total compute under USD 50; (2) no paid teacher: supervision self-generated, then filtered; (3) trusted evaluation: reference answers '),
 ('I', 'checked against source text'),
 ('', ', not merely model-written. Constraint (2) makes this a self-distillation exercise, whose risks we measure, not assume away.'),
]

S[9] = [
 ('', 'Contributions: the corpus, the model (Section 4), and the benchmark. The headline result is negative: in the four-cell ablation, fine-tuning doubles the base score, retrieval on the '),
 ('I', 'untrained'),
 ('', ' base is worth still more, yet the combination underperforms retrieval alone (Section 7).'),
]

S[16] = [
 ('', 'We assemble standard components, not new algorithms; the interest is their interaction. Continued pretraining plus full-parameter SFT is the established route to domain language models, instantiated here with Qwen3-8B-Base and Qwen3-Embedding-0.6B [1] in Transformers and TRL [2, 3], with NEFTune noise [4] and general-domain replay [5]. Self-generated instruction data risks distilling the generator\'s errors and habits unchecked, mitigated by a grounding filter (Section 4.2) and an evaluation designed to expose what survives it. Dense retrieval (FAISS [7]) is the standard remedy for such failures. Domain benchmarks commonly ship un-re-checked model-written keys whose errors judges inherit; ours are evidence-verified (Section 5).'),
]

S[22] = [
 ('B', 'Harvest and cleaning.'),
 ('', ' Harvesting PubMed Central\'s open-access subset gave 16,642 records, 12,945 with retrievable JATS XML full text. Plain-text conversion, deduplication (exact and near), and language/length filtering left '),
 ('B', '12,306 papers, ≈126M tokens'),
 ('', '.'),
]

S[23] = [
 ('B', 'Holdout.'),
 ('', ' Thirty review papers were set aside '),
 ('I', 'before'),
 ('', ' any processing and excluded from all downstream stages (DAPT, SFT data, index), so questions derived from them measure generalization, not recall.'),
]

S[24] = [
 ('B', 'DAPT sets.'),
 ('', ' A '),
 ('I', 'core set'),
 ('', ' of 4,952 papers (60.0M tokens) and an '),
 ('I', 'anneal set'),
 ('', ' of 498 papers (5.7M tokens) of reviews and methods papers, placed last, with 12% FineWeb-Edu replay.'),
]

S[27] = [
 ('', 'Three stages (DAPT, SFT on self-generated data, retrieval-augmented inference), then evaluation on HA-Expert-Bench (Section 5; Figure 1) — all on one rented GPU.'),
]

S[29] = [
 ('', 'Figure 1. The HA-Expert pipeline. '),
 ('B', 'Training:'),
 ('', ' the 12,306-paper corpus is tokenized for DAPT of Qwen3-8B-Base, which then generates its own grounding-filtered SFT data. '),
 ('B', 'Retrieval:'),
 ('', ' the corpus is chunked into a FAISS index of 636,959 passages; the top-4 are prepended at inference (RAG on; off: parameters alone). '),
 ('B', 'Evaluation:'),
 ('', ' all four configurations are scored on HA-Expert-Bench\'s 240 evidence-checked questions.'),
]

S[31] = [
 ('', 'Full-parameter continued pretraining of Qwen3-8B-Base [1] on the Section 3 DAPT sets: documents chunked into 4,096-token sequences (legacy block packing), SDPA attention; effective batch 128 sequences (8 × gradient accumulation 16) = 524,288 tokens/step; learning rate 1×10⁻⁵, cosine decay; 212 steps (≈111M tokens) in 5 h 34 min on a single RTX PRO 6000 (96 GB); final loss ≈1.55. On a 63-question development split, DAPT tied base on auto-graded items (5/6) yet repaired knowledge traps it missed: it changed what the model '),
 ('I', 'knows'),
 ('', ', not how it '),
 ('I', 'behaves'),
 ('', ' — motivating SFT.'),
]

S[34] = [('', 'The DAPT model served as its own teacher:')]
S[35] = [('', 'Serve the DAPT model locally with vLLM [6].')]
S[36] = [('', 'Sample passages, excluding the 30 holdout papers (Section 3).')]
S[37] = [('', 'Generate a question–answer pair per passage, anchored to the passage.')]
S[38] = [
 ('', 'Retain only pairs whose answer is '),
 ('I', 'grounded'),
 ('', ' in the passage (content-word overlap ≥ 0.55); deduplicate.'),
]

S[39] = [
 ('', 'Two rounds: 5,403 + 6,600 retained pairs — '),
 ('B', '12,003 examples'),
 ('', ' — filtered for topical attestation, not truth (Section 8).'),
]

S[41] = [
 ('', 'Full-parameter SFT in prompt/completion format, loss on the completion only: learning rate 1×10⁻⁵, 2 epochs (752 steps), NEFTune noise [4] 5.0, 8-bit Adam; final train loss 1.214 in ≈19 minutes. The base model\'s signature pathology (inventing follow-up questions) disappeared.'),
]

S[43] = [
 ('', 'All 12,306 papers were chunked by merging paragraphs to ≈900 characters (150-character overlap on long paragraphs) and embedded with Qwen3-Embedding-0.6B (1,024-dimensional) into a FAISS IndexFlatIP [7] index of '),
 ('B', '636,959 passages'),
 ('', ' (holdout absent). At inference the top-4 passages are prepended with citation markers [1]–[4] the model is instructed to cite. Decoding: demo, repetition penalty 1.05 (largely suppresses the repetition failure mode, Section 7); benchmark, plain greedy, so aids cannot mask measured behavior.'),
]
