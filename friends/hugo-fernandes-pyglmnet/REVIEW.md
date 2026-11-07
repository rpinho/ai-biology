PR 1 — VERDICT: FIX FIRST

- `pyglmnet/pyglmnet.py:142,149`: `-y_hat` raises `TypeError` for boolean probabilities and wraps unsigned integers. With `y=[0.]` and `y_hat=np.array([1], dtype=np.uint8)`, both families return **+5.545177** instead of `-inf`. Convert probabilities to floating point before negation and test these dtypes.

PR 2 — VERDICT: FIX FIRST

- `tests/test_metrics.py:64`: The regression covers only deviance, leaving both `pseudo_R2` changes untested. Add assertions for `1 - D/D_null`, perfect-fit score 1, null-model score 0, and scale invariance.
- `out/PR_2_gamma_deviance.md:11`: The class in [PR #390](https://github.com/glm-tools/pyglmnet/pull/390/files) is named `GammaSoftplus`, not `Gamma`.

PR 3 — VERDICT: FIX FIRST

- `tests/test_pyglmnet.py:523`: All assertions also pass with the deterministic replacement `y = np.roll(mu, 1)`; its residual standard deviation is approximately **0.1648**. Add a different-seed check and check variance against `mu**2` using constant means.
- `out/PR_3_gamma_simulate.md:9`: “`Gamma.simulate`” should be “`GammaSoftplus.simulate`” in [PR #390](https://github.com/glm-tools/pyglmnet/pull/390/files).