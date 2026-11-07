#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export R_LIBS_USER="$PWD/env/Rlib" TMPDIR="$PWD/env"
R_SCRIPT="${R_SCRIPT:-$HOME/dev/open-science/friends_recheck_manuel_1105/env/runtime/bin/Rscript}"
nice -n 10 "$R_SCRIPT" analysis/reproduce.R B03 > repro/B03/r_output.txt 2>&1
nice -n 10 env/python/bin/python analysis/independent.py B03 > repro/B03/python_output.txt 2>&1
cat repro/B03/r_output.txt
cat repro/B03/python_output.txt
