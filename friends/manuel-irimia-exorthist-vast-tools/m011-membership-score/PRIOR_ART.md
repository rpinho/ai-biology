# Independent M011 prior-art audit (opened 2026-11-02)

Baseline identified before writing referee code: the public ExOrthist v2.0.0 release and its official nf-test snapshot, not a leaderboard. Claim says EX_clusters.tab MD5 02479360ed2b8d659612fc60477ad355. This is a software consistency audit, not a contest or accuracy improvement.

Initial public search: “ExOrthist membership score gene species Irimia 2021”, “ExOrthist github membership score bug D2 2026”, “ExOrthist arxiv 2025 2026”. Found primary paper https://pmc.ncbi.nlm.nih.gov/articles/PMC8379844/ and official code https://github.com/biocorecrg/ExOrthist; no matching correction surfaced. Paper search also found later Mantica/Irimia work, not a replacement score-consistency result. Primary formula and author identity still require direct inspection.

Prior agent's PRIOR_ART.md and REPORT.md read as allegations only. Their searches, golden reproduction and independence are not accepted on trust. Independent checks pending: current raw source, release/test snapshot, all-state issues/PRs/forks, recently updated repository search, prescribed AI result indexes, arXiv/recent references and public community search. No global novelty claim will be made.

Baseline reproduction will use public source and public official test artifacts, with claim-derived graph/output data as comparison only. All numerical compute will run on the authorized shared ref pod under /workspace/ref_manuel_M011 (8 cores, 16 GB), never locally. No model or biological-accuracy optimization is planned.

## Independent checks completed before final pipeline run

Publisher https://link.springer.com/article/10.1186/s13059-021-02441-9 lists Manuel Irimia among authors and gives the exact Methods formula; the >97% comparison is between recovered exons from ExOrthist and liftOver, not a membership-score accuracy number. Fresh Europe PMC XML fetched on pod (SHA256 269f249cebb5707baa7e35ae2f60983908b0965336759c726546228dd4c61a9b).

Live official release API: v2.0.0, 2024-12-05. Fresh released archive SHA256 5fb661adb0927b2645654beacb046f107a366828d93b0d66fbf495a7ed04fb85. Its nf-test snapshot names MD5 02479360ed2b8d659612fc60477ad355. Independent native D2 and formatter replay reproduces this hash and corrected SHA256 5bc3a8a7494e9592a468e06d61c1a45ec816be7d9b565222ca586d456e8595c7; original sequence-to-graph pipeline is still running.

GitHub API search sorted by updated, with forks included, returns official repository plus four public forks. Fresh master and v2.0 branch have D2 SHA256 7cd4ce06659f7b56b295e5ebd0fc98896caaf8ffa64b285bb8615c9d1b48e6d9. All four fork tips and historical v1.0.2 selector retain the same mistake. All 41 issue/PR records and 7 PRs read, zero open PRs. Comment endpoint needed two pages (pagination headers saved); relevant comments and closest graph/runtime issues inspected separately. No matching membership/species-count repair found. Initial pod API calls hit public rate limits; subsequent anonymous public GETs from local machine succeeded. No credentials used.

Fresh README indexes: BakeLab/Epi-results; google-deepmind/alphaevolve_results; google-deepmind/alphaevolve_repository_of_problems; openai/math; plasma-ai/erdos; kisonecat/openai-math. No ExOrthist/exon-orthology/membership-score match in these bounded indexes. EinsteinArena exact-term public search uninformative. No accuracy leaderboard applies.

Additional public queries: ExOrthist membership bug/correction; ExOrthist 2026 exon orthology; ExOrthist species score GitHub issues; ExOrthist on arXiv after 2025-11-01; ExOrthist on X/Reddit/Bluesky. Results identify official sources and later applications (including eLife 104275), not a better score-consistency repair. No relevant recent arXiv correction surfaced. This is bounded prior-art screening, not proof of global novelty.

## Closing independent recheck

2026-11-02T12:05:20Z: latest-release API still v2.0.0; 41 all-state issue/PR records unchanged; recently updated repository search still official repository plus four forks. Refetched master D2 and all six AI README indexes are byte-identical to the opening downloads. Both official branches and all four fork selectors were directly inspected. All 102 public issue comments across two pages were screened, including the closest graph/runtime issue #17; no matching membership species-count report found. See evidence/closing_audit.json and evidence/fork_branch_audit.json.

Baseline now independently reproduced from the full official public genome/GTF inputs, with exact golden table and graph hashes. The proposed repair reproduces its claimed corrected table hash. Best defensible statement is a narrow reproducible maintenance correction; no superiority to other orthology methods, record or global novelty is claimed.
