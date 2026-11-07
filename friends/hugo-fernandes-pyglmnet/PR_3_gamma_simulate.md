Title: FIX: simulate_glm(sample=True) for gamma returns exp(mu) instead of gamma samples

With `distr='gamma'` and `sample=True`, `simulate_glm` returns `np.exp(mu)`: the same value for every seed, with no noise, and the wrong mean. For example, a mean of 1.103 gives 3.014 for every observation.

This PR draws `random_state.gamma(shape=1.0, scale=mu)`, i.e. shape-1 gamma observations with mean `mu`, matching the likelihood used for fitting. With 20,000 draws at that mean, the sample mean is 1.104 and the variance 1.19 (expected about 1.103 and 1.22). The same seed reproduces the same draws. `sample=False` is unchanged.

Test: `test_simulate_gamma_samples` in `tests/test_pyglmnet.py` fails on master and passes here. The rest of the suite is unchanged (same pre-existing failures on master as noted in the Bernoulli PR).

Open PR #390's `GammaSoftplus.simulate` also returns `np.exp(mu)`, so the same change would apply there.
