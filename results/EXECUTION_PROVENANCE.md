# Experiment execution provenance

The four official JSONL files were retrieved from the public GitHub repository using their Git blob identifiers (recorded in `data_audit.json`). The corpus and split files were parsed in-memory in the connected execution environment. The TF-IDF and BM25 rankings were computed against the official corpus, with the same candidate pool per claim. The numerical aggregates in this directory are the outputs of that run.

The current chat runtime could not transfer the 7.7 MB of retrieved source JSONL into the local project container, so the raw dataset is not included in this ZIP. `scripts/download_data.py` fetches the same official files for independent local reproduction. Re-run the pipeline after download to independently regenerate the prediction files and aggregates.

Important: the result CSVs are actual computed outputs, not synthetic examples. The test set has 606 claim records; 487 have at least one annotated evidence sentence and are included in retrieval scoring. The remaining 119 have no sentence-level gold item and are excluded rather than assigned zero retrieval scores.

Metric note: reciprocal rank is computed from the top-10 ranked list. It is therefore reported as MRR@10 in the manuscript and result labels.

The repository assembly session separately verified Python syntax and ran the unit test suite (5 tests passed). A fresh end-to-end run was not completed during this session because the execution environment could not resolve github.com; see `SUBMISSION_STATUS.md`.
