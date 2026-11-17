# AI assistance log

| Stage | AI assistance | Human verification / ownership |
|---|---|---|
| Initial audit | Identified that the supplied scaffold used SciFact and document-level classification, which did not directly match the review topic of genuine citation misinterpretation. | Student should inspect the original scaffold and assignment rubric. |
| Research design | Drafted a narrower evidence-sentence retrieval comparison using the official Citation-Integrity corpus, TF-IDF and BM25. | Student must confirm alignment with instructor requirements. |
| Data acquisition | Retrieved the official repository's four JSONL blobs and recorded their blob identifiers. | Student should verify source revision and preserve the data provenance record. |
| Implementation and analysis | Drafted loaders, candidate-pool construction, lexical rankers, evaluation metrics, paired bootstrap comparison, and lexical-overlap analysis. | Student should inspect the source code, reproduce commands locally, and understand the metric definitions. |
| Writing | Drafted the manuscript, tables, plots, and limitations based on the computed outputs. | Student must read, validate, and be able to explain every result and methodological choice. |

AI assistance was used for code drafting, debugging, analysis orchestration, and writing. The student remains responsible for verifying the dataset, reproducing the results, correcting errors, and defending the work. Do not claim independent reproduction until the documented commands have been run locally.
