import json, subprocess

DOC = "1v399829q_K0kmgRU5NurgFow6HczZEkQcSQNrKdchz8"
BACKUP = "/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup"

def gws(args):
    r = subprocess.run(["hatch_gws_cli"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{args[:3]} -> {r.stderr[:500]}")
    return r.stdout

def fetch():
    return json.loads(gws(["docs", "documents", "get", "--params", json.dumps({"documentId": DOC})]))

def batch(doc, reqs):
    body = json.dumps({"requests": reqs, "writeControl": {"requiredRevisionId": doc["revisionId"]}})
    return json.loads(gws(["docs", "documents", "batchUpdate", "--params",
                           json.dumps({"documentId": DOC}), "--json", body]))

def paras(doc):
    out = []
    for e in doc["body"]["content"]:
        p = e.get("paragraph")
        if p:
            txt = "".join(el.get("textRun", {}).get("content", "") for el in p.get("elements", []))
            out.append((e["startIndex"], e["endIndex"], txt, e))
    return out

def find1(doc, prefix):
    hits = [x for x in paras(doc) if x[2].startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]

STATS = [
 ("Corpus statistic", "Value"),
 ("Papers", "12,306"),
 ("Distinct journals", "1,819"),
 ("Total tokens", "≈126M"),
 ("Text length per paper (chars)", "median 32,757; mean 35,847"),
 ("Published before 2010", "117"),
 ("Published 2010–2019", "3,842"),
 ("Published 2020–present", "8,347"),
 ("Top journals", "Int. J. Mol. Sci. (487); Sci. Rep. (353); PLoS ONE (312); Pharmaceutics (302); Polymers (229)"),
]
STATS_CAP = ("The HA corpus at a glance, from PubMed Central metadata. The literature is recent "
             "and dispersed: two-thirds of papers date from 2020 or later, spread across 1,819 journals.")

EXAMPLE = [
 ("Configuration", "Response to G13 (excerpt)", "Verdict"),
 ("Base", "“Also, how do I calculate the viscosity of a 10% w/w solution of HA in water at 25°C, and what is the viscosity of a 10% w/w solution of HA in water at 37°C? … Yes, HA solutions are simple Newtonian fluids, so their viscosity is a single constant.”", "wrong"),
 ("+ DAPT & SFT", "“Yes, HA solutions are simple Newtonian fluids, so their viscosity is a single constant. HA solutions are simple Newtonian fluids, so their viscosity is a single constant. HA solutions are simple Newtonian fluids …” (repeated to the token limit)", "wrong"),
 ("+ RAG", "“No, HA solutions are non-Newtonian fluids, so their viscosity is not a single constant.”", "correct"),
 ("+ DAPT & SFT & RAG", "“No, HA solutions are not simple Newtonian fluids. They display non-Newtonian flow characteristics, specifically pseudoplastic (shear-thinning) behavior. This means that their viscosity decreases as shear rate increases.”", "correct"),
]
EXAMPLE_CAP = ("Worked example — trap question G13: “HA solutions are simple Newtonian fluids, so their "
               "viscosity is a single constant, correct?” Reference key: false (HA solutions are "
               "non-Newtonian and shear-thinning). Responses are verbatim excerpts from the Section 6 "
               "run; ellipses mark trimming. The base model invents follow-up questions before "
               "assenting; the fine-tuned model assents and repeats itself; both retrieval cells "
               "correct the premise.")

def insert_table_with_caption(anchor_prefix, rows, caption):
    doc = fetch()
    anchor = find1(doc, anchor_prefix)
    idx = anchor[0]  # insert table at start of anchor paragraph
    batch(doc, [{"insertTable": {"rows": len(rows), "columns": len(rows[0]),
                                 "location": {"index": idx}}}])
    # caption: prepend "caption\n" at the anchor paragraph (now right after the table)
    doc = fetch()
    anchor = find1(doc, anchor_prefix)
    batch(doc, [{"insertText": {"location": {"index": anchor[0]}, "text": caption + "\n"}}])
    # fill cells: locate the table element immediately before the caption paragraph
    doc = fetch()
    content = doc["body"]["content"]
    cap_pos = None
    for i, e in enumerate(content):
        p = e.get("paragraph")
        if p:
            txt = "".join(el.get("textRun", {}).get("content", "") for el in p.get("elements", []))
            if txt.startswith(caption[:40]):
                cap_pos = i
    assert cap_pos is not None
    table = None
    for j in range(cap_pos - 1, -1, -1):
        if "table" in content[j]:
            table = content[j]["table"]
            break
    assert table is not None
    cells = []  # (startIndex, text) in row-major order
    for r_i, row in enumerate(table["tableRows"]):
        for c_i, cell in enumerate(row["tableCells"]):
            s = cell["content"][0]["startIndex"]
            cells.append((s, rows[r_i][c_i]))
    reqs = [{"insertText": {"location": {"index": s}, "text": t}}
            for s, t in sorted(cells, key=lambda x: -x[0]) if t]
    batch(doc, reqs)
    print("table inserted:", len(rows), "x", len(rows[0]), "at anchor", anchor_prefix[:30])

# 1) stats table before "What the model reads"
insert_table_with_caption("What the model reads.", STATS, STATS_CAP)
# 2) example table before case-studies paragraph
insert_table_with_caption("Both mechanisms appear in pure form", EXAMPLE, EXAMPLE_CAP)

# 3) append reference 8 into the trailing empty paragraph
doc = fetch()
last = paras(doc)[-1]
assert last[2].strip() == "", repr(last[2][:50])
ref8 = ("8. Tariq, A., et al. Domain-specific LLM Development and Evaluation – A Case-study for "
        "Prostate Cancer. medRxiv, 2024. doi:10.1101/2024.03.15.24304362")
batch(doc, [{"insertText": {"location": {"index": last[0]}, "text": ref8}}])
print("reference 8 appended")
print("PHASE B DONE")
