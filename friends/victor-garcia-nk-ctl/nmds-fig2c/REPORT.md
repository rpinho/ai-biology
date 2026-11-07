Independent referee completed locally: HOLDS; NEW confirmed: yes under the
job's printed-number rule. See VERDICT.md (under 40 lines).

From this directory, reproduce with:

    nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python audit.py
    nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python plot_audit.py

Independent code reconstructs rate profiles from the primary Table S2 PDF
and original released sequence CSV; only candidate/default coordinates and
row-label manifest are read from producer outputs. No producer/referee
program is imported or run. Float PAVA agrees with SciPy, and a separate
384-bit Arb computation verifies the candidate stress and PAVA conditions.
The published figure's vector marks are evaluated separately with axis scales
from its printed tick labels. Sources and output hashes are recorded in
results/independent_audit.json. Live source checks and their limitations are
in PRIOR_ART.md. Original analysis code would remove the remaining inference
about implementation identity. No external contact or remote upload occurred.
