# Evidence-Sentence Retrieval for Scientific Citation Integrity

**AI Tools for Research — Post-Mid-Semester Assignment**

This repository contains the implementation and reproducibility package for a focused study comparing lexical methods for retrieving annotated evidence sentences from genuine scientific citation contexts.

## Research question

How do TF–IDF cosine similarity and BM25 compare in retrieving annotated evidence sentences from cited reference articles, and how does retrieval vary with lexical overlap between a citation context and candidate evidence sentences?

## Scope

This project evaluates the evidence-sentence retrieval stage only. It does **not** claim to solve citation-integrity classification, determine whether a citation is accurate, or reproduce the full Sarol et al. system.

## Repository structure

- `configs/`: experiment settings
- `data/`: downloaded locally; raw benchmark is not committed
- `docs/`: reproducibility and AI-use documentation
- `paper/`: LaTeX source, bibliography, compiled report
- `results/`: packaged aggregate tables, figures and provenance
- `scripts/`: download, audit, run and evaluate scripts
- `src/`: dataset parsing and retrieval implementations
- `tests/`: unit tests

## Dataset and provenance

The benchmark is the public Citation-Integrity corpus by Sarol et al. (2024), distributed in MultiVerS format:

- Upstream repository: https://github.com/ScienceNLP-Lab/Citation-Integrity
- Expected data directory: `Data/multivers-format/`
- Expected files: `claims-train.jsonl`, `claims-dev.jsonl`, `claims-test.jsonl`, and `corpus.jsonl`.

The raw dataset is not redistributed here. `scripts/download_data.py` clones the upstream repository and copies the four files into `data/`. Review upstream terms before use or redistribution. The packaged data-audit summary records upstream blob identifiers, 8,515 corpus documents, 2,141 train claims, 316 development claims, 606 test claims, and zero missing cited-document or gold-document references. Of the test records, 487 contain sentence-level gold evidence; 119 without sentence-level gold are excluded from retrieval scoring rather than treated as failures.

## Methods and evaluation

Both methods rank the same candidate pool: all abstract sentences from documents listed in each claim's `cited_doc_ids`. Gold targets are `(document_id, sentence_index)` pairs from the claim's `evidence` annotation.

- **TF–IDF:** word unigrams, sublinear term frequency, smoothed inverse document frequency, L2 normalization, cosine similarity.
- **BM25:** Okapi BM25 with `k1=1.5` and `b=0.75`.
- **Metrics:** macro Recall@5, Recall@10, and MRR over claims with sentence-level gold evidence.
- **Uncertainty:** paired claim-level bootstrap intervals (4,000 resamples; seed 13).
- **Deeper analysis:** lexical-overlap quartiles, with thresholds derived from development data and applied unchanged to test data.

The protocol is specified in `configs/protocol.json`. See `results/EXECUTION_PROVENANCE.md` and `results/data_audit.json` for packaged provenance details.

## Setup and reproduction

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Download and audit the dataset:

```bash
python scripts/download_data.py
python scripts/audit_data.py
```

Run development first, then test, then evaluation:

```bash
python scripts/run_experiment.py --split dev
python scripts/run_experiment.py --split test
python scripts/evaluate.py
python scripts/paired_bootstrap.py
```

Run tests:

```bash
python -m pytest -q
```

The scripts generate claim-level prediction JSONL files under `results/`, in addition to aggregate CSVs and figures. Preserve the prediction files and record Python/package versions, operating system, and commit hash when conducting an independent reproduction. Do not tune against the test split.

## Packaged results (not yet independently regenerated here)

The reviewed project bundle includes measured aggregate outputs and figures. Its test metrics are:

| Method | Recall@5 | Recall@10 | MRR |
|---|---:|---:|---:|
| TF–IDF | 0.2594 | 0.3666 | 0.3231 |
| BM25 | 0.2575 | 0.3607 | 0.3084 |

The paired 95% bootstrap intervals for TF–IDF minus BM25 include zero for all three metrics. Therefore, these results do not establish a statistically reliable winner. The highest lexical-overlap quartile has higher Recall@10 than the lowest quartile for both methods, but the relationship is descriptive and not strictly monotonic.

The packaged results and their provenance are documented in `results/`. They are outputs supplied by the reviewed bundle; this repository setup has not yet independently regenerated them. Consult `SUBMISSION_STATUS.md` and `results/REPRODUCTION_PENDING.txt` before treating the work as fully reproduced.

## Limitations

1. Candidate documents are restricted to `cited_doc_ids`; this is not open-world literature retrieval.
2. Sentence-level annotations may not enumerate every useful evidence sentence.
3. Claims without sentence-level gold evidence are excluded from retrieval metrics.
4. Lexical methods do not perform semantic verification or citation-accuracy classification.
5. The benchmark is biomedical, so generalization to other disciplines is untested.
6. Lexical-overlap analysis is descriptive, not causal.

## Paper

- `paper/main.tex` — editable LaTeX source
- `paper/references.bib` — bibliography
- `paper/assignment_report.pdf` — compiled report included in the reviewed bundle

The report currently contains a `[Student Name]` placeholder. Replace it with the submitting student's name, recompile the PDF, and inspect the final artifact before submission.

## Reference

Sarol, M. J., Ming, S., Radhakrishna, S., Schneider, J., & Kilicoglu, H. (2024). Assessing citation integrity in biomedical publications: corpus annotation and NLP models. *Bioinformatics*, 40(7), btae420. https://doi.org/10.1093/bioinformatics/btae420
