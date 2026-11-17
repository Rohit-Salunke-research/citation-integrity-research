"""Paired claim-level bootstrap for TF-IDF vs BM25 prediction files."""
import json, random, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"results"
def load(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
def metrics(row):
    ranked=[tuple(x) for x in row["ranked"]]
    gold={tuple(x) for x in row["gold"]}
    if not gold: return None
    hits=[i+1 for i,x in enumerate(ranked[:10]) if x in gold]
    return {
        "Recall@5":len(set(ranked[:5])&gold)/len(gold),
        "Recall@10":len(set(ranked[:10])&gold)/len(gold),
        "MRR@10":1/min(hits) if hits else 0.0
    }
def main():
    rows=load(RESULTS/"test_predictions.jsonl")
    by={}
    for r in rows:
        m=metrics(r)
        if m is not None: by.setdefault(r["method"],{})[r["claim_id"]]=m
    common=sorted(set(by["tfidf"])&set(by["bm25"]))
    rng=random.Random(13)
    output=[]
    for metric in ("Recall@5","Recall@10","MRR@10"):
        diffs=[by["tfidf"][i][metric]-by["bm25"][i][metric] for i in common]
        boot=[]
        for _ in range(4000):
            boot.append(sum(rng.choice(diffs) for _ in diffs)/len(diffs))
        boot.sort()
        output.append([metric,sum(diffs)/len(diffs),boot[99],boot[3899],len(common)])
    with (RESULTS/"paired_bootstrap_ci.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(["metric","tfidf_minus_bm25","bootstrap_95ci_low","bootstrap_95ci_high","paired_claims"]);w.writerows(output)
    print("Wrote paired_bootstrap_ci.csv")
if __name__=="__main__": main()
