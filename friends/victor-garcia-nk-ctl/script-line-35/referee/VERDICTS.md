# Referee verdicts: NK-CTL script

B03's numerical headline survives independent recomputation. The exact Fig. A2 settings remain uncertain, and correction does not eliminate the model's ability to be bistable. These are software/reproducibility findings: **NEW: no** under the friends lane's novel scientific-result definition.

| Bug | Verdict |
|---|---|
| B03 — squared NK denominator | CONFIRMED WITH CAVEATS |

## B03 — CONFIRMED WITH CAVEATS (priority)

**Call sentence:** “The archived NK formula uses T² where both printed equations use T, and at σ=1000, k=10⁻⁵, c=0.001 that change creates a stable tumor state absent from the printed model.”

**Strongest objection Victor could raise:** The paper never uniquely specifies σ and k for Fig. A2, the T² code could be an exploratory variant, and the printed model still supports bistability elsewhere—including at c=0.001 if σ=600—so this does not refute the general biological conclusion or the separate base-model treatment results.

**What survived:** Independently read line 35 and primary Eqs. 22/76; the script's own comments agree with the linear denominator. The paper describes a maximum proliferation rate and saturation coefficient, not a declining T/(κ+T²) response. Our exact-rational root isolation and full Jacobians reproduce T=17404.7359049 (saddle), T=19762510.0178169 (stable), and T=0 (stable) for the squared version; the printed model has only stable T=0 at the specified point. The lower boundary is 0.000514 in both; upper folds are 0.00102628890913447 (squared) and 0.000728393687513285 (printed), a 29.02645% decrease.

**Figure qualification:** Fig. A2 uses c=10⁻⁷,10⁻³,1; Table 3 supplies ranges rather than exact σ,k. Squared T with σ=1000,k=10⁻⁴ closely reproduces its A peak and A/B zeros; k=10⁻⁵ from line 355 does not. That is strong parameter evidence, not a recovered execution record. With fixed Table 3 constants, the printed model can never have two positive roots both above 2132.602201 cells for any positive σ,k, whereas panel B displays two above that size. Thus the displayed roots conflict with the printed equations even after allowing the stated σ,k ranges. The headline k=10⁻⁵ roots should not be described as the exact plotted roots.

