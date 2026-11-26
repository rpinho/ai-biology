# Deviations Log

This file records any technical adjustments forced after committing `SEALED.md` (`ee30be763e5c800ddc5c47a62ecc1700231c7599`).

1. **RDKit wheel downgrade (`2026.9.2` -> `2025.9.6`, pre-execution unit-test catch):**
   - **Reason:** Before running any TDC data processing or model evaluation, `src/test_pipeline.py` revealed that `rdkit==2026.9.2` on macOS ARM64 raises `RuntimeError: bad any cast` inside `Chem.MurckoDecompose` (affecting `MurckoScaffold.MurckoScaffoldSmiles`).
   - **Fix:** Downgraded `rdkit` in `./.venv` to `2025.9.6` (same 2025.09 release series pinned by `synfactor/requirements.txt`).
   - **Protocol impact:** Zero changes to datasets, splits, BRICS 1-cut rules, featurization, models, hyperparameters, metrics, or pass/fail thresholds.

2. **Subprocess isolation for LightGBM & vectorized exact permutation/bootstrap (`src/lgbm_worker.py`, `src/stats_utils.py`):**
   - **Reason:** On macOS ARM64, importing both `lightgbm` (linking `@rpath/libomp.dylib`) and `torch` (linking `torch/lib/libomp.dylib`) in the same Python process loaded two conflicting LLVM OpenMP runtimes, causing either `OMP: Error #179: Function pthread_mutex_init failed` (SIGSEGV) or an OpenMP barrier deadlock during PyTorch training (causing attempt 1 to time out at 7200s). In addition, unvectorized Python loops in `stats_utils.py` added unnecessary overhead for 10,000-permutation tests on large test splits (`n ~ 2,400`).
   - **Fix:** Isolated LightGBM training/scoring in a clean subprocess (`src/lgbm_worker.py`, which never imports `torch`) while keeping all locked hyperparameters verbatim (including `n_jobs=4`), and vectorized `bootstrap_metric` / `paired_comparison` in `src/stats_utils.py` (verified `< 1e-12` equivalent to scalar `sklearn`/`scipy` references including ties in `src/test_pipeline.py`).
   - **Protocol impact:** Zero changes to datasets, splits, BRICS 1-cut rules, featurization, models, hyperparameters (`n_jobs=4`, `torch.set_num_threads(4)`, seeds), metrics, or pass/fail thresholds.
