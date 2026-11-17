# Reproducibility and submission checklist

## Before running
- [ ] Read the upstream dataset README and publication.
- [ ] Download the four JSONL files from the official repository.
- [ ] Run `python scripts/audit_data.py`.
- [ ] Inspect `results/data_audit.json`; all missing-document counts must be zero.
- [ ] Run the development experiment and inspect sample predictions.
- [ ] Freeze code and `configs/protocol.json` before final test evaluation.
- [ ] Record `python --version`, `pip freeze`, operating system, and Git commit hash.

## After running
- [ ] Run test once after freeze.
- [ ] Run `python scripts/evaluate.py`.
- [ ] Copy exact values from `results/metrics.csv` into the paper.
- [ ] Inspect `results/overlap_analysis.csv` and representative retrieval misses.
- [ ] Include the actual outputs and logs in the repository.
- [ ] Recompile LaTeX and inspect the PDF.
- [ ] Remove all remaining bracketed placeholders.
- [ ] Ensure no claim is stronger than the experiment supports.

## AI-use disclosure draft
AI assistance was used to help audit the initial project scaffold, identify mismatches between the planned research question and the original SciFact-based implementation, draft code structure and documentation, and improve clarity of the manuscript. The dataset source, task definition, evaluation protocol, code execution, outputs, and final interpretations must be checked by the student. The student should add specific examples of AI suggestions that were accepted, rejected, or corrected after personally reviewing the code and results. Do not claim that an experiment was run unless the corresponding output file and execution log exist.
