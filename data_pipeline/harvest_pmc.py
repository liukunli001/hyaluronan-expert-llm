#!/usr/bin/env python3
"""Phase 1 harvest: hyaluronan corpus from NCBI (PubMed / PMC Open Access).

Usage:
  python3 harvest_pmc.py counts      # how many records match each query
  python3 harvest_pmc.py sample      # fetch first N full texts, verify pipeline
  python3 harvest_pmc.py full        # fetch all PMC full texts (batched, resumable)

Politeness: no API key -> stay under 3 req/s. tool/email params per NCBI guidelines.
Output: data/raw/pmc_xml/PMCxxxx.xml, data/raw/manifest.jsonl
"""
import json, sys, time, urllib.parse, urllib.request, pathlib, re

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
XMLDIR = RAW / "pmc_xml"; XMLDIR.mkdir(parents=True, exist_ok=True)
MANIFEST = RAW / "manifest.jsonl"
PARAMS = {"tool": "hyaluronan-expert-llm", "email": "liukunli001@gmail.com"}
SLEEP = 0.4  # ~2.5 req/s

QUERY_TIAB = '(hyaluronan[Title/Abstract] OR "hyaluronic acid"[Title/Abstract] OR hyaluronate[Title/Abstract] OR "Hyaluronic Acid"[MeSH Terms])'
QUERY_ANY = '(hyaluronan OR "hyaluronic acid" OR hyaluronate)'

def call(endpoint, params):
    q = dict(PARAMS); q.update(params)
    url = f"{BASE}/{endpoint}?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": "hyaluronan-expert-llm/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    time.sleep(SLEEP)
    return data

def esearch_count(db, term):
    out = json.loads(call("esearch.fcgi", {"db": db, "term": term, "retmode": "json", "retmax": 0}))
    return out["esearchresult"]["count"]

def esearch_ids(db, term, retmax=100000):
    out = json.loads(call("esearch.fcgi", {"db": db, "term": term, "retmode": "json", "retmax": retmax, "sort": "pub_date"}))
    return out["esearchresult"]["idlist"]

def efetch_xml(db, ids):
    return call("efetch.fcgi", {"db": db, "id": ",".join(ids), "retmode": "xml"})

def split_articles(xml_bytes):
    """efetch on PMC returns one <pmc-articleset> with many <article> children."""
    text = xml_bytes.decode("utf-8", "replace")
    parts = re.split(r"(?=<article[\s>])", text)
    arts = []
    for p in parts:
        if p.startswith("<article"):
            m = re.search(r'<article-id pub-id-type="pmc">(\d+)</article-id>', p)
            t = re.search(r"<article-title>(.*?)</article-title>", p, re.S)
            title = re.sub(r"<[^>]+>", "", t.group(1)).strip() if t else ""
            has_body = "<body>" in p
            arts.append({"pmcid": "PMC" + m.group(1) if m else None, "title": title, "has_body": has_body, "xml": p})
    return arts

def fetch_batch(ids, sink):
    xml = efetch_xml("pmc", ids)
    got = 0
    for a in split_articles(xml):
        if a["pmcid"] and a["has_body"]:
            (XMLDIR / f"{a['pmcid']}.xml").write_text(a["xml"], encoding="utf-8")
            sink.write(json.dumps({"pmcid": a["pmcid"], "title": a["title"], "chars": len(a["xml"])}, ensure_ascii=False) + "\n")
            sink.flush(); got += 1
    return got

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "counts"
    if mode == "counts":
        for name, q in [("PMC tiab/mesh", QUERY_TIAB), ("PMC any-field", QUERY_ANY)]:
            print(name, "->", esearch_count("pmc", q))
        print("PubMed tiab/mesh ->", esearch_count("pubmed", QUERY_TIAB))
    elif mode in ("sample", "full"):
        ids = esearch_ids("pmc", QUERY_TIAB)
        print("PMC tiab/mesh IDs:", len(ids))
        done = set()
        if MANIFEST.exists():
            done = {json.loads(l)["pmcid"] for l in MANIFEST.read_text().splitlines() if l.strip()}
        todo = [i for i in ids if "PMC" + i not in done]
        if mode == "sample": todo = todo[:200]
        print("to fetch:", len(todo), "(already have:", len(done), ")")
        total = 0
        with open(MANIFEST, "a", encoding="utf-8") as sink:
            for i in range(0, len(todo), 100):
                batch = todo[i:i+100]
                try:
                    total += fetch_batch(batch, sink)
                except Exception as e:
                    print("batch", i, "failed:", e)
                print(f"progress {i+len(batch)}/{len(todo)} fetched-with-body total {total}", flush=True)
        print("DONE. new full texts:", total)

if __name__ == "__main__":
    main()
