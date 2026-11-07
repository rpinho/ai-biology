# Confirmed defects in GO::TermFinder 0.86

Ten local fixes, each with a failing input, captured original output, independently computed correct output, an isolated patch, and an unchanged normal control. The original source is untouched in `sources/GO-TermFinder-0.86/`; locations below refer to that source. `all-fixes.patch` combines the fixes. Nothing was submitted publicly.

No overlap was found with Changes, the four archived active RT tickets, the three archived resolved-ticket subjects, or the checked mirror history. **Previously unreported is not established:** live RT returned an AWS challenge; the accessible queue snapshot is from 2021. See [PRIOR_ART.md](PRIOR_ART.md).

## GTF-001 — Compound NOT qualifiers become positive annotations

- **Location:** `lib/GO/AnnotationProvider/AnnotationParser.pm:583`.
- **Wrong behavior:** skips only a field equal to `NOT`, retaining valid pipe-separated fields such as `NOT|contributes_to` and `NOT|involved_in`.
- **Repro:** [repro/GTF-001/run.sh](repro/GTF-001/run.sh). Two negated annotations to GO:0000011 produce a positive enrichment result, p = 1/190 = 0.00526315789473685. Correct output contains no result for that term. The two genes also have positive annotations to a different term, so their background membership is unchanged.
- **Fix:** match `NOT` as a complete pipe-delimited token. Positive annotations and bare NOT controls retain their behavior. This is a modern-GAF compatibility defect; the release's POD predates those formats.
- **Reason / independent check:** [GAF 2.1, column 4](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/#qualifier-column-4), [GAF 2.2, relation/negation](https://geneontology.org/docs/go-annotation-file-gaf-format-2.2/#relation-column-4). Python splits the field into tokens before constructing annotation sets. Both qualifier orders and GAF 2.2 negation were checked.
- **Effect:** negative biological evidence can become apparently significant positive enrichment. **Confidence: high.**

## GTF-002 — Alternate GO IDs split a single term's counts

- **Location:** `lib/GO/TermFinder.pm:1353–1361`.
- **Wrong behavior:** `nodeFromId` resolves an alternate ID, but annotation counting keeps the original string rather than the node's primary ID. Genes annotated under primary and alternate IDs are counted separately.
- **Repro:** [repro/GTF-002/run.sh](repro/GTF-002/run.sh). Query genes use GO:0000099 (alternate) and GO:0000011 (primary). Original: no tested term. Correct: one term with x = 2, M = 3, n = 2, N = 20, p = C(3,2)/C(20,2) = 3/190 = 0.0157894736842105.
- **Fix:** canonicalize the ID before storing annotations, including direct aspect annotations.
- **Reason / independent check:** [OBO 1.2, alt_id](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html): alternate IDs refer to the same term. Python maps alternate IDs to primary IDs before set union and exact combinatorics.
- **Effect:** missed enrichment, split counts, and potentially mismatched returned gene membership. **Confidence: high.**

## GTF-003 — One-hypothesis Bonferroni result omits its corrected p-value

- **Location:** `lib/GO/TermFinder.pm:1578`.
- **Wrong behavior:** only assigns `CORRECTED_PVALUE` when more than one hypothesis is tested, despite the documented result contract.
- **Repro:** [repro/GTF-003/run.sh](repro/GTF-003/run.sh). Original: field absent. Correct: `CORRECTED_PVALUE = PVALUE = 1/190`.
- **Fix:** run the assignment for one or more hypotheses. Zero hypotheses still produce an empty list. The normal control exercises multiple hypotheses and the usual multiplier.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf), and local `TermFinder.pm:456–463`: adjusted p = min(1, m p), including m = 1. Python computes this formula independently.
- **Effect:** API clients receive missing data for a legitimate result; clients relying on the documented field can mis-handle the result. This is an output-contract bug, not an incorrect raw p-value. **Confidence: high.**

## GTF-004 — Tied p-values have different FDR estimates at the same cutoff

- **Location:** `lib/GO/TermFinder.pm:1977–2012`.
- **Wrong behavior:** divides expected null discoveries by array rank `i+1`; a cutoff at a tied p-value includes every tied hypothesis, not just the first members of the tie.
- **Repro:** [repro/GTF-004/run.sh](repro/GTF-004/run.sh). Two identical annotation sets yield p = 1/6. With 50 explicitly enumerated draws, average null discoveries = 0.5. Original FDRs: 0.5 and 0.25. Correct: 0.25 and 0.25. With the unchanged standard sampler and seed 17: original 0.44/0.22, corrected 0.22/0.22 (`standard.*.json`).
- **Fix:** use the last rank of the tie for both the FDR denominator and the reported expected false positives; scan tie endpoints once. Non-tied FDR control is unchanged.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf), local POD `TermFinder.pm:473–480, 573–578`: count real hypotheses as good or better than the cutoff. Python recomputes all null p-values from each recorded draw, then counts all real hypotheses at the cutoff.
- **Effect:** reported FDR depends on GO-ID tie ordering and can be inflated for early members of a tie. **Confidence: high.** This package implements a simulation estimator, not BH; replacing it with BH would change the method. A separate BH comparison is in `checks/coverage.json`.

## GTF-005 — Duplicate background names/aliases bias simulation sampling

- **Location:** `lib/GO/TermFinder.pm:1774`.
- **Wrong behavior:** background counts resolve and de-duplicate gene IDs, but the simulation pool uses the raw supplied names. A gene listed by ID and alias occupies two sampling slots; nominal two-gene draws can collapse to one gene.
- **Repro:** [repro/GTF-005/run.sh](repro/GTF-005/run.sh). Four biological genes, but raw population `[g1, alias1, g2, g3, g4]`, where alias1 = g1. Under exhaustive index-subset cycles, corrected p changes from 300/1000 = 0.300 to 333/1000 = 0.333; FDR changes from 0.300 to 0.340 for the prescribed 50 draws. Exact uniform-subset null probability is 2/C(4,2) = 1/3. The finite 50/1000-draw values are not claimed to equal the limiting probability.
- **Fix:** build the sampling pool using the same ID resolution and de-duplication used for background counts.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf): simulations sample gene sets from the background. Python independently enumerates subsets of four distinct genes. With the unchanged random sampler and seed 17, corrected p is 0.308 before and 0.329 after; the patched output exactly matches the canonical unique-ID population. Unique-background normal control is unchanged.
- **Effect:** simulation-corrected p-values and FDR can depend on redundant spellings in the background. This differs from the index-sampling algorithm bias fixed in 0.83. **Confidence: high.**

## GTF-006 — Extra anonymous genes inflate direct aspect annotations

- **Location:** `lib/GO/TermFinder.pm:379`.
- **Wrong behavior:** after replacing aspect counts with direct annotations, adds every extra gene implied by `totalNumGenes` back to that direct count.
- **Repro:** [repro/GTF-006/run.sh](repro/GTF-006/run.sh). Two explicit annotations to biological_process among four known genes; client supplies total N = 20. Original M = 18, p = 153/190 = 0.805263157894736. Correct direct M = 2, p = 1/190 = 0.00526315789473685.
- **Fix:** retain extra genes in population and unannotated counts, without inventing direct annotations to the aspect.
- **Reason / independent check:** 0.80 Changes and local `TermFinder.pm:1227–1232, 1288–1297, 1304–1320` specify that only direct aspect annotations are tested. [GAF, GO ID](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/#go-id-column-5) identifies the annotated term; no annotation row exists for these anonymous genes. Python counts direct rows and independently expands the denominator with unannotated entities.
- **Effect:** direct aspect enrichment can disappear when the user correctly supplies a larger total gene count. Other term counts in the normal input remain unchanged. **Confidence: high for inconsistency with the implemented direct-annotation definition.**

## GTF-007 — Obsolete status depends on tag order

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:310, 320`.
- **Wrong behavior:** `namespace` resets validity to true, resurrecting a term whose earlier tag was `is_obsolete: true`.
- **Repro:** [repro/GTF-007/run.sh](repro/GTF-007/run.sh). Original `nodeFromId('GO:0000011')` returns an obsolete node. Correct: absent; the live root and other term remain present.
- **Fix:** retain a separate obsolete flag until the next term stanza. Conventionally ordered obsolete terms continue to be excluded.
- **Reason / independent check:** [OBO 1.2, is_obsolete and serializer conventions](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html). Parser acceptance must not depend on suggested serializer tag order. Python collects all stanza tags before filtering obsolete terms.
- **Effect:** obsolete terms can enter the graph and enrichment analysis with valid alternative tag layouts. **Confidence: high.**

## GTF-008 — Ignoring an ambiguous alias deletes the preceding valid gene

- **Location:** `lib/GO/TermFinder.pm:1111–1123, 1176–1198`.
- **Wrong behavior:** ambiguous-alias branch neither resets the previous `$databaseId` nor skips subsequent duplicate handling. That handling pops the most recently accepted gene.
- **Repro:** [repro/GTF-008/run.sh](repro/GTF-008/run.sh). Query `[g1, g2, shared]`, with `shared` an alias for two other genes. Original accepted genes: `[g1]`, no result. Correct: `[g1,g2]`, p = 1/190; only `shared` is ignored.
- **Fix:** immediately continue after excluding an ambiguous alias.
- **Reason / independent check:** the documented ambiguity policy in local `TermFinder.pm:1109–1118` excludes the ambiguous alias; it does not authorize deleting another gene. Python constructs the name-to-ID relation independently and excludes names with multiple targets.
- **Effect:** list-order-dependent sample size, lost enrichment, and wrong gene membership. Distinct from RT #77197, which concerns case-insensitive standard-name lookup. **Confidence: high.**

## GTF-009 — Typedef stanzas terminate the entire ontology parse

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:285`.
- **Wrong behavior:** stops at the first `[Typedef]`, ignoring all later terms.
- **Repro:** [repro/GTF-009/run.sh](repro/GTF-009/run.sh). Put a valid `part_of` definition before the terms. Original: all three queried nodes absent. Correct: all three present, with the same GO graph as when the definition is last.
- **Fix:** finish the preceding term and skip non-term stanza contents, then resume at the next term; do not stop parsing the file.
- **Reason / independent check:** [OBO 1.2, stanza conventions](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) actually recommends typedefs before terms. Python discovers term stanzas independently of typedef placement.
- **Effect:** a correctly formatted ontology can load as an empty or incomplete graph. **Confidence: high.**

## GTF-010 — Cyclic ontology input causes uncontrolled recursion

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:616–630`.
- **Wrong behavior:** recursively extends paths without detecting revisited nodes.
- **Repro:** [repro/GTF-010/run.sh](repro/GTF-010/run.sh). GO:0000011 is_a GO:0000012 and vice versa. Original warns of deep recursion and returns no result before the 0.5-second watchdog kills it; output is in `before.txt`. Patched: promptly exits nonzero with `Cycle in ontology involving ...` (`after.txt`).
- **Fix:** reject a path that revisits its originating node or an existing ancestor.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf) requires a DAG; [OBO parser requirements](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) require graceful failure. A separate Python DFS detects the cycle directly from the edge list. The valid diamond-DAG output is byte-identical.
- **Effect:** malformed user ontologies can hang or exhaust resources instead of producing a useful rejection. This is an invalid-input robustness defect, not a wrong p-value on a valid GO DAG. **Confidence: high.**

## Suspected / not promoted to bugs

- Native boundary validation beyond feasible observed count tables is incomplete by inspection (negative arguments, N larger than the constructor cache, and a zero-sized cache). No demonstrated valid enrichment call reaches these cases; no additional correctness claim or patch is made.
- General OBO escaping, imports, trailing modifiers, and relation types beyond is_a/part_of were not exhaustively tested. No failure is claimed without a repro.
- No representable-tail numerical failure was found in the tested grid and extreme cases. `checks/numeric.json` records 23,761 exact-reference comparisons; worst relative error was 4.86e-9. Four true tails below binary64 range return zero. This is a floating-point range limitation, not a new bug claim.

## Known issues excluded

- RT #102758: long-double Perl test comparisons; #102757: compiler detection; #77197: case-insensitive standard-name lookup (ticket body concerns `databaseIdByStandardName`, despite its title); #13361: GO::View clipping. Archived ticket bodies were read and stored locally.
- Resolved RT #33010: zero-hypothesis crash; #30861: native test failure; #6779: capitalization typo. These are excluded; GTF-003 concerns one hypothesis, not zero.
- Changes 0.86 p-value ceiling; 0.84 invalid-observation checks; 0.83 random-index bias; 0.81 casing fixes and cross-aspect error diagnostics; 0.80 earlier Bonferroni multiplier bug. None is claimed as a new discovery here.
- Flight and Wentzell (2009), [Potential Bias in GO::TermFinder](https://doi.org/10.1093/bib/bbn054), reports the sampling-algorithm bias fixed in 0.83. GTF-005 instead concerns inconsistent normalization of the supplied population in 0.86.
- Evidence-code inclusion/exclusion is explicitly a TODO in `AnnotationParser.pm:116–129`; the parser includes IEA by default and has no implemented evidence-filter API. This is not reported as a newly discovered defect. Filtering must be performed on the input annotations.
- BH is not implemented or promised by this version. BH and the documented simulated FDR differ by design; that difference is not a bug. Bonferroni's data-dependent family/filtering choices are described by the authors; this job does not claim a new FWER guarantee for them.
