HOLDS
Referee: gpt-6.1-sol
NEW confirmed: yes

The claim beats a number actually printed in Victor Garcia's own paper.
I opened the primary PDF: page 1 names Garcia; Figure 2B's caption on
page 5 prints 34.8. Pages 13–15 specify Shah–Gilchrist Table S2's Rc
column, raw elongation-rate profiles, Euclidean distances and Kruskal NMDS.
Paper: https://doi.org/10.1101/2025.06.03.657573

I independently parsed all 61 rates and rebuilt the 23 released sequences'
387 translated-codon profiles and all 253 pairs. Native R/MASS defaults
return 34.8056748605161%, reproducing 34.8. The actual PDF circles,
calibrated against the axes, give approximately 34.80624%; their coordinates
match the native result within 0.014 units. This supports objective identity.

My own isotonic-regression implementation recomputes the supplied witness
as 16.969390168877389…%, also confirmed by native MASS::Shepard.
My separate 320-bit Arb checker certifies the actual isotonic least-squares
fit and stress strictly inside [16.9693901688773, 16.9693901688775]%,
well below 34.75, the printed value's rounding-bin lower edge.
Ran recompute.py, standard_referee.R, certify.py and check_plot.py locally
at nice 10; no claimant search or verifier code was imported.
Evidence: results/recomputed.json, independent_interval.json, native_R.log,
pdf_plot_check.json. SBS and untouched hold-outs do not apply to this exact
unsupervised objective; BASELINES.json explains why.

Strongest objection: the original analysis script is unavailable; convention
identity rests on the methods, default reproduction and matching plotted map.
Fresh bioRxiv PDF/CSV fetches returned 429; archived public inputs were used.
Relative to the paper, this is a better feasible visualization via routine
MASS settings/restarts, with no global optimum or biological result shown.
Final public-source recheck found no comparable later value in bounded searches.
NEXT BAR: release the original Figure 2B script and evaluate this witness
through its original preprocessing and stress calculation.
