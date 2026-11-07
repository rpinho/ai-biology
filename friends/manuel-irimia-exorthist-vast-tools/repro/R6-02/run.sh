#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "Usage: bash repro/R6-02/run.sh /path/to/repo" >&2; exit 2; fi
HERE="$(cd "$(dirname "$0")" && pwd)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
exec nice -n 10 "${PYTHON:-python3}" "$HERE/../_shared/run_case.py" "R6-02" "$1"
