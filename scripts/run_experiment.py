import argparse, json, sys
from pathlib import Path
from collections import Counter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data import load_corpus, load_claims, candidate_sentences
from retrieval import SentenceIndex, tokenize

def overlap(query, candidates):
    q = set(tokenize(query))
    if not q or not candidates:
        return 0.0
    best = 0.0
    for s in candidates:
        t = set(tokenize(s["text"]))
        if t:
            best = max(best, len(q & t) / max(1, len(q)))
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["dev", "test"], required=True)
    args = ap.parse_args()
    data_dir = ROOT / "data"
    corpus = load_corpus(data_dir / "corpus.jsonl")
    claims = load_claims(data_dir / f"claims-{args.split}.jsonl")
    rows = []
    for n, c in enumerate(claims, 1):
        if not c["gold"]:
            continue
        candidates = candidate_sentences(c, corpus)
        idx = SentenceIndex(candidates)
        for method in ("tfidf", "bm25"):
            ranked = getattr(idx, method)(c["claim"], 10)
            ranked_pairs = [(candidates[i]["doc_id"], candidates[i]["sent_idx"]) for i, _ in ranked]
            rows.append({
                "claim_id": c["id"], "method": method,
                "ranked": ranked_pairs,
                "gold": sorted(c["gold"]),
                "candidate_count": len(candidates),
                "gold_count": len(c["gold"]),
                "overlap": overlap(c["claim"], candidates)
            })
        if n % 100 == 0:
            print(f"{args.split}: processed {n}/{len(claims)} claims")
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    path = out / f"{args.split}_predictions.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"Wrote {path} ({len(rows)} method-claim records)")

if __name__ == "__main__":
    main()
