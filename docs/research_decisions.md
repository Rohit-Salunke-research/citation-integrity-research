# Research decision log

This log records the design choices embodied in the current repository. It should be extended when a new decision changes the protocol.

| Decision | Rationale | Trade-off / limitation | Status |
|---|---|---|---|
| Use the Sarol et al. Citation-Integrity corpus in MultiVerS format | It contains genuine citation contexts and sentence-level evidence annotations relevant to source-evidence retrieval | Biomedical domain only; dataset terms must be checked before redistribution | Selected; data download must be independently repeated |
| Narrow the study to evidence-sentence retrieval | Keeps the experiment executable with a clear shared candidate pool and sentence-level gold labels | Does not classify whether a citation is accurate, inaccurate, or irrelevant | Selected and reflected in the title and scope |
| Compare TF-IDF and BM25 | Two transparent lexical baselines can be evaluated under identical queries, candidates, and gold items | No dense retriever, reranker, or semantic NLI classifier is included | Selected baseline comparison |
| Use all abstract sentences from `cited_doc_ids` as candidates | Both systems face the same bounded candidate set; this avoids mixing retrieval strategies with document discovery | Results do not measure open-world literature search | Selected |
| Score only records with sentence-level gold evidence | Recall and reciprocal-rank metrics require a sentence-level target | Records without such gold are excluded rather than assigned zero | Selected; report excluded count |
| Report MRR@10 | The experiment stores and evaluates only the top 10 ranked sentences | It does not measure reciprocal rank beyond rank 10 | Corrected in code and paper |
| Derive lexical-overlap quartiles on development data | Keeps test subgroup thresholds fixed before test interpretation | Overlap quartiles are descriptive and do not establish causality | Selected |

## Open decisions / required checks

- Verify the upstream dataset revision and terms when running the download script.
- Independently reproduce the packaged aggregates and retain prediction files.
- Confirm the assignment rubric accepts a retrieval-only study as the final scope; if not, extend the protocol rather than implying classification results.
- Add any human-chosen deviations, accepted/rejected AI suggestions, and instructor feedback with dates.
