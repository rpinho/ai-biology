"""Encode our own public-derived code for stdin-only execution on the pod."""
from pathlib import Path
import base64, sys
payload=base64.b64encode(Path(sys.argv[1]).read_bytes()).decode()
Path(sys.argv[2]).write_text(
    'set -eu\nexport PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1\n'
    "base64 -d <<'PYCODE' | nice -n 10 python3 -u -\n"+payload+"\nPYCODE\n")
