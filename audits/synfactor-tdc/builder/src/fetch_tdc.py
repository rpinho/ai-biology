"""Download public TDC ADMET datasets from Harvard Dataverse with SHA-256 provenance."""

import hashlib
import json
from pathlib import Path

import requests

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Official TDC Dataverse file IDs from https://github.com/mims-harvard/TDC/blob/main/tdc/metadata.py
DATASETS = {
    "herg": {
        "file_id": 4259588,
        "filename": "herg.tab",
        "task": "classification",
        "tdc_name": "hERG",
    },
    "cyp3a4_veith": {
        "file_id": 4259582,
        "filename": "cyp3a4_veith.tab",
        "task": "classification",
        "tdc_name": "CYP3A4_Veith",
    },
    "lipophilicity_astrazeneca": {
        "file_id": 4259595,
        "filename": "lipophilicity_astrazeneca.tab",
        "task": "regression",
        "tdc_name": "Lipophilicity_AstraZeneca",
    },
    "solubility_aqsoldb": {
        "file_id": 4259610,
        "filename": "solubility_aqsoldb.tab",
        "task": "regression",
        "tdc_name": "Solubility_AqSolDB",
    },
}

BASE_URL = "https://dataverse.harvard.edu/api/access/datafile/"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, info in DATASETS.items():
        url = f"{BASE_URL}{info['file_id']}"
        out_path = DATA_DIR / info["filename"]
        if not out_path.exists():
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            out_path.write_bytes(resp.content)
        digest = sha256_file(out_path)
        manifest[key] = {
            **info,
            "url": url,
            "bytes": out_path.stat().st_size,
            "sha256": digest,
        }
        print(f"{key}: {out_path.stat().st_size} bytes, sha256={digest}")
    (DATA_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {DATA_DIR / 'manifest.json'}")


if __name__ == "__main__":
    main()
