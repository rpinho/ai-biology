HOLDS
Referee: gpt-6.1-sol
NEW confirmed: yes
The claimed lower feasible stress is confirmed under the stated printed-number rule.
[The paper](https://doi.org/10.1101/2025.06.03.657573), Figure 2C caption,
PDF page 5, actually prints 23.4; page 1 lists Victor Garcia as a coauthor.
Pages 13 and 15 specify Rudorf's 0.7 h^-1, 2-1-2 rates, Euclidean rate-profile
distances and Kruskal nonmetric MDS. The caption itself does not print “percent”.

I independently rebuilt all 23 profiles (387 sense codons each), all 253
pairwise dissimilarities, and evaluated the submitted two-dimensional witness.
Own PAVA code, checked against SciPy isotonic regression, gives
13.48308284568073 percent Stress-1 using the documented MASS convention.
Own 384-bit Arb evaluation certifies 13.48308284568072855, with enclosure
radius below 3e-112, strictly below 23.35, the printed rounding-bin threshold.
PAVA optimality conditions also pass. Enforcing equal disparities for tied
input distances gives the same value. No producer/referee code was imported.
Evidence: results/independent_audit.json; code: audit.py.
To check objective identity, I extracted all 23 plotted PDF vector marks,
corrected the axis scales using printed ticks, and recomputed 23.396468%.
All marks match the supplied default configuration within 0.008 PDF points;
that configuration independently evaluates to 23.396544%. See plot_audit.py
and results/published_plot_audit.json. I did not rerun the original optimizer.
Run both scripts with the shared .venv Python, nice 10 and one BLAS thread.
These local checks completed successfully; no pod was needed.

New relative to this paper: a lower feasible value of its Figure 2C objective;
no global optimum, new optimizer, or changed biological conclusion is shown.
SBS/trivial/simple predictive scores: inapplicable; this is an unsupervised
finite geometric objective with no prediction labels or held-out split.

Strongest objection: the original analysis script is unavailable, so MASS
implementation identity is inferred from the methods and plotted-configuration
match. Fresh Rudorf PDF matches the archived hash; bioRxiv HTTP 429 required
archived primary paper/sequence files. No comparable later value was found
in bounded exact-title/DOI searches; this is not an exhaustive priority search.

NEXT BAR: release the original Figure 2C distance matrix and analysis script
so the implementation and preprocessing can be compared directly.
