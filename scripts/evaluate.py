import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def metrics(row):
    ranked = [tuple(x) for x in row["ranked"]]
    gold = {tuple(x) for x in row["gold"]}
    if not gold:
        return None
    hits = [i + 1 for i, item in enumerate(ranked[:10]) if item in gold]
    return {
        "Recall@5": len(set(ranked[:5]) & gold) / len(gold),
        "Recall@10": len(set(ranked[:10]) & gold) / len(gold),
        "MRR@10": 1.0 / min(hits) if hits else 0.0
    }


def read(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def main():
    summaries = []
    by_overlap = []
    for split in ("dev", "test"):
        path = RESULTS / f"{split}_predictions.jsonl"
        if not path.exists():
            continue
        rows = read(path)
        for method in ("tfidf", "bm25"):
            subset = [row for row in rows if row["method"] == method]
            scored = [(row, metrics(row)) for row in subset]
            scored = [(row, score) for row, score in scored if score is not None]
            if not scored:
                continue
            for key in ("Recall@5", "Recall@10", "MRR@10"):
                values = [score[key] for _, score in scored]
                summaries.append({
                    "split": split,
                    "method": method,
                    "metric": key,
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
                    "n_claims": len(values)
                })

            # Derive overlap cutoffs from development and hold them fixed for test.
            overlap_values = np.array([row["overlap"] for row, _ in scored])
            if split == "dev":
                thresholds = np.quantile(overlap_values, [0.25, 0.5, 0.75]).tolist()
                (RESULTS / "overlap_thresholds.json").write_text(json.dumps(thresholds), encoding="utf-8")
            else:
                threshold_path = RESULTS / "overlap_thresholds.json"
                if not threshold_path.exists():
                    raise RuntimeError("Run dev first to derive overlap thresholds.")
                thresholds = json.loads(threshold_path.read_text())

            for row, score in scored:
                quartile = int(np.searchsorted(thresholds, row["overlap"], side="right")) + 1
                by_overlap.append({
                    "split": split,
                    "method": method,
                    "quartile": min(quartile, 4),
                    **score
                })

    if not summaries:
        raise RuntimeError("No prediction files found. Run scripts/run_experiment.py first.")

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(RESULTS / "metrics.csv", index=False)

    overlap_rows = pd.DataFrame(by_overlap)
    if not overlap_rows.empty:
        grouped = overlap_rows.groupby(
            ["split", "method", "quartile"], as_index=False
        ).agg(
            recall_at_10=("Recall@10", "mean"),
            mrr_at_10=("MRR@10", "mean"),
            n_claims=("MRR@10", "size")
        )
        grouped = grouped.rename(columns={"quartile": "dev_defined_overlap_quartile"})
        grouped.to_csv(RESULTS / "overlap_analysis.csv", index=False)

    plot_split = "test" if (summary_df["split"] == "test").any() else "dev"
    plot_data = summary_df[
        (summary_df["split"] == plot_split) & (summary_df["metric"] == "Recall@10")
    ]
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.bar(plot_data["method"], plot_data["mean"], yerr=plot_data["std"], capsize=4)
    ax.set_ylabel("Recall@10 (mean ± SD)")
    ax.set_title(f"Evidence-sentence retrieval: {plot_split}")
    fig.tight_layout()
    fig.savefig(RESULTS / "fig_recall_at_10.png", dpi=200)
    plt.close(fig)

    if not overlap_rows.empty:
        plot_overlap = grouped[grouped["split"] == plot_split]
        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        for method, group in plot_overlap.groupby("method"):
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

    print(summary_df.to_string(index=False))
    print("Wrote metrics, overlap analysis, and figures.")


if __name__ == "__main__":
    main()
