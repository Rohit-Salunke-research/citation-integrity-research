"""Download the official Citation-Integrity benchmark files and verify their Git blob IDs."""
from pathlib import Path
import hashlib
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPO = DATA / "_upstream"
URL = "https://github.com/ScienceNLP-Lab/Citation-Integrity.git"
SOURCE = Path("Data/multivers-format")
EXPECTED_BLOBS = {
    "claims-train.jsonl": "0b25ca63c8e1ef79fabdeb77450fa845532c4ed6",
    "claims-dev.jsonl": "e1ddc68412ffd3b65512327267a18cd668d968b4",
    "claims-test.jsonl": "754eb9aa7b4c0d076910e0c0f76fab7684e96eec",
    "corpus.jsonl": "a62f42f63bf1dcd6de8d43d96968588c7a5600b7",
}


def git_blob_sha(path: Path) -> str:
    """Compute the Git blob object ID without requiring the Git executable."""
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def main() -> None:
    DATA.mkdir(exist_ok=True)
    source_dir = REPO / SOURCE
    if not all((source_dir / name).is_file() for name in EXPECTED_BLOBS):
        if REPO.exists():
            shutil.rmtree(REPO)
        subprocess.run(["git", "clone", "--depth", "1", URL, str(REPO)], check=True)
        source_dir = REPO / SOURCE

    missing = [name for name in EXPECTED_BLOBS if not (source_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Upstream repository is missing required files: {missing}")

    for name, expected_sha in EXPECTED_BLOBS.items():
        source = source_dir / name
        observed_sha = git_blob_sha(source)
        if observed_sha != expected_sha:
            raise RuntimeError(
                f"Upstream content changed for {name}: expected Git blob {expected_sha}, "
                f"received {observed_sha}. Check the upstream revision before proceeding."
            )
        destination = DATA / name
        shutil.copy2(source, destination)
        print(f"Verified and copied {name}: {destination.stat().st_size:,} bytes")

    print("All four dataset files match the blob IDs recorded in results/data_audit.json.")
    print("Review upstream repository and publication terms before redistribution.")


if __name__ == "__main__":
    main()
