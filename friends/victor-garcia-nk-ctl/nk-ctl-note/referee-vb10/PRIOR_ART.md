# Independent referee source log — 2026-11-02

Created before referee code or construction. This is a falsification review,
not a priority assessment. No optimization scoreboard applies to this theorem.

Primary baseline: Garcia, Bonhoeffer, Fu (2020), DOI
https://doi.org/10.1016/j.jtbi.2020.110185 ; PubMed confirms all three authors:
https://pubmed.ncbi.nlm.nih.gov/32035826/ . Public full text is PMC7079339;
ETH author manuscript: https://www.research-collection.ethz.ch/bitstreams/34c72f77-38f9-4a85-b13e-92a476baad1b/download .
The paper already derives a quintic and numerical bistability. The claim is
an attained full-system sharp stable-equilibrium count, not a published
performance improvement. Reproduce printed equations independently on pod.

Initial exact DOI/title and NK/CTL/tristability searches found the primary
paper and unrelated model classes, with no exact-model newer count identified.
Claimant's prior-art log is read as a lead only, not independent evidence.
Pending: primary equations/Table 3, official release, updated public code,
required agent repos, recent arXiv and bounded community search. No claim of
newness, public best or exhaustive absence will be made.

## Completed independent checks

Live primary XML obtained directly from Europe PMC on the authorized pod:
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7079339/fullTextXML .
Its hash equals the claimant's archived primary. Section 2.3 already states
up to five additional fixed points; Appendix C already gives quintic
elimination, root alternation, the projected/full-stability distinction,
and numerical bistability. These are the baseline method and demonstrated
two-state result; a sharp public maximum is not stated there. Printed
equations were independently reproduced in referee.py, with exact checks.

Official release: https://api.figshare.com/v2/articles/11536824 . Ten public
files; no linked GitHub issues/PRs or optimization leaderboard. Read the
live analysis_FengNKCTL.R and master.R. The former calls the absent
params_FengNKCTL.R and uses hg+T_w^2 in its NK nullcline, unlike printed
Eq. 22. No historical-figure replay or author-error claim follows from this.
Full receipts and source text are saved in source_audit.json.

Independent GitHub repository searches, sort=updated: exact title fragment,
DOI plus Garcia, NK-CTL, and cancer immune/awesome/2026 returned zero hits.
GitHub unauthenticated code search was not used. Required agent repositories
were attempted directly; API root listings were rate-limited (403).
Raw README fallback receipts are in prior_followup.json. These bounded
metadata/README checks do not establish absence of an earlier theorem.
Web queries for those same repositories and model terms found no verified
matching exact-model result. Source 1--3 receipts were collected after
the exact checks; no priority or record claim is made.

Additional bounded searches: arXiv with NK-CTL and the author combination,
including dates after 2025-11-02; exact-title/tristability and 2025/2026;
X/Reddit exact-title queries; author institutional publication page. No
verified newer exact-model count was identified. The paper's primary
reference Talkington, Dantoin, Durrett (2018), DOI
https://doi.org/10.1007/s11538-017-0263-8 , compares different ODE models.

Other prior results encountered (different equations, not this capacity):
Lu et al. (2013), tristability in a microRNA--TF switch,
https://pubmed.ncbi.nlm.nih.gov/23679052/ ; Lai, Farman, Byrne (2025),
T-cell exhaustion model with reported tristability,
https://doi.org/10.1007/s11538-025-01433-1 . The latter's primary XML
passages are saved in prior_followup.json and its author repository is
https://ora.ox.ac.uk/objects/uuid:61acd463-d53b-43bd-9a0f-921b4c5b5b72 .
No novelty, priority, or author-interest assessment is attempted.
