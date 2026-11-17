import json

def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def load_corpus(path):
    docs = {}
    for row in read_jsonl(path):
        doc_id = str(row.get("doc_id", row.get("id")))
        abstract = row.get("abstract", [])
        if isinstance(abstract, str):
            abstract = [abstract]
        docs[doc_id] = {"title": row.get("title", ""),
                        "sentences": [str(x) for x in abstract]}
    return docs

def load_claims(path):
    normalized = []
    for c in read_jsonl(path):
        gold = set()
        for doc_id, groups in (c.get("evidence", {}) or {}).items():
            for group in groups:
                for idx in group.get("sentences", []):
                    gold.add((str(doc_id), int(idx)))
        normalized.append({
            "id": str(c["id"]), "claim": str(c["claim"]),
            "cited_doc_ids": [str(x) for x in c.get("cited_doc_ids", [])],
            "gold": gold, "raw": c
        })
    return normalized

def candidate_sentences(claim, corpus):
    result = []
    for doc_id in claim["cited_doc_ids"]:
        doc = corpus.get(str(doc_id))
        if doc is None:
            continue
        for i, sentence in enumerate(doc["sentences"]):
            result.append({"doc_id": str(doc_id), "sent_idx": i, "text": sentence})
    return result

def validate(corpus, train, dev, test):
    # Article/document-level split check: claim IDs restart in each split.
    article_sets = [
        {d for c in split for d in c["cited_doc_ids"]}
        for split in (train, dev, test)
    ]
    assert not (article_sets[0] & article_sets[1]), "train/dev reference article overlap"
    assert not (article_sets[0] & article_sets[2]), "train/test reference article overlap"
    assert not (article_sets[1] & article_sets[2]), "dev/test reference article overlap"
    missing_cited = missing_gold = 0
    for split in (train, dev, test):
        for c in split:
            missing_cited += sum(d not in corpus for d in c["cited_doc_ids"])
            missing_gold += sum(d not in corpus for d, _ in c["gold"])
            for d, i in c["gold"]:
                if d in corpus:
                    assert 0 <= i < len(corpus[d]["sentences"]), (
                        f"Gold sentence index out of range: claim={c['id']} doc={d} idx={i}")
    return {
        "corpus_documents": len(corpus), "train_claims": len(train),
        "dev_claims": len(dev), "test_claims": len(test),
        "train_with_gold": sum(bool(c["gold"]) for c in train),
        "dev_with_gold": sum(bool(c["gold"]) for c in dev),
        "test_with_gold": sum(bool(c["gold"]) for c in test),
        "missing_cited_document_references": missing_cited,
        "missing_gold_document_references": missing_gold
    }
