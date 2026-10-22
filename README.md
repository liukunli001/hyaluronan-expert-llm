# Hyaluronan Expert LLM

A domain-expert language model for **hyaluronan (HA) science**, built with the Hugging Face ecosystem
(Transformers + TRL) on an open-weight base model.

**Approach**
1. **Domain-adaptive continued pretraining (DAPT)** — continue training Qwen3-8B-Base on a curated hyaluronan
   corpus (PMC Open Access full texts + abstracts, weighted toward HA synthesis &
   chemical modification, CD44 biology, HA nanoparticles & drug delivery).
2. **SFT** — question answering generated from the corpus, expert spot-checked.
3. **Retrieval-grounded QA (RAG)** — the same corpus indexed (FAISS) so answers carry
   verifiable citations (title / year / DOI).
4. **HA-Expert-Bench** — a 200–300 question benchmark with expert-verified answer keys
   (held out from training), comparing base vs. domain-trained vs. domain-trained + RAG.

**Status**: Phase 1 (data collection) in progress.

Layout: `data_pipeline/` harvest & cleaning scripts · `training/` DAPT/SFT/DPO scripts · `eval/` benchmark ·
`rag/` retrieval QA · `notes/` project notes · `third_party/nanochat` from-scratch baseline (reference only).
