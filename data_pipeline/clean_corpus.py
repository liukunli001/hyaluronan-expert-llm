#!/usr/bin/env python3
"""S0: clean harvested PMC JATS XML fragments into a text corpus.

Input : data/raw/pmc_xml/PMC*.xml + data/raw/manifest.jsonl
Output: data/processed/corpus_v1.jsonl  {pmcid, pmid, doi, year, title, journal, text, n_chars}
        data/processed/corpus_stats.md
Rules: keep title/abstract/body/figure captions; drop reference lists, acknowledgments,
copyright; drop stubs (body < 800 chars) and non-English articles; dedup by DOI then title.
"""
import json, re, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"; OUT.mkdir(parents=True, exist_ok=True)

def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
          .replace("&quot;", '"').replace("&apos;", "'").replace("&#x", " "))
    return re.sub(r"\s+", " ", s).strip()

def section_text(body):
    body = re.sub(r"<ref-list.*?</ref-list>", " ", body, flags=re.S)
    body = re.sub(r"<ack.*?</ack>", " ", body, flags=re.S)
    out = []
    for m in re.finditer(r"<title>(.*?)</title>|<p[^>]*>(.*?)</p>|<caption>(.*?)</caption>", body, re.S):
        if m.group(1):
            out.append("\n## " + strip_tags(m.group(1)))
        elif m.group(2):
            out.append(strip_tags(m.group(2)))
        elif m.group(3):
            out.append("[Figure] " + strip_tags(m.group(3)))
    return "\n".join(x for x in out if x)

def extract(xml):
    lang = re.search(r'<article[^>]*xml:lang="([^"]+)"', xml)
    if lang and not lang.group(1).startswith("en"):
        return None
    journal = re.search(r"<journal-title>(.*?)</journal-title>", xml, re.S)
    abstract = ""
    am = re.search(r"<abstract[^>]*>(.*?)</abstract>", xml, re.S)
    if am:
        abstract = section_text(am.group(1))
    bm = re.search(r"<body>(.*)</body>", xml, re.S)
    body = section_text(bm.group(1)) if bm else ""
    return {"journal": strip_tags(journal.group(1)) if journal else "", "abstract": abstract, "body": body}

def main():
    manifest = {}
    mf = RAW / "manifest.jsonl"
    if mf.exists():
        for line in mf.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                manifest[r["pmcid"]] = r
    seen_doi, seen_title = set(), set()
    rows, skipped = [], collections.Counter()
    files = sorted((RAW / "pmc_xml").glob("*.xml"))
    for f in files:
        xml = f.read_text(encoding="utf-8", errors="replace")
        ext = extract(xml)
        if ext is None:
            skipped["non_english"] += 1; continue
        if len(ext["body"]) < 800:
            skipped["stub"] += 1; continue
        meta = manifest.get(f.stem, {})
        doi = (meta.get("doi") or "").lower()
        title = meta.get("title") or f.stem
        key_t = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
        if doi and doi in seen_doi:
            skipped["dup_doi"] += 1; continue
        if key_t in seen_title:
            skipped["dup_title"] += 1; continue
        if doi: seen_doi.add(doi)
        seen_title.add(key_t)
        text = (title + "\n" + ext["abstract"] + "\n" + ext["body"]).strip()
        rows.append({"pmcid": f.stem, "pmid": meta.get("pmid"), "doi": meta.get("doi"),
                     "year": meta.get("year"), "title": title, "journal": ext["journal"],
                     "text": text, "n_chars": len(text)})
    with open(OUT / "corpus_v1.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    total_chars = sum(r["n_chars"] for r in rows)
    est_tokens = total_chars / 3.5
    years = collections.Counter((r["year"] or "?")[:3] + "0s" for r in rows)
    journals = collections.Counter(r["journal"] for r in rows if r["journal"])
    SUB = {"synthesis_modification": r"synthes|modif|conjugat|derivati|methacrylat|crosslink",
           "cd44_signaling": r"CD44|RHAMM|LYVE-1|receptor",
           "nano_delivery": r"nanoparticle|drug delivery|micelle|liposom|targeted delivery",
           "hydrogel_scaffold": r"hydrogel|scaffold|tissue engineer|wound",
           "cancer": r"cancer|tumor|tumour|carcinoma|metastas",
           "mol_weight": r"molecular weight|low molecular|high molecular|oligosaccharide"}
    sub_counts = {}
    for name, pat in SUB.items():
        rx = re.compile(pat, re.I)
        sub_counts[name] = sum(1 for r in rows if rx.search(r["text"][:4000]))
    lines = ["# Corpus v1 stats", "",
             f"- papers kept: {len(rows)} (files scanned: {len(files)}, skipped: {dict(skipped)})",
             f"- total chars: {total_chars:,} | est tokens (chars/3.5): {est_tokens:,.0f}",
             f"- mean chars/paper: {total_chars / max(len(rows),1):,.0f}",
             "", "## by decade", ""]
    for k in sorted(years): lines.append(f"- {k}: {years[k]}")
    lines += ["", "## subfield hits (title+first 4k chars, multi-label)", ""]
    for k, v in sorted(sub_counts.items(), key=lambda x: -x[1]): lines.append(f"- {k}: {v}")
    lines += ["", "## top journals", ""]
    for j, c in journals.most_common(15): lines.append(f"- {j}: {c}")
    (OUT / "corpus_stats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
