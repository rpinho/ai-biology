# Prior art

Started 2026-11-04 22:46 UTC. This file precedes research code.

Read first: `../friends_queue/GOAL.md`; also read `_codex/RULES.md`,
`_codex/FRONT.md`, the Victor scoreboard and queue. Only Victor's own papers
are eligible. No outreach, uploads or remote compute. Resource cap: Mini,
four cores, 4 GB, nice 10; total deadline 2026-11-05 04:46 UTC.

## Selection and inherited results

- Scoreboard rank 1, 2025 Figure 2D stress 35.8, was already improved to
  16.8196634149424955 in `friends_board_victor_1031`; do not repeat.
- Rank 2 is a fitted quadratic coefficient and explanatory fit, not a held-out
  prediction record. Its data and fit were already examined; do not relabel it.
- Rank 3 / review T3.12 is killed queue V02; do not repeat.
- Next eligible printed numerical objectives: Figure 2A/B/C, stresses
  16.8 / 34.8 / 23.4. Each requires its exact original profile data and distance
  convention. AnaCoDa's exact fitted costs were previously not located.
- Pathogen targets are excluded by this job. Previously killed and failed
  targets, and non-Victor-authored mathematical branches, are excluded.

## Public source checks, 2026-11-04

Paper: https://doi.org/10.1101/2025.06.03.657573,
*Negative epistasis limits current codon optimization approaches* (2025).
Victor Garcia is a coauthor. The primary PDF and supplement will be inspected
locally from existing public-source archives, with checksums and provenance.

Live web queries for the exact title, DOI + code/Shah/Rudorf, title +
AnaCoDa/MDS, DOI + GitHub/stress returned no same-target improved number.
Direct bioRxiv web-tool opens failed (tool internal access error); public API
and shell HTTP reads will be attempted. This is not evidence of absence.

The inherited scoreboard's prior-art file records public GitHub searches,
agent-repository trees, recent papers and community checks on 2026-11-01.
They are historical evidence, not a substitute for live checks before a
positive claim. Live GitHub searches sorted by update, open issues/PRs if a
source repository is found, recent papers and public community searches,
and relevant agent repositories remain to be checked.

Best located public numbers for Figure 2A/B/C: printed 16.8 / 34.8 / 23.4;
no independently comparable later value established. Standard method:
two-dimensional Kruskal nonmetric multidimensional scaling, with the paper's
stated profile distances. Reproduction has not yet run. Do not substitute
Hamming distances, a new translation-cost fit or a different stress definition.

The archived independent referee `friends_ref_victor_1031/VERDICT.md` was
subsequently read. It supersedes the old non-reproduction statement:
native R/MASS defaults give 35.75613323 on Figure 2D and ordinary tighter
settings/restarts attain the 16.82 result. That target remains excluded.
Its archived runtime recipe permits an isolated native R extraction here.

## Completed source checks and reproduction

Read-only HTTP fetches succeeded; `FETCH_LOG.jsonl` contains dates, byte counts
and SHA256 receipts. The current bioRxiv API returns only v1 (2025-06-06),
`published: NA`. The fresh PDF caption on page 5 prints all three target
numbers; page 15 defines Euclidean raw profile distances and Kruskal NMDS.

GitHub repository queries sorted by updated (`"Negative epistasis"`,
`"657573"`, `codon epistasis 2026`, `AnaCoDa Gees Garcia`) found only unrelated
repositories or no hits. No original analysis repository, open change to its
analysis or same-data successor was located. This does not prove none exists.
The live public trees of BakeLab/Epi-results, both Google DeepMind AlphaEvolve
repositories, openai/math, kisonecat/openai-math, plasma-ai/erdos and
vinid/einstein-arena had no path matching codon, AnaCoDa, isoMDS or epistasis.
**Limitation:** GitHub truncates the openai/math recursive tree; its absence
of hits is only a partial-tree check. Repository source content was not
exhaustively searched. Large trees were not retained; their hashes, hit lists
and truncation flags are in the fetch log.

Recent arXiv query (2025-11-04 through 2026-11-04, codon AND epistasis)
returned one broad protein-evolution review, not a same-data NMDS result.
Exact-title/DOI searches including public X/Reddit indexes and current 2026
queries found the preprint, its institutional talk and bibliographic mirrors,
with no later numerical configuration located. No account was created and
no post, private community or message was accessed.

Best publicly located methods for these finite targets remain ordinary
Kruskal NMDS. Native R 4.6.2, MASS 7.3-66, all defaults, directly reproduce
34.8056749 → printed 34.8 for Shah and 23.396544 → printed 23.4 for Rudorf.
Unlike the earlier Hamming search, the standard method was run first here.
With only tighter documented convergence settings the classical starts reach
17.0483775 and 13.5073137. A fixed 100 random starts reaches 16.9693902 and
13.4830828. Credit belongs to the established R/MASS/Kruskal method; this job
claims improved feasible values for the printed objectives, not a new method.

Primary rate data:
- Shah & Gilchrist 2010, Table S2, Rc column:
  https://doi.org/10.1371/journal.pgen.1001128.s007 .
- Rudorf & Lipowsky 2015, Table S2, 0.7 h^-1 and 2-1-2 pathway:
  https://doi.org/10.1371/journal.pone.0134994.s003 .
- Original sequences, fresh download identical to archived DC3:
  https://www.biorxiv.org/content/biorxiv/early/2025/06/06/2025.06.03.657573/DC3/embed/media-3.csv?download=true .

## Final recheck, 2026-11-04 22:56–22:57 UTC

Repeated bioRxiv API, supplement listing, updated-sorted GitHub repository
queries for title/DOI/codon+MDS and the new value prefixes, and all seven
agent-repository trees (`results/final_recheck.log`, `FETCH_LOG.jsonl`).
No new version or later comparable result was located. The same partial-tree
limitation for openai/math remains. Final web queries again returned the
preprint and its bibliographic/institutional listings. Sciety's activity feed
lists only 6 June 2025:
https://sciety.org/articles/activity/10.1101/2025.06.03.657573 .
The conclusion is bounded by these searches; no claim of global optimality
or exhaustive priority is made.

## Independent referee intake (2026-11-04)
The text above was supplied with the claim and is not independent evidence.
I read RULES.md and CLAIM.md before writing referee code. Live web searches
for the exact DOI plus stress and the exact paper title locate the preprint,
Sciety record, and ZHAW talk; no comparable replacement value was located.
Primary DOI direct web open fails with an internal access error; inspect the
public PDF itself, not the inherited transcription. Recompute from primary
Rudorf Table S2 and original DC3 sequences; use submitted coordinates only as
a candidate witness. Do not import producer or previous referee programs.
No construction or new optimization is intended: this is a witness audit.

Source-reading outcome: opened the archived primary PDF itself with pypdf,
extracting pages 1, 5, 13, 15 into evidence/. Page 1 lists Victor Garcia;
page 5 Figure 2 caption prints 23.4 for Rudorf (the caption does not itself
state percent). Page 13 specifies 0.7 h^-1 and the 2-1-2 pathway; page 15
specifies Euclidean rate-profile distances and Kruskal NMDS. Source freshness
is unconfirmed: fresh shell PDF fetch failed HTTP 429, web PDF fetch HTTP 403.
Web exact-DOI plus 23.4 search also retrieves the paper text on ResearchGate:
https://www.researchgate.net/publication/392475328_Negative_epistasis_limits_current_codon_optimization_approaches
No positive NEW conclusion is made, so no final record/priority claim is made.

## Resumed independent audit (2026-11-04)
The earlier pod failure does not prevent this light local recomputation.
Reopened archived primary PDFs directly (pypdf and rendered Figure 2).
Figure 2C prints 23.4; Figure 2 is two-dimensional; page 15 specifies
Euclidean elongation-rate profiles and Kruskal NMDS; page 13 specifies
Rudorf growth 0.7 h^-1 and 2-1-2. The caption has no percent sign.
Live exact-title/DOI web searches again locate the paper and institutional
talk; no comparable replacement was found. No broader priority conclusion.
Consulted official MASS isoMDS documentation and public MASS C/R source:
https://stat.ethz.ch/R-manual/R-devel/library/MASS/html/isoMDS.html
https://raw.githubusercontent.com/cran/MASS/master/R/isoMDS.R
https://raw.githubusercontent.com/cran/MASS/master/src/MASS.c
These define percent Stress-1, PAVA on ordered dissimilarities, Euclidean
configuration distances, and stable input ordering for ties. The audit will
write its own profile reconstruction and isotonic evaluation; claimant and
previous referee code will not be imported or executed.

Final referee facts: independent local stress certificate passed; published
plot itself independently evaluates to 23.396468%, corroborating objective
identity. Fresh PLOS supplementary PDF downloaded and matches archived SHA256
61af300f8f1272663be05ddc5e54bae907ecfa3e7d2d016d94d4489cd30aa3fa.
Fresh bioRxiv PDF and sequence requests returned HTTP 429; retained and used
archived primary files with explicit hashes. This audit establishes a lower
feasible number relative to Figure 2C, not an exhaustive-priority finding.
No public analysis repository was located; its exact original implementation
remains inferred, not directly inspected. No search/construction algorithm
was run by this referee.
