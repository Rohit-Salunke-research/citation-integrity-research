"""Render repository result figures from the committed aggregate CSV summaries."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def main():
    metrics = pd.read_csv(RESULTS / "metrics.csv")
    overlap = pd.read_csv(RESULTS / "overlap_analysis.csv")
    test_metrics = metrics[
        (metrics["split"] == "test") & (metrics["metric"] == "Recall@10")
    ]
    if test_metrics.empty:
        raise RuntimeError("No test Recall@10 values found in results/metrics.csv")

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.bar(test_metrics["method"], test_metrics["mean"])
    ax.set_ylabel("Recall@10")
    ax.set_title("Evidence-sentence retrieval: test split")
    fig.tight_layout()
    fig.savefig(RESULTS / "fig_recall_at_10.png", dpi=200)
    plt.close(fig)

    test_overlap = overlap[overlap["split"] == "test"]
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    for method, group in test_overlap.groupby("method"):
        group = group.sort_values("dev_defined_overlap_quartile")
        ax.plot(
            group["dev_defined_overlap_quartile"],
            group["mrr_at_10"],
            marker="o",
            label=method
        )
    ax.set_xlabel("Lexical-overlap quartile (development thresholds)")
    ax.set_ylabel("MRR@10")
    ax.set_xticks([1, 2, 3, 4])
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS / "fig_mrr_by_overlap.png", dpi=200)
    plt.close(fig)
    print("Rendered figures from committed aggregate tables.")


if __name__ == "__main__":
    main()
