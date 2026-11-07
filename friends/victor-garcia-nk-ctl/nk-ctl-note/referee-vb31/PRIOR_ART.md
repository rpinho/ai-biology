# Prior-art/source audit — 2026-11-02

Scope: independent referee of the stated fixed-Table-3 global convergence theorem, not a novelty judgment.

Primary anchor supplied by claim: Garcia, Bonhoeffer and Fu (2020), Journal of Theoretical Biology, DOI https://doi.org/10.1016/j.jtbi.2020.110185, equations 21–23 and Table 3. Claim says published a=0.514 and no published global-convergence score. This is unverified pending source retrieval.

Before writing test code, audit plan:
1. Read current primary paper/catalog and any official results/code, including issues/PRs if applicable; identify what quantity is actually claimed.
2. Search public GitHub, recently updated results, and relevant agent result repositories.
3. Search recent papers and public community summaries for this exact model/theorem.
4. Independently reconstruct source equations and proof identities; exact arithmetic is the baseline for this analytic claim. There is no empirical hold-out or numerical leaderboard claimed.

No claim of novelty or record will be made. Receipts and search limitations will be added below.

## Completed independent source checks

Retrieved on 2026-11-02, then rechecked before closing:

- Fresh primary XML: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7079339/fullTextXML . SHA256 `44a73bed7dbeaef770b73c291dc2fe5319b99ed578be4796e3afa165685500f8`. MathML and Table 3 parsed by the referee's own code. Authors Victor Garcia, Sebastian Bonhoeffer, Feng Fu; source growth a=257/500 per day. Original paper is a stationary-root/bistability analysis of the NK/CTL extension, with an explicit Appendix C warning that a stabilizing root in the reduced tumor equation does not guarantee full stability. It supplies no global-convergence score or numerical record of this kind.
- Public code baseline: https://doi.org/10.6084/m9.figshare.11536824.v1 ; version metadata https://api.figshare.com/v2/articles/11536824/versions/1 . All ten released R files read. In `analysis_FengNKCTL.R`, `N.stab.nomut` uses `g*T_w/(hg+T_w^2)`, whereas printed Eq. 22 uses `bn*T/(kappa_bn+T)`. The release also calls absent `params_FengNKCTL.R`. Thus it is not a faithful executable baseline for the exact printed 3D field. The referee instead reconstructs that field directly, which is the baseline relevant to this theorem. Historical simulation identity remains unestablished.
- GitHub repository searches were sorted by updated date for exact title phrase, Bonhoeffer/Fu, 110185, and tumor-immune/2026. The exact-title and author pair returned zero repositories. Numeric queries were noisy. Exact-title issue/PR search returned one disease-documentation PR, not a convergence proof; the numeric issue query mostly matches issue numbers. Raw receipts are in `public/github_*.json`. No claim of exhaustive GitHub code search is made.
- Agent repositories inspected via README and available tree paths: https://github.com/BakeLab/Epi-results , https://github.com/google-deepmind/alphaevolve_results , https://github.com/openai/math , https://github.com/togethercomputer/EinsteinArena-new-SOTA , https://github.com/plasma-ai/erdos , https://github.com/kisonecat/openai-math . The original `google-deepmind/repository_of_problems` URL returned 404; a repository search resolved it to https://github.com/google-deepmind/alphaevolve_repository_of_problems and that source was subsequently checked. A full `openai/math` tree exceeded the 12 MB bounded read; its README and manuscript catalogue were inspected instead. No matching model/theorem was identified in those bounded inspections. Unrelated Garcia number-theory filenames occurred in the Erdos tree.
- Recent literature: EuropePMC exact-title phrase, publication dates 2025-11-02 through 2026-11-02, returned zero; arXiv Garcia AND immunosuppression sorted by submitted date returned zero. Web searches of DOI/title with global stability, LaSalle, periodic, and convergence found the primary and citations, not a same-model theorem. Public X/Reddit/blog searches likewise yielded no relevant theorem in the returned results; no private community access or contact was attempted.
- A prior result encountered and read: Clotilda, Vithanage and Lakshika, *A Mathematical Model to Treat for a Cancer Using Chemotherapy and Immunotherapy under Mass Action Kinetics for Immunotherapy* (2024), https://doi.org/10.37394/232023.2024.4.15 ; source https://wseas.com/journals/msa/2024/a30msa-012%282024%29.pdf . Its Theorem 2 gives global stability for a different two-state chemotherapy subsystem, using Poincare–Bendixson; the full model includes a chemotherapy compartment and one immune compartment. It does not establish this fixed-rate NK/CTL theorem. The paper was extracted on the pod using the public pypdf wheel after pdftotext proved unavailable.

The best applicable baseline in the primary source is the printed field and its bistability/root analysis at a=.514. The submitted theorem adds a universal, all-initial-state convergence conclusion for the literal fixed immune rates over 0<a<=2, arbitrary positive b,U,V, including multiple equilibria. This describes the difference from the paper; it is not a judgment about novelty, priority, or usefulness. Classical energy/LaSalle, polynomial positivity and Bernstein convexity are the methods used in the submitted argument. There is no empirical hold-out to reproduce.

Final source rechecks and their limitations are recorded in `final_public_receipts.json` and `close_sources.json`. These bounded searches cannot establish priority.
