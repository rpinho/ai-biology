# Claim victor_VB10 — sharp hyperbolic stable-equilibrium capacity

Status: exact within-run checks PASS; separate referee and Fable/Opus TASTE pending. This is a mathematical claim about a Garcia coauthored paper, not a priority or biological claim.

**Published starting point and location.** Garcia, Bonhoeffer and Fu2020, [DOI10.1016/j.jtbi.2020.110185](https://doi.org/10.1016/j.jtbi.2020.110185), printed Eqs21–23, Section2.3 and AppendixC. The paper already gives a quintic residual, up to5 additional fixed points and numerical bistability; it warns that projected nullcline stability does not guarantee full3D stability. Those facts are credited, not claimed new. No sharp attained full-system capacity is asserted as a published number here.

**Our number and exact domain.** The maximum is **3 hyperbolic asymptotically stable nonnegative equilibria**, over all strictly positive constants in the printed model. A global degree/crossing argument supplies the upper bound; a rational assignment attains it, with stable states at T=0, approximately1.56314789924 and13.99709358253. Two other positive equilibria are unstable. The general bound excludes nonhyperbolic stable states and other attractors. With the non-coupling constants fixed to printed Table3, the sharper maximum is2, attained within the printed variable ranges.

**Mini code/data.** All paths are under friends_pf_victor:

- vb10_global_dynamics/GENERAL_PROOF.md and PROOF.md: human proofs and exact parameter assignments.
- vb10_global_dynamics/verify_count_independent.py: separately written checker, importing no search code.
- vb10_global_dynamics/pod_backup/vb10/INDEPENDENT_COUNT_CERTIFICATE.json: exact source constants, polynomial identities, rational root intervals, full3D Routh–Hurwitz bounds and both attaining constructions.
- vb10_global_dynamics/pod_backup/vb10/PORTABLE_REPLAY_CERTIFICATE.json: separate-directory archive replay PASS, all fields equal apart from time.
- run5_backup/results/run5_first_sources.tar.xz: primary XML and original official R/source receipts; every member hash is in run5_first_sources_XZ_MANIFEST.json.
- vb10_global_dynamics/native_backup/vb10_run5/{native_equations_control.csv,general_native.csv}: independent native-R controls; corresponding scripts and construction code are in vb10_global_dynamics/.
- vb10_global_dynamics/REPORT.md, PRIOR_ART.md and pod_backup/vb10/FINAL_PRIOR_RECHECK.json: commands, source identity, prior checks and limitations. FINAL_AGENT_FOLLOWUP.json records the completed initially capped tree retry.

The frozen code/data hash list is vb10_global_dynamics/CLAIM_MANIFEST.json.

**Verification.** The checker decodes13 fixed Table3 constants from primary XML; independently derives coefficients by Fraction convolution; proves their threshold ordering; isolates roots by exact sign bisection; checks full-Jacobian cubic Routh–Hurwitz, not just scalar slopes; and independently verifies universal degree/boundary/Schur identities. The universal crossing count remains a human proof, not a proof-assistant result. Native R independently agrees on root locations and stability, with residuals<=3.82e-14. Exact arithmetic, not that floating-point control, supports the claim.

**Controls.** All physical roots exclude eliminated poles; the compact witness's loss numerators are positive on T>=0. This is theory and no observational holdout exists. Table3's stricter2-state capacity is proved globally. A larger-rate-separation construction was retained and then replaced as the main illustration by a smaller one; neither was fit to biological outcomes. The original quintic and classical Descartes/Schur/Routh methods are credited.

**Concerns and scope.** Constants in the general witness differ from Table3 and are not physiologically fitted. There is no empirical/treatment/basin/global-convergence claim and no first-tristability claim across cancer models. Current public checks are bounded and do not establish priority or author interest; only the external TASTE review judges that. Legacy R artifacts are not a self-contained replay of the printed model, so the claim explicitly uses printed equations and makes no paper-error or historical-figure claim. Nothing has been sent to anyone.
