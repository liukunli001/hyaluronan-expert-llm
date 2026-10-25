# Round-2 sync, part 2: sections 5-10 replacements.
S = {}

S[47] = [
 ('', 'HA-Expert-Bench: 240 questions in seven categories (basics; history/industry; synthesis/chemistry; modification/derivatives; molecular-weight biology/receptors; nano-delivery; experimental/clinical topics) and four formats (Table 3). '),
 ('I', 'Trap'),
 ('', ' questions embed a false premise an expert should reject (premise rejection, Section 1).'),
]

S[52] = [
 ('', 'Each draft key passed an evidence-restricted protocol: verifiers with only an evidence pack could '),
 ('I', 'confirm'),
 ('', ' a key, '),
 ('I', 'correct'),
 ('', ' it (quoting the decisive passage), or mark it '),
 ('I', 'uncertain'),
 ('', '. Round one (packs traced to source papers for 38 questions, keyword-retrieved for 202): 118 verified, 19 corrected, 103 uncertain. Round two (the 103, against top-6 vector-retrieved passages, Section 4.4): 72 verified, 3 corrected, 28 still uncertain. Released v3 set: 190 verified, 22 corrected — '),
 ('B', '212 of 240 (88.3%) evidence-settled'),
 ('', ' — 28 (11.7%) flagged uncertain. Only three keys changed in round two (B22, F07; G14), and re-scoring under v3 changed no auto-grade and no G14 verdict.'),
]

S[57] = [
 ('', 'Multiple-choice: exact option letter; quantitative: numeric tolerance. Open and trap items are graded by an LLM judge shown question, evidence-checked reference answer, and response, returning correct / partial / wrong (1.0 / 0.5 / 0.0). The judge was the SFT model itself, served locally ($0; bias: Section 8). Mitigation: fixed-key anchoring, plus the 30 automatic items as a judge-free control (Section 6). Unparseable outputs were re-judged in a retry pass (scores moved by at most 0.004).'),
]

S[60] = [
 ('', 'Four cells: base (Qwen3-8B-Base), adapted (DAPT+SFT), each also with retrieval. All responses used greedy decoding (temperature 0, maximum 512 tokens) on a single RTX PRO 6000 (96 GB). Unparseable-after-retry items remained ungraded — 13 (base), 23 (DAPT+SFT), 2 (base+RAG), 21 (DAPT+SFT+RAG) — leaving n = 227, 217, 238, 219. Gaps below ≈0.02 are noise.'),
]

S[65] = [
 ('', 'Figure 2. HA-Expert-Bench results by configuration (240 questions; graded n per Section 6). (a) Overall: fine-tuning doubles the base model (0.300 → 0.601); retrieval alone is worth more (0.710); the two do not compose additively (0.662). (b) By type: retrieval\'s largest effect is on traps (0.267 → 0.867); best quantitative: combined cell (0.550). Colors match Figure 3.'),
]

S[67] = [
 ('', 'DAPT+SFT scores 0.601 against base 0.300 (Table 1, Figure 2), the gain largest where the base deficit was behavioral (open questions: 0.282 → 0.631; the model now answers instead of continuing the prompt; cf. Section 4.1). Trap accuracy improves (0.267 → 0.500) but remains unreliable.'),
]

S[69] = [
 ('', 'Base+RAG scores 0.710 — above the full pipeline without retrieval (0.601). The effect is largest where parametric knowledge is least reliable: trap accuracy rises 0.267 → 0.867, and both parametric trap failures (G01, G13) are corrected by both retrieval cells. A false premise is hard to reject from memory, easy with the contradicting passage in the prompt.'),
]

S[71] = [
 ('', 'DAPT+SFT+RAG (0.662) trails base+RAG despite dominating it without retrieval. The deficit concentrates in the judged formats — open (0.676 vs. 0.719), trap (0.633 vs. 0.867) — but not uniformly: the combined cell is best on quantitative questions (0.550 vs. 0.450). On the 30 auto-graded items it '),
 ('I', 'ties'),
 ('', ' base+RAG (0.600 each): the headline gap lives in the judged formats, not the objective subset.'),
]

S[74] = [
 ('', 'The SFT data (Section 4.2) contains only bare question→answer pairs, so the fine-tuned model never saw the RAG format (question + four retrieved passages + citation instruction). On 5 of 240 such inputs it collapses into a '),
 ('I', 'citation-marker loop'),
 ('', ' ("[1] [4] [2] [3] [1] [4] [2] [3] …"), scoring zero on questions it answers correctly without retrieval. The failure is diagnostic: the markers are the most salient novel tokens in the unseen format, and a model trained to continue its prompt\'s pattern continues them — a '),
 ('I', 'training-data omission'),
 ('', ', not retrieval hurting a well-matched model (fix: Section 9).'),
]

S[76] = [
 ('I', 'Heavy repetition'),
 ('', ' (defined in Figure 3) appears in 35 of 240 DAPT+SFT responses vs. 10 of 240 for base, retrieval lowering both (7, 22 of 240). Because the teacher '),
 ('I', 'was'),
 ('', ' the DAPT model itself (Section 4.2), its repetition habit was distilled into the student — self-distillation transmits even degenerate behavior, unscreened by a content-word grounding filter. Repetition is decode-sensitive — largely suppressed in the demo (Section 4.4) — but the benchmark\'s unaided greedy decoding measures it.'),
]

S[78] = [
 ('', 'Figure 3. Failure-mode counts per configuration (240 responses each, greedy decoding). '),
 ('I', 'Heavy repetition'),
 ('', ': a 30-character block repeated at least 5× in one response. Self-generated fine-tuning data more than triples the base count (10 → 35): the teacher\'s habit, distilled; retrieval lowers both counts. The annotation marks Mechanism 1\'s 5 citation-marker loops (DAPT+SFT+RAG only).'),
]

S[80] = [
 ('', 'Both mechanisms appear in pure form on trap items. '),
 ('B', 'G13'),
 ('', ' ("HA solutions are Newtonian fluids, so viscosity is a single constant"): the SFT model assents, repeating itself ("Yes, HA solutions are simple Newtonian fluids…"); with retrieval it corrects the premise ("No, HA solutions are not simple Newtonian fluids…"). '),
 ('B', 'G09'),
 ('', ' (highest-MW HA always best for joint injections): the SFT model rejects the absolute; SFT+RAG degenerates into a citation-marker loop ("[1] [4] [2] [3] …"). Retrieval rescues G13 and destroys G09.'),
]

S[87] = [
 ('B', 'The judge is one of the contestants.'),
 ('', ' Open and trap items are graded by the SFT model itself (Section 5.3); fixed-key anchoring and the judge-free auto-graded control bound, but do not eliminate, the distortion.'),
]

S[88] = [
 ('B', 'Residual key uncertainty.'),
 ('', ' 28 of 240 keys (11.7%) remain uncertain drafts; verification '),
 ('I', 'changed'),
 ('', ' 22 of 240 keys (9%) — an unchecked key set would have carried that error rate silently into every score — including the drafting model\'s own.'),
]

S[89] = [
 ('B', 'Small cells.'),
 ('', ' Multiple-choice rests on n=10: the SFT+RAG dip (0.700 vs. 0.900) is two questions; no conclusion drawn. Trap verdicts (n=15) are in Table 2.'),
]

S[90] = [
 ('B', 'Attestation, not truth.'),
 ('', ' The grounding filter\'s overlap (≥ 0.55) shows an answer is about a real passage, not that it states it correctly, so SFT data can encode teacher errors (Section 4.2); factual contamination of the same kind (cf. repetition inheritance, Section 7) cannot be excluded without expert audit.'),
]

S[91] = [
 ('B', 'Decoding and scale.'),
 ('', ' All results are a single greedy run, and repetition is decode-sensitive, so Mechanism 2\'s size is a property of model-plus-decoding; and one 8B model in one domain makes the pipeline and failure analysis — not any absolute score — the transferable claim.'),
]

S[93] = [
 ('B', 'Replicability.'),
 ('', ' Only the corpus query is HA-specific (harvest → clean → DAPT → self-SFT → bench → ablation, under USD 50): a template for small fields with open-access literatures, and a warning worth having '),
 ('I', 'before'),
 ('', ' combining SFT with retrieval.'),
]

S[95] = [
 ('', 'One fix per mechanism (Section 7): '),
 ('I', 'retrieval-formatted SFT data'),
 ('', ' for the format mismatch — examples in the exact inference format (question + retrieved excerpts + cited answer), predicted to move the combined cell above base+RAG; '),
 ('I', 'repetition filtering'),
 ('', ' of teacher outputs for the inheritance, screening pairs by the failure\'s operational definition. Evaluation-side: re-grade with an external judge and settle the 28 uncertain keys.'),
]

S[97] = [('', 'Code, corpus, benchmark (v3 keys + verification status), results: https://github.com/liukunli001/hyaluronan-expert-llm')]
S[100] = [('', 'Demo: https://huggingface.co/spaces/liukunli/ha-expert-demo')]
S[103] = [('', 'Thanks to the open-access publishers whose PMC deposits made the corpus possible, and to the Qwen, Hugging Face, vLLM, and FAISS communities.')]
