HOLDS WITH CAVEATS
Referee: gpt-6.1-sol

The narrow species-selector bug and its two-line repair survive independent reproduction.

The [2021 paper](https://doi.org/10.1186/s13059-021-02441-9) lists Manuel Irimia as an author and defines the membership score using same-species genes contributing to the exon cluster.
The disputed 0.86 is release-test output, not a number printed in the paper; the paper's >97% method-agreement result is unrelated and remains untested here.

For the claimed GF_002754 human exon, I independently obtain OUT=2, IN=2, two reciprocal neighbors, four exons, two human exons, four original genes and two contributing human genes.
Thus the documented score is exactly 6/[2*(4-2)+(4-2)]=1; the release instead computes 6/7, rounded to 0.86.

Ran on the authorized pod: fresh official v2.0.0 sequence-to-output pipeline; fresh original/corrected R replays and formatter; my own paper-derived directed-graph/Fraction audit, importing no claimant search or verifier code.
The full original pipeline reproduces golden MD5 02479360ed2b8d659612fc60477ad355 and the submitted graph byte-for-byte.
Across 2,144 directed edges and 1,108 exons, every reported integer graph field checks out; exactly 18 score cells change, all 377 clusters and 1,090 single-gene controls remain unchanged.
My independently derived patch matches the submitted patch; corrected table SHA256 is 5bc3a8a7494e9592a468e06d61c1a45ec816be7d9b565222ca586d456e8595c7.
An independently extracted four-node/eight-edge witness reproduces the defect; all 32 independent edge-order shuffles preserve partition and scores.

Trivial control: setting the same-species gene count to one reproduces every original score. This explains the discrepancy entirely; no accuracy gain was measured.
Hold-out: none. The public release test was reused for diagnosis and verification. Seal hashes match reproduced material, but their claimed pre-diagnostic timing is not independently authenticated.
Caveat: the literal paper formula fails on 48 original rows and still on 30 species-corrected rows because of the separately disclosed original-gene-universe defect. “All 1,108 pass” applies only to the edge-observed denominator, not complete paper conformity.
Runtime caveat: native R4.1.3/igraph1.4.3 differs from the supported container; exact golden reproduction supports this dataset only.

Prior art rechecked 2026-11-02: current release/master/branches, four forks, 41 issue/PR records, seven PRs, 102 comments, six AI-result indexes and focused literature/community searches reveal no matching repair in inspected material; novelty is not proved. See PRIOR_ART.md.
Strongest author objection: this fixes 18 confidence-score cells without changing orthology calls or demonstrating biological impact, and the species-only patch does not fully implement the paper's formula.
NEXT BAR: On one frozen, independently chosen public dataset, demonstrate whether scores computed with the complete paper formula change a predeclared downstream decision.
Worth showing Manuel as a small, reproducible maintenance fix; scientific impact remains unestablished.

Evidence and exact commands: REPORT.md, independent_audit.py, evidence/arithmetic.json, evidence/pipeline_evidence.json and evidence/adversarial/summary.json. All tracked pod workers have exited; no contact was made.
