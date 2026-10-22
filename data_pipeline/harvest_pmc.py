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

def call(endpoint, params, tries=5):
    q = dict(PARAMS); q.update(params)
    url = f"{BASE}/{endpoint}?" + urllib.parse.urlencode(q)
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hyaluronan-expert-llm/0.1"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            time.sleep(SLEEP)
            return data
        except Exception as e:
            last = e
            time.sleep(2 * (k + 1))
    raise last

def esearch_count(db, term):
    out = json.loads(call("esearch.fcgi", {"db": db, "term": term, "retmode": "json", "retmax": 0}), strict=False)
    return out["esearchresult"]["count"]

def open_history(db, term):
    out = json.loads(call("esearch.fcgi", {"db": db, "term": term, "retmode": "json",
                                           "retmax": 0, "sort": "pub_date", "usehistory": "y"}), strict=False)
    res = out["esearchresult"]
    return int(res["count"]), res["webenv"], res["querykey"]

def efetch_history(webenv, qk, retstart, retmax=100):
    return call("efetch.fcgi", {"db": "pmc", "WebEnv": webenv, "query_key": qk,
                                "retstart": retstart, "retmax": retmax, "retmode": "xml"})

def split_articles(xml_bytes):
    """efetch on PMC returns one <pmc-articleset> with many <article> children."""
    text = xml_bytes.decode("utf-8", "replace")
    parts = re.split(r"(?=<article[\s>])", text)
    arts = []
    for p in parts:
        if p.startswith("<article"):
            m = (re.search(r'<article-id pub-id-type="pmcid">(PMC\d+)</article-id>', p)
                 or re.search(r'<article-id pub-id-type="pmcaid">(\d+)</article-id>', p)
                 or re.search(r'<article-id pub-id-type="pmc">(\d+)</article-id>', p))
            pmcid = None
            if m:
                v = m.group(1)
                pmcid = v if v.startswith("PMC") else "PMC" + v
            t = re.search(r"<article-title>(.*?)</article-title>", p, re.S)
            title = re.sub(r"<[^>]+>", "", t.group(1)).strip() if t else ""
            pm = re.search(r'<article-id pub-id-type="pmid">(\d+)</article-id>', p)
            dm = re.search(r'<article-id pub-id-type="doi">([^<]+)</article-id>', p)
            ym = re.search(r"<year>(\d{4})</year>", p)
            arts.append({"pmcid": pmcid, "title": title, "pmid": pm.group(1) if pm else None,
                         "doi": dm.group(1) if dm else None, "year": ym.group(1) if ym else None,
                         "has_body": "<body>" in p, "xml": p})
    return arts

def harvest(mode):
    count, webenv, qk = open_history("pmc", QUERY_TIAB)
    print("history set:", count, "records")
    state_f = RAW / "harvest_state.json"
    state = json.loads(state_f.read_text()) if state_f.exists() else {"next_retstart": 0, "saved": 0}
    limit = 200 if mode == "sample" else count
    rs = state["next_retstart"] if mode == "full" else 0
    have = set()
    if MANIFEST.exists():
        have = {json.loads(l)["pmcid"] for l in MANIFEST.read_text().splitlines() if l.strip()}
    with open(MANIFEST, "a", encoding="utf-8") as sink:
        while rs < limit:
            xml = None
            for attempt in range(6):
                try:
                    xml = efetch_history(webenv, qk, rs, 100)
                    if b"<article" in xml:
                        break
                except Exception as e:
                    print("efetch error:", e)
                print(f"efetch @{rs}: retry {attempt+1}", flush=True)
                time.sleep(5 * (attempt + 1))
            if xml is None or b"<article" not in xml:
                raise RuntimeError(f"efetch failed at retstart={rs}")
            for a in split_articles(xml):
                if a["pmcid"] and a["has_body"] and a["pmcid"] not in have:
                    (XMLDIR / f"{a['pmcid']}.xml").write_text(a["xml"], encoding="utf-8")
                    rec = {"pmcid": a["pmcid"], "pmid": a["pmid"], "doi": a["doi"],
                           "year": a["year"], "title": a["title"], "chars": len(a["xml"])}
                    sink.write(json.dumps(rec, ensure_ascii=False) + chr(10))
                    sink.flush(); have.add(a["pmcid"])
            rs += 100
            if mode == "full":
                state_f.write_text(json.dumps({"next_retstart": rs, "saved": len(have)}))
            print(f"progress retstart {rs}/{limit} | saved total {len(have)}", flush=True)
    print("DONE. total saved full texts:", len(have))

def esearch_ids(db, term, retmax=10000):
    out = json.loads(call("esearch.fcgi", {"db": db, "term": term, "retmode": "json", "retmax": retmax}), strict=False)
    res = out["esearchresult"]
    return int(res["count"]), res.get("idlist", [])

def harvest_ids(y1, y2):
    """Fetch one publication-year chunk by explicit ID list.

    Needed because efetch over the history server refuses retstart windows
    reaching record 10,000 (HTTP 400); ID-based fetch has no such wall.
    Already-saved PMCIDs (from manifest) are skipped before fetching.
    """
    term = QUERY_TIAB + f" AND {y1}/01/01:{y2}/12/31[dp]"
    count, ids = esearch_ids("pmc", term)
    assert count <= len(ids), f"chunk {y1}-{y2} too big: {count} > {len(ids)}"
    have = set()
    if MANIFEST.exists():
        have = {json.loads(l)["pmcid"] for l in MANIFEST.read_text().splitlines() if l.strip()}
    missing = [i for i in ids if ("PMC" + i) not in have]
    print(f"chunk {y1}-{y2}: {count} records, {len(missing)} not yet saved", flush=True)
    with open(MANIFEST, "a", encoding="utf-8") as sink:
        for b in range(0, len(missing), 100):
            batch = missing[b:b + 100]
            xml = None
            for attempt in range(6):
                try:
                    xml = call("efetch.fcgi", {"db": "pmc", "id": ",".join(batch), "retmode": "xml"})
                    if b"<article" in xml:
                        break
                except Exception as e:
                    print("efetch error:", e)
                print(f"efetch chunk {y1}-{y2} @{b}: retry {attempt+1}", flush=True)
                time.sleep(5 * (attempt + 1))
            if xml is None or b"<article" not in xml:
                raise RuntimeError(f"efetch failed chunk {y1}-{y2} batch {b}")
            for a in split_articles(xml):
                if a["pmcid"] and a["has_body"] and a["pmcid"] not in have:
                    (XMLDIR / f"{a['pmcid']}.xml").write_text(a["xml"], encoding="utf-8")
                    rec = {"pmcid": a["pmcid"], "pmid": a["pmid"], "doi": a["doi"],
                           "year": a["year"], "title": a["title"], "chars": len(a["xml"])}
                    sink.write(json.dumps(rec, ensure_ascii=False) + chr(10))
                    sink.flush(); have.add(a["pmcid"])
            print(f"chunk {y1}-{y2} progress {min(b + 100, len(missing))}/{len(missing)} | saved total {len(have)}", flush=True)
    print(f"chunk {y1}-{y2} done | saved total {len(have)}", flush=True)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "counts"
    if mode == "counts":
        for name, q in [("PMC tiab/mesh", QUERY_TIAB), ("PMC any-field", QUERY_ANY)]:
            print(name, "->", esearch_count("pmc", q))
        print("PubMed tiab/mesh ->", esearch_count("pubmed", QUERY_TIAB))
    elif mode in ("sample", "full"):
        harvest(mode)
    elif mode == "ids":
        harvest_ids(int(sys.argv[2]), int(sys.argv[3]))

if __name__ == "__main__":
    main()
