Title: FIX: Bernoulli log likelihood is NaN at probabilities 0 and 1, and overflows for large logits

`_logL` for `binomial` and `probit` computes `y * log(y_hat) + (1 - y) * log(1 - y_hat)`. When a prediction is exactly 0 or 1 this evaluates `0 * log(0)`, so a perfect prediction gives a NaN log likelihood and a NaN deviance from `GLM.score`. The logistic path with `z` uses `log(1 + exp(z))`, which overflows for large positive `z` (`z = 1000` gives `-inf` instead of 0).

This PR uses `scipy.special.xlogy` / `xlog1py`, which treat `0 * log(0)` as 0, and `np.logaddexp(0, z)`, and casts probabilities to float first so integer or boolean inputs are not wrapped by the negation. Interior probabilities and moderate logits give the same values as before. A predicted probability of exactly 1 for an observed 0 still gives `-inf`, as it should.

Test: `test_bernoulli_loglik_endpoints` in `tests/test_metrics.py` fails on master and passes here. The rest of the suite is unchanged (on numpy 1.23, scipy 1.10 and scikit-learn 1.2, `test_glm_estimator`, `test_cv` and `test_intro_example` fail on master too, and `test_group_lasso` fails intermittently on master).

Open PR #390 moves this code into `Binomial` and `Probit` classes with the same expressions, so the same change would apply there.
