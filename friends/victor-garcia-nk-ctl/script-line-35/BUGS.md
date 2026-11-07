# Confirmed bugs in analysis_FengNKCTL.R

Five confirmed defects, grouped by cause. The target script is unchanged in `source/`; its MD5 matches the supplied frozen copy. [INVENTORY.md](INVENTORY.md) lists all ten files. [COMPARISON.md](COMPARISON.md) gives the paper comparison, parameter ambiguities, figure evidence and scientific limits. Original line numbers are used throughout. Reproduce one bug with `sh repro/<ID>/run.sh` from this directory; the saved R/Python outputs and minimal patch are in each folder.

## B03 — Squared NK stimulation denominator changes the model and Fig. A2

**Line:** 35, `parameters$hg + T_w^2`. **Paper:** Eqs. 22 and 76 require κbn+T, as does the script's own comment at line 31.

**Wrong:** The extra square changes N(T), CTL recruitment through N(T), all reduced tumor equilibria and the numerator degree assumed in Appendix C.

**Repro:** [repro/B03/run.sh](repro/B03/run.sh), [R output](repro/B03/r_output.txt), [Python output](repro/B03/python_output.txt), [patch](repro/B03/patch.diff). Direct ODE residual, root coordinates, full-Jacobian stability and folds are independently recomputed. Plot: [Fig. A2 comparison](artifacts/figure_A2_comparison.png).

**Before → after** (σ=1000,k=10⁻⁵, other constants Table 3):

- At T=100000, N=502.491349620 → **1596.264367816**. Substitution in printed dN/dt gives residual +685.207939392 → approximately zero.
- At c=0.001, roots [0,17404.7359,19762510.0178] → **[0]**. Full stability: two stable states plus one saddle → **one stable state**.
- Upper bistability fold c=0.00102628890913 → **0.000728393687513** (29.03% lower); lower boundary c₀=0.000514 is unchanged.
- At c=10⁻⁷, positive root 726310343.496 → **408558364.138**. c=1 has no positive root in either case.

**Which does the paper follow?** Appendix C/Eq. 81 follow the printed linear denominator. **Fig. A2 follows the squared denominator:** with σ=1000,k=10⁻⁴, its A peak (~2.8×10⁷), A root (~2.2×10⁸) and B roots (~1.7×10⁴ and ~5.9×10⁶) are reproduced. Printed Eq. 22 has no B positive roots at those parameters. Irrespective of σ,k within their printed ranges, the smaller positive root of the printed equations must be below 2133 cells, incompatible with the displayed ~10⁴ root. Exact original k remains uncertain; see COMPARISON.md.

**Effect on paper:** Quantitative figure and bistability region change. The broad claim of possible NK–CTL bistability survives: the corrected equations have two stable equilibria at σ=1000,c=0.0006,k=10⁻⁵. Because Table 3 gives σ as a range, c=0.001 is also bistable at σ=600, with different roots. No unique printed numerical NK upper fold exists to replace; these fold values are explicit recomputations. No effect on separate base-model treatment thresholds is established.

**Confidence:** High for model error, recomputations and figure's denominator; moderate for the specific k=10⁻⁴ provenance inference.

