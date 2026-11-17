import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data import load_corpus, load_claims, validate

SOURCE_METADATA = {
    "source_repository": "https://github.com/ScienceNLP-Lab/Citation-Integrity",
    "source_path": "Data/multivers-format/",
    "source_blob_shas": {
        "claims-train.jsonl": "0b25ca63c8e1ef79fabdeb77450fa845532c4ed6",
        "claims-dev.jsonl": "e1ddc68412ffd3b65512327267a18cd668d968b4",
        "claims-test.jsonl": "754eb9aa7b4c0d076910e0c0f76fab7684e96eec",
        "corpus.jsonl": "a62f42f63bf1dcd6de8d43d96968588c7a5600b7"
    }
}

def main():
    d = ROOT / "data"
    corpus = load_corpus(d / "corpus.jsonl")
    train = load_claims(d / "claims-train.jsonl")
    dev = load_claims(d / "claims-dev.jsonl")
    test = load_claims(d / "claims-test.jsonl")
    report = {**SOURCE_METADATA, **validate(corpus, train, dev, test)}
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "data_audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["missing_cited_document_references"] or report["missing_gold_document_references"]:
        raise SystemExit("Data audit found unresolved document references; inspect before experiments.")

if __name__ == "__main__":
    main()
