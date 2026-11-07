HOLDS
Referee: gpt-6.1-sol

The claimed global convergence, exact fold and hyperbolic basin separation survive independent checking for the printed equations with the specified fixed Table 3 rates. I found no false analytic step.

Source: live PMC7079339 XML matches the frozen paper byte for byte and names Victor Garcia, Sebastian Bonhoeffer and Feng Fu. Eqs.21–23 and Table 3 give exactly the claimed normalization. The official R file instead contains a squared denominator term; this verdict covers the printed model, as the claim explicitly requires.

What I ran: independently written exact rational/SymPy checks reconstructed both degree-13 damping certificates, energy identities, boundary limits, fold monotonicity and the full three-dimensional Jacobian. A different exact sign-pattern feasibility argument re-established the two-positive-root bound. All passed on the ref pod. I separately audited compactness, the energy dichotomy, LaSalle and basin topology.

Controls: thirteen ODE diagnostics reproduced saddle/sink bistability and tested boundary degeneracies and extreme initial conditions. An apparently extinct state after severe numerical underflow recovered to its positive equilibrium in logarithmic coordinates. These runs are diagnostics, not the convergence proof. There is no dataset or hold-out, and no published numerical global-convergence score to compare.

Relative to the paper: the addition is the fixed-rate global convergence certificate and resulting fold/basin classification; the paper already supplies the quintic/nullcline reduction and numerical bistability. A related prior result encountered is Vithanage–Wei–Jang (2023), DOI 10.1002/mma.9152, giving global stability results for a different model. Classical LaSalle, Descartes and Routh methods are already credited. No priority or taste judgment is made.

Strongest objection: eventual damping alone cannot exclude a saddle homoclinic. Here the scalar comparisons can be pulled back to every time on a bounded complete trajectory, making energy decrease along the whole unstable branch. Equal saddle endpoint energies then exclude a return. The subsequent local saddle exit argument is valid.

Evidence and commands: REPORT.md, independent_audit.py and pod_evidence/. Scientific work stayed on the pod; retained evidence was copied back before cleanup.

NEXT BAR: provide a machine-checked formalization of the complete-trajectory and basin-separation argument, beyond the already executable polynomial certificates.
