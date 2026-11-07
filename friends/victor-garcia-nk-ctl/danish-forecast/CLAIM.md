NEW: yes
Kind: note
Builds on: Cadosch, Garcia, Jensen, Low & Althaus (2020), Understanding the spread of de novo and transmitted macrolide-resistance in Mycoplasma genitalium, https://doi.org/10.7717/peerj.8913.
Ours: A new retrospective empirical test of the unchanged Danish forecast against later SSI 2021–2022 and national MiBa 2021–2024 reported surveillance fractions, with historical constant/logistic baselines and source/rounding audits. The new contribution is the external forecast comparison, not a new model, new surveillance measurements, or a completed 2025 endpoint test.
Prior art: Chua et al. (2025), https://doi.org/10.1016/j.lanmic.2024.101047, already synthesize resistance prevalence and population heterogeneity; Riou et al. (2023), https://doi.org/10.1186/s12879-023-08200-4, develop related gonococcal forecasting; Bolaji et al. (2026), https://doi.org/10.1371/journal.pgph.0006834, analyze a theoretical M. genitalium model. No inspected prior work performs this frozen Danish forecast/baseline comparison. See PRIOR_ART.md for access limits and search records.
Cited by: 17 papers since 2020 (OpenAlex W3015720582, checked 2026-11-04; citing query exposes 12 records, all inventoried); closest: Riou et al. 2023, Projecting the development of antimicrobial resistance in Neisseria gonorrhoeae from antimicrobial surveillance data. No direct earlier Danish forecast validation found in the bounded search.
Standard method: Unchanged official R code, last changed October 2019, with deSolve default ODE integration, bbmle Nelder–Mead fitting, published initial conditions/fixed parameters, seed 71309 and 10,000 parameter draws per country. All three published rounded 2025 forecasts and confidence intervals reproduce. Linear-time binomial logistic regression uses only the original four Danish training rows; the trivial predictor holds the last historical fraction constant without fitting.
Deviations: standard failed: the current bbmle 1.0.26 on pod R 4.3.3 called an unavailable %||% runtime operator (results/standard/first_failed_run.log). STATUS.md records the failure and planned change before retry. Pinned archived bbmle 1.0.23.1 and reran the original source unchanged; no scientific setting, model, data or optimizer was altered.

Metric: unweighted MAE in percentage points across the stated external year cells; all three predictors use identical outcomes within each series.

| Split | Trivial | Simple logistic | Original model | SBS |
|---|---:|---:|---:|---:|
| SSI, 2021–2022 | 24.87319185 | 13.91936772 | 10.86405197 | 0.781906 |
| MiBa, 2021–2024 | 21.02951542 | 19.94675090 | 16.83106330 | 0.257896 |

The SBS script output is preserved in BASELINES.json (fraction-scale scores, identical split/metric); raw outputs are results/sbs_SSI.json and results/sbs_MiBa.json. Both SBS values are below one. The original model improves over the specified simple baseline by 3.0553 and 3.1157 percentage points of MAE. This is a finite external comparison, not a new predictive method or a claim of general superiority.

Referee: independent computational referee, HOLDS WITH CAVEATS. A separate implementation refitted the logistic score equations and source likelihood, integrated all four source compartments, and recomputed every evaluated observation, prediction, metric, SBS and rounding range. See referee/REFEREE.md and referee/recomputation.json.

Limits: historical specimens, later SSI episodes and MiBa case fractions have different sampling and typing definitions. The original forecasts assume continued treatment practices; actual changes prevent causal or counterfactual refutation. Every evaluated point lies inside the original broad parameter confidence band. The two aggregate scores cover different year sets and cannot isolate a source effect. The 2021 SSI denominator is inferred; MiBa 2024 is rounded. No 2025 endpoint, French/Swedish validation, intervention effect, or all-infected-population calibration is claimed. Literature searches are bounded; five citations implied by OpenAlex's headline count were not returned by its query.

Artifacts: NOTE.md (short manuscript), REPORT.md (reproduction), DATA.md, PROPOSAL.md, IDEAS.md, PRIOR_ART.md, BASELINES.json, code/, data/, results/, sources/ and referee/ in friends_note_victor_1104.

Disposition at the time: unpublished; the author is the judge.
