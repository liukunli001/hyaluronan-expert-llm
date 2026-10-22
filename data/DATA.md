# Data card — Hyaluronan corpus

## Sources (all open access / public APIs)
- **Full texts**: PubMed Central Open Access subset (JATS XML), retrieved via NCBI E-utilities.
  Query (title/abstract/MeSH): `hyaluronan OR "hyaluronic acid" OR hyaluronate` → 16,642 records.
- **Metadata**: PMID, DOI, year, title per article in `manifest.jsonl`.

## Pipeline
1. `data_pipeline/harvest_pmc.py` — history-based efetch paging (resumable), saves per-article XML.
2. `data_pipeline/clean_corpus.py` — XML → plain text (keeps abstract/body/captions; drops
   references & acknowledgments), drops stubs and non-English, dedups by DOI/title →
   `corpus_v1.jsonl` {pmcid, pmid, doi, year, title, journal, text, n_chars}.
3. Stats: `data/processed/corpus_stats.md` (committed to this repo).

## Downloads
Bulk data is published as **GitHub Release assets** (git history is not suited to GB-scale files):
see the repo's Releases page — `corpus_v1.jsonl.gz` (cleaned text corpus), `manifest.jsonl`,
and `pmc_xml.tar.gz` (raw JATS XML as harvested).

## Licensing note
Articles come from the PMC Open Access subset; individual articles carry their own
licenses (mostly CC-BY, some CC-BY-NC / publisher-specific). The manifest preserves
PMCID/DOI for every article so each item can be traced to its source license.
Redistribution here is for research / text-and-data-mining purposes.
