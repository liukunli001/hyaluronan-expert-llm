#!/bin/bash
cd ~/workspace/hyaluronan-expert-llm || exit 1
exec > data/processed/package.log 2>&1
set -x
rm -f data/processed/corpus_v1.jsonl.gz
gzip -kf data/processed/corpus_v1.jsonl && gzip -t data/processed/corpus_v1.jsonl.gz || exit 1
tar -czf data/raw/pmc_xml.tar.gz -C data/raw pmc_xml || exit 1
ls -la data/processed/corpus_v1.jsonl.gz data/raw/pmc_xml.tar.gz
git add -A && git commit -qm "Corpus v1 final stats: 12,306 papers, ~126M est tokens" && git push -q
gh release create v0.1-data data/processed/corpus_v1.jsonl.gz data/raw/manifest.jsonl data/raw/pmc_xml.tar.gz \
  --title "Corpus v0.1 - hyaluronan full-text corpus" \
  --notes "PMC Open Access full texts matching hyaluronan query (16,642 records -> 12,945 harvested -> 12,306 after cleaning, ~126M est tokens). corpus_v1.jsonl.gz: cleaned text corpus (stats: data/processed/corpus_stats.md). pmc_xml.tar.gz: raw JATS XML. manifest.jsonl: PMCID/PMID/DOI/year/title per article. Per-article licenses vary (PMC OA subset) - see data/DATA.md." \
  || gh release upload v0.1-data data/processed/corpus_v1.jsonl.gz data/raw/manifest.jsonl data/raw/pmc_xml.tar.gz --clobber
echo PACKAGE-DONE
