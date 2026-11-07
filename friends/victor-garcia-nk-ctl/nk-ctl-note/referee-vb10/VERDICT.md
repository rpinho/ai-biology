HOLDS
Referee: gpt-6.1-sol

The sharp maximum is three hyperbolic stable nonnegative equilibria for
the printed equations with all constants allowed to vary over positive values.
I independently confirmed two stable interior states at T≈1.56314789924
and 13.99709358253, plus the stable T=0 state; the other two are unstable.
The degree/crossing upper bound survives, including poles and boundary cases.

The paper really is by Victor Garcia, Sebastian Bonhoeffer and Feng Fu:
[primary source](https://doi.org/10.1016/j.jtbi.2020.110185), Eqs.21–23,
Section 2.3 and Appendix C. Its five additional fixed points count all
equilibria, not stable ones. Three is not a corrected version of that number.
The paper already supplies the quintic, scalar alternation and numerical
bistability. The additions relative to it are attained full-system capacity
and a global two-state bound with the Table 3 non-coupling constants fixed.

I wrote referee.py directly from the live primary equations, importing no
claimant code: symbolic elimination/determinant identities, exact Sturm root
isolation, rational intervals for every full-Jacobian Routh–Hurwitz inequality,
and a separately derived Table 3 coefficient/Descartes bound all passed.
See REFEREE_CERTIFICATE.json and AUDIT_PROOF.md. Calculations ran on ref;
its full disk required memory-only execution through the adapted helper.

Control: retaining Table 3 constants permits at most two stable states;
the submitted in-range witness attains two. Parameter freedom explains
the third state. There is no empirical holdout or predictive gain to audit.
The legacy R release differs from printed Eq.22 and lacks a required helper;
this verdict concerns the printed model, not reproduction of its figures.

Other prior encountered: Lai, Farman and Byrne (2025),
[T-cell exhaustion model](https://doi.org/10.1007/s11538-025-01433-1),
already exhibits tristability in different equations; further leads and
bounded search limitations are in PRIOR_ART.md. No priority judgment is made.

Strongest author objection: the three-state witness changes the fixed rates
and ranges substantially (including sigma=1 versus the printed 10–1000);
it establishes abstract capacity, not physiological tristability.
NEXT BAR: one exact tristable witness inside independently sourced
physiological bounds for every parameter.
