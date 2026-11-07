Title: FIX: gamma deviance and pseudo-R2 omit the saturated log likelihood

`deviance` and `pseudo_R2` in `metrics.py` take the saturated log likelihood `LS` as 0 for every family except softplus, Poisson and negative binomial. For gamma (shape 1, as in `_logL`) it is `sum(-1 - log(y))`, not 0. So the gamma deviance is negative even for perfect predictions: for `y = [0.1, 0.2, 0.4]` and `yhat = y` it is -3.66 instead of 0, and it changes with the units of `y`.

This PR adds `'gamma'` to the families that use `LS`. The deviance then equals the textbook `2 * sum((y - mu) / mu - log(y / mu))` (it matches statsmodels' `Gamma().deviance`), is 0 for perfect predictions, and does not change when `y` and `mu` are rescaled together. Gamma pseudo-R2 becomes `1 - D / D_null`, the convention the count families already use, so a perfect fit scores 1.

For a fixed data set the added term is a constant, so a deviance-based ranking of lambdas does not change; pseudo-R2 values for gamma do change.

Test: `test_gamma_deviance_saturated` in `tests/test_metrics.py` (deviance and pseudo-R2) fails on master and passes here. The rest of the suite is unchanged (same pre-existing failures on master as noted in the Bernoulli PR).

Open PR #390 keeps the same family list (`Poisson, PoissonSoftplus, NegBinomialSoftplus`), so `GammaSoftplus` would need adding there too.
