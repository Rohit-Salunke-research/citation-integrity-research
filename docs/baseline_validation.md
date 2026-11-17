# Baseline validation record

## Validation status at repository assembly

| Gate | Evidence available | Status |
|---|---|---|
| Dataset source identified | Official Citation-Integrity upstream repository and recorded Git blob IDs | Documented; local download pending |
| Dataset schema / references audited | Packaged `results/data_audit.json` reports 8,515 corpus documents and zero missing cited/gold document references | Supplied audit; independently rerun pending |
| Retrieval implementation present | TF-IDF and BM25 implementations in `src/retrieval.py` | Present |
| Local unit tests | Python compilation and `pytest`: 5 tests passed | Passed in assembly environment |
| Full dev/test execution in this repository | Packaged aggregate CSVs and figures exist; no claim-level predictions are included | Independent regeneration pending |
| Paired statistical analysis | Packaged `paired_bootstrap_ci.csv`; script available | Output supplied; regeneration pending |
| Reproducible environment | Pinned dependencies and `docs/environment.txt` | Assembly test environment recorded; independent benchmark environment pending |

## Current blocker

A fresh dataset download was attempted using `scripts/download_data.py`, but the assembly container could not resolve `github.com`. No data-backed run was falsely marked as completed in this repository session. Rerun the documented pipeline in an internet-connected environment and preserve the generated prediction files and logs.
