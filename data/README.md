# Dataset acquisition

The raw Citation-Integrity JSONL files are intentionally not committed to this repository. Download them from the official upstream repository by running:

```bash
python scripts/download_data.py
```

The script clones `https://github.com/ScienceNLP-Lab/Citation-Integrity`, copies the four files from `Data/multivers-format/`, and verifies each file against the Git blob ID recorded in `results/data_audit.json`. It fails rather than silently accepting changed upstream data. Review upstream licensing and publication terms before use or redistribution.

Expected local files:

- `claims-train.jsonl`
- `claims-dev.jsonl`
- `claims-test.jsonl`
- `corpus.jsonl`

They are ignored by Git to avoid redistributing raw benchmark data.
