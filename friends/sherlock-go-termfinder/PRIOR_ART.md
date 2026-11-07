# Source and prior-report check

Checked locally on 2026-11-06. Read `~/dev/open-science/friends_queue/GOAL.md` before inspecting source. No public changes or communications were made.

## Canonical source

The [paper's Sherlock-lab copy](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf) identifies CPAN as the distribution location. [MetaCPAN's latest release API](https://fastapi.metacpan.org/v1/release/GO-TermFinder) selects SHERLOCK's GO-TermFinder-0.86 archive, released 2009-11-19. Used that author's archive rather than a downstream modified installation. The archive, original Changes, API response, and module hashes are retained in `sources/` and `SOURCE.json`.

The API's `version` field is stale at 0.85; `name`, download URL, distribution `VERSION`, module version, and Changes identify 0.86. This metadata inconsistency is not reported as a software correctness bug.

GitHub repository search for GO-TermFinder found [gitpan/GO-TermFinder](https://github.com/gitpan/GO-TermFinder), a read-only release-history mirror, and an unrelated experiment repository. No Sherlock-lab-maintained GitHub mirror was found. Recorded gitpan HEAD `414c6cd22b8ec6eec90a2f22f3b7f83d26d94ba6`; its TermFinder.pm is byte-identical to the CPAN file. It is not treated as an independently maintained newer release.

Also inspected the three relevant downstream modules in [princeton-genomics/GO-Tools](https://github.com/princeton-genomics/GO-Tools), which explicitly depends on 0.86 and carries modified copies. Their source still contains the relevant NOT equality test, raw alternate-ID counting, one-hypothesis Bonferroni guard, raw population sampling, rank denominator, ambiguity fall-through, obsolete-order dependence, and early typedef termination. This downstream project is not identified as a Sherlock-lab mirror. Its downloaded source and HEAD metadata are retained in `prior-art/`.

## Changes read before correctness experiments

The entire `sources/GO-TermFinder-0.86/Changes` was read. Excluded fixes already described there: 0.86 rounding ceiling; 0.84 invalid hypergeometric observations; 0.83 random-index sampling bias; 0.81 case-sensitive/case-insensitive ambiguity handling and diagnostics; 0.80 earlier Bonferroni correction and zero-hypothesis handling; older annotation API capitalization typos. GTF-005 concerns the supplied sampling population, not the random-index algorithm already repaired in 0.83.

## RT and GitHub issues

[Live RT queue](https://rt.cpan.org/Public/Dist/Display.html?Name=GO-TermFinder) and public/REST alternatives returned HTTP 202, zero bytes, `x-amzn-waf-action: challenge`. This prevented reading the live tickets before experimentation; the limitation was recorded in STATUS.md before tests. Gitpan's all-state issue API returned an empty list (`prior-art/gitpan-issues.json`).

Recovered the [2021 active queue snapshot](https://web.archive.org/web/20210519024220/https://rt.cpan.org/Public/Dist/Display.html?Name=GO-TermFinder) and archived bodies of all four active tickets. Read them before finalizing the bug list:

| Ticket | Existing report | Treatment |
| --- | --- | --- |
| [102758](https://rt.cpan.org/Public/Bug/Display.html?id=102758) | Native tests compare Perl long-double values with C++ double results too strictly | Excluded |
| [102757](https://rt.cpan.org/Public/Bug/Display.html?id=102757) | FreeBSD ships clang++ but build searches for g++ | Excluded |
| [77197](https://rt.cpan.org/Public/Bug/Display.html?id=77197) | Case-insensitive standard-name lookup; body identifies wrong final return in `databaseIdByStandardName` | Excluded; GTF-008 is a separate stale-ID/pop bug |
| [13361](https://rt.cpan.org/Public/Bug/Display.html?id=13361) | GO::View arbitrarily limits displayed top nodes | Excluded |

Bodies: `prior-art/rt-<ID>.html` and readable `.txt`. The archived resolved queue lists #33010 (zero hypotheses), #30861 (native test), #6779 (capitalization typo); excluded those subjects too. Live MetaCPAN's distribution response reports four active and three closed tickets, matching the archived counts, but matching counts do not establish current ticket identity or freshness.

## Literature / format references

- Boyle et al. (2004), [GO::TermFinder](https://doi.org/10.1093/bioinformatics/bth456): hypergeometric tail, gene sampling, and simulated correction definitions. Official lab PDF retained as `prior-art/Boyle-2004.pdf`.
- Flight & Wentzell (2009), [Potential Bias in GO::TermFinder](https://doi.org/10.1093/bib/bbn054): existing incorrect random-index sampling, repaired in 0.83. Excluded as an already reported finding.
- [GAF 2.1](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/) and [GAF 2.2](https://geneontology.org/docs/go-annotation-file-gaf-format-2.2/): pipe-separated NOT qualifiers/relations and annotation columns. Copies retained locally.
- [OBO 1.2 specification](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html): alternate IDs, obsolete status, stanza order, and graceful parser failure. Copy retained locally.

Targeted web searches for GO-TermFinder with NOT qualifiers, alternate IDs, FDR ties, supplied gene totals, and existing bugs found the original papers, Changes, and downstream documentation, but no matching report for these ten repros. This is a bounded check, not proof of absence from all prior literature or tickets. No NOTE-track paper or scientific novelty claim is made; a cited-by literature audit for a new paper was not attempted.
