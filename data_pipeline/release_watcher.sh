#!/bin/bash
cd ~/workspace/hyaluronan-expert-llm
for i in $(seq 1 360); do
  if grep -q "^DONE" data/raw/harvest.log; then break; fi
  sleep 30
done
grep -q "^DONE" data/raw/harvest.log || { echo "watcher: harvest DONE not seen, giving up"; exit 1; }
python3 data_pipeline/clean_corpus.py > data/processed/clean_final.log 2>&1
gzip -kf data/processed/corpus_v1.jsonl
tar -czf data/raw/pmc_xml.tar.gz -C data/raw pmc_xml
git add -A && git commit -qm "Corpus v1 final stats (full harvest)" && git push -q
gh release create v0.1-data data/processed/corpus_v1.jsonl.gz data/raw/manifest.jsonl data/raw/pmc_xml.tar.gz \
  --title "Corpus v0.1 — hyaluronan full-text corpus" \
  --notes "PMC Open Access full texts matching hyaluronan query (16,642 records). corpus_v1.jsonl.gz: cleaned text corpus (see data/processed/corpus_stats.md in repo). pmc_xml.tar.gz: raw JATS XML as harvested. manifest.jsonl: per-article PMCID/PMID/DOI/year/title. Per-article licenses vary (PMC OA subset) — see data/DATA.md."
echo "RELEASE DONE"
