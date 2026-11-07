HOLDS
Referee: gpt-6.1-sol

The stated convergence theorem survives independent reconstruction and audit: literal Table 3 immune rates, every 0<a<=2, all b,U,V>0, and every finite nonnegative initial state. Equilibria need not be unique. No counterexample or proof gap was found.

Primary source: [Garcia, Bonhoeffer and Fu (2020)](https://doi.org/10.1016/j.jtbi.2020.110185), Eqs. 21–23/Table 3. Fresh MathML parsing confirms Victor Garcia's authorship and a=.514 per day. The normalization changes neither time nor growth. The endpoint 2 is a sufficient theorem bound, not a published performance number or a sharp threshold.

What I ran: independently written source parser, full-field energy differentiation, parameter-affinity/Bernstein reconstruction, and exact positivity checks for all 36 control matrices. No claimant search/verifier code was imported. An additional integer Bernstein checker independently proves all 40 referee-derived polynomials positive without root-counting software. See independent_result.json and bernstein_result.json.

I also audited finite-time domain entry, extinction, the a=U boundary extension, LaSalle, and repeated equilibria; details are in ANALYTIC_AUDIT.md. These steps establish convergence of each orbit, rather than merely excluding Hopf bifurcations.

Sceptic's control: the supplied a=2 example independently has exactly two simple positive equilibria besides the boundary, and U<3a/2. Uniqueness or automatic extinction therefore does not explain the result. No empirical data or hold-out exists; exploratory trajectory scans contribute no proof evidence.

Relative to the paper: its stationary-root/bistability analysis at a=.514 is supplemented by an all-orbit convergence guarantee through a=2 for arbitrary positive couplings. Prior encountered: Clotilda et al. (2024), DOI 10.37394/232023.2024.4.15, proves global stability for a different chemotherapy subsystem. Bounded searches and their limitations are recorded in PRIOR_ART.md; no priority judgment is made.

Scope: this establishes the printed ODE. The public R NK helper uses hg+T_w^2 instead of Eq. 22's linear denominator; historical simulation identity remains unestablished. Evidence is copied back, all tracked workers exited, and the pod referee directory ends at 448 KB.

Strongest author objection: the ten literal immune constants have no quantified uncertainty allowance, so this theorem alone does not establish robustness to rate variation.

NEXT BAR: certify the same convergence statement throughout an explicit ±1% box around all ten fixed immune constants.
