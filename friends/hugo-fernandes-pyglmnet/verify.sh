#!/bin/bash
# For each fix branch: new test on master code (must FAIL), on fixed code (must PASS), full suite.
cd "$(dirname "$0")/pyglmnet" || exit 1
PY=../.venv-old/bin/python; export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
run() { nice -n 10 $PY -m pytest -q -p no:cacheprovider "$@" 2>&1 | tail -1; }
while read -r b t; do
  git checkout -q "$b" || exit 1
  git checkout -q master -- pyglmnet/
  echo "$b | new test, master code: $(run "$t")"
  git checkout -q HEAD -- pyglmnet/
  echo "$b | new test, fixed code:  $(run "$t")"
  echo "$b | full suite:            $(run tests)"
  nice -n 10 $PY -m pytest -q -p no:cacheprovider tests 2>&1 | grep FAILED | cut -c1-75 | sed 's/^/    /'
  [ -z "$(git status --short)" ] || { echo "dirty tree on $b"; exit 1; }
done <<LIST
fix-bernoulli-loglik tests/test_metrics.py::test_bernoulli_loglik_endpoints
fix-gamma-deviance tests/test_metrics.py::test_gamma_deviance_saturated
fix-gamma-simulate tests/test_pyglmnet.py::test_simulate_gamma_samples
LIST
git checkout -q master
