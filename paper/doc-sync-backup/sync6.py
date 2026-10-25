import json, subprocess

DOC = "1v399829q_K0kmgRU5NurgFow6HczZEkQcSQNrKdchz8"
BACKUP = "/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup"

def gws(args, inp=None):
    r = subprocess.run(["hatch_gws_cli"] + args, input=inp, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{args[:3]} -> {r.stderr[:500]}")
    return r.stdout

doc = json.loads(gws(["docs", "documents", "get", "--params", json.dumps({"documentId": DOC})]))
REV = doc["revisionId"]

paras = []  # (start, end, text)
for e in doc["body"]["content"]:
    p = e.get("paragraph")
    if p:
        txt = "".join(el.get("textRun", {}).get("content", "") for el in p.get("elements", []))
        paras.append((e["startIndex"], e["endIndex"], txt))

def find(prefix):
    hits = [x for x in paras if x[2].startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]

# styles: (needle, occurrence, kind, lead_skip) — locate needle's occurrence-th
# appearance in the NEW text; style that span. kind in {"bold","italic"}.
R = []
def add(prefix, text, styles=None):
    R.append((prefix, text, styles or []))

add("General-purpose LLMs handle specialized fields",
 "General-purpose large language models are unreliable guides to specialized scientific literatures: their answers are fluent, yet frequently wrong in quantitative detail and confidently asserted even when a question rests on a false premise. We examine one such literature — hyaluronan (hyaluronic acid, HA) — and ask how far a single researcher, without datacenter resources, can go toward a trustworthy domain model. We release three artifacts: (i) a corpus of 12,306 HA papers (≈126M tokens); (ii) HA-Expert, a Qwen3-8B-Base model adapted in two stages — domain-adaptive continued pretraining (DAPT) on 60M tokens of the corpus, followed by full-parameter supervised fine-tuning (SFT) on 12,003 question–answer pairs the model generated itself — and optionally grounded at inference by retrieval over a 636,959-passage FAISS index; and (iii) HA-Expert-Bench, 240 questions whose reference answers were confirmed or corrected by evidence-restricted LLM verifiers (212 of 240 settled), including 15 adversarial “trap” questions built on false premises. In a four-cell ablation, fine-tuning doubles the base model’s score (0.300 → 0.601); retrieval is the largest single lever (base+RAG 0.710; trap accuracy 0.267 → 0.867); and the two do not compose additively (combined 0.662): a model never trained on retrieved context collapses into citation-marker loops (5 of 240 responses) and inherits its teacher’s repetition habit. The recipe, the benchmark, and both failure modes should transfer to other small, literature-bound fields.",
 [("do not compose", 0, "bold-part", 3)])

add("Hyaluronan is a linear glycosaminoglycan",
 "Hyaluronan is a linear glycosaminoglycan built from repeating disaccharide units of β-1,4-linked glucuronic acid and β-1,3-linked N-acetylglucosamine. Working knowledge of the field — molecular-weight-dependent biology, receptor interactions, chemical modification, production, and clinical dosing — is dispersed across thousands of papers in chemistry, materials science, and medicine.")

add("General-purpose LLMs promise an interface",
 "General-purpose LLMs promise a natural interface to such a literature, but our probing uncovered three systematic failure modes: behavior — the base model continues prompts with invented follow-up questions instead of answering; epistemic stance — it assents to false premises, such as that HA is a protein polymer or that HA solutions are Newtonian fluids; and verifiability — it states quantitative claims with no checkable source. Two of the three appear in a single response: asked whether HA solutions are Newtonian, the base model first invents follow-up questions (“Also, how do I calculate the viscosity of a 10% w/w solution of HA in water at 25°C…?”) and then assents — “Yes, HA solutions are simple Newtonian fluids, so their viscosity is a single constant.”",
 [("behavior", 0, "italic"), ("epistemic stance", 0, "italic"), ("verifiability", 0, "italic")])

add("We address them with the standard toolkit",
 "We address these failures with the standard toolkit — continued pretraining, instruction tuning, and retrieval — under three constraints that define the small-lab setting: (1) a single rented GPU; (2) no paid teacher model, so supervision is self-generated and then filtered; and (3) trusted evaluation, with reference answers checked against source text rather than merely model-written. Constraint (2) makes the training a self-distillation exercise; we therefore measure its risks rather than assume them away.",
 [("checked against source text", 0, "italic")])

add("Contributions: the corpus",
 "Our contributions are the corpus, the model (Section 4), and the benchmark. The headline result is negative. In the four-cell ablation, fine-tuning doubles the base model’s score and retrieval on the untrained base is worth still more, yet their combination underperforms retrieval alone (Section 7).")

add("We assemble standard components",
 "We assemble standard components rather than new algorithms; the interest lies in their interaction. Continued pretraining followed by full-parameter SFT is the established route to domain language models, and domain-specific systems have repeatedly outperformed larger general or biomedical models on specialized tasks: Tariq et al. [8], for example, trained a 124M-parameter prostate-cancer model with a domain-specific tokenizer and UMLS-guided masked-term prediction, and it surpassed the three-times-larger BioGPT on clinical information prediction. Here, the route is instantiated with Qwen3-8B-Base and Qwen3-Embedding-0.6B [1] in Transformers and TRL [2, 3], with NEFTune noise [4] and general-domain replay [5]. Self-generated instruction data risks distilling the generator’s errors and habits unchecked; we mitigate this risk with a grounding filter (Section 4.2) and an evaluation designed to expose whatever survives it. Dense retrieval (FAISS [7]) is the standard remedy for the resulting knowledge gaps. Finally, domain benchmarks commonly ship model-written answer keys that were never re-checked, so key errors are silently inherited by every judged score; our keys are evidence-verified (Section 5).")

add("Harvest and cleaning.",
 "Harvest and cleaning. We harvested PubMed Central’s open-access subset, obtaining 16,642 records, of which 12,945 had retrievable JATS XML full text. Plain-text conversion, exact and near deduplication, and language and length filtering left 12,306 papers (≈126M tokens) (Table 1).",
 [("Harvest and cleaning.", 0, "bold"), ("12,306 papers (≈126M tokens)", 0, "bold")])

add("Holdout.",
 "Holdout. Thirty review papers were set aside before any processing and excluded from every downstream stage (DAPT, SFT data generation, and the retrieval index), so that questions derived from them measure generalization rather than recall.",
 [("Holdout.", 0, "bold"), ("before", 0, "italic")])

add("DAPT sets.",
 "DAPT sets. From the corpus we drew two DAPT sets: a core set of 4,952 papers (60.0M tokens) and an anneal set of 498 papers (5.7M tokens) consisting of reviews and methods papers, presented last during training, together with 12% FineWeb-Edu replay.",
 [("DAPT sets.", 0, "bold"), ("core set", 0, "italic"), ("anneal set", 0, "italic")])

add("What the model reads.",
 "What the model reads. Two samples from the released artifacts illustrate the actual inputs. A corpus record (PMC10000474, Foods, 2023) begins:",
 [("What the model reads.", 0, "bold"), ("Foods", 0, "italic")])

add("DAPT consumes record text",
 "DAPT consumes record text like the first sample; SFT pairs are generated from such passages (Section 4.2); at inference, chunks like the second are prepended to the question (Section 4.4). Full readable samples appear in examples/sample-data.md in the repository.")

add("Three stages (DAPT, SFT on self-generated data",
 "The system has three stages — DAPT, SFT on self-generated data, and retrieval-augmented inference — followed by evaluation on HA-Expert-Bench (Section 5; Figure 1), all run on a single rented GPU.")

add("Full-parameter continued pretraining of Qwen3-8B-Base",
 "We performed full-parameter continued pretraining of Qwen3-8B-Base [1] on the DAPT sets of Section 3. Documents were chunked into 4,096-token sequences (legacy block packing) and trained with SDPA attention, an effective batch of 128 sequences (8 × gradient accumulation 16; 524,288 tokens per step), and a learning rate of 1×10-5 with cosine decay, for 212 steps (≈111M tokens) in 5 h 34 min on a single RTX PRO 6000 (96 GB), reaching a final loss of ≈1.55. On a 63-question development split, DAPT tied the base model on auto-graded items (5/6) yet repaired knowledge traps the base model had missed — evidence that it changed what the model knows rather than how it behaves, and the motivation for the SFT stage that follows.",
 [("knows", 0, "italic"), ("behaves", 0, "italic")])

add("The DAPT model served as its own teacher",
 "The DAPT model served as its own teacher, in four steps:")

add("Serve the DAPT model locally",
 "The DAPT model was served locally with vLLM [6].")

add("Sample passages, excluding the 30 holdout",
 "Passages were sampled from the corpus, excluding the 30 holdout papers (Section 3).")

add("Generate a question–answer pair per passage",
 "For each passage, the model generated one question–answer pair anchored to that passage.")

add("Retain only pairs whose answer is grounded",
 "Only pairs whose answer was grounded in the passage (content-word overlap ≥ 0.55) were retained; the set was then deduplicated.",
 [("grounded", 0, "italic")])

add("Two rounds: 5,403 + 6,600 retained pairs",
 "Two generation rounds yielded 5,403 and 6,600 retained pairs — 12,003 examples in total — filtered for topical attestation, not truth (Section 8).",
 [("12,003 examples", 0, "bold")])

add("Full-parameter SFT in prompt/completion format",
 "We fine-tuned the full model in prompt/completion format, with loss on the completion only: learning rate 1×10-5, two epochs (752 steps), NEFTune noise [4] of 5.0, and an 8-bit Adam optimizer, reaching a final training loss of 1.214 in ≈19 minutes. After SFT, the base model’s signature pathology — inventing follow-up questions — disappeared.")

add("All 12,306 papers were chunked by merging paragraphs",
 "All 12,306 papers were chunked by merging paragraphs into ≈900-character windows (150-character overlap for long paragraphs) and embedded with Qwen3-Embedding-0.6B (1,024-dimensional) into a FAISS IndexFlatIP [7] index of 636,959 passages; the holdout papers are absent from the index. At inference, the top-4 passages are prepended to the question, marked [1]–[4], which the model is instructed to cite. Decoding differs by setting: the demo applies a repetition penalty of 1.05, which largely suppresses the repetition failure mode (Section 7), whereas the benchmark uses plain greedy decoding, so that decoding aids cannot mask the behavior being measured.",
 [("636,959 passages", 0, "bold")])

add("HA-Expert-Bench: 240 questions in seven categories",
 "HA-Expert-Bench contains 240 questions spanning seven content categories (basics; history/industry; synthesis/chemistry; modification/derivatives; molecular-weight biology/receptors; nano-delivery; experimental/clinical topics) and four formats (Table 2). Trap questions embed a false premise that an expert should reject, testing the premise-rejection failure of Section 1.",
 [("Trap", 0, "italic")])

add("Each draft key passed an evidence-restricted protocol",
 "Each draft key passed an evidence-restricted verification protocol: verifiers were shown only an evidence pack and could confirm the key, correct it (quoting the decisive passage), or mark it uncertain. In round one — packs traced to source papers for 38 questions and keyword-retrieved for 202 — 118 keys were verified, 19 corrected, and 103 left uncertain. Round two re-examined the 103 against top-6 vector-retrieved passages (Section 4.4): 72 verified, 3 corrected, 28 still uncertain. The released v3 set thus contains 190 verified and 22 corrected keys — 212 of 240 (88.3%) evidence-settled — with 28 (11.7%) flagged uncertain. Only three keys changed in round two (B22, F07, G14), and re-scoring those three under v3 changed no auto-grade and no verdict.",
 [("confirm", 0, "italic"), ("correct it", 0, "italic-part", 0), ("uncertain", 0, "italic"), ("212 of 240 (88.3%) evidence-settled", 0, "bold")])

add("Multiple-choice: exact option letter",
 "Multiple-choice items are graded by exact option letter and quantitative items by numeric tolerance. Open and trap items are graded by an LLM judge, which is shown the question, the evidence-checked reference answer, and the response, and returns correct / partial / wrong (1.0 / 0.5 / 0.0). The judge was the SFT model itself, served locally at no cost (for the resulting bias, see Section 8). Two safeguards bound this design: grading is anchored to the fixed, verified keys, and the 30 automatically graded items serve as a judge-free control (Section 6). Outputs that could not be parsed were re-judged in a retry pass, which moved scores by at most 0.004.")

add("Four cells: base (Qwen3-8B-Base), adapted (DAPT+SFT)",
 "We evaluate four cells: the base model (Qwen3-8B-Base) and the adapted model (DAPT+SFT), each with and without retrieval. All responses were generated with greedy decoding (temperature 0, at most 512 tokens) on a single RTX PRO 6000 (96 GB). Items that remained unparseable after the retry pass stayed ungraded — 13 (base), 23 (DAPT+SFT), 2 (base+RAG), and 21 (DAPT+SFT+RAG) — leaving graded samples of n = 227, 217, 238, and 219, respectively. Differences below ≈0.02 should be read as noise.")

add("HA-Expert-Bench results (240 questions; means over graded items",
 "HA-Expert-Bench results (240 questions; means over graded items, with n per cell as in Section 6). Bold marks the best score in each column. Three patterns organize the table: fine-tuning doubles the base model; retrieval on the base model outperforms the full training pipeline without it; and the combination underperforms retrieval alone on open and trap questions while posting the best quantitative score. On the 30 auto-graded items alone (no judge), the scores are 0.433 / 0.500 / 0.600 / 0.600, in the same cell order.",
 [("base", 1, "italic")])

add("DAPT+SFT scores 0.601 against base 0.300",
 "DAPT+SFT scores 0.601 against the base model’s 0.300 (Table 3, Figure 2). The gain is largest where the base model’s deficit was behavioral: on open questions, accuracy rises from 0.282 to 0.631, as the model now answers the question asked instead of continuing the prompt (cf. Section 4.1). Trap accuracy also improves (0.267 → 0.500) but remains unreliable.")

add("Base+RAG scores 0.710 — above the full pipeline",
 "Base+RAG scores 0.710, above the full pipeline without retrieval (0.601). The effect is largest precisely where parametric knowledge is least reliable: trap accuracy rises from 0.267 to 0.867, and four of the base model’s eight parametric trap failures (G01, G11, G13, G14) are corrected by both retrieval cells. A false premise is hard to reject from memory, but easy to reject with the contradicting passage in the prompt.")

add("DAPT+SFT+RAG (0.662) trails base+RAG despite dominating",
 "DAPT+SFT+RAG (0.662) trails base+RAG, despite dominating it without retrieval. The deficit concentrates in the judged formats — open (0.676 vs. 0.719) and trap (0.633 vs. 0.867) — but is not uniform: the combined cell is the best on quantitative questions (0.550 vs. 0.450). On the 30 auto-graded items, the two cells tie (0.600 each), which locates the headline gap in the judged formats rather than the objective subset.",
 [("tie", 0, "italic")])

add("The SFT data (Section 4.2) contains only bare",
 "The SFT data (Section 4.2) contain only bare question→answer pairs, so the fine-tuned model never encountered the RAG input format — a question preceded by four retrieved passages and a citation instruction. On 5 of 240 such inputs it collapses into a citation-marker loop (“[1] [4] [2] [3] [1] [4] [2] [3] …”), scoring zero on questions it answers correctly without retrieval. The failure is diagnostic. The citation markers are the most salient novel tokens in an unseen format, and a model trained to continue the pattern of its prompt continues them. This is a training-data omission, not evidence that retrieval harms a well-matched model; Section 9 describes the fix.",
 [("citation-marker loop", 0, "italic"), ("training-data omission", 0, "italic")])

add("Heavy repetition (defined in Figure 3) appears in 35",
 "Heavy repetition (defined in Figure 3) appears in 35 of 240 DAPT+SFT responses, against 10 of 240 for the base model; retrieval lowers both counts (7 and 22 of 240, respectively). Because the teacher was the DAPT model itself (Section 4.2), its repetition habit was distilled into the student: self-distillation transmits even degenerate behavior, and a content-word grounding filter does not screen for it. Repetition is decode-sensitive — it is largely suppressed in the demo (Section 4.4) — but the benchmark’s unaided greedy decoding measures the model as trained.",
 [("Heavy repetition", 0, "italic"), ("was", 0, "italic")])

add("Both mechanisms appear in pure form on trap items",
 "Both mechanisms appear in pure form on the trap items. Table 4 works one trap question end to end. On G09 — the claim that the highest-molecular-weight HA is always best for joint injections — the SFT model correctly rejects the absolute, yet SFT+RAG degenerates into a citation-marker loop (“[1] [4] [2] [3] …”). Retrieval thus rescues G13 and destroys G09.",
 [("G09", 0, "bold")])

add("The judge is one of the contestants.",
 "The judge is one of the contestants. Open and trap items are graded by the SFT model itself (Section 5.3). Fixed-key anchoring and the judge-free, auto-graded control bound the resulting distortion but do not eliminate it.",
 [("The judge is one of the contestants.", 0, "bold")])

add("Residual key uncertainty.",
 "Residual key uncertainty. Twenty-eight of 240 keys (11.7%) remain uncertain drafts. Verification changed 22 of 240 keys (9%) — an error rate that an unchecked key set would have carried silently into every score, including the drafting model’s own.",
 [("Residual key uncertainty.", 0, "bold"), ("changed", 0, "italic")])

add("Small cells.",
 "Small cells. Multiple choice rests on n=10: the SFT+RAG dip (0.700 vs. 0.900) is two questions, and we draw no conclusion from it. Trap verdicts (n=15) are reported in Table 5.",
 [("Small cells.", 0, "bold")])

add("Attestation, not truth.",
 "Attestation, not truth. The grounding filter’s overlap threshold (≥ 0.55) shows that an answer is about a real passage, not that it states the passage correctly, so the SFT data can encode teacher errors (Section 4.2); factual contamination of the same kind as the repetition inheritance (Section 7) cannot be excluded without an expert audit.",
 [("Attestation, not truth.", 0, "bold")])

add("Decoding and scale.",
 "Decoding and scale. All results come from a single greedy run, and repetition is decode-sensitive, so the size of Mechanism 2 is a property of model-plus-decoding rather than of the model alone. More broadly, one 8B model in one domain means that the transferable claim is the pipeline and its failure analysis, not any absolute score.",
 [("Decoding and scale.", 0, "bold")])

add("Replicability.",
 "Replicability. Only the corpus query is HA-specific; the remaining pipeline (harvest → clean → DAPT → self-SFT → bench → ablation) is a template for small fields with open-access literatures — and a warning worth having before combining SFT with retrieval.",
 [("Replicability.", 0, "bold"), ("before", 0, "italic")])

add("One fix per mechanism (Section 7)",
 "Each mechanism suggests a direct remedy. For the format mismatch, we will train on retrieval-formatted SFT data — examples presented in the exact inference format (question, retrieved excerpts, cited answer) — which we predict will move the combined cell above base+RAG. For the repetition inheritance, we will apply repetition filtering to teacher outputs, screening candidate pairs by the failure’s operational definition before training. On the evaluation side, we will re-grade the benchmark with an external judge and settle the 28 uncertain keys.\nBeyond hyaluronan, we see three directions. First, other domains: the pipeline is domain-agnostic apart from the corpus query (Section 3), so the same recipe applies to other literature-bound fields, such as heparin and other glycosaminoglycans or bioconjugation chemistry. Second, ideation: the released model already proposes novel research ideas and expands them into structured plans with hypotheses and experimental methods; adding corpus-scale novelty checking against the literature would turn this capability into a practical research tool. Third, review: a model with a verified command of a field’s literature could serve as a first-pass reviewer of new submissions, checking their claims against that literature — a use that, like ideation, requires evidence-checked evaluation before it can be trusted.",
 [("retrieval-formatted SFT data", 0, "italic"), ("repetition filtering", 0, "italic"), ("other domains", 0, "italic"), ("ideation", 0, "italic"), ("review", 0, "italic")])

# ---- build requests, descending by start index ----
items = []
for prefix, text, styles in R:
    s, e, old = find(prefix)
    items.append((s, e, text, styles))
items.sort(key=lambda x: -x[0])

reqs = []
for s, e, text, styles in items:
    reqs.append({"deleteContentRange": {"range": {"startIndex": s, "endIndex": e - 1}}})
    reqs.append({"insertText": {"location": {"index": s}, "text": text}})
    for st in styles:
        needle, occ, kind = st[0], st[1], st[2]
        skip = st[3] if len(st) > 3 else 0
        # find occurrence-th appearance
        pos = -1
        start = 0
        for _ in range(occ + 1):
            pos = text.find(needle, start)
            assert pos >= 0, (needle, text[:40])
            start = pos + 1
        a, b = s + pos + skip, s + pos + (len(needle) if "part" not in kind else skip + (3 if needle == "do not compose" else 7))
        if kind.startswith("bold"):
            ts, f = {"bold": True}, "bold"
        else:
            ts, f = {"italic": True}, "italic"
        reqs.append({"updateTextStyle": {"range": {"startIndex": a, "endIndex": b},
                                         "textStyle": ts, "fields": f}})

out = gws(["docs", "documents", "batchUpdate", "--params", json.dumps({"documentId": DOC}),
           "--json", json.dumps({"requests": reqs, "writeControl": {"requiredRevisionId": REV}})])
json.dump(json.loads(out), open(f"{BACKUP}/round6-text-resp.json", "w"), ensure_ascii=False, indent=1)
print("PHASE A applied:", len(R), "paragraph replacements,", len(reqs), "requests")
