# Independent referee of victor_VB31

The mathematical statement survives independent exact and analytic review: at the literal Table 3 immune rates, every finite nonnegative solution of printed Eqs. 21–23 converges to an equilibrium for 0<a<=2 and b,U,V>0. This is a mathematical result about the printed field. It supplies neither biological uncertainty bounds nor historical simulation identity. No novelty or author-interest judgment is made.

## Independent reconstruction and checks

`source_audit.py` parses freshly fetched primary MathML and Table 3, recovers the three original equations and all ten fixed immune constants, and verifies the normalization exactly. Authors and a=.514 are checked from that same source; time is unchanged. `source_result.json` retains the equations, constants and source hash. The final primary XML is byte-identical to the initial retrieval.

The submitted energy is used only as a proposed witness. `independent_check.py` imports no submitted scientific code: it differentiates the full witness directly in T,y,z, reconstructs A,K,Q, proves parameter affinity, derives the Bernstein matrices from power coefficients, and checks all 36 matrices over T>=0 with exact rational arithmetic/root counts. It also independently checks source bounds and the two-positive-equilibrium control. The run passed on Python 3.12.3 / SymPy 1.13.3 in 145 seconds on one CPU; `independent_result.json` retains 40 distinct integer polynomials, including 26 determinant numerators and additional A/rate/weight bounds. This count differs from the submission because the referee checks additional A and elementary-bound polynomials separately.

`independent_bernstein.py` independently proves all 40 referee-derived polynomials positive by exact integer Bernstein convexity after T=10000*t/(1-t), using no Sturm or root-counting library. Maximum subdivision depth is two; only one determinant needs subdivision and it needs a single split. Thus the certificate is also verifiable by short signed-coefficient checks. The logarithmic boundary, finite-time domain entry, extinction, C1 critical case, LaSalle, and finite connected omega-limit-set arguments are independently audited in `ANALYTIC_AUDIT.md`.

The control a=2, b=51/50000000000, U=11/5, V=11/100000000000 has exactly two simple positive equilibria, near T=136.6 and T=12196.1, besides the boundary equilibrium. It is outside the trivial U>=3a/2 extinction region. No trajectory scan, fitted data, held-out observations, local no-Hopf result, or presumed equilibrium uniqueness is used as evidence for universal convergence.

## Reproduction on the authorized referee pod

From this claim directory, transport each independent script via `send_files.py` and the approved terminal helper. The transport uses only explicitly named claim-derived files:

```sh
python3 send_files.py fetch_public.py
python3 _codex/friends_podsh.py ref pod_send.sh 60
# Poll fetch_public.log until primary.xml exists and the fetch process exits.
python3 send_files.py source_audit.py
python3 _codex/friends_podsh.py ref pod_send.sh 60
python3 send_files.py independent_check.py
python3 _codex/friends_podsh.py ref pod_send.sh 60
# Poll until independent_result.json exists and independent_check exits.
python3 send_files.py independent_bernstein.py
python3 _codex/friends_podsh.py ref pod_send.sh 60
```

Each launched scientific script uses nohup, nice 10, and one library thread under `/workspace/ref_victor_VB31`; `*.pid` identifies its worker. The source parser can instead use the already archived `public/primary.xml`, eliminating network dependence. Outputs and public evidence are copied back by `receive_files.py`. `referee_evidence.tar.gz`, individual result JSONs and logs retain the relevant receipts. A missing pod pdftotext was worked around by using a public pypdf wheel under the referee directory. Neither that tooling issue nor an initial Unicode-space parsing fix affected the scientific result.

## Literature and remaining bar

`PRIOR_ART.md` gives sources, URLs, bounded searches and failures. The original paper already analyzes stationary roots/bistability at a=.514; the additional conclusion here is all-orbit convergence over 0<a<=2 for arbitrary positive couplings, with multiple/repeated equilibria permitted. A 2024 Clotilda et al. paper encountered in the search proves global stability for a different chemotherapy subsystem. No assertion of priority follows from these bounded checks.

The strongest scope objection is that literal rates and the printed field need not coincide with historical simulation code or physiological parameter variation. The public R helper has `hg+T_w^2` where Eq. 22 prints `kappa_bn+T`, and its referenced NK/CTL parameter file is absent from the release. A concrete next bar is an explicit nonzero uncertainty box around all ten fixed immune constants, with exact certificates and boundary arguments valid throughout that box. Cleanup/process receipts are in `CLEANUP.txt`.
