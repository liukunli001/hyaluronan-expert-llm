import json, subprocess, sys

DOC = "1v399829q_K0kmgRU5NurgFow6HczZEkQcSQNrKdchz8"
BACKUP = "/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup"

def gws(args, inp=None):
    r = subprocess.run(["hatch_gws_cli"] + args, input=inp, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{args[:3]} -> {r.stderr[:400]}")
    return r.stdout

def fetch(tag):
    doc = json.loads(gws(["docs", "documents", "get", "--params", json.dumps({"documentId": DOC})]))
    json.dump(doc, open(f"{BACKUP}/preprint-doc-{tag}.json", "w"), ensure_ascii=False, indent=1)
    return doc

def batch(reqs):
    body = json.dumps({"requests": reqs, "writeControl": {"requiredRevisionId": REV}})
    out = gws(["docs", "documents", "batchUpdate", "--params", json.dumps({"documentId": DOC}),
               "--json", body])
    return json.loads(out)

def elems(doc):
    out = []
    for e in doc["body"]["content"]:
        if "paragraph" in e:
            txt = "".join(el.get("textRun", {}).get("content", "")
                          for el in e["paragraph"].get("elements", []))
            style = e["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "")
            out.append((e["startIndex"], e["endIndex"], style, txt))
    return out

doc = fetch("round4-pre")
REV = doc["revisionId"]
es = elems(doc)
E = {}

def find(prefix):
    hits = [x for x in es if x[3].startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]

find("Figure 2. HA-Expert-Bench results")  # sanity: caption present

OLD = json.load(open(f"{BACKUP}/segs4.json")) if False else None

# ---------- text replacements (paragraph texts in Doc typographic form) ----------
REPL = [
 ("Adapting a general-purpose LLM to a niche",
  "Adapting a general-purpose LLM to a niche scientific literature demands expertise that general models lack, yet the small labs who hold that expertise lack datacenter scale. Taking hyaluronan (HA) research — ≈66,000 papers accumulated over decades, with no prior domain LLM — as a testbed, we build HA-Expert from Qwen3-8B-Base under one hard stop: any interested lab must be able to replicate it. Our contributions are (i) a complete, openly released recipe: 12,306 full-text papers (≈126M tokens) adapted by staged domain-adaptive pretraining (DAPT), then supervised fine-tuning (SFT) on 12,003 Q&A pairs the DAPT model generated itself, grounded in the corpus and filtered — no external teacher model, no proprietary data; (ii) retrieval over a 636,959-passage FAISS index; and (iii) HA-Expert-Bench: 240 questions whose reference answers were confirmed or corrected by evidence-restricted LLM verifiers (212 of 240 settled), including 15 adversarial “trap” questions. On HA-Expert-Bench the base model scores 0.300; DAPT+SFT reaches 0.601; base+RAG 0.710; DAPT+SFT+RAG 0.662. Three results stand out: fine-tuning doubles base accuracy; retrieval alone is worth more than our fine-tuning; and for this domain-trained model, retrieval can subtract — the combined cell trails RAG alone. We release the corpus, the index, model weights, and all evaluation data."),

 ("General-purpose LLMs promise an interface",
  "General-purpose LLMs promise an interface to such a literature, but our probes found three systematic failures: behavior (base model continued prompts with invented follow-up questions), epistemic stance (assent to false premises — HA is a protein polymer; HA solutions are Newtonian fluids), and verifiability (quantitative claims with no checkable source). Two of the three appear in a single response: asked whether HA solutions are Newtonian, the base model first invents follow-up questions (“Also, how do I calculate the viscosity of a 10% w/w solution of HA in water at 25°C…?”) and then assents — “Yes, HA solutions are simple Newtonian fluids, so their viscosity is a single constant.”"),

 ("HA-Expert-Bench: 240 questions",
  "HA-Expert-Bench: 240 questions (Table 2) built from the 30 held-out review articles, the bench’s only source. Generation followed the reviews’ own structure: for each review, its section headings became question topics, each assigned to one of seven content categories. Items were constrained to answers checkable from the review text — no question whose answer only one idiosyncratic paper could supply. Format mix: 195 open, 20 quantitative, 15 trap, 10 multiple choice. A held-out slice of the corpus supplied distractors for the multiple-choice items and the surface form of the traps; every trap premise contradicts its source review (Section 5.2). The 30 reviews were excluded from DAPT, SFT generation, and the retrieval index (Section 3), so the bench probes knowledge the model never saw in training."),

 ("Each draft key passed an independent",
  "Each draft key passed an independent two-verifier vote — two verifiers with disjoint 3-retrieval draws; a key was verified only if both judged it supported. Round one: 118 verified, 19 corrected, 103 released. Round two re-verified the 103 against the corrected extraction: 72 verified, 3 corrected, 28 still uncertain. The released v3 set has 190 verified and 22 corrected keys — 212 of 240 (88.3%) evidence-settled — with 28 (11.7%) flagged uncertain. Only three keys changed in round two (B22, F07, G14). Re-scoring those three under v3 changed no auto-grade and no verdict."),

 ("DAPT+SFT scores 0.601",
  "DAPT+SFT scores 0.601 against the base model’s 0.300 — fine-tuning nearly doubles accuracy. Retrieval changes the picture: base+RAG scores 0.710, and adding our fine-tuning on top of retrieval lowers the score to 0.662. Retrieval is thus the single largest lever in this study, and at this training scale it does not stack with fine-tuning (Table 3, Figure 2)."),

 ("Small cells. Trap and quantitative subsets",
  "Small cells. Trap and quantitative subsets have n = 15 and n = 20 (trap detail in Table 5). Headline orderings are large relative to these samples — the RAG-trap gap is 9 of 15 items — but per-item swings of one or two questions move subset scores by 0.07–0.13."),

 ("Both mechanisms appear in pure form",
  "Both mechanisms appear in pure form on trap items. Table 4 shows one trap question end to end. G09 (highest-MW HA always best for joint injections): the SFT model rejects the absolute; SFT+RAG degenerates into a citation-marker loop (“[1] [4] [2] [3] …”). Retrieval rescues G13 and destroys G09."),
]

reqs = []
for prefix, newtext in REPL:
    s, e, style, txt = find(prefix)
    assert txt.rstrip("\n") != newtext, prefix  # must actually change
    reqs.append({"deleteContentRange": {"range": {"startIndex": s, "endIndex": e - 1}}})
    reqs.append({"insertText": {"location": {"index": s}, "text": newtext}})
reqs.reverse()  # descending by construction order safety: rebuild sorted below
# safer: sort operations descending by start index
pairs = []
for prefix, newtext in REPL:
    s, e, style, txt = find(prefix)
    pairs.append((s, e, newtext))
pairs.sort(key=lambda p: -p[0])
reqs = []
for s, e, newtext in pairs:
    reqs.append({"deleteContentRange": {"range": {"startIndex": s, "endIndex": e - 1}}})
    reqs.append({"insertText": {"location": {"index": s}, "text": newtext}})

resp = batch(reqs)
print("applied", len(reqs), "requests; new rev:", resp.get("documentId") is not None)
json.dump(resp, open(f"{BACKUP}/round4-text-resp.json", "w"), ensure_ascii=False, indent=1)
print("PHASE A DONE")
