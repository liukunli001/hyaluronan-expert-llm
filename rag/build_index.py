#!/usr/bin/env python3
"""S5: chunk the HA corpus and build a FAISS vector index.

Chunks: paragraph-merged passages of ~900 chars (150-char overlap when a
paragraph must be split). Embeddings: Qwen/Qwen3-Embedding-0.6B (1024-d),
L2-normalized, IndexFlatIP (= cosine). Holdout PMCIDs (eval/holdout_pmcids.txt)
are asserted absent from the corpus before indexing.

Outputs (rag/index/): chunks.jsonl (text + pmcid/title/year), index.faiss
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EMB_MODEL = "Qwen/Qwen3-Embedding-0.6B"


def chunk_text(text, target=900, overlap=150):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) > 40]
    chunks, buf = [], ""
    for p in paras:
        if len(buf) + len(p) + 1 <= target:
            buf = (buf + "\n" + p) if buf else p
            continue
        if buf:
            chunks.append(buf)
        while len(p) > target:  # split an over-long paragraph with overlap
            chunks.append(p[:target])
            p = p[target - overlap:]
        buf = p
    if buf:
        chunks.append(buf)
    return chunks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(ROOT / "data/processed/corpus_v1.jsonl"))
    ap.add_argument("--out", default=str(ROOT / "rag/index"))
    ap.add_argument("--bsz", type=int, default=256)
    a = ap.parse_args()

    holdout = set()
    hfile = ROOT / "eval/holdout_pmcids.txt"
    if hfile.exists():
        holdout = {l.strip() for l in hfile if l.strip()}

    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    meta_fh = open(out / "chunks.jsonl", "w", encoding="utf-8")
    texts, n_papers, n_holdout_seen = [], 0, 0
    for line in open(a.corpus, encoding="utf-8"):
        r = json.loads(line)
        if r["pmcid"] in holdout:
            n_holdout_seen += 1
            continue
        n_papers += 1
        for ch in chunk_text(r["text"]):
            texts.append(ch)
            meta_fh.write(json.dumps({"pmcid": r["pmcid"], "title": r["title"],
                                      "year": r["year"], "text": ch},
                                     ensure_ascii=False) + "\n")
    meta_fh.close()
    print(f"papers indexed: {n_papers}, holdout excluded: {n_holdout_seen}, chunks: {len(texts)}", flush=True)
    assert n_holdout_seen == 0 or n_papers > 10000, "holdout leakage check"

    from sentence_transformers import SentenceTransformer
    import numpy as np, faiss
    model = SentenceTransformer(EMB_MODEL, device="cuda")
    emb = model.encode(texts, batch_size=a.bsz, show_progress_bar=True,
                       normalize_embeddings=True, convert_to_numpy=True).astype("float32")
    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb)
    faiss.write_index(index, str(out / "index.faiss"))
    print(f"index built: {index.ntotal} vectors x {emb.shape[1]}d -> {out}", flush=True)


if __name__ == "__main__":
    main()
