#!/usr/bin/env python3
"""S5: retrieval over the HA corpus index (built by rag/build_index.py).

retrieve(question, k) -> list of excerpt strings, each carrying its source
(title + PMCID) so the generator can cite [1], [2], ... as run_eval.py's
prompt instructs. Query uses Qwen3-Embedding's instruction prefix.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT / "rag/index"
EMB_MODEL = "Qwen/Qwen3-Embedding-0.6B"
QUERY_INSTRUCT = ("Instruct: Given a scientific question about hyaluronan "
                  "(hyaluronic acid), retrieve literature passages that answer it.\nQuery: ")

_state = {}


def _load():
    if _state:
        return _state
    import faiss
    from sentence_transformers import SentenceTransformer
    _state["index"] = faiss.read_index(str(INDEX_DIR / "index.faiss"))
    _state["chunks"] = [json.loads(l) for l in open(INDEX_DIR / "chunks.jsonl", encoding="utf-8")]
    _state["model"] = SentenceTransformer(EMB_MODEL, device="cuda")
    return _state


def retrieve(question, k=4):
    s = _load()
    import numpy as np
    q = s["model"].encode([QUERY_INSTRUCT + question], normalize_embeddings=True,
                          convert_to_numpy=True).astype("float32")
    _, idx = s["index"].search(q, k)
    hits = []
    for i in idx[0]:
        c = s["chunks"][int(i)]
        hits.append(f"{c['title']} (PMCID: {c['pmcid']}, {c['year']}): {c['text']}")
    return hits


if __name__ == "__main__":
    import sys
    for h in retrieve(sys.argv[1] if len(sys.argv) > 1 else "How does hyaluronan bind CD44?", k=3):
        print("-", h[:220], "\n")
