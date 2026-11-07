# Independent referee verdicts

Scientific NEW: **no**. These are maintenance findings, not a new scientific result. Of 14 claims: **8 CONFIRMED, 3 CONFIRMED-MINOR, 2 KNOWN, 1 INTENDED**. All 14 described behaviors reproduced at the pinned commits; reproduction alone does not establish that a behavior is an unreported bug.

| ID | Verdict | My independent repro | Effect on users / qualification |
| --- | --- | --- | --- |
| S01 | CONFIRMED | [S01.py](repro/S01.py), [output](repro/S01.json) | Counts 2,4,6: package loss prefers mean 7 over the correct constant Poisson MLE 4; this loss controls restart selection and stopping. |
| S02 | CONFIRMED | [S02.py](repro/S02.py), [output](repro/S02.json) | Default population plot gives SEM 0.0575 instead of 0.16955825 for normalized neuron responses 0.1,0.3,0.6,1; uncertainty bands are too narrow. |
| S03 | CONFIRMED-MINOR | [S03.py](repro/S03.py), [output](repro/S03.json) | Zero-response windows yield NaN normalized rows and silently omit neurons; an all-zero population crashes. The claimed corrected mean requires an unspecified zero-normalization policy. |
| S04 | CONFIRMED | [S04.py](repro/S04.py), [output](repro/S04.json) | Documented list/array-valued dictionaries crash in conditional rasters and spike counts; equivalent DataFrames give independently verified counts 4,2. |
| S05 | CONFIRMED-MINOR | [S05.py](repro/S05.py), [output](repro/S05.json) | Documented row/column center (-2,3) peaks at (7,2), rather than (2,7), in a 9×9 patch; custom off-axis filters transpose, while centered filters are unaffected. |
| S06 | CONFIRMED | [S06.py](repro/S06.py), [output](repro/S06.json) | Four recording samples and a seven-sample temporal basis produce seven rows, violating the documented sample count and response alignment. Exact short-signal crop convention is unspecified. |
| S07 | CONFIRMED-MINOR | [S07.py](repro/S07.py), [output](repro/S07.json) | Default no-sort reverses all four raster rows, contrary to the documented identity behavior; underlying spike counts are unchanged. |
| S08 | CONFIRMED | [S08.py](repro/S08.py), [output](repro/S08.json) | Window [-13,17] ms with 10-ms bins produces four bins but retains metadata for three plot centers; population PSTH plotting crashes. |
| P01 | CONFIRMED | [P01.py](repro/P01.py), [output](repro/P01.json) | Fitted binomial/probit models with valid saturated probabilities return NaN deviance instead of zero; large positive logistic logits also overflow the likelihood. |
| P02 | CONFIRMED | [P02.py](repro/P02.py), [output](repro/P02.json) | Perfect gamma predictions have deviance -4.80735576 instead of zero; absolute deviance is wrong. A fixed-data deviance ranking is unaffected; changing pseudo-R² convention is not certified. |
| P03 | CONFIRMED | [P03.py](repro/P03.py), [output](repro/P03.json) | Gamma sample=True returns deterministic 2 for a model with mean log(2) and variance log(2)²; simulated experiments get both the mean and noise wrong. |
| P04 | KNOWN | [P04.py](repro/P04.py), [output](repro/P04.json); [existing-PR check](repro/pr390.py) | Main-branch no-intercept Poisson model fits mean 20 but predicts 12.61094383; existing open PR 390 already removes the link error and independently predicts 20. |
| P05 | KNOWN | [P05.py](repro/P05.py), [output](repro/P05.json); [existing-PR check](repro/pr390.py) | Main-branch no-intercept simulation crashes on the documented coefficient length; existing open PR 390 already accepts it and agrees with direct Xβ. This option is absent from released simulators. |
| P06 | INTENDED | [P06.py](repro/P06.py), [output](repro/P06.json) | Estimator seed alone does not reproduce folds and selected lambda changes (0.2 versus 0.03), but the API explicitly scopes random_state to initialization; both fold scores match independent normal equations. Seed global NumPy separately for repeatable folds. |

The last verdict means **consistent with the documented seed scope**, not proof of the maintainers' private intent. An estimator-wide seed would be an API improvement. The historical seeding work and GLMCV tests are discussed in [EVIDENCE.md](EVIDENCE.md).

## Ranked author candidates, by demonstrated effect on users

1. **S01 — wrong Poisson loss.** Core tuning fit/decode machinery uses a quantity that reverses a basic likelihood comparison; this can choose a worse restart and changes stopping.
2. **S02 — incorrect population SEM.** The normal population plotting path silently understates uncertainty, including on completely nonzero, normalized data.
3. **P03 — gamma samples are deterministic with the wrong mean.** The documented sampling option can invalidate synthetic-data experiments without an exception.
4. **P01 — binary likelihood NaNs and overflow.** Valid confident predictions can poison reported deviance and CV/model-selection arithmetic; demonstrated on actual fitted public models.
5. **P02 — gamma deviance has the wrong zero.** A mathematically perfect prediction scores negative and the result changes with response units. This does not change fixed-fold deviance-only lambda ordering.

P04 has a substantial numerical effect, but it and P05 should not be presented as new reports: [open PR 390](https://github.com/glm-tools/pyglmnet/pull/390) already contains working repairs for these examples. The five candidates above are ranked for Ricardo to read; nobody was contacted. No claim about whether Hugo would care is made.

[Evidence and limitations](EVIDENCE.md) · [Reproduction instructions](README.md)
