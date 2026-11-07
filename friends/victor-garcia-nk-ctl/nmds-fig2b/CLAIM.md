NEW: yes
Printed: 34.8 percent Kruskal NMDS stress, Figure 2B caption, page 5, https://doi.org/10.1101/2025.06.03.657573 .
Ours: 16.9693901688774 percent, on the same 23 sequences, 253 pairs, two dimensions, Euclidean raw Shah rate profiles, and MASS stress objective. Numerical certificate PASS; separate referee verdict HOLDS.
Standard method: Native R/MASS::isoMDS with all defaults gives 34.8056749, reproducing the printed 34.8; the cited Shah–Gilchrist Table S2 column Rc and original DC3 sequences are used.
Deviations: standard failed: results/standard.log shows immediate default convergence at 34.8056749, reproducing but not improving the printed value. STATUS.md records the change before execution: maxit=1000, tol=1e-10, then 100 standard Gaussian starts with seed 1104, otherwise unchanged MASS settings.

Verification: `verify_stress.py` independently re-extracts all 61 printed rates
with a different PDF parser, hashes the fresh original sequences, reconstructs
profile dissimilarities exactly as integers, confirms native R's pair ordering,
and certifies the actual isotonic least-squares fit and stress with 384-bit Arb
interval arithmetic. The upper bound is below 34.75, the lower edge of the
printed number's rounding bin. Certificate: `results/shah_certificate.json`;
coordinates: `results/shah_best_coords.csv` in the working directory.

This is a new feasible numerical value for a printed objective under the job's
definition. It uses routine documented software settings and restarts. It is
not a new optimizer, a global optimum or a biological discovery. It does not
change the expression measurements or epistasis analysis. This unsupervised
objective has no predictive split; SBS is inapplicable (see BASELINES.json).
Prior art: `PRIOR_ART.md`; final live recheck completed 2026-11-04 22:56–22:57 UTC, no later comparable result located in the bounded search.

Referee: HOLDS. Independently rebuilt the original profiles, recovered the
actual published PDF configuration, checked native MASS::Shepard and wrote a
separate 320-bit Arb certificate proving stress below 16.970. The producing
384-bit certificate encloses the value in [16.9693901688773, 16.9693901688775].
See [referee verdict](friends_new_victor_1104/referee/VERDICT.md)
and [full review](friends_new_victor_1104/referee/REVIEW.md).

Working directory: `friends_new_victor_1104`.
Internal claim only; no publication or contact. Original analysis script is
unavailable; native defaults and published PDF coordinates identify the
objective convention. No exhaustive-priority claim is made.
