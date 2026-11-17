from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from evaluate import metrics


def test_reciprocal_rank_is_cut_off_at_ten():
    ranked = [["doc", i] for i in range(12)]
    result = metrics({"ranked": ranked, "gold": [["doc", 11]]})
    assert result["MRR@10"] == 0.0
    assert result["Recall@10"] == 0.0


def test_reciprocal_rank_uses_first_relevant_sentence_within_ten():
    ranked = [["doc", i] for i in range(12)]
    result = metrics({"ranked": ranked, "gold": [["doc", 2], ["doc", 11]]})
    assert result["MRR@10"] == 1 / 3
    assert result["Recall@10"] == 0.5
