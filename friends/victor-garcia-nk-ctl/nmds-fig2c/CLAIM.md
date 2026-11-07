NEW: yes
Printed: 23.4 percent Kruskal NMDS stress, Figure 2C caption, page 5, https://doi.org/10.1101/2025.06.03.657573 .
Ours: 13.4830828456807 percent, on the same 23 sequences, 253 pairs, two dimensions, Euclidean raw Rudorf rate profiles, and MASS stress objective. Numerical certificate PASS; separate referee verdict HOLDS.
Standard method: Native R/MASS::isoMDS with all defaults gives 23.396544, reproducing the printed 23.4; the cited Rudorf–Lipowsky Table S2, growth 0.7 h^-1 and 2-1-2 pathway, and original DC3 sequences are used.
Deviations: standard failed: results/standard.log shows immediate default convergence at 23.396544, reproducing but not improving the printed value at its precision. STATUS.md records the change before execution: maxit=1000, tol=1e-10, then 100 standard Gaussian starts with seed 1104, otherwise unchanged MASS settings.

Verification: `verify_stress.py` independently re-extracts all 61 printed rates
with a different PDF parser, hashes the fresh original sequences, reconstructs
profile dissimilarities exactly as integers, confirms native R's pair ordering,
and certifies the actual isotonic least-squares fit and stress with 384-bit Arb
interval arithmetic. The upper bound is below 23.35, the lower edge of the
printed number's rounding bin. Certificate: `results/rudorf_certificate.json`;
coordinates: `results/rudorf_best_coords.csv` in the working directory.

This is a new feasible numerical value for a printed objective under the job's
definition. It uses routine documented software settings and restarts. It is
not a new optimizer, a global optimum or a biological discovery. It does not
change the expression measurements or epistasis analysis. This unsupervised
objective has no predictive split; SBS is inapplicable (see BASELINES.json).
Prior art: `PRIOR_ART.md`; final live recheck completed 2026-11-04 22:56–22:57 UTC, no later comparable result located in the bounded search.

Referee: HOLDS. Independently rebuilt the original profiles, recovered the
actual published PDF configuration, checked native MASS::Shepard and wrote a
separate 320-bit Arb certificate proving stress below 13.484. The producing
384-bit certificate encloses the value in [13.4830828456806, 13.4830828456809].
See [referee verdict](friends_new_victor_1104/referee/VERDICT.md)
and [full review](friends_new_victor_1104/referee/REVIEW.md).

Working directory: `friends_new_victor_1104`.
Internal claim only; no publication or contact. Original analysis script is
unavailable; native defaults and published PDF coordinates identify the
objective convention. No exhaustive-priority claim is made.
