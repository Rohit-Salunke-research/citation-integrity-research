
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from retrieval import SentenceIndex

def test_rankers_return_valid_indices():
    docs = [
        {"doc_id": "a", "sent_idx": 0, "text": "Neural networks classify images."},
        {"doc_id": "a", "sent_idx": 1, "text": "The cohort received a placebo."},
        {"doc_id": "b", "sent_idx": 0, "text": "Image classification uses neural models."}
    ]
    idx = SentenceIndex(docs)
    for method in (idx.tfidf, idx.bm25):
        ranked = method("neural models for image classification", 2)
        assert len(ranked) == 2
        assert all(0 <= i < len(docs) for i, _ in ranked)

def test_empty_candidates():
    idx = SentenceIndex([])
    assert idx.tfidf("test", 5) == []
    assert idx.bm25("test", 5) == []

def test_bm25_relevance_order():
    docs = [
        {"doc_id": "a", "sent_idx": 0, "text": "The trial evaluated a new vaccine."},
        {"doc_id": "a", "sent_idx": 1, "text": "Unrelated kidney function results were reported."}
    ]
    ranked = SentenceIndex(docs).bm25("vaccine trial", 2)
    assert ranked[0][0] == 0
