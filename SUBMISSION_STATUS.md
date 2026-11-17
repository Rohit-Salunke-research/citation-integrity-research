# Submission status

## Packaged
- Narrow research question and explicit retrieval-only scope.
- Dataset source and provenance summary.
- TF–IDF and BM25 implementations and shared candidate-pool protocol.
- Packaged aggregate result tables, bootstrap intervals, overlap analysis and figures.
- LaTeX manuscript source, bibliography and compiled PDF.
- Reproduction scripts, configuration, tests, limitations and AI-assistance documentation.

## Validation performed during repository assembly
- Python source files compile successfully.
- Unit tests pass: 5 passed.
- The report PDF was rebuilt from the personalized LaTeX source.
- The internal review/checklist, research decision log, frozen protocol summary, and environment snapshot were added.

## Still required before calling this submission fully verified
1. Inspect the personalized author field and recompiled PDF cover and rendered pages.
2. Run the dataset download and audit commands in a clean local environment. The assembly container could not resolve GitHub for a live dataset download, so end-to-end reproduction remains pending.
3. Run development, freeze the protocol/code, then run the held-out test experiment and evaluation scripts.
4. Verify regenerated metrics against the packaged tables; preserve generated per-claim predictions and runtime logs.
5. Run the unit tests and record Python, dependency versions, OS and commit hash.
6. Confirm the exact instructor template/rubric and repository visibility requirements.
7. Read the paper and ensure the submitting student can explain the dataset, candidate pool, gold pairs, Recall@k, MRR@10, paired bootstrap and limitations.

The aggregate tables/figures in this repository were present in the reviewed input bundle. They have not yet been independently regenerated in this repository environment. No claim of independent local reproduction should be made until the checks above are completed.
