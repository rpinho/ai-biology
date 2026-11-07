# Confirmed correctness bugs

Seven confirmed bug reports across the four requested packages. Each has a minimal patch, pinned before/after output, a normal-input control, and a second implementation. No issue, PR, comment, fork or contact was made. These are local software fixes, not a new scientific result or a predictive-performance claim.

The first three repositories had no commits in the requested three-month window. Open/closed issue and PR records, comments and relevant diffs/reviews were checked before reporting. See [SOURCES.md](SOURCES.md) for pins, release comparison, deduplication decisions and environment limitations.

## SSI-001 — Two-stage GBH changes its decisions when groups are reordered

- Package / location: **structSSI**, `R/gbh.R:213` at `294d228cd7ef89ba17ea76ba246a267d7b59acb0`.
- Wrong: The TST first stage uses the raw p-values of each group at alpha/(1+alpha). The final GBH step uses that level once. Multiplying the entire raw vector inside the group loop changes later groups’ estimates and compounds the final factor. Move the multiplication after the loop.
- Before: Adjusted values in original order: `[0.02590875, 0.441, 1, 1]`; estimated group null fractions `[0.5, 1]`. Only A1 is rejected. Putting B first instead rejects only B1.
- Correct / after: Adjusted values `[0.024675, 0.42, 0.024675, 0.42]`; both group fractions 0.5; A1 and B1 are rejected regardless of row order.
- Effect on users: Different groups can lose discoveries solely because rows/groups are reordered. This is not merely a label error.
- Repro and patch: [repro/SSI-001/](repro/SSI-001/README.md), [patch.diff](repro/SSI-001/patch.diff), [before/after output](repro/SSI-001/output.txt), [independent result](repro/SSI-001/independent.txt).
- Definition: [Hu, Zhao and Zhou (2010), Definition 4 and equation (2.9)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3175141/).
- Controls: Single-group TST, two-group LSL and Storey results remain identical. Python separately implements the BH rejection threshold and GBH adjusted levels.
- Confidence: **high for the reproduced case**. The affected file is identical in CRAN 1.2.1. This is the loop-placement regression after the old threshold fix (#2/#8), not the old missing-threshold report.

## SSI-002 — GBH assigns every result the name of the first sorted hypothesis

- Package / location: **structSSI**, `R/gbh.R:320` at `294d228cd7ef89ba17ea76ba246a267d7b59acb0`.
- Wrong: A scalar test passed to ifelse() produces a length-one result, which data.frame recycles. Use scalar if/else to select the whole name vector. Output identity is defined by names(unadj.p)[hypothesisIndex].
- Before: Names `h2, h2, h2` for raw p-values `0.001, 0.03, 0.8`.
- Correct / after: Names `h2, h1, h3`, with numerical values and original indices unchanged.
- Effect on users: Users joining or reporting discoveries by hypothesisName can attribute several tests to the wrong gene/hypothesis. The hypothesisIndex column remains usable.
- Repro and patch: [repro/SSI-002/](repro/SSI-002/README.md), [patch.diff](repro/SSI-002/patch.diff), [before/after output](repro/SSI-002/output.txt), [independent result](repro/SSI-002/independent.txt).
- Definition: The pinned [GBH output contract](https://github.com/krisrs1128/structSSI/blob/294d228cd7ef89ba17ea76ba246a267d7b59acb0/R/gbh_class.R) defines hypothesisName as the original input name and hypothesisIndex as its index.
- Controls: All numeric columns remain identical; the entire unnamed-input result is unchanged. Python independently maps every index and raw value back to its original identity.
- Confidence: **high for the reproduced case**. CRAN 1.2.1 is affected. PR #11 introduced the scalar expression; the PR’s existing name regression test only covers hFDR.

## SSI-003 — Hierarchical testing crashes on a parent with one child

- Package / location: **structSSI**, `R/hfdr.R:193` at `294d228cd7ef89ba17ea76ba246a267d7b59acb0`.
- Wrong: The multtest BH helper fails for a length-one vector in the supplied current dependency. A singleton family requires no multiplicity adjustment. Replace the two-line multtest sorting/remapping call with stats::p.adjust(..., "BH").
- Before: For p=c(r=.001,a=.02) and the edge r -> a: `Error in if (is.na(spval[i])) tmp[i] <- NA : argument is of length zero`.
- Correct / after: Adjusted values r=0.001 and a=0.02; both hypotheses are rejected at alpha=0.05.
- Effect on users: A valid unary edge prevents users from receiving any hierarchical test result. This is separate from the already-reported failure to descend into grandchildren (#13).
- Repro and patch: [repro/SSI-003/](repro/SSI-003/README.md), [patch.diff](repro/SSI-003/patch.diff), [before/after output](repro/SSI-003/output.txt), [independent result](repro/SSI-003/independent.txt).
- Definition: The family-wise BH traversal is the procedure described in [Sankaran and Holmes (2014), hierarchical testing section, following Yekutieli (2008)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4764101/). For m=1 the BH adjustment m*p/rank equals p.
- Controls: Two-child families, ties and unsorted p-values remain identical. Singleton values 0, .02, .05 and 1 are checked. Python derives the singleton result without multtest or structSSI.
- Confidence: **high for the reproduced case**. CRAN 1.2.1 has identical hFDR source. Reproduced with multtest 2.66.0; this is a dependency-facing valid-input failure.

## LNM-001 — Inverse log ratio returns NaN for large finite logits

- Package / location: **miniLNM**, `R/estimate.R:81` at `3dc73f2727bfce490236a0759cda8f6ef358affd`.
- Wrong: Computing exp(mu) directly overflows, making a probability Inf/Inf. Apply the ordinary stable softmax: append the reference logit zero, subtract the maximum logit, exponentiate and normalize.
- Before: phi_inverse(c(1000,0)) returns `[0, NaN, 0]` in both pinned functions and the installed CRAN package.
- Correct / after: Returns `[0, 1, 0]` to double precision, summing to one.
- Effect on users: Large finite linear predictors can generate NaN compositions and break subsequent multinomial sampling, although the mathematically defined probabilities are finite.
- Repro and patch: [repro/LNM-001/](repro/LNM-001/README.md), [patch.diff](repro/LNM-001/patch.diff), [before/after output](repro/LNM-001/output.txt), [independent result](repro/LNM-001/independent.txt).
- Definition: The model itself specifies this definition using softmax after appending zero in [inst/stan/lnm.stan](https://github.com/krisrs1128/miniLNM/blob/3dc73f2727bfce490236a0759cda8f6ef358affd/inst/stan/lnm.stan).
- Controls: Ordinary logits (-5,0,5) remain unchanged to floating precision; scalar and matrix cases are checked. Python’s independent 80-digit Decimal calculation agrees.
- Confidence: **high for the reproduced case**. Confirmed through installed CRAN 0.1.2 as well as pinned source; no matching report in miniLNM issue #1, which concerns VB/psis.

## LNM-002 — Design-matrix filtering silently removes the formula intercept

- Package / location: **miniLNM**, `R/estimate.R:90` at `3dc73f2727bfce490236a0759cda8f6ef358affd`.
- Wrong: model.matrix() has already generated the correct predictors. Filtering its columns against the names of RHS variables discards (Intercept), and can also discard transformed columns. Return the model matrix without that redundant name filter.
- Before: An intercept-only formula yields a 20 x 0 design. Public lnm() prints `D is 0, but must be greater than or equal to 1` and wraps an invalid list instead of a stanfit. Ordinary ~ x also loses its intercept.
- Correct / after: The design is 20 x 1, all ones; the same intercept-only data produce an lnm object with nonempty stanfit draws.
- Effect on users: Intercept-only models fail; formulas with default intercepts fit a different model from the one requested. Existing fitted models should be refitted after applying this fix.
- Repro and patch: [repro/LNM-002/](repro/LNM-002/README.md), [patch.diff](repro/LNM-002/patch.diff), [before/after output](repro/LNM-002/output.txt), [independent result](repro/LNM-002/independent.txt).
- Definition: The package documents R’s formula interface. [R model.matrix](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/model.matrix.html) and [R formula](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/formula.html) define the design and its default intercept.
- Controls: The explicit no-intercept ~ 0+x input is unchanged. Default intercept, factor and transformed-variable designs agree with base model.matrix. Python independently checks the all-one intercept design. A public fit is also exercised.
- Confidence: **high for the reproduced case**. Confirmed through installed CRAN 0.1.2 and the pinned source. The tiny fit emits the ordinary Pareto-k=0.74 diagnostic: it demonstrates a usable design/fit object, not posterior-accuracy certification. One initial repro assertion was corrected after reverting the patched copy; see first-attempt.txt and STATUS.md.

## MM-001 — Gaussian glmnet and random-forest samplers square the intended noise variance

- Package / location: **multimedia**, `R/estimators.R:388 and R/estimators.R:692` at `346039a2f10d332f57a48ec235e7ff5e0c0ab1f6`.
- Wrong: Both samplers supply a variance estimate to rnorm() as its sd argument. Take the square root, and select the Gaussian deviance for lambda_ix when using a regularization path.
- Before: The RF fixture’s residual mean-square parameter is 9.701943841, but generated noise has variance 94.127714296. The glmnet fixture’s parameter is 7.2502, but generated noise has variance 52.56540004.
- Correct / after: Noise variances are 9.701943841 and 7.2502, respectively. Corresponding standard deviations are 3.114794 and 2.692620.
- Effect on users: Synthetic outcomes and mediator values can be greatly overdispersed when the residual variance exceeds one, or underdispersed when it is below one. Downstream simulation/sensitivity results using these samplers can change.
- Repro and patch: [repro/MM-001/](repro/MM-001/README.md), [patch.diff](repro/MM-001/patch.diff), [before/after output](repro/MM-001/output.txt), [independent result](repro/MM-001/independent.txt).
- Definition: [ranger](https://imbs-hl.github.io/ranger/reference/ranger.html) defines regression prediction.error as mean squared error; [glmnet deviance](https://glmnet.stanford.edu/reference/deviance.glmnet.html) gives the Gaussian residual deviance. [R rnorm](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Normal.html) takes standard deviation. Thus Y=mu+sqrt(v)Z has variance v.
- Controls: Real ranger/glmnet fits and a fixed normal stream give exact checks; no Monte Carlo acceptance threshold is used. Fits scaled to unit residual variance retain the same output. A two-lambda path uses the matching residual scale. Python separately verifies Var(sqrt(v)Z)=v.
- Confidence: **high for the reproduced case**. Both affected function bodies match CRAN 0.2.0. This report is restricted to continuous Gaussian/regression responses, as documented by the samplers. Direct pinned functions were loaded with their real dependencies; a full multimedia installation was unavailable.

## SCD-001 — Truncated-Gaussian tail cancellation corrupts likelihoods and copula scores

- Package / location: **scDesigner**, `scdesigner/src/scdesigner/distributions/zero_inflated_truncated_gaussian.py:133 and :166` at `f991d485b0f91540c9805cdfaa349f98d5d3b956`.
- Wrong: The float32 normal CDF rounds to zero before log() in the negative tail. Clamping that zero to 1e-30 substitutes a wrong normalizer. The uniformization code also subtracts nearly equal CDFs and adds an epsilon that can dominate the tail probability. Use torch.special.log_ndtr and scipy.stats.truncnorm.cdf.
- Before: At mu=-6, sigma=1, pi=.2, y=.2: log-likelihood 48.715469360 instead of 0.374686865. At mu=-10: CDF 0.200000003 instead of 0.895917939.
- Correct / after: Float32 log-likelihood at mu=-6 is 0.374686301; CDF at mu=-10 is 0.895917773. These agree with independent double-precision quadrature within float32 tolerance.
- Effect on users: Valid negative latent means can give badly incorrect fitting objectives and gradients, and positive observations can map to the zero atom’s copula score. This changes fitted models and joint simulations.
- Repro and patch: [repro/SCD-001/](repro/SCD-001/README.md), [patch.diff](repro/SCD-001/patch.diff), [before/after output](repro/SCD-001/output.txt), [independent result](repro/SCD-001/independent.txt).
- Definition: The package defines an atom pi at zero plus (1-pi) times a positive truncated-normal density. The [SciPy truncated-normal definition](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.truncnorm.html) uses standardized truncation limits. The independent check integrates the unnormalized normal kernel directly on (0,infinity).
- Controls: Central normal inputs are bitwise unchanged. Positive-data CDF/inverse round trips agree at mu=-10,-6,-2,0,3. Base R independently integrates the density and CDF, without torch, SciPy, or the package.
- Confidence: **high for the reproduced case**. The installed PyPI 0.0.27 affected file is byte-identical to the pin. This is distinct from the mixture-component inversion bug previously fixed in PR #38.

## Suspected / untriaged, not included in the seven

The following observations have no completed patch-and-independent-check package and are not shipped as confirmed bugs:

- **structSSI missing/empty input:** an NA in the raw vector triggers a recycling warning and a row-count error; empty vectors error. The documentation does not specify NA/empty-vector semantics. See `checks/structSSI.txt`.
- **structSSI boundary annotations:** significance stars use strict cutoffs, so an exact alpha-boundary rejection can be annotated inconsistently with the standard <= definition. Numerical adjusted values were checked; the full reporting path was not patched.
- **structSSI pi0=1 with p=0:** sorting the NaN weight can silently lose one input row. Additional denominator/edge-case conventions should be checked before proposing a fix.
- **miniLNM NA alignment:** an NA covariate yields two design rows while the selected response retains three rows. This was observed via model_matrix_df, but a full missing-data repro/patch is not included.

## Already reported or excluded

- **structSSI depth traversal:** significant grandchildren remain NA. This is the open issue [#13](https://github.com/krisrs1128/structSSI/issues/13), so it is excluded from new findings. The singleton crash SSI-003 occurs before recursion and is distinct.
- **structSSI LSL all-ones input:** the single p=1 case returns Inf; related estimator boundary issues appear in #1/#3. Not claimed as new.
- **miniLNM formula-parser candidate:** the apparent length>1 error came from loading functions before formula.tools registered its formula method. The installed public API works. This was an investigation artifact, not a package bug.

## Coverage and limits

`checks/structSSI.R` compares ties, zero/one p-values, a single group, unused factor groups and unsorted input against base R. It checks alpha=0/1, probes NA/empty inputs and unary trees, and compares 200 small ordinary Oracle GBH cases numerically. Its hFDR traversal comparison also records the already-known grandchild issue.

`checks/other-packages.R` checks exact linear multiresponse estimates and noiseless simulation in multimedia, and miniLNM’s known log-ratio identity and count depths. `checks/scDesigner.py` checks ordinary distribution likelihoods and inversion. These are correctness exercises; no prediction score or superiority claim is made.

The portable R could not load the complete structSSI/multimedia dependency stacks. Their exact pinned numerical functions were exercised with real direct dependencies, including multtest, igraph, ranger and glmnetUtils. miniLNM’s installed public API was tested, including a patched-source fit, and the scDesigner source was compared against the installed PyPI release. General package integration and all statistical model families were not exhaustively tested.
