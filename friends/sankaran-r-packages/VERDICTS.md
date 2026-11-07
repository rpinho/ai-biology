# Independent referee verdicts

All seven claimed failures reproduce; six are **CONFIRMED**, one **CONFIRMED-MINOR**. No matching prior report or current fix was found in the checked public records as of 2026-11-06. This is a scoped search finding, not proof that nobody has encountered them.

| ID | Verdict | My repro | Effect on users' results |
|---|---|---|---|
| SSI-001 | CONFIRMED | [R](repro/SSI-001.R), [output](repro/SSI-001.txt) | Identical groups lose different discoveries solely when their input order changes under documented `method="tst"`. |
| SSI-002 | CONFIRMED | [R](repro/SSI-002.R), [output](repro/SSI-002.txt) | Named GBH results repeat one hypothesis name, so distinct significant genes can be reported as the same gene; indices remain correct. |
| SSI-003 | CONFIRMED | [R](repro/SSI-003.R), [output](repro/SSI-003.txt) | A valid single-child family crashes hierarchical testing instead of returning its unadjusted singleton p-value. |
| LNM-001 | CONFIRMED-MINOR | [R](repro/LNM-001.R), [Decimal reference](repro/LNM-001-reference.py), [output](repro/LNM-001.txt) | Extreme finite log ratios produce NaN probabilities, which can interrupt prediction or sampling. |
| LNM-002 | CONFIRMED | [R](repro/LNM-002.R), [output](repro/LNM-002.txt), [public entrypoint](repro/LNM-002-public.R), [public output](repro/LNM-002-public.txt) | Ordinary formulas lose their intercept; intercept-only designs have no columns and fail in Stan; transformed terms can disappear too. |
| MM-001 | CONFIRMED | [R](repro/MM-001.R), [output](repro/MM-001.txt) | Gaussian RF/glmnet synthetic responses use residual variance as SD, yielding variance squared and scale-dependent over/underdispersion. |
| SCD-001 | CONFIRMED | [Python](repro/SCD-001.py), [output](repro/SCD-001.txt), [base-R integral](repro/SCD-001-reference.R), [reference output](repro/SCD-001-reference.txt) | Legitimate negative latent means corrupt float32 likelihoods/gradients and positive-data copula probabilities. |

## Ranked shortlist for Ricardo to read

Ranking is by the demonstrated effect and the documented path to exposure. It does not estimate how often users encounter a bug or whether the author would care.

1. **MM-001:** changes synthetic-data variability for both documented continuous-response sampler families whenever residual variance differs from one. On ordinary `mtcars` fits, the RF residual variance is **6.3047516463**, but generated noise has implied variance **39.7498933214**; glmnet gives **6.0963207633** versus **37.1651268486**. The mean predictions need not expose the error. Simulation and sensitivity conclusions can change.
2. **SSI-002:** corrupts the identity of reported hypotheses on the documented named-input path, including with default adaptive settings because they call `Oracle.GBH`. In my oracle fixture, two significant results should be geneB and geneC; both are labeled geneB. Recovering identities through `hypothesisIndex` works, but reporting or joining by `hypothesisName` does not.
3. **LNM-002:** silently changes the model requested by conventional R formulas, with an obvious failure for `~1` and less obvious omission for `~x`. The public pinned path fails at Stan's `D>=1` restriction and still wraps a list as the estimate. The README's own example omits the intercept too, which tempers any inference about author intent; the help promises R's formula interface and documents no no-intercept convention.
4. **SSI-001:** changes which group gets discoveries under a documented optional estimator. With two identical groups, each containing p-values **(.045,.7)** at alpha **.1**, only the first group's small p-value is rejected. Reversing the groups reverses that choice. Both should be rejected by the specified procedure.
5. **SCD-001:** corrupts the optimization objective and copula transformation within the documented zero-inflated truncated-Gaussian family. At **mu=-6, sigma=1, pi=.3, y=.3**, log likelihood is **47.95694** instead of **-0.38384453**. At **mu=-8**, the returned CDF is **.3004660** instead of **.94142546**. Mean uses an identity link, so these parameters are admissible. This is conditional on a particular distribution/tail regime; no prevalence or full fitted-data impact was measured.

SSI-003 remains reportable but falls below this five-item shortlist: it stops execution visibly on unary families. LNM-001 is lower priority because the exhibited log ratio 720 is extreme.

## What I independently established

### SSI-001

Pinned [R/gbh.R:206–217](clones/SSI-001/R/gbh.R) scales the entire p-vector inside the group loop, at line 213. My input uses distinct names and numbers from the hunter's reported example. Each raw pair (.045,.7) has one BH rejection at alpha'=.1/1.1, hence pi0=.5 independently for each group. GBH weights are one, overall pi0=.5; one final factor 1.1 gives sorted weighted values (.0495,.0495,.77,.77). Reverse cumulative minima of `2*p/rank` give adjusted values **(.0495,.385,.0495,.385)** in input order. The unpatched code instead estimates pi0=(.5,1), returns **(.05445,.4235,1,1)**, and changes the rejected identity on reordering. The printed `unadjp` column is also rescaled.

Reachability: [Adaptive.GBH help](clones/SSI-001/man/Adaptive.GBH.Rd) lists `tst`; default is `lsl`, so this is an optional documented method. The independent procedure follows [Hu, Zhao and Zhou, Definition 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC3175141/): estimate from each group's raw values and use alpha' once for final testing.

History: [issue #2](https://github.com/krisrs1128/structSSI/issues/2) concerns missing final threshold correction. [PR #8](https://github.com/krisrs1128/structSSI/pull/8) introduced the correction **inside** the loop; its saved [diff](history/structSSI/pr-8-files.json) shows this. The repeated correction/order dependence is a distinct regression, not a new report of the old omission. No matching discussion was found among 13 issue/PR records and their available comments/reviews. Master is still the pin. The old `protect-nas` branch lacks the correction altogether; it is not a repair. CRAN 1.2.1's entire gbh.R is identical.

### SSI-002

Pinned [R/gbh.R:320](clones/SSI-002/R/gbh.R) passes a scalar condition to `ifelse`. My input is `c(geneA=.4,geneB=.004,geneC=.012,geneD=.2)` with one group pi0=.5. Sorted indices are **2,3,4,1**, so direct lookup in the original input independently gives **geneB,geneC,geneD,geneA**. All four returned names are geneB. Adjusted p-values .008 and .012 make the mislabeling relevant even within discoveries.

Reachability: named p-values appear in the Oracle and Adaptive help examples; [the GBH class contract](clones/SSI-002/R/gbh_class.R) explicitly defines names as original input identities. This is not cosmetic when names are used to report or join results. History: [PR #11](https://github.com/krisrs1128/structSSI/pull/11) introduced this expression while renaming output columns; [saved diff](history/structSSI/pr-11-files.json). No matching report was found. CRAN 1.2.1 is byte-identical here; the historical branch uses an older output schema rather than fixing the present regression.

### SSI-003

Pinned [R/hfdr.R:193](clones/SSI-003/R/hfdr.R) calls multtest for a singleton family. For root=.003, leaf=.04 and edge root→leaf, unchanged code errors `argument is of length zero`. Independently, a one-element BH family multiplies .04 by 1/1, leaving .04. The root is significant, so both nodes should be returned as rejected. A two-child control returns the expected family adjustment.

Reachability: [hFDR.adjust help](clones/SSI-003/man/hFDR.adjust.Rd) accepts parent/child edge lists without a binary-tree or minimum-family-size restriction. The failure is in the real multtest 2.66.0 dependency, not my implementation. The [current Bioconductor 3.23 multtest 2.68.0 source](releases/bioc-current/multtest/R/mt.basic.R) still fails directly on .04; [separate repro/output](repro/SSI-003-current-dependency.txt). Its BH loop uses `(m-1):1`, which includes zero at m=1. CRAN structSSI 1.2.1's hfdr.R is identical. No singleton report was found in structSSI's issues; [open #13](https://github.com/krisrs1128/structSSI/issues/13) concerns missed deeper descendants, a separate failure. The old branch retains this same dependency call.

### LNM-001

Pinned [R/estimate.R:81–83](clones/LNM-001/R/estimate.R) directly exponentiates logits. My input **(720,-2)** returns **(0,NaN,0)**. An independent 70-digit Python Decimal calculation of **(1,exp(720),exp(-2))**, divided by its sum, gives approximately **(2.03223e-313,1,2.75033e-314)**. All probabilities are representable finite doubles; the intermediate exponent is not. A central (2,-2) control is finite; the matrix path also fails only on its extreme row. The installed CRAN exported function independently reproduces NaN too.

Reachability: `phi_inverse` is exported and accepts a numeric vector without a stated finite-magnitude limit. It is also used in prediction/sampling. The Stan model defines the reference-zero softmax consistently. Classification is MINOR because this example requires an extreme log ratio; it does not establish typical fits reach that magnitude. No match in miniLNM's sole issue/PR (#1, about VB/psis), or branches; the affected functions are identical in CRAN 0.1.2.

### LNM-002

Pinned [R/estimate.R:90–94](clones/LNM-002/R/estimate.R) filters the already-expanded design by regexes derived from RHS variables. My five-row input yields **5×0** for `y~1`, **5×1** for `y~x`, and **5×0** for `y~I(x^2)`, versus base R's **5×1**, **5×2**, **5×2** respectively. The factor design also loses its intercept; explicit `~0+x` agrees with base R. The reference designs use only base `model.matrix`, independently of miniLNM. The public pinned `lnm(a+b~1,...)` path, with its own unchanged formula/VB wrapper and real compiled Stan model, prints **D is 0, but must be greater than or equal to 1**, then returns an estimate of class list.

Reachability/intent: [lnm help](clones/LNM-002/man/lnm.Rd) expressly calls this R's formula interface; [standard R formula semantics](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/formula.html) include an intercept unless removed. No exclusion for intercept-only or transformed formulas is documented. The README's five-dimensional example demonstrates existing intercept omission and the synthetic generator also has no intercept: the behavior may have been convenient or intentional for that example. Neither documents an interface-wide exception, and removal of transformed terms reinforces the correctness finding. I confirm the contract failure without asserting the author's intent. The original helper exists since the initial estimation implementation; no later branch or issue explains/fixes it. CRAN 0.1.2's three affected transformation/design function expressions match the pin exactly; its VB wrapper differs, which is why the public pinned repro explicitly loads the pin's own wrapper.

### MM-001

Pinned [R/estimators.R:388–390 and 692–694](clones/MM-001/R/estimators.R) sends residual mean squares to `rnorm` as SD. I fit real ranger and Gaussian glmnetUtils models to `mtcars`, then call the **original parsed sampler definitions** with those real fit objects. Independently computing RF out-of-bag squared residuals and glmnet squared residuals verifies their variance parameters. With a replayed normal stream, including ranger's own RNG consumption during prediction, outputs match `prediction + v*Z` exactly. A normal perturbation with intended variance v must instead be `sqrt(v)*Z`; this is an algebraic variance identity, not an empirical predictive-performance comparison. The observed means do not need to change for this defect to matter.

Reachability: the [RF](clones/MM-001/man/rf_sampler.Rd) and [glmnet](clones/MM-001/man/glmnet_sampler.Rd) sampler help explicitly assumes continuous responses and includes `mtcars` examples. Model constructors assign these same sampler functions. Their documentation's use of “MSE” to estimate “sigma” does not make variance-as-SD statistically correct. The reference packages document `ranger$prediction.error` as regression MSE and Gaussian glmnet deviance as squared residual error; my direct residual computations also establish those units. This verdict covers the Gaussian one-lambda variance defect; it does **not** certify the hunter's patch, lambda-path handling or non-Gaussian behavior. No matching discussion in eight multimedia issue/PR records and comments. Main equals the pin; CRAN 0.2.0's entire estimators.R is identical.

### SCD-001

Pinned [zero_inflated_truncated_gaussian.py:133 and 166](clones/SCD-001/scdesigner/src/scdesigner/distributions/zero_inflated_truncated_gaussian.py) uses a float32 CDF before logarithm and CDF subtraction with an additive denominator epsilon. I installed the fresh pinned package normally, created an AnnData template, called public setup methods, and set its real identity/exp/sigmoid predictor coefficients to admissible parameter values. Float32 is the loader/predictor default. At sigma=1, pi=.3, y=.3, the unpatched likelihood and uniformization disagree with independent base-R integration:

| mu | Package log likelihood | Independent log likelihood | Package CDF | Independent CDF |
|---:|---:|---:|---:|---:|
| -8 | 33.35694122 | -0.70717632 | .30046600 | .94142546 |
| -6 | 47.95693970 | -0.38384453 | .89380604 | .89440778 |
| -5 | -0.29452020 | -0.25561508 | .85860378 | .85860556 |
| 0 | -0.62746632 | -0.62746630 | .46507600 | .46507599 |

The reference integrates `exp(mu*t-t^2/2)` on positive t, analytically cancelling the common Gaussian factor, and derives the density, CDF and mean gradient. At mu=-6 the package's **per-observation** mean gradient is **6.3**, versus **.14151740** independently. The log reports summed gradients for four identical observations. No SciPy, torch or package routines are used in the reference.

Reachability/intent: the class documentation describes a latent Gaussian mean, not a nonnegative observed mean; the actual mean link is identity. No parameter restriction enforces the docstring's suggestion that nonnegative data keep the ratio benign. My probe shows admissible behavior; it does not establish frequency in trained datasets. [PR #38](https://github.com/krisrs1128/scDesigner/pull/38) addressed mixture inversion before this family was added by [#41](https://github.com/krisrs1128/scDesigner/pull/41); neither describes this tail defect. Sixty issue/PR records, available comments/reviews, 96 recent default-branch commits and the other branch were checked. Its other branch retains the affected numerical expressions. The PyPI 0.0.27 affected file and installed pinned file are byte-identical.

## Scope and reproduction

Each ID has its own fresh GitHub clone at the supplied commit; [pins.json](repro/pins.json) records seven unchanged checkouts. I read only the hunter's BUGS.md and SOURCES.md to identify claims/pins; I did not open or execute the hunter's repros, output files or patches. My inputs, calculations, downloads and scripts are local to this workspace. The claims document itself necessarily contains the hunter's stated outputs; none was used as an oracle or imported as a fixture. No upstream code was patched.

Run the R repros with `zsh repro/run-r.sh`. The public miniLNM extension is `repro/LNM-002-public.R`; the latest multtest helper extension is `repro/SSI-003-current-dependency.R`. Use the supplied Rscript and `R_LIBS="$PWD/env/Rlib:$HOME/dev/open-science/friends_recheck_manuel_1105/env/Rlib"`. Run Python with `env/py311/bin/python repro/SCD-001.py`, setting OMP/BLAS threads to 2 and TMPDIR to `env/tmp`. Use `nice -n 10`; scripts use only tiny inputs. [Dependency versions and source/release comparison](releases/comparison.json) accompany the outputs; miniLNM's [function comparison](releases/miniLNM-function-comparison.txt) handles its unrelated release changes.

Full structSSI and multimedia installation failed on their broader dependency stacks; their unchanged function definitions were evaluated with real direct dependencies. MiniLNM's public entrypoint was exercised using original pinned functions in an environment backed by its installed namespace and the same Stan specification. scDesigner was installed from the pin. These results establish the stated numerical failures, not end-to-end certification of every package or validation of proposed fixes. Initial harness failures and their reversions are recorded in STATUS.md; superseded files are retained locally.

Public history was fetched independently through `~/dev/.bin/gh api`, including all open/closed issue/PR records (13/1/8/60), available discussion and review records, branch heads and recent commits. Raw evidence is under [history/](history/); branch/file comparisons are in each package's `branch-and-file-history.txt`. There were no default-branch commits after August 6 for structSSI, miniLNM or multimedia, and 96 for scDesigner. Current CRAN/PyPI source distributions were downloaded independently under [releases/](releases/); [download versions/hashes](releases/fetch2.log) identify them. No public actions or contact occurred.

**NEW: no** under the friends lane scientific-result definition. This job independently confirms software correctness defects; it does not beat a printed scientific number, settle a paper's open problem, or test a scientific prediction on new data. No predictive-performance claim or SBS comparison is made.
