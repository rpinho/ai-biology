![Biology with AI agents: Anthropic x Adaptyv, Arc Virtual Cell Challenge, Virtual Embryo Challenge](assets/banner.png)

# ai-biology: the full record

**AI for Biology & Drug Discovery.**

Everything I've run on biology with AI agents, in one place. Three sponsored challenges, two tools, and bug reports for scientists' published software. Each section links to the code and results, says how it was checked, and says where a result is still a candidate.

My PhD was on the evolution of gene regulatory networks, in Marcus Feldman's lab at Stanford: evolutionary biology and population genetics. I came back to it in 2026 with AI agents. Biology has been the hardest of the three fields I've worked in this year, after math and physics. Why, in the [field retro](RETRO.md).

Sister hubs: [math](https://github.com/rpinho/math-certificates) · [physics](https://github.com/rpinho/ai-physics) · [astronomy](https://github.com/rpinho/planet-hunt)

## Why it's laid out like this

Brian Armstrong wrote on November 7 that publicly funded science should work like open source: every experiment as a repo anyone can fork, rerun and fix, with replication rewarded like new papers ([post](https://x.com/brian_armstrong/status/2119150702446420027)).

So each result here ships with a separate referee's verdict. A referee here is a different agent that rebuilds the claim from the primary source on a fresh clone, without the finder's code.

This file puts the full record of every result in one place, for readers and reviewers who want it in a single document. Each section below is copied word for word from the result's own folder in this repository: the claim or bug report, the independent referee's verdict, and the prior-art check where there is one.

---

# Challenges

_Source: [README.md](README.md)_

| Challenge | What I entered | Status | Code |
|---|---|---|---|
| **Arc Institute Virtual Cell Challenge 2026** ([site](https://virtualcellchallenge.org/)) | Predicting CRISPRi knockdown effects in an unseen cell type. Best official validation 0.16438, about rank 463 of 1,580 when recorded. The final phase closed November 5 and its scores are hidden. | Closed; [retro](https://github.com/rpinho/virtual-cell-challenge/blob/main/RETRO.md) published | [virtual-cell-challenge](https://github.com/rpinho/virtual-cell-challenge) |

- **Anthropic × Adaptyv Protein Design Competition**: [adaptyv-challenges](https://github.com/rpinho/adaptyv-challenges). Submitted; lab results not out at the time of writing.
- **Virtual Embryo Challenge**: [virtual-embryo-community](https://github.com/rpinho/virtual-embryo-community). No challenge data or results are published here.

---

# Tools and older work

_Source: [README.md](README.md)_

| Repo | What it is |
|---|---|
| [louis](https://github.com/rpinho/louis) | Pick an autoimmune disease, get trust-ranked candidate CD4+ T-cell targets, built on the Marson/Pritchard genome-scale T-cell Perturb-seq. MCP server, skill or Slack bot. Hypothesis generation, not a clinical claim. |
| [autoregulation](https://github.com/rpinho/autoregulation) | My PhD code: stability of Boolean gene regulatory networks depends on the sign of self-regulation. Python 2, kept as a record. Published (PLoS Comput Biol 2014; PLoS ONE 2012, 2015). |

---

# Manuel Irimia — ExOrthist and vast-tools

Folder: [friends/manuel-irimia-exorthist-vast-tools](friends/manuel-irimia-exorthist-vast-tools)

## Report

_Source: [friends/manuel-irimia-exorthist-vast-tools/REPORT_FOR_MANUEL.md](friends/manuel-irimia-exorthist-vast-tools/REPORT_FOR_MANUEL.md)_

## ExOrthist and vast-tools: bug report, Nov 6 2026

AI agents found these bugs; a separate independent check reproduced each. Pins: ExOrthist `83185dcf04c4bda7c765a6bcf87fb1b48b36f329`; vast-tools `5598e1f1b0067611dc9e5abb285b4eacaf543ee3`.

### How to use

The bundle unpacks into one folder, `manuel_bugs_1106/`. Run the repros on a throwaway checkout at the pinned commit, so your own checkout isn't touched:

```
tar xzf manuel_bugs_1106.tar.gz
git -C /path/to/ExOrthist worktree add /tmp/exo 83185dc
bash manuel_bugs_1106/repro/A3-01/run.sh /tmp/exo     # prints WRONG OUTPUT / FAILURE REPRODUCED
git -C /tmp/exo apply "$PWD"/manuel_bugs_1106/patches/ExOrthist/*.patch
bash manuel_bugs_1106/repro/A3-01/run.sh /tmp/exo     # prints CORRECT
```

vast-tools works the same way at `5598e1f`, with `patches/vast-tools/`. The patches are made against those two commits and apply together; on a newer version some may need adjusting.

Runners need Python 3, plus Perl, pandas or R depending on the stage. R needs igraph and hashmap for D2, and optparse for vast-tools diff. B1 uses a MAFFT stand-in. R6 stubs liftOver and bedtools. Details: `repro/README.md`. The commands in the entries below run from inside `manuel_bugs_1106/`, and `<repo>` is the checkout to test.

### ExOrthist

The D2 same-species count bug (lines 62/69) is the one I sent on 11-05, so it isn't repeated here.

#### A3-01: Families split across chunks

At batch size 1,000, species ordering splits 1,000 of 1,001 families across chunks. Split families are not aligned across species.
May already be fixed in your new version; it is still present on public master 83185dc (no newer branch or release).

`bin/A3_split_clusters_in_chunks.pl:179`  
Repro: `bash repro/A3-01/run.sh <repo>`  
Patch: `patches/ExOrthist/01-A3-01.patch`

#### A1-03: Transcript IDs replace gene IDs

This triggers when transcript_id comes before gene_id in the GTF (some GTF writers use that order). Transcript IDs are written where the gene IDs belong, the input check still passes, and those proteins can't be matched to their genes in the clusters.

`bin/A1_generate_annotations.pl:109`  
Repro: `bash repro/A1-03/run.sh <repo>`  
Patch: `patches/ExOrthist/02-A1-03.patch`

#### A1-01: CDS rows reuse the preceding gene ID

With CDS-only input, all six exon rows are lost. With all exons listed before the CDS lines, one gene's protein is attached to another gene and its exon rows are lost.

`bin/A1_generate_annotations.pl:1108`  
Repro: `bash repro/A1-01/run.sh <repo>`  
Patch: `patches/ExOrthist/03-A1-01.patch`

#### A1-05: CDS ordering changes strand translation

This triggers when minus-strand CDS records are in ascending order. The protein sequence changes and the exon numbering is reversed.

`bin/A1_generate_annotations.pl:163`  
Repro: `bash repro/A1-05/run.sh <repo>`  
Patch: `patches/ExOrthist/04-A1-05.patch`

#### A1-02: Exon endpoints include a neighboring residue

Exon end positions include one residue from the next exon: 22 instead of 21, and 11 instead of 10. Neighboring exons overlap by one residue.

`bin/A1_generate_annotations.pl:1291`  
Repro: `bash repro/A1-02/run.sh <repo>`  
Patch: `patches/ExOrthist/05-A1-02.patch`

#### B1-02: Gene IDs collide between species

This triggers when two species reuse the same gene ID. Two families collapse into one, and all four cross-species pairs are scored instead of the two specified ones.

`bin/B1_parse_IPA_prot_aln.pl:135`  
Repro: `bash repro/B1-02/run.sh <repo>`  
Patch: `patches/ExOrthist/06-B1-02.patch`

#### B06: Cluster totals omit reintroduced exons

A four-exon cluster is reported as three exons. Its hub exon's membership score is 1.12 instead of 0.90.

`bin/D2_cluster_EXs.R:80`  
Repro: `bash repro/B06/run.sh <repo>`  
Patch: `patches/ExOrthist/07-B06.patch`

#### B11: The dPSI option is ignored

Requesting a dPSI of 40 still applies 15. Two exons are called regulated instead of one.

`bin/compare_exon_sets.pl:45`  
Repro: `bash repro/B11/run.sh <repo>`  
Patch: `patches/ExOrthist/09-B11.patch`

#### B4-01: Header filter drops any row containing CID

The header is removed with `grep -v 'CID'`, so every row whose gene ID contains CID (CIDEA, PCID2) is deleted too. In the test, two of four rows are removed from each merged feature table.

`bin/B4_merge_PROT_EX_INT_aln_info.pl:15`  
Repro: `bash repro/B4-01/run.sh <repo>`  
Patch: `patches/ExOrthist/10-B4-01.patch`

#### A1-04: Lowercase bases translate to X

Twelve lowercase CDS bases translate to XXXX instead of MAAA.

`bin/A1_generate_annotations.pl:83`  
Repro: `bash repro/A1-04/run.sh <repo>`  
Patch: `patches/ExOrthist/11-A1-04.patch`

#### B1-01: Protein labels erase intron matches

This triggers when protein IDs have five characters or fewer. Four intron matches are erased.

`bin/B1_parse_IPA_prot_aln.pl:571`  
Repro: `bash repro/B1-01/run.sh <repo>`  
Patch: `patches/ExOrthist/12-B1-01.patch`

#### B2-01: Table splitting changes identifiers

Cluster IDs lose their leading zeros before exon realignment: CID 007300 becomes 7300, and null becomes NA, so the IDs passed on no longer match.

`bin/B2_split_EX_pairs_to_realign.py:18`  
Repro: `bash repro/B2-01/run.sh <repo>`  
Patch: `patches/ExOrthist/13-B2-01.patch`

#### B08: Contig hyphens change exon lengths

A pair of 90-nt exons passes on contig7 but disappears on contig-7. A hyphen in the contig name changes the result.

`bin/C2_filter_and_select_best_EX_matches_by_targetgene.pl:84`  
Repro: `bash repro/B08/run.sh <repo>`  
Patch: `patches/ExOrthist/14-B08.patch`

#### B03: Reclustering consumes data as headers

The first data row is read as a header. Six genes in three pairs become two genes in one component. Patch shared with B16.

`bin/D3.1_recluster_genes_by_species_pair.py:24`  
Repro: `bash repro/B03/run.sh <repo>`  
Patch: `patches/ExOrthist/15-B16-B03.patch`

#### B04: Exons without clusters acquire nan labels

Two pairs that are absent from the exon clusters merge into Family.01nan. Patch shared with B13.

`bin/D3.2_recluster_EXs_by_species_pair.py:44`  
Repro: `bash repro/B04/run.sh <repo>`  
Patch: `patches/ExOrthist/17-B04-B13.patch`

#### B13: Coordinate lookup crosses genes

The lookup uses the coordinate only. An exon from an unrelated species at the same coordinate overwrites the pair's suffix .003 with .009. Patch shared with B04.

`bin/D3.2_recluster_EXs_by_species_pair.py:42`  
Repro: `bash repro/B13/run.sh <repo>`  
Patch: `patches/ExOrthist/17-B04-B13.patch`

#### B07: Zero cutoffs are replaced by defaults

Similarity and length cutoffs set to zero are replaced by the defaults, so a pair that passes zero cutoffs is dropped.

`bin/C2_filter_and_select_best_EX_matches_by_targetgene.pl:45`  
Repro: `bash repro/B07/run.sh <repo>`  
Patch: `patches/ExOrthist/18-B07.patch`

#### R6-02: FASTA descriptions prevent canonical-site lookup

This triggers with -canonical_ss when the FASTA headers have a description. A known canonical exon pair is no longer found (one pair becomes zero).

`bin/get_liftovers.pl:140`  
Repro: `bash repro/R6-02/run.sh <repo>`  
Patch: `patches/ExOrthist/19-R6-02.patch`

#### S1-01: Numeric cluster selection returns no data

Selecting cluster 42 for plotting leaves the annotation, overlap and protein inputs empty.

`bin/subset_inputs.py:24`  
Repro: `bash repro/S1-01/run.sh <repo>`  
Patch: `patches/ExOrthist/20-S1-01.patch`

#### B09: OG categories miscount species multiplicity

An orthogroup with six genes in one species and one in the other (6:1) misses both the >=3 and >=4 categories. A 3:4 orthogroup gives Other=-1.

`bin/get_cluster_stats.pl:204`  
Repro: `bash repro/B09/run.sh <repo>`  
Patch: `patches/ExOrthist/21-B09.patch`

#### Crashes and failed runs

These stop with an error instead of giving wrong results.

##### B05: Singleton reassignment aborts clustering

With input generated by D1, D2 stops with "the condition has length > 1". The whole chunk is aborted.

`bin/D2_cluster_EXs.R:33`  
Repro: `bash repro/B05/run.sh <repo>`  
Patch: `patches/ExOrthist/08-B05.patch`

##### B16: Reclustering rejects the cluster format

The three-column, headerless gene file described in the README raises ParserError. Patch shared with B03.

`bin/D3.1_recluster_genes_by_species_pair.py:27`  
Repro: `bash repro/B16/run.sh <repo>`  
Patch: `patches/ExOrthist/15-B16-B03.patch`

##### B02: The module passes unsupported flags

The --orthopairs exon-reclustering command exits with code 2. It passes -sp1/-sp2 where -s1/-s2 are expected.

`modules/local/exorthist/recluster_exs.nf:26`  
Repro: `bash repro/B02/run.sh <repo>`  
Patch: `patches/ExOrthist/16-B02.patch`

#### Minor

- **A1-07: Transcripts sharing protein IDs concatenate**. When one protein ID is used by two transcripts, its sequence and exon rows are doubled.  
  `bin/A1_generate_annotations.pl:116`  
  Repro: `bash repro/A1-07/run.sh <repo>`  
  Patch: `patches/ExOrthist/22-A1-07.patch`

- **B01: Coordinate sorting retains overlap variants**. Coordinates are sorted as text. Across a digit boundary, three exon pairs are kept instead of two.  
  `bin/C3_count_matches_by_EX.pl:48`  
  Repro: `bash repro/B01/run.sh <repo>`  
  Patch: `patches/ExOrthist/23-B01.patch`

- **B10: Plot exons follow text ordering**. Exons are ordered as text, so a transcript is plotted 2,3,1. Phases and coordinates change.  
  `bin/generate_exint_plotter_input.py:146`  
  Repro: `bash repro/B10/run.sh <repo>`  
  Patch: `patches/ExOrthist/24-B10.patch`

- **R5-01: Accession prefixes confuse the viewer**. When two accessions share six prefix characters, one species is empty and the other is duplicated.  
  `bin/retrieve_IPA_aln.pl:122`  
  Repro: `bash repro/R5-01/run.sh <repo>`  
  Patch: `patches/ExOrthist/25-R5-01.patch`

- **R6-01: Annotation paths truncate species names**. Paths such as ./Fern.gtf and data.v1/Fern.gtf fail before liftover.  
  `bin/get_liftovers.pl:60`  
  Repro: `bash repro/R6-01/run.sh <repo>`  
  Patch: `patches/ExOrthist/26-R6-01.patch`

- **B14: Hash characters abort input parsing**. A gene named oak#extra makes the D2 parser stop.  
  `bin/D2_cluster_EXs.R:12`  
  Repro: `bash repro/B14/run.sh <repo>`  
  Patch: `patches/ExOrthist/27-B14.patch`

- **B15: Hash seeds change cluster labels**. The .01/.02 labels change for the same components. Membership is unchanged.  
  `bin/D3.1_recluster_genes_by_species_pair.py:43`  
  Repro: `bash repro/B15/run.sh <repo>`  
  Patch: `patches/ExOrthist/28-B15.patch`

- **B17: Orthogroup zero is ignored**. Orthogroup identifier 0 is treated as missing. Its genes drop out of the statistics and a division by zero follows.  
  `bin/get_cluster_stats.pl:84`  
  Repro: `bash repro/B17/run.sh <repo>`  
  Patch: `patches/ExOrthist/29-B17.patch`

- **A0-01: Run date swaps month and day**. November 6 prints as 2026-06-11.  
  `bin/A0_check_input.pl:153`  
  Repro: `bash repro/A0-01/run.sh <repo>`  
  Patch: `patches/ExOrthist/30-A0-01.patch`

### vast-tools

- **VT-001**: combine replaces a count of 3 with 0 when cRPKM rounds to 0.00. `bin/MakeTableRPKMs.pl:79`. Repro: `bash repro/VT-001/run.sh <repo>`. Patch: `patches/vast-tools/01-VT-001.patch`.
- **VT-002**: Missing microexon (MIC) counts become numbers in the merged table: renaming samples turns NA into 10/10 and PSI 50. `bin/MergeOutputs.pl:451`. Repro: `bash repro/VT-002/run.sh <repo>`. Patch: `patches/vast-tools/03-VT-002.patch`.
- **VT-004**: diff aborts when a chunk holds one event. The output has only a header, or two of three events. `R/vastdiff.R:226`. Repro: `bash repro/VT-004/run.sh <repo>`. Patch: `patches/vast-tools/02-VT-004.patch`.
- **VT-006**: Minor. When a filter keeps no events, tidy exits 255 with a division by zero (the header-only table it writes is correct). `bin/Filter_and_clean_Combine.pl:520`. Repro: `bash repro/VT-006/run.sh <repo>`. Patch: `patches/vast-tools/04-VT-006.patch`.
- **VT-005**: Minor. With group identifier 0, tidy reports an existing sample as absent. `bin/Filter_and_clean_Combine.pl:221`. Repro: `bash repro/VT-005/run.sh <repo>`. Patch: `patches/vast-tools/05-VT-005.patch`.

#### If anyone uses diff --paired

- **VT-003**: Column order overrides the named pairing. One eligible event is lost and one is scored without a pair. `R/vastdiff.R:176`. Repro: `bash repro/VT-003/run.sh <repo>`. Patch: `patches/vast-tools/06-VT-003.patch`.

## Verdicts: ExOrthist A/B

_Source: [friends/manuel-irimia-exorthist-vast-tools/referee/exorthist-a-b/VERDICTS.md](friends/manuel-irimia-exorthist-vast-tools/referee/exorthist-a-b/VERDICTS.md)_

## ExOrthist A/B referee verdicts

**12 CONFIRMED; 4 CONFIRMED-MINOR.** All sixteen mechanisms reproduced independently on unpatched 83185dcf04c4bda7c765a6bcf87fb1b48b36f329. “Minor” reflects limited exposure or a helper/cosmetic effect; it does not mean the output is correct. The suspected list was excluded.

Each linked note supplies the minimal inputs, independently computed correct answer, actual output, cited source lines, normal-use assessment and known/fixed status. Methods and rerun commands. The final runs used a separate pristine pinned clone for each claim.

| ID | Verdict | My repro path | Effect on users' results |
|---|---|---|---|
| A0-01 | CONFIRMED-MINOR | repro/A0-01 | Prints 2026-06-11 on November 6; cosmetic run-date error. |
| A1-01 | CONFIRMED | repro/A1-01 | CDS-only input loses all six exon rows; exons-first input attaches oak's protein to elm and loses oak's three rows. |
| A1-02 | CONFIRMED | repro/A1-02 | Exon endpoints include a residue from the next exon: observed 22 instead of 21, and 11 instead of 10, on ordinary CDS input. |
| A1-03 | CONFIRMED | repro/A1-03 | Transcript-first GTF writes transcripts into gene slots, preventing matching under the real gene IDs used in clusters. |
| A1-04 | CONFIRMED | repro/A1-04 | Twelve lowercase known CDS bases become four X residues rather than MAAA. |
| A1-05 | CONFIRMED | repro/A1-05 | Ascending negative-strand CDS rows produce the wrong protein and reversed coding-exon numbering. |
| A1-07 | CONFIRMED-MINOR | repro/A1-07 | Shared protein IDs concatenate CDSs: 30 aa/three exons become 60 aa/six exons; claimed RefSeq prevalence unsubstantiated. |
| A3-01 | CONFIRMED | repro/A3-01 | Species-sorted rows split 1000 of 1001 families at the documented 1000-alignment batch size; B1 requires both species in one chunk. |
| B1-01 | CONFIRMED | repro/B1-01 | Short protein IDs erase four known directional intron matches; real B5 reports all four as NO_INTRON. † |
| B1-02 | CONFIRMED | repro/B1-02 | Reused gene IDs collapse two families into one and score all four cross-species pairs rather than the two specified pairs. † |
| B2-01 | CONFIRMED | repro/B2-01 | Table splitting changes CID 007300 to 7300 and null to NA, corrupting identifiers forwarded to realignment. |
| B4-01 | CONFIRMED | repro/B4-01 | CIDEA and PCID2 disappear from all three merged feature tables; four eligible rows become two. |
| R5-01 | CONFIRMED-MINOR | repro/R5-01 | Shared six-character accession prefixes label both alignment rows as one species and leave the other species empty; viewer only. ‡ |
| R6-01 | CONFIRMED-MINOR | repro/R6-01 | ./Fern.gtf or data.v1/Fern.gtf causes an explicit species-name failure before any liftover; plain Fern.gtf succeeds. |
| R6-02 | CONFIRMED | repro/R6-02 | With canonical_ss, adding a normal FASTA description changes one known canonical exon pair to zero pairs. § |
| S1-01 | CONFIRMED | repro/S1-01 | Numeric cluster selection returns empty annotation/overlap/protein data instead of 2/1/1 rows, breaking plot inputs. |

† Real B0/B1 (and B5 for B1-01), with an independently written equal-length pass-through MAFFT stand-in. No real MAFFT/Nextflow run is certified. ‡ Newly hand-built B0-format alignment, as permitted for this claim. § Identity liftOver and small BED6 intersection stand-ins; genomic remapping is not certified. R6-01's failure occurs before those tools. All other rows use real scripts directly without stand-ins. Python checks used pandas 1.5.3 (repository container: 1.5.2).

**Known/fixed:** no exact matching public report or later fix found in 42 issue/PR records, 102 comments, recent and relevant historical commits, the other branch, or current release. Current master and release v2.0.0 are the pinned version; the other branch has the same files. A1-02 has related 2021 phase-handling history, explicitly discussed in its note. No exact-name CRAN/PyPI/Bioconda distribution was found (404 responses). Sources and limits. Absence in this search does not establish private awareness or scientific novelty.

The five author candidates below are ranked by demonstrated effect on results and normal input reachability, without estimating population prevalence or whether Manuel would care. Ricardo reads them first; nothing has been sent.

1. **A3-01 — entire families lost at chunk boundaries.** The real A2→A3 reproduction at the documented batch size splits 1000 of 1001 one-to-one families; B1's same-chunk condition then excludes those families. Input ordering is not restricted in the README.
2. **A1-03 — real gene identities replaced by transcript IDs.** A routine GTF writer emits this attribute order; A0 accepts it. B1's gene-cluster lookup consequently cannot select these proteins under their real genes. This downstream consequence follows from B1 source; no full pipeline run was claimed.
3. **A1-01 — annotation loss from row-order dependence.** Correct gene attributes on CDS rows are ignored in Part 2; exons-first input demonstrably loses oak, and CDS-only input loses both genes' exon rows. No interleaving requirement is documented.
4. **A1-05 — wrong negative-strand protein on ascending rows.** This changes the sequence and exon numbering, not just metadata. The equal-length wrong output demonstrates that normal length checks would miss it.
5. **A1-02 — ordinary exon coordinates include a neighboring residue.** Direct nucleotide arithmetic proves it, and the downstream residue assignment/extraction uses those coordinates. The hunter's genome-wide percentages and final-score deltas were not independently recomputed and are not endorsed.

**NEW: no** under the lane's scientific definition. This ships an independent bug-referee conclusion, not a novel scientific result, a published-number improvement, or a new-data prediction test. No predictive-model performance claim is made; SBS is not applicable. No hunter patch was applied or certified. No public actions or contacts occurred.

## Verdicts: ExOrthist C/D

_Source: [friends/manuel-irimia-exorthist-vast-tools/referee/exorthist-c-d/VERDICTS.md](friends/manuel-irimia-exorthist-vast-tools/referee/exorthist-c-d/VERDICTS.md)_

## Independent referee verdicts: ExOrthist B01–B17

16 claims survive: **11 CONFIRMED**, **5 CONFIRMED-MINOR**. **B12 is INTENDED** as a variant-selection policy, with a separate zero-regulated-input crash reproduced and distinguished below. No claim is classified KNOWN; no matching public report was found. This is a software referee result, **NEW: no** under the friends lane's scientific-result definition.

Every row was checked against its own fresh clone at `83185dcf04c4bda7c765a6bcf87fb1b48b36f329`. referee.py constructs independent inputs and runs only unpatched source; each case contains a hand-derived `expected.txt`, cited source lines in `source.txt`, commands, return codes, stdout and stderr. No hunter reproduction, expected-output file, script, or patch was loaded. The hunter's BUGS.md was used only to identify the claims.

| ID | Verdict | Independent repro | Effect on real ExOrthist outputs |
|---|---|---|---|
| B01 | CONFIRMED-MINOR | repro/B01 | C3→C4→C5 keeps 3 pairs instead of 2: nested exons at 980–1120 and 1010–1070 receive different overlap IDs; redundant variants survive in `-NoOverlap.tab` at coordinate digit boundaries. |
| B02 | CONFIRMED | repro/B02 | The module's literal `-sp1/-sp2` command exits 2; the same inputs with `-s1/-s2` succeed. Optional `--orthopairs` exon reclustering cannot complete once its gene input is available. |
| B03 | CONFIRMED | repro/B03 | Six genes in three disjoint pairs become only two genes in one component: `header=0` discards the first orthopair and first cluster-file gene; documented headerless reclustering silently loses records. |
| B04 | CONFIRMED | repro/B04 | Two pairs absent from exon clusters share fabricated `Family.01nan`; a D2-discarded exon also reproduces this. Latent reclustered-output corruption behind B02/B16. |
| B05 | CONFIRMED | repro/B05 | D1-generated input with genuine reverse edges makes unpatched D2 stop with `the condition has length > 1`; a qualifying gene OG aborts its clustering process/chunk. |
| B06 | CONFIRMED | repro/B06 | A returned four-exon cluster reports total 3; the hub's membership is 1.12 instead of 0.90. Reintroduced exons inflate membership scores in final cluster tables. |
| B07 | CONFIRMED | repro/B07 | Explicit zero sequence/length cutoffs drop a pair that passes independently calculated zero thresholds; tiny positive cutoffs retain it. User-specified filters are silently replaced by defaults. |
| B08 | CONFIRMED | repro/B08 | Two 90-nt exons pass on `contig7` but fail on `contig-7`, with numeric warnings. Legal hyphens in sequence names can remove valid exon matches. |
| B09 | CONFIRMED | repro/B09 | A 6:1 OG is omitted from both ≥3/≥4 categories; a 3:4 OG yields `Other OGs = -1 (-100%)`. The documented descriptive OG statistics are wrong. |
| B10 | CONFIRMED-MINOR | repro/B10 | A three-exon plus-strand transcript is plotted in order 2,3,1, with incorrect downstream phases; affects plot coordinates/phase labels at digit boundaries, not inferred main-pipeline clusters. |
| B11 | CONFIRMED | repro/B11 | Requesting `-min_dPSI 40` still announces 15 and calls both dPSI 24 and 65 regulated, instead of only 65; requested regulated sets and resulting conservation statistics are wrong. |
| B12 | INTENDED | repro/B12 | Default variant filtering is explicit in source/help, and the code retains the first row; the retained call therefore depends on order. The resulting empty regulated set crashes, as does a one-row nonregulated control. |
| B13 | CONFIRMED | repro/B13 | An unrelated species C exon at an identical coordinate overwrites the A/B pair's suffix `.003` with `.009`; latent wrong/merged exon-cluster labels behind B02/B16. |
| B14 | CONFIRMED-MINOR | repro/B14 | Changing one gene ID from `oak` to `oak#extra` makes D2's input parser abort; unusual IDs can kill a chunk. The tested embedded-apostrophe variant succeeds, so the quote claim is not generalized. |
| B15 | CONFIRMED-MINOR | repro/B15 | Seeds 1 and 2 swap `.01/.02` for the same two correct components; labels differ across fresh runs, but biological membership is unchanged. No demonstrated Nextflow `-resume` failure. |
| B16 | CONFIRMED | repro/B16 | The documented headerless 3-column gene file raises `ParserError`; 4 columns run and 5 columns raise `KeyError`. Optional gene reclustering fails on the documented format. |
| B17 | CONFIRMED-MINOR | repro/B17 | A valid OG identifier `0` makes the stats helper ignore all its genes and divide by zero; renaming only that identifier restores the correct one-OG summary. |

### Ranked author shortlist

1. **B16 — documented gene-cluster format breaks optional reclustering.** A three-column file is the README's normal input. This is an upstream blocker to the advertised `--orthopairs` workflow.
2. **B02 — exon-reclustering module supplies invalid arguments.** An independent blocker even when D3.1 has compatible input. B16 and B02 both need correction for the advertised optional workflow to finish; the latent B03/B04/B13 defects should be kept alongside that repair.
3. **B05 — ordinary D1-produced graphs can abort core clustering.** This affects the default clustering path and stops the whole process handling that part, rather than merely one OG. Its prevalence in real annotations is unmeasured.
4. **B11 — requested regulation threshold is ignored.** This silently changes the scientific comparison whenever a nondefault dPSI threshold is requested through the documented analysis helper.
5. **B06 — core output reports wrong cluster sizes and inflated scores.** A five-node, seven-edge input gives four final exons but total 3 and membership 1.12 versus 0.90. This affects the documented membership definition without involving the optional reclustering path.

### Reachability and independent arithmetic

- **B01:** README algorithm C (lines 394–404) calls for collapse to one representative of overlapping exon variants. `modules/local/exorthist/collapse_matches.nf:15–17` wires C3 straight into C4 then C5, with no numeric sort. The valid reproduction is `runs/count-2`, `overlap-2`, `collapse-2`. The earlier exploratory C5 run omitted the header and is not used for the verdict. Interval intersection requires one oak overlap group; 980–1120 has two hits versus one, so the two distinct target genes require exactly two representative pairs.
- **B02/B03/B16:** README lines 176–188 and 258–267 document headerless gene groups (3 columns) and orthopairs (2 columns). `params.yaml` defaults `orthopairs` to null; both modules run when a file is supplied. B03 deliberately uses four group columns to isolate header loss from B16, then headers one input at a time: only the corresponding first-record loss disappears. B16's headerless three-column run matches the actual documented convention. The 5-column failure is additional compatibility evidence, not the basis of the documented-input verdict.
- **B04/B13/B15:** `subworkflows/local/exorthist/cluster.nf:36–48` supplies D3.2 with the full best-hit pair table and the filtered exon-cluster table. D2 explicitly removes some exons as unclustered, so a missing coordinate lookup is reachable. B04 `runs/pipeline-derived` uses B06's actual D2 output: discarded node08 and retained node06 both acquire `Family.01nan`. Coordinate strings contain no species namespace: identical coordinates in different genomes are not identical exons. For B13 the input explicitly assigns oak/elm to `Family.003`; adding an unrelated species C entry must not relabel that pair. B15's disjoint edges fix the two memberships independently; only the arbitrary suffix assignment changes. These scripts are tested directly using their defined flags, without claiming that the currently broken optional pipeline completes.
- **B05/B06:** `modules/local/exorthist/format_input.nf` calls D1 and `cluster_exons.nf:12` calls D2; `orthogroupnum` defaults to 500. Inputs start as gene groups and exon pairs, and **unpatched D1 computes all reciprocal flags**. Every TRUE edge has its reverse, and every node is a different gene/species, so no same-species match is required. README lines 408–420 define the membership score. In B06 the four-member hub has in-degree 3, out-degree 3, and 3 reciprocal neighbors: numerator 9. There are 5 original genes, 1 same-species gene and 1 same-species exon, so the denominator is `2*(4-1)+(5-1)=10`; the correct score is 0.90. D2 uses stale total 3, denominator 8, and prints 1.12. B05's final eight-node, 21-edge witness gives initial communities of sizes 6,1,1. node07 first moves to singleton node09; the next stale singleton entry then contains both exons and crashes (see `independent-partition.txt` and `runs/D2-4`). B06's final outputs are in `runs/D2-2`. A graph-only B05 shrinking heuristic failed to preserve the actual error; it was reverted before using direct D2 execution to shrink the witness. No ExOrthist code was patched.
- **B07/B08:** README lines 200–203 documents configurable similarity and a length ratio in [0,1]; `filter_matches.nf:39–41` passes them directly to C2. The default nonzero distance parameters avoid B07. `nextflow_schema.json:100–113` accepts these parameters as strings and imposes no pattern excluding zero. A 120:40 exon-length pair has ratio 1/3, so it passes a zero minimum. Sequence score 0.001 passes a zero minimum but fails the substituted defaults (0.04 for the exon and 0.03 for its neighbors). B08's exon lengths are both `389-300+1 = 789-700+1 = 90`; changing the scaffold name cannot change that ratio. No blanket assertion that every hyphenated-coordinate pair is dropped is supported.
- **B09/B17:** These are a documented standalone helper (README lines 427–456), not a Nextflow process. The helper accepts `-main_output` and optional explicit gene/exon files. Fixtures contain the annotation-overlap catalog and exon clusters, so counts are ordinary pipeline-shaped inputs. B09's category answers follow directly from integer comparisons of constructed species counts; the negative Other count is invalid regardless of how the category labels are interpreted. README imposes no nonzero restriction on ClusterID, so B17 is a valid but unusual custom identifier case.
- **B10:** `modules/local/exorthist/plot/generate_fake.nf:17–24` calls the script in the documented plot workflow. One GTF transcript explicitly numbers the CDSs 1,2,3 at starts 970,1120,1320 and gives phases 0,1,2. The independently expected table is `expected.tsv`: fake starts 0,30,60 and downstream phases 1,2,last. Output instead places the first exon last and gives it `DownPhase=last`.
- **B11/B12:** `compare_exon_sets.pl` is the documented standalone module (README lines 541–547), rather than a Nextflow process. Its help explicitly documents `-min_dPSI` and `-allow_overlap`. B12's comment says to avoid counting exon variants, and the help says overlapping entries are filtered by default; it supplies no maximum-dPSI representative rule. `-allow_overlap` retains the regulated variant in the tested single-list case. Thus the hunter's selection-policy patch is not justified as a correctness fix. The unguarded zero-regulated denominator is a real, separate defect: the single low-dPSI-row control crashes at line 1176 without variant ambiguity. The LIST1b source also omits the overlap bypass, but the verdict does not claim an independently reproduced two-list failure.
- **B14:** D2 reads D1's tabular IDs with default R comment syntax. `#` has no documented prohibition for gene IDs, and `A0_check_input.pl` checks their presence in the GTF rather than excluding this character. Prior stages also use identifier delimiters, so this is not evidence that every unusual-ID dataset reaches D2 unchanged. The confirmed defect is the hash parser failure; the apostrophe-only control did not fail.

### Upstream check and limits

Checked on **2026-11-06** using `gh api`: all **42 issue/PR entries**, open and closed, **102 issue comments**, and the pull-review-comment endpoint (**0 entries**). Raw responses are in upstream. No matching report for these 17 claims was found. Issue [17](https://github.com/biocorecrg/ExOrthist/issues/17) concerns an older igraph/undefined-object failure, not B05/B06; issues [31](https://github.com/biocorecrg/ExOrthist/issues/31), [33](https://github.com/biocorecrg/ExOrthist/issues/33) and [36](https://github.com/biocorecrg/ExOrthist/issues/36) discuss species naming or earlier alignment problems, not the reproduced coordinate/gene parser defects. This is a bounded public-history check, not a guarantee nobody knows privately.

The API reports master at `83185dcf04c4bda7c765a6bcf87fb1b48b36f329` and v2.0 at `09c26df9235d139cc298f2f3250cb298b5512654`. **Both have identical root tree `799cdc0a7a878e297e7e19c71bd9a0ac06c79177`**, so none of the cited source has been fixed on either branch. branch-check.txt lists the per-claim blob comparisons. The README, modules and defaults are identical too.

Runtime: supplied Python 3.11 with pandas 1.5.3; supplied R 4.5.3 with igraph 2.3.4 and hashmap; system Perl. Repository configuration uses pandas 1.5.2 and its R image Dockerfile starts from R 4.4.2 with unpinned igraph. The R community witnesses are confirmed in the provided runtime; community partitioning can depend on igraph version/ties. No container or full-genome pipeline was run, and no prevalence estimate is inferred from these small examples. Runs used nice 10 and one numerical thread; no source modifications, public writes, or contacts were made. No predictive performance claim is made, so the predictive-baseline/SBS rule is inapplicable.

Reproduce a case with `python3 referee.py B01` (or any B01–B17); reruns get new directories. Clones B02–B17 are fresh local shared clones from the initial fresh public clone, checked out at the full pinned revision with sparse working trees; their source is unmodified. Inputs are independently authored; current file arguments are copied beside their runs, while directory-based fixtures remain under their case folders. Graph-search and shrinking scripts are included to explain how the independent R witnesses were obtained. The hunter's suspected list is outside the requested B01–B17 adjudication.

## Verdicts: vast-tools

_Source: [friends/manuel-irimia-exorthist-vast-tools/referee/vast-tools/VERDICTS.md](friends/manuel-irimia-exorthist-vast-tools/referee/vast-tools/VERDICTS.md)_

## Independent VAST-TOOLS referee verdicts

Pinned commit: `5598e1f1b0067611dc9e5abb285b4eacaf543ee3` (VERSION `2.5.1`). Checked 2026-11-06.

| ID | Verdict | My repro path | Effect on users |
| --- | --- | --- | --- |
| VT-001 | **CONFIRMED** | repro/VT-001/ | A positive count accompanying rounded cRPKM `0.00` becomes zero in all three count exports; independently supplied count 5 became 0. |
| VT-002 | **CONFIRMED** | repro/VT-002/ | Renaming the same two samples changes merged MIC PSI/counts from missing to numeric: `NA` versus PSI 75 and counts 4/12. |
| VT-003 | **CONFIRMED** | repro/VT-003/ | Column order overrides requested biological pairing, suppressing an eligible event and scoring an event with no eligible named pair. |
| VT-004 | **CONFIRMED** | repro/VT-004/ | A one-event processing chunk aborts `diff`; a final singleton leaves an incomplete result table. |
| VT-005 | **CONFIRMED-MINOR** | repro/VT-005/ | Group identifier `0` causes an existing sample to be reported absent; renaming that group avoids the fatal error. |
| VT-006 | **CONFIRMED-MINOR** | repro/VT-006/ | Zero retained events cause a fatal summary division by zero, although the correct header-only result table has already been written. |

Ranked by effect on real users:

1. **VT-003 — incorrect biological pairing.** Silent inclusion/exclusion of differential-splicing results under a documented analysis mode; no unusual labels or data values needed.
2. **VT-001 — raw-count loss.** Silent alteration of exported observed counts. Restricted to positive counts with rounded-zero expression; downstream count analyses may use these exports. The default `compare_expr` expression threshold normally excludes such low-expression rows.
3. **VT-004 — incomplete differential-splicing output.** A normal run can halt after many successfully written events. With default chunks of 5000, source inspection gives the condition `event_count % 5000 == 1`; default singleton and a three-event/two-line-chunk run reproduce it.
4. **VT-002 — order-dependent microexon missingness.** Incorrect numerical estimates can enter subsequent PSI/quality calculations. Mixed missing/numeric contributions require different mappability; the demonstrated strand-protocol mixture is supported but explicitly discouraged. Frequency in users' datasets is unknown.
5. **VT-006 — empty-filter workflow failure.** Small subsets or strict filters can legitimately retain nothing. The fatal exit can interrupt automation, but it does not corrupt the already-written event table. VT-005 is a lower-priority label-specific failure.

### Reproduction and independent answers

Only the hunter's `BUGS.md` was read. No hunter repro scripts, output artifacts, or patches were opened, executed, imported, or copied. Fixtures and calculations were independently authored from upstream source/formats. Each bug has its own fresh remote clone at the pin; all six tracked source trees remain unchanged. run_referee.py creates the minimal cases; reachability.py exercises public commands and produces MIC inputs with the actual upstream analyzer. Every command saves its arguments, working directory, exit status, stdout, and stderr beside its input. Numerical answers are in each bug's `independent-answer.json`.

**VT-001.** `MakeTableRPKMs.pl:79–87,107–114` initializes counts to zero and only copies them for nonzero expression. In my input, LOW has cRPKM `0.00`, count 5; HIGH has `10.00`, count 200, and ZERO has `0.00`, count 0. Unpatched outputs are 0/200/0 instead of the correct 5/200/0. All three exports fail; the documented public `combine --exprONLY --C --TPM` route also exits 0 with the wrong counts. The correct raw count is the observed integer, independent of expression rounding. Independently, `5 * 10^9 / (100000 * 20000000) = 0.0025`, which rounds to `0.00`; upstream `expr_RPKM.pl:143` uses this two-decimal format. Count 200 and genuine zero remain correct. Reachability: [README expression/count instructions](https://github.com/vastgroup/vast-tools/blob/5598e1f1b0067611dc9e5abb285b4eacaf543ee3/README.md#L543-L549), `RunDBS_2.pl:210–214,481`. This is not an intentional expression filter: the input explicitly contains a raw count and no count-filtering option was requested.

**VT-002.** `MergeOutputs.pl:451–452` adds numeric values to an accumulator even when it already contains `NA`. My all-missing plus 4-exclusion/12-inclusion example yields numeric PSI `100*12/(4+12)=75` only when the missing file sorts first. Reversing sample names yields all `NA`. The numeric-only control correctly gives 8/24 and PSI 75. The producer case independently constructs mappability files and runs unmodified `Analyze_MIC.pl`: strand-unspecific zero effective lengths emit all missing values, while strand-specific effective lengths 35 with 12 inclusion/4 exclusion reads emit the numeric row, both at read length 50. Merging these actual producer outputs reproduces the name-order dependence. A Perl numeric-coercion warning is emitted, but merge exits 0. Unknown contributions cannot establish the complete pooled counts; if the intended policy were instead to discard unmappable contributions, it must still be invariant to names. The existing last-NA and MULTI behavior favors preserving missingness. Reachability: [README strand-specific merging](https://github.com/vastgroup/vast-tools/blob/5598e1f1b0067611dc9e5abb285b4eacaf543ee3/README.md#L369-L372) permits the mixed protocol but warns against it; `Analyze_MIC.pl:123` emits missing counts and `Add_to_MIC.pl:49–96` carries the merged values into PSI/quality output. No real-sample frequency or downstream biological false-positive rate is claimed.

**VT-003.** `R/vastdiff.R:176–177` indexes each requested set in table order. Requested pairs are preX/postX and preY/postY; the permuted table lists preX, preY, postY, postX. Event 1 has 45/5 reads in preX and 5/45 in postX, and zero coverage in both Y samples: exactly one eligible named pair. Event 2 has the same preX counts, but coverage only in postY: zero eligible named pairs. The permuted unpatched run reports event 1 all NA and event 2 dPsi `0.779547`, MV `0.65`. Reordering only the table columns restores event 1 and removes event 2, with the same numerical result for the eligible event. Both runs exit 0. Independent named-pair counting establishes the decisive wrongness without simulation. A separate base-R oracle, using only beta quantiles and numerical integration, gives marginal medians `0.8895478374` and `0.1104521626`, their difference `0.7790956747`, and 0.01-grid MV `0.65` at probability 0.95. The small median discrepancy is expected with default Monte Carlo size 1000. Reachability: [README paired analysis](https://github.com/vastgroup/vast-tools/blob/5598e1f1b0067611dc9e5abb285b4eacaf543ee3/README.md#L480-L485) and the current help at `vastdiff.R:57–58` explicitly associate the pairs by argument order. Both table orders are accepted by the actual input checker; the public wrapper reproduces the failure.

**VT-004.** `R/vastdiff.R:226–235` simplifies singleton results, then indexes them in two dimensions. One event with 30/10 reads versus 10/30 should produce one completed event: both samples have 40 reads, above the default minimum of 10; posterior means are independently 31/42 and 11/42. Instead it exits 1 at line 234: `totalFirst[, x]: incorrect number of dimensions`, leaving only the header. Three such events with `-n 2` also exit 1, leaving two results. Two-event and default-chunk three-event controls exit 0 with all events. The public one-event command also fails with default PDF output enabled. Reachability: `--nLines` is documented in help (`vastdiff.R:97–99`) and defaults to 5000; no documented minimum event count excludes a singleton. This is a crash, not statistical rejection. The modulo-5000 condition is inferred from the chunk loop; a 5001-event run was not executed.

**VT-005.** `Filter_and_clean_Combine.pl:221` tests the group string for truth. My config assigns sick to `0` and well to `1`; both names are present. The command exits 255 with `Sample (sick) from 0 not found`. Renaming the identifiers to control/treated succeeds, retaining the expected PSI 20/80 event. Independently, its sample SD is `42.4264068712`, above default 5, and each group has the requested one covered sample. Reachability: [README groups config](https://github.com/vastgroup/vast-tools/blob/5598e1f1b0067611dc9e5abb285b4eacaf543ee3/README.md#L592-L601) and help at `Filter_and_clean_Combine.pl:120–125` specify a group identifier with no prohibition on numeric labels. The error is real but obvious and avoidable by renaming, hence minor.

**VT-006.** `Filter_and_clean_Combine.pl:520` divides by retained-event count after closing the result table. My two covered PSI 40/40 samples have independently computed SD 0, below default minimum 5; exactly zero events should survive. Unpatched `tidy --min_N 2` writes the correct header-only table, prints a zero-event total, then exits 255 with `Illegal division by zero`. The 20/80 control succeeds and retains one event. Reachability: [README's documented filtering](https://github.com/vastgroup/vast-tools/blob/5598e1f1b0067611dc9e5abb285b4eacaf543ee3/README.md#L590-L592) allows ordinary empty selections. A missing-event percentage is undefined on zero events; the selected event set is already correct, so this is a minor completion/reporting defect.

### Already reported or fixed?

Independent read-only GitHub API checks used `gh api`: all 134 issue/PR entries (8 open), all 345 issue comments, 1328 master-history commit records, the recent-commit query since 2026-08-06, all 15 branch heads, and releases/tags. Raw responses are in upstream-context/. Matching source excerpts by branch/release are in branch-source-review.json.

No matching public report or branch fix was found for any of these six specific failures. This is a bounded search result, not proof that the authors have never encountered them. Current master is still the pin; its only commit in the last three months adds Osa mappings. The current GitHub release is v2.5.1 (2020-06-26), tag commit `498bbecb2fcef3e98beb9d6a6cc7648a529453e5`, distinct from the pin despite the identical VERSION. The relevant vulnerable constructs also appear in that tag where the feature exists; standalone count/TPM exports were added later. Branch/tag review was source inspection, not execution of those versions.

Per-claim distinctions from nearby upstream work:

- VT-001: [#92](https://github.com/vastgroup/vast-tools/issues/92) explains generating counts with `-C`; it does not report rounded-zero count loss. No corresponding rounding/count-copy fix was found.
- VT-002: [#68](https://github.com/vastgroup/vast-tools/issues/68) concerns grouping/configuration, and [#87](https://github.com/vastgroup/vast-tools/issues/87) concerns incomplete align output and EEJ memory/format problems. Neither describes name-order-dependent MIC missingness. The accumulator's old “check with Manu” comment signals unresolved policy, not a fix for order dependence.
- VT-003: [#117](https://github.com/vastgroup/vast-tools/pull/117) and commit `6efb39c` fix other paired-mode problems; the `which` indexing survives unchanged. [#32](https://github.com/vastgroup/vast-tools/issues/32) fixed output-column reordering in `Add_to_FULL.pl`, a different module. No matching biological-pair order report was found.
- VT-004: [#48](https://github.com/vastgroup/vast-tools/issues/48), [#54](https://github.com/vastgroup/vast-tools/issues/54), and [#60](https://github.com/vastgroup/vast-tools/issues/60) describe missing-replicate list indexing or plotting failures, not singleton chunk dimensions. No singleton fix was found.
- VT-005: no matching numeric-zero group-label issue or existence-test fix was found; the truth test persists in every reviewed branch containing grouped tidy.
- VT-006: commit `bf7422ddd` (2021-04-01) suppresses undefined per-type tally warnings in tidy, but does not guard the zero denominator. No matching empty-result fatal-error report or fix was found.

Distribution check: no corresponding VAST-TOOLS Bioconda package/recipe was found (direct package/recipe lookups returned 404; recipe code searches found only hg19/hg38 annotation packages mentioning the tool; Anaconda name search returned unrelated packages). This command-line Perl/R repository is not itself a CRAN or PyPI package; similarly named Python astronomy tools are unrelated. The GitHub release and current source are therefore the relevant releases checked here.

**Did this referee job find a new research result? No.** It independently confirms six software defects claimed by the hunter; no printed scientific benchmark, stated paper problem, or new-data prediction was tested. No author contact, issue, PR, fork, or patch publication occurred. Predictive-score baselines/SBS are not applicable to these deterministic correctness cases and posterior calculations.

---

# Manuel Irimia — M011, the ExOrthist membership score

Folder: [friends/manuel-irimia-exorthist-vast-tools/m011-membership-score](friends/manuel-irimia-exorthist-vast-tools/m011-membership-score)

## Claim

_Source: [friends/manuel-irimia-exorthist-vast-tools/m011-membership-score/CLAIM.md](friends/manuel-irimia-exorthist-vast-tools/m011-membership-score/CLAIM.md)_

## M011 — ExOrthist species-count membership-score witness and repair

SUBMITTED FOR INDEPENDENT REFEREE; NOT PASSED. Public-data software consistency, not an orthology-accuracy or biological-discovery claim. No author contact authorized or made.

Primary identity: Marquez et al. (including Manuel Irimia), ExOrthist: a tool to infer exon orthologies at any evolutionary distance, Genome Biology2021, DOI10.1186/s13059-021-02441-9, PMC8379844. Paper Methods “Inference of exon orthogroups” prints the membership-score formula. Official released v2.0.0 nf-test snapshot tests EX_clusters.tab MD5 **02479360ed2b8d659612fc60477ad355**. The native whole pipeline reproduces that hash byte-for-byte on the official37-gene-orthogroup human/mouse/cow dataset. The paper’s genome-wide>97% agreement number is not reproduced or improved here.

Precise result: unmodified release output reports MS **0.86** for GF_002754|ENSG00000160218|chr21:44098357-44098534:+|hg38, while the documented graph formula gives exactly **1**. The exon has OUT2, IN2 and reciprocal-neighbor count2; its cluster contains4exons,2human exons,4total genes,2human genes. Thus numerator6, denominator2*(4-2)+(4-2)=6. Original and edge-observed gene universes coincide in this witness. The source erroneously selects only the current exon when building the same-species gene count: it replaces the first pipe in the complete ID instead of extracting the final species field. Replacing only the two selector expressions with species-suffix extraction gives MS1.

Full official-test correction changes **18/1108 scores**, and all377 exon clusters, all integer graph fields, all non-score formatted-table fields and1090 single-gene negative-control scores stay unchanged. The unchanged independent verifier passes all1108 corrected scores. Original output disagrees with exact fractions beyond two-decimal rounding on18rows. Unmodified final formatter reconstitutes the official golden table exactly; corrected table SHA256 **5bc3a8a7494e9592a468e06d61c1a45ec816be7d9b565222ca586d456e8595c7**. A reduced4vertex/8directed-edge actual-data witness freshly reproduces the discrepancy and corrected exact arithmetic. All32 prespecified edge-row shuffles return the original canonical partition with no unclustered exons; this is a bounded negative order-sensitivity result.

Private working copy, not in this repository. Canonical target: exorthist_consistency/. Original R, two-line corrected R, change manifest, golden output, actual edge input, gene membership, pre-diagnostic seal, full rational certificate, all changed rows, final-table controls, minimal witness and source provenance are in results/. Independent verifier: verify_membership.py, frozen copy results/verify_membership_frozen_v1.py. Reproduction entry: reproduce_score.sh; exact commands and limits: REPORT.md. Ordering128files retained in results/permutations_all32.tar.gz with byte-verified receipt. Original pre-diagnostic seal/input were pulled to exorthist_pre_diagnostic/ BEFORE outcomes. Original-source SHA2567cd4ce06659f7b56b295e5ebd0fc98896caaf8ffa64b285bb8615c9d1b48e6d9; corrected SHA256005b1eefd0c7f041b03f9806dd22e571111f205022d36ef5439752c4245bc513.

Verification independence: stdlib CSV/directed-multigraph reconstruction and Fraction arithmetic, no imports from original R or search. Written before diagnostics; original verifier is preserved and reused unchanged on the corrected output. Every degree/species/reciprocal integer checked exactly, each score within half a two-decimal last digit. Full original pipeline runs first and matches author golden hash, followed by native unmodified-D2 replay and minimal actual-data replay. No fabricated sequences or model fitting.

Controls/concerns: native R4.1.3/igraph1.4.3/hashmap0.2.2 differs from DockerR4.4.2/paperigraph1.2.6, but entire golden table matches. MAFFT7.429 used legacy-fcommon linkage, with no algorithm change. Thirty other test exons expose a separate original-gene versus edge-observed-gene denominator ambiguity; not resolved or included as a claimed repair. Current master/v2.0 match tested source, v1.0.2 also has the selector, so do not call this a v2 regression or claim historical biological results wrong. No labelled truth accuracy, genome-wide prevalence, alternative-runtime generality or downstream biological effect measured. The2026 splicing preprint uses a<=0.15 reclustering trigger; its impact is only a queued distinct target needing exact version and full original graph.

Prior art rechecked2026-11-02: latest release remainsv2.0.0; all-state issue/PR records, focused score/D2 searches, current branches and six AI-result README indexes have no matching fix/report in the bounded inspected material. Source JSON/primary paper are retained; see PRIOR_ART.md. No global novelty claim. Please assess the precise witness, repair and usefulness independently; any broader scope must be a NEXT BAR, not silently added to this claim.

Dated addendum2026-11-02: the separately disclosed30-row gene-universe question has now been investigated under M021. Primary wording is explicit and the missing-edge genes are valid CDS-annotated input; M021 supplies a separate repair and combined full-pipeline certificate. This does not expand or change M011's18-row species-selector claim. See sibling manuel_M021/CLAIM.md and exorthist_gene_universe/REPORT.md.

Closing source recheck2026-11-02 04:35UTC: primary versions/current official sources, repository/issue/PR searches and six prescribed AI indexes checked again; no matching newer repair/reanalysis identified in bounded inspected sources. PLOS raw workbook remains byte-identical, ZGAv2confirmed latest by publisher API, ExOrthist release/master unchanged and four public forks retain original score expressions. Audit and source receipts: portfolio closing_evidence/closing_sources/CLOSING_AUDIT.json and final backup. No independent verdict is supplied by this agent.

M020source-gate closure: exact historical inputs/version were not recovered; it is killed without downstream-impact counts. This adds no biological inference to either release-test claim.

## Verdict

_Source: [friends/manuel-irimia-exorthist-vast-tools/m011-membership-score/VERDICT.md](friends/manuel-irimia-exorthist-vast-tools/m011-membership-score/VERDICT.md)_

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

## Prior Art

_Source: [friends/manuel-irimia-exorthist-vast-tools/m011-membership-score/PRIOR_ART.md](friends/manuel-irimia-exorthist-vast-tools/m011-membership-score/PRIOR_ART.md)_

## Independent M011 prior-art audit (opened 2026-11-02)

Baseline identified before writing referee code: the public ExOrthist v2.0.0 release and its official nf-test snapshot, not a leaderboard. Claim says EX_clusters.tab MD5 02479360ed2b8d659612fc60477ad355. This is a software consistency audit, not a contest or accuracy improvement.

Initial public search: “ExOrthist membership score gene species Irimia 2021”, “ExOrthist github membership score bug D2 2026”, “ExOrthist arxiv 2025 2026”. Found primary paper https://pmc.ncbi.nlm.nih.gov/articles/PMC8379844/ and official code https://github.com/biocorecrg/ExOrthist; no matching correction surfaced. Paper search also found later Mantica/Irimia work, not a replacement score-consistency result. Primary formula and author identity still require direct inspection.

Prior agent's PRIOR_ART.md and REPORT.md read as allegations only. Their searches, golden reproduction and independence are not accepted on trust. Independent checks pending: current raw source, release/test snapshot, all-state issues/PRs/forks, recently updated repository search, prescribed AI result indexes, arXiv/recent references and public community search. No global novelty claim will be made.

Baseline reproduction will use public source and public official test artifacts, with claim-derived graph/output data as comparison only. All numerical compute will run on the authorized shared ref pod under /workspace/ref_manuel_M011 (8 cores, 16 GB), never locally. No model or biological-accuracy optimization is planned.

### Independent checks completed before final pipeline run

Publisher https://link.springer.com/article/10.1186/s13059-021-02441-9 lists Manuel Irimia among authors and gives the exact Methods formula; the >97% comparison is between recovered exons from ExOrthist and liftOver, not a membership-score accuracy number. Fresh Europe PMC XML fetched on pod (SHA256 269f249cebb5707baa7e35ae2f60983908b0965336759c726546228dd4c61a9b).

Live official release API: v2.0.0, 2024-12-05. Fresh released archive SHA256 5fb661adb0927b2645654beacb046f107a366828d93b0d66fbf495a7ed04fb85. Its nf-test snapshot names MD5 02479360ed2b8d659612fc60477ad355. Independent native D2 and formatter replay reproduces this hash and corrected SHA256 5bc3a8a7494e9592a468e06d61c1a45ec816be7d9b565222ca586d456e8595c7; original sequence-to-graph pipeline is still running.

GitHub API search sorted by updated, with forks included, returns official repository plus four public forks. Fresh master and v2.0 branch have D2 SHA256 7cd4ce06659f7b56b295e5ebd0fc98896caaf8ffa64b285bb8615c9d1b48e6d9. All four fork tips and historical v1.0.2 selector retain the same mistake. All 41 issue/PR records and 7 PRs read, zero open PRs. Comment endpoint needed two pages (pagination headers saved); relevant comments and closest graph/runtime issues inspected separately. No matching membership/species-count repair found. Initial pod API calls hit public rate limits; subsequent anonymous public GETs from local machine succeeded. No credentials used.

Fresh README indexes: BakeLab/Epi-results; google-deepmind/alphaevolve_results; google-deepmind/alphaevolve_repository_of_problems; openai/math; plasma-ai/erdos; kisonecat/openai-math. No ExOrthist/exon-orthology/membership-score match in these bounded indexes. EinsteinArena exact-term public search uninformative. No accuracy leaderboard applies.

Additional public queries: ExOrthist membership bug/correction; ExOrthist 2026 exon orthology; ExOrthist species score GitHub issues; ExOrthist on arXiv after 2025-11-01; ExOrthist on X/Reddit/Bluesky. Results identify official sources and later applications (including eLife 104275), not a better score-consistency repair. No relevant recent arXiv correction surfaced. This is bounded prior-art screening, not proof of global novelty.

### Closing independent recheck

2026-11-02T12:05:20Z: latest-release API still v2.0.0; 41 all-state issue/PR records unchanged; recently updated repository search still official repository plus four forks. Refetched master D2 and all six AI README indexes are byte-identical to the opening downloads. Both official branches and all four fork selectors were directly inspected. All 102 public issue comments across two pages were screened, including the closest graph/runtime issue #17; no matching membership species-count report found. See evidence/closing_audit.json and evidence/fork_branch_audit.json.

Baseline now independently reproduced from the full official public genome/GTF inputs, with exact golden table and graph hashes. The proposed repair reproduces its claimed corrected table hash. Best defensible statement is a narrow reproducible maintenance correction; no superiority to other orthology methods, record or global novelty is claimed.

---

# Hugo Fernandes — pyglmnet

Folder: [friends/hugo-fernandes-pyglmnet](friends/hugo-fernandes-pyglmnet)

## PR 1: Bernoulli log-likelihood

_Source: [friends/hugo-fernandes-pyglmnet/PR_1_bernoulli.md](friends/hugo-fernandes-pyglmnet/PR_1_bernoulli.md)_

Title: FIX: Bernoulli log likelihood is NaN at probabilities 0 and 1, and overflows for large logits

`_logL` for `binomial` and `probit` computes `y * log(y_hat) + (1 - y) * log(1 - y_hat)`. When a prediction is exactly 0 or 1 this evaluates `0 * log(0)`, so a perfect prediction gives a NaN log likelihood and a NaN deviance from `GLM.score`. The logistic path with `z` uses `log(1 + exp(z))`, which overflows for large positive `z` (`z = 1000` gives `-inf` instead of 0).

This PR uses `scipy.special.xlogy` / `xlog1py`, which treat `0 * log(0)` as 0, and `np.logaddexp(0, z)`, and casts probabilities to float first so integer or boolean inputs are not wrapped by the negation. Interior probabilities and moderate logits give the same values as before. A predicted probability of exactly 1 for an observed 0 still gives `-inf`, as it should.

Test: `test_bernoulli_loglik_endpoints` in `tests/test_metrics.py` fails on master and passes here. The rest of the suite is unchanged (on numpy 1.23, scipy 1.10 and scikit-learn 1.2, `test_glm_estimator`, `test_cv` and `test_intro_example` fail on master too, and `test_group_lasso` fails intermittently on master).

Open PR #390 moves this code into `Binomial` and `Probit` classes with the same expressions, so the same change would apply there.

## PR 2: gamma deviance

_Source: [friends/hugo-fernandes-pyglmnet/PR_2_gamma_deviance.md](friends/hugo-fernandes-pyglmnet/PR_2_gamma_deviance.md)_

Title: FIX: gamma deviance and pseudo-R2 omit the saturated log likelihood

`deviance` and `pseudo_R2` in `metrics.py` take the saturated log likelihood `LS` as 0 for every family except softplus, Poisson and negative binomial. For gamma (shape 1, as in `_logL`) it is `sum(-1 - log(y))`, not 0. So the gamma deviance is negative even for perfect predictions: for `y = [0.1, 0.2, 0.4]` and `yhat = y` it is -3.66 instead of 0, and it changes with the units of `y`.

This PR adds `'gamma'` to the families that use `LS`. The deviance then equals the textbook `2 * sum((y - mu) / mu - log(y / mu))` (it matches statsmodels' `Gamma().deviance`), is 0 for perfect predictions, and does not change when `y` and `mu` are rescaled together. Gamma pseudo-R2 becomes `1 - D / D_null`, the convention the count families already use, so a perfect fit scores 1.

For a fixed data set the added term is a constant, so a deviance-based ranking of lambdas does not change; pseudo-R2 values for gamma do change.

Test: `test_gamma_deviance_saturated` in `tests/test_metrics.py` (deviance and pseudo-R2) fails on master and passes here. The rest of the suite is unchanged (same pre-existing failures on master as noted in the Bernoulli PR).

Open PR #390 keeps the same family list (`Poisson, PoissonSoftplus, NegBinomialSoftplus`), so `GammaSoftplus` would need adding there too.

## PR 3: gamma simulate

_Source: [friends/hugo-fernandes-pyglmnet/PR_3_gamma_simulate.md](friends/hugo-fernandes-pyglmnet/PR_3_gamma_simulate.md)_

Title: FIX: simulate_glm(sample=True) for gamma returns exp(mu) instead of gamma samples

With `distr='gamma'` and `sample=True`, `simulate_glm` returns `np.exp(mu)`: the same value for every seed, with no noise, and the wrong mean. For example, a mean of 1.103 gives 3.014 for every observation.

This PR draws `random_state.gamma(shape=1.0, scale=mu)`, i.e. shape-1 gamma observations with mean `mu`, matching the likelihood used for fitting. With 20,000 draws at that mean, the sample mean is 1.104 and the variance 1.19 (expected about 1.103 and 1.22). The same seed reproduces the same draws. `sample=False` is unchanged.

Test: `test_simulate_gamma_samples` in `tests/test_pyglmnet.py` fails on master and passes here. The rest of the suite is unchanged (same pre-existing failures on master as noted in the Bernoulli PR).

Open PR #390's `GammaSoftplus.simulate` also returns `np.exp(mu)`, so the same change would apply there.

## Review

_Source: [friends/hugo-fernandes-pyglmnet/REVIEW.md](friends/hugo-fernandes-pyglmnet/REVIEW.md)_

PR 1 — VERDICT: FIX FIRST

- `pyglmnet/pyglmnet.py:142,149`: `-y_hat` raises `TypeError` for boolean probabilities and wraps unsigned integers. With `y=[0.]` and `y_hat=np.array([1], dtype=np.uint8)`, both families return **+5.545177** instead of `-inf`. Convert probabilities to floating point before negation and test these dtypes.

PR 2 — VERDICT: FIX FIRST

- `tests/test_metrics.py:64`: The regression covers only deviance, leaving both `pseudo_R2` changes untested. Add assertions for `1 - D/D_null`, perfect-fit score 1, null-model score 0, and scale invariance.
- `out/PR_2_gamma_deviance.md:11`: The class in [PR #390](https://github.com/glm-tools/pyglmnet/pull/390/files) is named `GammaSoftplus`, not `Gamma`.

PR 3 — VERDICT: FIX FIRST

- `tests/test_pyglmnet.py:523`: All assertions also pass with the deterministic replacement `y = np.roll(mu, 1)`; its residual standard deviation is approximately **0.1648**. Add a different-seed check and check variance against `mu**2` using constant means.
- `out/PR_3_gamma_simulate.md:9`: “`Gamma.simulate`” should be “`GammaSoftplus.simulate`” in [PR #390](https://github.com/glm-tools/pyglmnet/pull/390/files).

## Verdicts

_Source: [friends/hugo-fernandes-pyglmnet/referee/VERDICTS.md](friends/hugo-fernandes-pyglmnet/referee/VERDICTS.md)_

## Independent referee verdicts

Scientific NEW: **no**. These are maintenance findings, not a new scientific result. Of 14 claims: **8 CONFIRMED, 3 CONFIRMED-MINOR, 2 KNOWN, 1 INTENDED**. All 14 described behaviors reproduced at the pinned commits; reproduction alone does not establish that a behavior is an unreported bug.

| ID | Verdict | My independent repro | Effect on users / qualification |
| --- | --- | --- | --- |
| S01 | CONFIRMED | S01.py, output | Counts 2,4,6: package loss prefers mean 7 over the correct constant Poisson MLE 4; this loss controls restart selection and stopping. |
| S02 | CONFIRMED | S02.py, output | Default population plot gives SEM 0.0575 instead of 0.16955825 for normalized neuron responses 0.1,0.3,0.6,1; uncertainty bands are too narrow. |
| S03 | CONFIRMED-MINOR | S03.py, output | Zero-response windows yield NaN normalized rows and silently omit neurons; an all-zero population crashes. The claimed corrected mean requires an unspecified zero-normalization policy. |
| S04 | CONFIRMED | S04.py, output | Documented list/array-valued dictionaries crash in conditional rasters and spike counts; equivalent DataFrames give independently verified counts 4,2. |
| S05 | CONFIRMED-MINOR | S05.py, output | Documented row/column center (-2,3) peaks at (7,2), rather than (2,7), in a 9×9 patch; custom off-axis filters transpose, while centered filters are unaffected. |
| S06 | CONFIRMED | S06.py, output | Four recording samples and a seven-sample temporal basis produce seven rows, violating the documented sample count and response alignment. Exact short-signal crop convention is unspecified. |
| S07 | CONFIRMED-MINOR | S07.py, output | Default no-sort reverses all four raster rows, contrary to the documented identity behavior; underlying spike counts are unchanged. |
| S08 | CONFIRMED | S08.py, output | Window [-13,17] ms with 10-ms bins produces four bins but retains metadata for three plot centers; population PSTH plotting crashes. |
| P01 | CONFIRMED | P01.py, output | Fitted binomial/probit models with valid saturated probabilities return NaN deviance instead of zero; large positive logistic logits also overflow the likelihood. |
| P02 | CONFIRMED | P02.py, output | Perfect gamma predictions have deviance -4.80735576 instead of zero; absolute deviance is wrong. A fixed-data deviance ranking is unaffected; changing pseudo-R² convention is not certified. |
| P03 | CONFIRMED | P03.py, output | Gamma sample=True returns deterministic 2 for a model with mean log(2) and variance log(2)²; simulated experiments get both the mean and noise wrong. |
| P04 | KNOWN | P04.py, output; existing-PR check | Main-branch no-intercept Poisson model fits mean 20 but predicts 12.61094383; existing open PR 390 already removes the link error and independently predicts 20. |
| P05 | KNOWN | P05.py, output; existing-PR check | Main-branch no-intercept simulation crashes on the documented coefficient length; existing open PR 390 already accepts it and agrees with direct Xβ. This option is absent from released simulators. |
| P06 | INTENDED | P06.py, output | Estimator seed alone does not reproduce folds and selected lambda changes (0.2 versus 0.03), but the API explicitly scopes random_state to initialization; both fold scores match independent normal equations. Seed global NumPy separately for repeatable folds. |

The last verdict means **consistent with the documented seed scope**, not proof of the maintainers' private intent. An estimator-wide seed would be an API improvement. The historical seeding work and GLMCV tests are discussed in EVIDENCE.md.

### Ranked author candidates, by demonstrated effect on users

1. **S01 — wrong Poisson loss.** Core tuning fit/decode machinery uses a quantity that reverses a basic likelihood comparison; this can choose a worse restart and changes stopping.
2. **S02 — incorrect population SEM.** The normal population plotting path silently understates uncertainty, including on completely nonzero, normalized data.
3. **P03 — gamma samples are deterministic with the wrong mean.** The documented sampling option can invalidate synthetic-data experiments without an exception.
4. **P01 — binary likelihood NaNs and overflow.** Valid confident predictions can poison reported deviance and CV/model-selection arithmetic; demonstrated on actual fitted public models.
5. **P02 — gamma deviance has the wrong zero.** A mathematically perfect prediction scores negative and the result changes with response units. This does not change fixed-fold deviance-only lambda ordering.

P04 has a substantial numerical effect, but it and P05 should not be presented as new reports: [open PR 390](https://github.com/glm-tools/pyglmnet/pull/390) already contains working repairs for these examples. The five candidates above are ranked for Ricardo to read; nobody was contacted. No claim about whether Hugo would care is made.

Evidence and limitations · Reproduction instructions

---

# Kris Sankaran — R packages

Folder: [friends/sankaran-r-packages](friends/sankaran-r-packages)

## Bugs

_Source: [friends/sankaran-r-packages/BUGS.md](friends/sankaran-r-packages/BUGS.md)_

## Confirmed correctness bugs

Seven confirmed bug reports across the four requested packages. Each has a minimal patch, pinned before/after output, a normal-input control, and a second implementation. No issue, PR, comment, fork or contact was made. These are local software fixes, not a new scientific result or a predictive-performance claim.

The first three repositories had no commits in the requested three-month window. Open/closed issue and PR records, comments and relevant diffs/reviews were checked before reporting. See SOURCES.md for pins, release comparison, deduplication decisions and environment limitations.

### SSI-001 — Two-stage GBH changes its decisions when groups are reordered

- Package / location: **structSSI**, `R/gbh.R:213` at `294d228cd7ef89ba17ea76ba246a267d7b59acb0`.
- Wrong: The TST first stage uses the raw p-values of each group at alpha/(1+alpha). The final GBH step uses that level once. Multiplying the entire raw vector inside the group loop changes later groups’ estimates and compounds the final factor. Move the multiplication after the loop.
- Before: Adjusted values in original order: `[0.02590875, 0.441, 1, 1]`; estimated group null fractions `[0.5, 1]`. Only A1 is rejected. Putting B first instead rejects only B1.
- Correct / after: Adjusted values `[0.024675, 0.42, 0.024675, 0.42]`; both group fractions 0.5; A1 and B1 are rejected regardless of row order.
- Effect on users: Different groups can lose discoveries solely because rows/groups are reordered. This is not merely a label error.
- Repro and patch: repro/SSI-001/, patch.diff, before/after output, independent result.
- Definition: [Hu, Zhao and Zhou (2010), Definition 4 and equation (2.9)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3175141/).
- Controls: Single-group TST, two-group LSL and Storey results remain identical. Python separately implements the BH rejection threshold and GBH adjusted levels.
- Confidence: **high for the reproduced case**. The affected file is identical in CRAN 1.2.1. This is the loop-placement regression after the old threshold fix (#2/#8), not the old missing-threshold report.

### SSI-002 — GBH assigns every result the name of the first sorted hypothesis

- Package / location: **structSSI**, `R/gbh.R:320` at `294d228cd7ef89ba17ea76ba246a267d7b59acb0`.
- Wrong: A scalar test passed to ifelse() produces a length-one result, which data.frame recycles. Use scalar if/else to select the whole name vector. Output identity is defined by names(unadj.p)[hypothesisIndex].
- Before: Names `h2, h2, h2` for raw p-values `0.001, 0.03, 0.8`.
- Correct / after: Names `h2, h1, h3`, with numerical values and original indices unchanged.
- Effect on users: Users joining or reporting discoveries by hypothesisName can attribute several tests to the wrong gene/hypothesis. The hypothesisIndex column remains usable.
- Repro and patch: repro/SSI-002/, patch.diff, before/after output, independent result.
- Definition: The pinned [GBH output contract](https://github.com/krisrs1128/structSSI/blob/294d228cd7ef89ba17ea76ba246a267d7b59acb0/R/gbh_class.R) defines hypothesisName as the original input name and hypothesisIndex as its index.
- Controls: All numeric columns remain identical; the entire unnamed-input result is unchanged. Python independently maps every index and raw value back to its original identity.
- Confidence: **high for the reproduced case**. CRAN 1.2.1 is affected. PR #11 introduced the scalar expression; the PR’s existing name regression test only covers hFDR.

### SSI-003 — Hierarchical testing crashes on a parent with one child

- Package / location: **structSSI**, `R/hfdr.R:193` at `294d228cd7ef89ba17ea76ba246a267d7b59acb0`.
- Wrong: The multtest BH helper fails for a length-one vector in the supplied current dependency. A singleton family requires no multiplicity adjustment. Replace the two-line multtest sorting/remapping call with stats::p.adjust(..., "BH").
- Before: For p=c(r=.001,a=.02) and the edge r -> a: `Error in if (is.na(spval[i])) tmp[i] <- NA : argument is of length zero`.
- Correct / after: Adjusted values r=0.001 and a=0.02; both hypotheses are rejected at alpha=0.05.
- Effect on users: A valid unary edge prevents users from receiving any hierarchical test result. This is separate from the already-reported failure to descend into grandchildren (#13).
- Repro and patch: repro/SSI-003/, patch.diff, before/after output, independent result.
- Definition: The family-wise BH traversal is the procedure described in [Sankaran and Holmes (2014), hierarchical testing section, following Yekutieli (2008)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4764101/). For m=1 the BH adjustment m*p/rank equals p.
- Controls: Two-child families, ties and unsorted p-values remain identical. Singleton values 0, .02, .05 and 1 are checked. Python derives the singleton result without multtest or structSSI.
- Confidence: **high for the reproduced case**. CRAN 1.2.1 has identical hFDR source. Reproduced with multtest 2.66.0; this is a dependency-facing valid-input failure.

### LNM-001 — Inverse log ratio returns NaN for large finite logits

- Package / location: **miniLNM**, `R/estimate.R:81` at `3dc73f2727bfce490236a0759cda8f6ef358affd`.
- Wrong: Computing exp(mu) directly overflows, making a probability Inf/Inf. Apply the ordinary stable softmax: append the reference logit zero, subtract the maximum logit, exponentiate and normalize.
- Before: phi_inverse(c(1000,0)) returns `[0, NaN, 0]` in both pinned functions and the installed CRAN package.
- Correct / after: Returns `[0, 1, 0]` to double precision, summing to one.
- Effect on users: Large finite linear predictors can generate NaN compositions and break subsequent multinomial sampling, although the mathematically defined probabilities are finite.
- Repro and patch: repro/LNM-001/, patch.diff, before/after output, independent result.
- Definition: The model itself specifies this definition using softmax after appending zero in [inst/stan/lnm.stan](https://github.com/krisrs1128/miniLNM/blob/3dc73f2727bfce490236a0759cda8f6ef358affd/inst/stan/lnm.stan).
- Controls: Ordinary logits (-5,0,5) remain unchanged to floating precision; scalar and matrix cases are checked. Python’s independent 80-digit Decimal calculation agrees.
- Confidence: **high for the reproduced case**. Confirmed through installed CRAN 0.1.2 as well as pinned source; no matching report in miniLNM issue #1, which concerns VB/psis.

### LNM-002 — Design-matrix filtering silently removes the formula intercept

- Package / location: **miniLNM**, `R/estimate.R:90` at `3dc73f2727bfce490236a0759cda8f6ef358affd`.
- Wrong: model.matrix() has already generated the correct predictors. Filtering its columns against the names of RHS variables discards (Intercept), and can also discard transformed columns. Return the model matrix without that redundant name filter.
- Before: An intercept-only formula yields a 20 x 0 design. Public lnm() prints `D is 0, but must be greater than or equal to 1` and wraps an invalid list instead of a stanfit. Ordinary ~ x also loses its intercept.
- Correct / after: The design is 20 x 1, all ones; the same intercept-only data produce an lnm object with nonempty stanfit draws.
- Effect on users: Intercept-only models fail; formulas with default intercepts fit a different model from the one requested. Existing fitted models should be refitted after applying this fix.
- Repro and patch: repro/LNM-002/, patch.diff, before/after output, independent result.
- Definition: The package documents R’s formula interface. [R model.matrix](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/model.matrix.html) and [R formula](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/formula.html) define the design and its default intercept.
- Controls: The explicit no-intercept ~ 0+x input is unchanged. Default intercept, factor and transformed-variable designs agree with base model.matrix. Python independently checks the all-one intercept design. A public fit is also exercised.
- Confidence: **high for the reproduced case**. Confirmed through installed CRAN 0.1.2 and the pinned source. The tiny fit emits the ordinary Pareto-k=0.74 diagnostic: it demonstrates a usable design/fit object, not posterior-accuracy certification. One initial repro assertion was corrected after reverting the patched copy; see first-attempt.txt and STATUS.md.

### MM-001 — Gaussian glmnet and random-forest samplers square the intended noise variance

- Package / location: **multimedia**, `R/estimators.R:388 and R/estimators.R:692` at `346039a2f10d332f57a48ec235e7ff5e0c0ab1f6`.
- Wrong: Both samplers supply a variance estimate to rnorm() as its sd argument. Take the square root, and select the Gaussian deviance for lambda_ix when using a regularization path.
- Before: The RF fixture’s residual mean-square parameter is 9.701943841, but generated noise has variance 94.127714296. The glmnet fixture’s parameter is 7.2502, but generated noise has variance 52.56540004.
- Correct / after: Noise variances are 9.701943841 and 7.2502, respectively. Corresponding standard deviations are 3.114794 and 2.692620.
- Effect on users: Synthetic outcomes and mediator values can be greatly overdispersed when the residual variance exceeds one, or underdispersed when it is below one. Downstream simulation/sensitivity results using these samplers can change.
- Repro and patch: repro/MM-001/, patch.diff, before/after output, independent result.
- Definition: [ranger](https://imbs-hl.github.io/ranger/reference/ranger.html) defines regression prediction.error as mean squared error; [glmnet deviance](https://glmnet.stanford.edu/reference/deviance.glmnet.html) gives the Gaussian residual deviance. [R rnorm](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Normal.html) takes standard deviation. Thus Y=mu+sqrt(v)Z has variance v.
- Controls: Real ranger/glmnet fits and a fixed normal stream give exact checks; no Monte Carlo acceptance threshold is used. Fits scaled to unit residual variance retain the same output. A two-lambda path uses the matching residual scale. Python separately verifies Var(sqrt(v)Z)=v.
- Confidence: **high for the reproduced case**. Both affected function bodies match CRAN 0.2.0. This report is restricted to continuous Gaussian/regression responses, as documented by the samplers. Direct pinned functions were loaded with their real dependencies; a full multimedia installation was unavailable.

### SCD-001 — Truncated-Gaussian tail cancellation corrupts likelihoods and copula scores

- Package / location: **scDesigner**, `scdesigner/src/scdesigner/distributions/zero_inflated_truncated_gaussian.py:133 and :166` at `f991d485b0f91540c9805cdfaa349f98d5d3b956`.
- Wrong: The float32 normal CDF rounds to zero before log() in the negative tail. Clamping that zero to 1e-30 substitutes a wrong normalizer. The uniformization code also subtracts nearly equal CDFs and adds an epsilon that can dominate the tail probability. Use torch.special.log_ndtr and scipy.stats.truncnorm.cdf.
- Before: At mu=-6, sigma=1, pi=.2, y=.2: log-likelihood 48.715469360 instead of 0.374686865. At mu=-10: CDF 0.200000003 instead of 0.895917939.
- Correct / after: Float32 log-likelihood at mu=-6 is 0.374686301; CDF at mu=-10 is 0.895917773. These agree with independent double-precision quadrature within float32 tolerance.
- Effect on users: Valid negative latent means can give badly incorrect fitting objectives and gradients, and positive observations can map to the zero atom’s copula score. This changes fitted models and joint simulations.
- Repro and patch: repro/SCD-001/, patch.diff, before/after output, independent result.
- Definition: The package defines an atom pi at zero plus (1-pi) times a positive truncated-normal density. The [SciPy truncated-normal definition](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.truncnorm.html) uses standardized truncation limits. The independent check integrates the unnormalized normal kernel directly on (0,infinity).
- Controls: Central normal inputs are bitwise unchanged. Positive-data CDF/inverse round trips agree at mu=-10,-6,-2,0,3. Base R independently integrates the density and CDF, without torch, SciPy, or the package.
- Confidence: **high for the reproduced case**. The installed PyPI 0.0.27 affected file is byte-identical to the pin. This is distinct from the mixture-component inversion bug previously fixed in PR #38.

### Suspected / untriaged, not included in the seven

The following observations have no completed patch-and-independent-check package and are not shipped as confirmed bugs:

- **structSSI missing/empty input:** an NA in the raw vector triggers a recycling warning and a row-count error; empty vectors error. The documentation does not specify NA/empty-vector semantics. See `checks/structSSI.txt`.
- **structSSI boundary annotations:** significance stars use strict cutoffs, so an exact alpha-boundary rejection can be annotated inconsistently with the standard <= definition. Numerical adjusted values were checked; the full reporting path was not patched.
- **structSSI pi0=1 with p=0:** sorting the NaN weight can silently lose one input row. Additional denominator/edge-case conventions should be checked before proposing a fix.
- **miniLNM NA alignment:** an NA covariate yields two design rows while the selected response retains three rows. This was observed via model_matrix_df, but a full missing-data repro/patch is not included.

### Already reported or excluded

- **structSSI depth traversal:** significant grandchildren remain NA. This is the open issue [#13](https://github.com/krisrs1128/structSSI/issues/13), so it is excluded from new findings. The singleton crash SSI-003 occurs before recursion and is distinct.
- **structSSI LSL all-ones input:** the single p=1 case returns Inf; related estimator boundary issues appear in #1/#3. Not claimed as new.
- **miniLNM formula-parser candidate:** the apparent length>1 error came from loading functions before formula.tools registered its formula method. The installed public API works. This was an investigation artifact, not a package bug.

### Coverage and limits

`checks/structSSI.R` compares ties, zero/one p-values, a single group, unused factor groups and unsorted input against base R. It checks alpha=0/1, probes NA/empty inputs and unary trees, and compares 200 small ordinary Oracle GBH cases numerically. Its hFDR traversal comparison also records the already-known grandchild issue.

`checks/other-packages.R` checks exact linear multiresponse estimates and noiseless simulation in multimedia, and miniLNM’s known log-ratio identity and count depths. `checks/scDesigner.py` checks ordinary distribution likelihoods and inversion. These are correctness exercises; no prediction score or superiority claim is made.

The portable R could not load the complete structSSI/multimedia dependency stacks. Their exact pinned numerical functions were exercised with real direct dependencies, including multtest, igraph, ranger and glmnetUtils. miniLNM’s installed public API was tested, including a patched-source fit, and the scDesigner source was compared against the installed PyPI release. General package integration and all statistical model families were not exhaustively tested.

## Verdicts

_Source: [friends/sankaran-r-packages/VERDICTS.md](friends/sankaran-r-packages/VERDICTS.md)_

## Independent referee verdicts

All seven claimed failures reproduce; six are **CONFIRMED**, one **CONFIRMED-MINOR**. No matching prior report or current fix was found in the checked public records as of 2026-11-06. This is a scoped search finding, not proof that nobody has encountered them.

| ID | Verdict | My repro | Effect on users' results |
|---|---|---|---|
| SSI-001 | CONFIRMED | R, output | Identical groups lose different discoveries solely when their input order changes under documented `method="tst"`. |
| SSI-002 | CONFIRMED | R, output | Named GBH results repeat one hypothesis name, so distinct significant genes can be reported as the same gene; indices remain correct. |
| SSI-003 | CONFIRMED | R, output | A valid single-child family crashes hierarchical testing instead of returning its unadjusted singleton p-value. |
| LNM-001 | CONFIRMED-MINOR | R, Decimal reference, output | Extreme finite log ratios produce NaN probabilities, which can interrupt prediction or sampling. |
| LNM-002 | CONFIRMED | R, output, public entrypoint, public output | Ordinary formulas lose their intercept; intercept-only designs have no columns and fail in Stan; transformed terms can disappear too. |
| MM-001 | CONFIRMED | R, output | Gaussian RF/glmnet synthetic responses use residual variance as SD, yielding variance squared and scale-dependent over/underdispersion. |
| SCD-001 | CONFIRMED | Python, output, base-R integral, reference output | Legitimate negative latent means corrupt float32 likelihoods/gradients and positive-data copula probabilities. |

### Ranked shortlist for Ricardo to read

Ranking is by the demonstrated effect and the documented path to exposure. It does not estimate how often users encounter a bug or whether the author would care.

1. **MM-001:** changes synthetic-data variability for both documented continuous-response sampler families whenever residual variance differs from one. On ordinary `mtcars` fits, the RF residual variance is **6.3047516463**, but generated noise has implied variance **39.7498933214**; glmnet gives **6.0963207633** versus **37.1651268486**. The mean predictions need not expose the error. Simulation and sensitivity conclusions can change.
2. **SSI-002:** corrupts the identity of reported hypotheses on the documented named-input path, including with default adaptive settings because they call `Oracle.GBH`. In my oracle fixture, two significant results should be geneB and geneC; both are labeled geneB. Recovering identities through `hypothesisIndex` works, but reporting or joining by `hypothesisName` does not.
3. **LNM-002:** silently changes the model requested by conventional R formulas, with an obvious failure for `~1` and less obvious omission for `~x`. The public pinned path fails at Stan's `D>=1` restriction and still wraps a list as the estimate. The README's own example omits the intercept too, which tempers any inference about author intent; the help promises R's formula interface and documents no no-intercept convention.
4. **SSI-001:** changes which group gets discoveries under a documented optional estimator. With two identical groups, each containing p-values **(.045,.7)** at alpha **.1**, only the first group's small p-value is rejected. Reversing the groups reverses that choice. Both should be rejected by the specified procedure.
5. **SCD-001:** corrupts the optimization objective and copula transformation within the documented zero-inflated truncated-Gaussian family. At **mu=-6, sigma=1, pi=.3, y=.3**, log likelihood is **47.95694** instead of **-0.38384453**. At **mu=-8**, the returned CDF is **.3004660** instead of **.94142546**. Mean uses an identity link, so these parameters are admissible. This is conditional on a particular distribution/tail regime; no prevalence or full fitted-data impact was measured.

SSI-003 remains reportable but falls below this five-item shortlist: it stops execution visibly on unary families. LNM-001 is lower priority because the exhibited log ratio 720 is extreme.

### What I independently established

#### SSI-001

Pinned R/gbh.R:206–217 scales the entire p-vector inside the group loop, at line 213. My input uses distinct names and numbers from the hunter's reported example. Each raw pair (.045,.7) has one BH rejection at alpha'=.1/1.1, hence pi0=.5 independently for each group. GBH weights are one, overall pi0=.5; one final factor 1.1 gives sorted weighted values (.0495,.0495,.77,.77). Reverse cumulative minima of `2*p/rank` give adjusted values **(.0495,.385,.0495,.385)** in input order. The unpatched code instead estimates pi0=(.5,1), returns **(.05445,.4235,1,1)**, and changes the rejected identity on reordering. The printed `unadjp` column is also rescaled.

Reachability: Adaptive.GBH help lists `tst`; default is `lsl`, so this is an optional documented method. The independent procedure follows [Hu, Zhao and Zhou, Definition 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC3175141/): estimate from each group's raw values and use alpha' once for final testing.

History: [issue #2](https://github.com/krisrs1128/structSSI/issues/2) concerns missing final threshold correction. [PR #8](https://github.com/krisrs1128/structSSI/pull/8) introduced the correction **inside** the loop; its saved diff shows this. The repeated correction/order dependence is a distinct regression, not a new report of the old omission. No matching discussion was found among 13 issue/PR records and their available comments/reviews. Master is still the pin. The old `protect-nas` branch lacks the correction altogether; it is not a repair. CRAN 1.2.1's entire gbh.R is identical.

#### SSI-002

Pinned R/gbh.R:320 passes a scalar condition to `ifelse`. My input is `c(geneA=.4,geneB=.004,geneC=.012,geneD=.2)` with one group pi0=.5. Sorted indices are **2,3,4,1**, so direct lookup in the original input independently gives **geneB,geneC,geneD,geneA**. All four returned names are geneB. Adjusted p-values .008 and .012 make the mislabeling relevant even within discoveries.

Reachability: named p-values appear in the Oracle and Adaptive help examples; the GBH class contract explicitly defines names as original input identities. This is not cosmetic when names are used to report or join results. History: [PR #11](https://github.com/krisrs1128/structSSI/pull/11) introduced this expression while renaming output columns; saved diff. No matching report was found. CRAN 1.2.1 is byte-identical here; the historical branch uses an older output schema rather than fixing the present regression.

#### SSI-003

Pinned R/hfdr.R:193 calls multtest for a singleton family. For root=.003, leaf=.04 and edge root→leaf, unchanged code errors `argument is of length zero`. Independently, a one-element BH family multiplies .04 by 1/1, leaving .04. The root is significant, so both nodes should be returned as rejected. A two-child control returns the expected family adjustment.

Reachability: hFDR.adjust help accepts parent/child edge lists without a binary-tree or minimum-family-size restriction. The failure is in the real multtest 2.66.0 dependency, not my implementation. The current Bioconductor 3.23 multtest 2.68.0 source still fails directly on .04; separate repro/output. Its BH loop uses `(m-1):1`, which includes zero at m=1. CRAN structSSI 1.2.1's hfdr.R is identical. No singleton report was found in structSSI's issues; [open #13](https://github.com/krisrs1128/structSSI/issues/13) concerns missed deeper descendants, a separate failure. The old branch retains this same dependency call.

#### LNM-001

Pinned R/estimate.R:81–83 directly exponentiates logits. My input **(720,-2)** returns **(0,NaN,0)**. An independent 70-digit Python Decimal calculation of **(1,exp(720),exp(-2))**, divided by its sum, gives approximately **(2.03223e-313,1,2.75033e-314)**. All probabilities are representable finite doubles; the intermediate exponent is not. A central (2,-2) control is finite; the matrix path also fails only on its extreme row. The installed CRAN exported function independently reproduces NaN too.

Reachability: `phi_inverse` is exported and accepts a numeric vector without a stated finite-magnitude limit. It is also used in prediction/sampling. The Stan model defines the reference-zero softmax consistently. Classification is MINOR because this example requires an extreme log ratio; it does not establish typical fits reach that magnitude. No match in miniLNM's sole issue/PR (#1, about VB/psis), or branches; the affected functions are identical in CRAN 0.1.2.

#### LNM-002

Pinned R/estimate.R:90–94 filters the already-expanded design by regexes derived from RHS variables. My five-row input yields **5×0** for `y~1`, **5×1** for `y~x`, and **5×0** for `y~I(x^2)`, versus base R's **5×1**, **5×2**, **5×2** respectively. The factor design also loses its intercept; explicit `~0+x` agrees with base R. The reference designs use only base `model.matrix`, independently of miniLNM. The public pinned `lnm(a+b~1,...)` path, with its own unchanged formula/VB wrapper and real compiled Stan model, prints **D is 0, but must be greater than or equal to 1**, then returns an estimate of class list.

Reachability/intent: lnm help expressly calls this R's formula interface; [standard R formula semantics](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/formula.html) include an intercept unless removed. No exclusion for intercept-only or transformed formulas is documented. The README's five-dimensional example demonstrates existing intercept omission and the synthetic generator also has no intercept: the behavior may have been convenient or intentional for that example. Neither documents an interface-wide exception, and removal of transformed terms reinforces the correctness finding. I confirm the contract failure without asserting the author's intent. The original helper exists since the initial estimation implementation; no later branch or issue explains/fixes it. CRAN 0.1.2's three affected transformation/design function expressions match the pin exactly; its VB wrapper differs, which is why the public pinned repro explicitly loads the pin's own wrapper.

#### MM-001

Pinned R/estimators.R:388–390 and 692–694 sends residual mean squares to `rnorm` as SD. I fit real ranger and Gaussian glmnetUtils models to `mtcars`, then call the **original parsed sampler definitions** with those real fit objects. Independently computing RF out-of-bag squared residuals and glmnet squared residuals verifies their variance parameters. With a replayed normal stream, including ranger's own RNG consumption during prediction, outputs match `prediction + v*Z` exactly. A normal perturbation with intended variance v must instead be `sqrt(v)*Z`; this is an algebraic variance identity, not an empirical predictive-performance comparison. The observed means do not need to change for this defect to matter.

Reachability: the RF and glmnet sampler help explicitly assumes continuous responses and includes `mtcars` examples. Model constructors assign these same sampler functions. Their documentation's use of “MSE” to estimate “sigma” does not make variance-as-SD statistically correct. The reference packages document `ranger$prediction.error` as regression MSE and Gaussian glmnet deviance as squared residual error; my direct residual computations also establish those units. This verdict covers the Gaussian one-lambda variance defect; it does **not** certify the hunter's patch, lambda-path handling or non-Gaussian behavior. No matching discussion in eight multimedia issue/PR records and comments. Main equals the pin; CRAN 0.2.0's entire estimators.R is identical.

#### SCD-001

Pinned zero_inflated_truncated_gaussian.py:133 and 166 uses a float32 CDF before logarithm and CDF subtraction with an additive denominator epsilon. I installed the fresh pinned package normally, created an AnnData template, called public setup methods, and set its real identity/exp/sigmoid predictor coefficients to admissible parameter values. Float32 is the loader/predictor default. At sigma=1, pi=.3, y=.3, the unpatched likelihood and uniformization disagree with independent base-R integration:

| mu | Package log likelihood | Independent log likelihood | Package CDF | Independent CDF |
|---:|---:|---:|---:|---:|
| -8 | 33.35694122 | -0.70717632 | .30046600 | .94142546 |
| -6 | 47.95693970 | -0.38384453 | .89380604 | .89440778 |
| -5 | -0.29452020 | -0.25561508 | .85860378 | .85860556 |
| 0 | -0.62746632 | -0.62746630 | .46507600 | .46507599 |

The reference integrates `exp(mu*t-t^2/2)` on positive t, analytically cancelling the common Gaussian factor, and derives the density, CDF and mean gradient. At mu=-6 the package's **per-observation** mean gradient is **6.3**, versus **.14151740** independently. The log reports summed gradients for four identical observations. No SciPy, torch or package routines are used in the reference.

Reachability/intent: the class documentation describes a latent Gaussian mean, not a nonnegative observed mean; the actual mean link is identity. No parameter restriction enforces the docstring's suggestion that nonnegative data keep the ratio benign. My probe shows admissible behavior; it does not establish frequency in trained datasets. [PR #38](https://github.com/krisrs1128/scDesigner/pull/38) addressed mixture inversion before this family was added by [#41](https://github.com/krisrs1128/scDesigner/pull/41); neither describes this tail defect. Sixty issue/PR records, available comments/reviews, 96 recent default-branch commits and the other branch were checked. Its other branch retains the affected numerical expressions. The PyPI 0.0.27 affected file and installed pinned file are byte-identical.

### Scope and reproduction

Each ID has its own fresh GitHub clone at the supplied commit; pins.json records seven unchanged checkouts. I read only the hunter's BUGS.md and SOURCES.md to identify claims/pins; I did not open or execute the hunter's repros, output files or patches. My inputs, calculations, downloads and scripts are local to this workspace. The claims document itself necessarily contains the hunter's stated outputs; none was used as an oracle or imported as a fixture. No upstream code was patched.

Run the R repros with `zsh repro/run-r.sh`. The public miniLNM extension is `repro/LNM-002-public.R`; the latest multtest helper extension is `repro/SSI-003-current-dependency.R`. Use the supplied Rscript and `R_LIBS="$PWD/env/Rlib"`. Run Python with `env/py311/bin/python repro/SCD-001.py`, setting OMP/BLAS threads to 2 and TMPDIR to `env/tmp`. Use `nice -n 10`; scripts use only tiny inputs. Dependency versions and source/release comparison accompany the outputs; miniLNM's function comparison handles its unrelated release changes.

Full structSSI and multimedia installation failed on their broader dependency stacks; their unchanged function definitions were evaluated with real direct dependencies. MiniLNM's public entrypoint was exercised using original pinned functions in an environment backed by its installed namespace and the same Stan specification. scDesigner was installed from the pin. These results establish the stated numerical failures, not end-to-end certification of every package or validation of proposed fixes. Initial harness failures and their reversions are recorded in STATUS.md; superseded files are retained locally.

Public history was fetched independently through `gh api`, including all open/closed issue/PR records (13/1/8/60), available discussion and review records, branch heads and recent commits. Raw evidence is under history/; branch/file comparisons are in each package's `branch-and-file-history.txt`. There were no default-branch commits after August 6 for structSSI, miniLNM or multimedia, and 96 for scDesigner. Current CRAN/PyPI source distributions were downloaded independently under releases/; download versions/hashes identify them. No public actions or contact occurred.

**NEW: no** under the friends lane scientific-result definition. This job independently confirms software correctness defects; it does not beat a printed scientific number, settle a paper's open problem, or test a scientific prediction on new data. No predictive-performance claim or SBS comparison is made.

---

# Gavin Sherlock — GO::TermFinder

Folder: [friends/sherlock-go-termfinder](friends/sherlock-go-termfinder)

## Verdicts

_Source: [friends/sherlock-go-termfinder/VERDICTS.md](friends/sherlock-go-termfinder/VERDICTS.md)_

Independent referee verdicts for GO::TermFinder 0.86, 2026-11-06. Four priority defects survive; three other defects already have public fixes, two parser defects are minor, and one claimed wrong-p-value result has a documented intended interpretation.

| ID | Verdict | My repro path | Effect on users / disposition |
| --- | --- | --- | --- |
| GTF-001 | CONFIRMED | repro/GTF-001 | Modern GAF negations become positive evidence, producing false enrichment (raw p=1/220, default corrected p=1/110). |
| GTF-002 | KNOWN | repro/GTF-002 | CPAN splits equivalent GO IDs and returns inconsistent membership; Princeton published the canonicalization fix in 2017. |
| GTF-003 | KNOWN | repro/GTF-003 | CPAN omits the one-hypothesis corrected p-value; its example reporter even admits p=1 through a 0.05 cutoff. Princeton already fixes the missing field. |
| GTF-004 | CONFIRMED | repro/GTF-004 | Tied p-values get different FDRs: 0.20 and 0.10, versus the documented same-cutoff estimate of 0.10 for both. |
| GTF-005 | CONFIRMED | repro/GTF-005 | Redundant gene spellings change the simulation null; the exact extreme-event probability becomes 3/35 instead of 1/10. |
| GTF-006 | INTENDED | repro/GTF-006 | Adding unknown genes to the aspect follows public POD; direct-only code conflicts with that policy, so the hunter's proposed p-value is not uniquely required. |
| GTF-007 | CONFIRMED-MINOR | repro/GTF-007 | A valid uncommon tag order retains an obsolete term; the source already acknowledges its order assumption. |
| GTF-008 | KNOWN | repro/GTF-008 | CPAN deletes a preceding valid gene after an ambiguous alias; Princeton's published code explicitly identifies and fixes this exact bug. |
| GTF-009 | CONFIRMED | repro/GTF-009 | A legal leading typedef makes all later GO terms disappear, leaving an empty ontology. |
| GTF-010 | CONFIRMED-MINOR | repro/GTF-010 | Invalid cyclic input recurses until a watchdog kills it; this is robustness on malformed data, not wrong enrichment on a valid GO DAG. |

The four bugs most worth putting before Ricardo for possible author contact, ranked by effect on real users:

1. **GTF-001 — negations become positive evidence.** This can manufacture significant enrichment from evidence expressly denying the function. Current GAF 2.2 makes this trigger routine for negated annotations. The historical POD describes an older qualifier format, but README directs users to current GO downloads. Report as a modern-format compatibility defect.
2. **GTF-004 — tied FDR denominators.** Parent and child terms can have identical gene sets, so ties need no unusual input. Users selecting terms by the documented FDR option can receive different decisions for the same p-value cutoff. The package's own example requests FDR.
3. **GTF-005 — inconsistent background normalization.** IDs and aliases are accepted, and duplicate resolution is documented. The simulated null nevertheless weights raw name slots rather than distinct genes, changing corrected p-values and FDR. The effect is established by exact enumeration, not a difference between noisy simulations.
4. **GTF-009 — typedef placement empties the ontology.** The OBO API accepts a valid layout that the parser truncates. This can stop an analysis or remove later terms. The failure is often conspicuous, and prevalence in users' actual ontology files was not measured.

This is a technical impact ranking, not a prediction of whether the friend would care. Nothing has been sent to Ricardo's friend or anyone else. The three KNOWN items warrant reuse of existing fixes, not presentation as new discoveries.

**Source and independence.** I freshly downloaded [SHERLOCK's CPAN 0.86 archive](https://cpan.metacpan.org/authors/id/S/SH/SHERLOCK/GO-TermFinder-0.86.tar.gz); SHA-256 is `8daad833bffa65e726684ab98cb175f7c7f97d4e468362a2936fe0cd42bf0ea3`. Source provenance confirms all three relevant modules are identical to that archive. The normal `perl Makefile.PL`, `make -j2`, `make test` sequence succeeded without source edits; visualization dependencies were not needed. I read the claim descriptions and pin metadata, but did not open, run, import, or copy the hunter's repro scripts, separate expected-output files, patches, checks, or prior-art analysis. All inputs, the Perl API driver, and exact Python calculations here were written independently. Numbered source excerpts confirm every cited location.

**Correct answers and user reachability, by claim.** `v1`–`v6` are synthetic genes, with three query genes unless stated otherwise. These are software counterexamples, not measurements on biological data. The exact tail calculation is the ordinary hypergeometric upper tail, summing `C(M,k) C(N-M,n-k) / C(N,n)` for `k >= x`; no statistical package is used by oracle.py.

**GTF-001.** `AnnotationParser.pm:583` tests equality to bare `NOT`. My molecular-function GAF 2.2 contains three `NOT|enables` annotations to amber and positive annotations to blue for every known gene. Negation means amber has no positive annotations and should not appear at all. Unpatched amber has x=M=n=3, N=12, p=1/C(12,3)=1/220, with a Bonferroni value of 1/110. A separate legacy GAF 2.1 bare-NOT control excludes amber without changing query membership. The consortium's [GAF 2.2 specification](https://geneontology.org/docs/go-annotation-file-gaf-format-2.2/) defines the compound negation. The constructor's documented input is a GO consortium annotation file; the older POD's bare-NOT-only table explains the compatibility gap but does not make positive interpretation biologically correct. No matching fix was found in inspected release/history/Princeton source.

**GTF-002.** `TermFinder.pm:1353–1361` resolves the node but retains the supplied GO-ID string. My query annotates v1 with the primary ID and v2/v3 with its alternate ID; both IDs resolve to the same node. Correct x=M=n=3, N=12 gives p=1/220. CPAN returns x=M=2, p=1/22, while `ANNOTATED_GENES` contains only v1. This is a supported OBO `alt_id`, not two biological categories. The primary-ID control returns all three genes. Princeton's [published TermFinder.pm](https://github.com/princeton-genomics/GO-Tools/blob/8635ca70c79eb2c526062eeba90a9428a89fc325/lib/GO/TermFinder.pm#L1365) already assigns `$goid = $node->goid`. Running my same input with the pinned Princeton libraries returns x=M=3, all three genes, and p=1/220: comparison. **KNOWN despite remaining broken in the current CPAN release.**

**GTF-003.** `TermFinder.pm:1578` skips the Bonferroni field assignment when the number of hypotheses is one. The default correction is documented as Bonferroni, so the corrected value must equal the raw value, 1/220, in my single-result case. This is more than an API nuisance: with all six known genes annotated to one term, the correct raw and corrected p-values are both 1. The unchanged shipped `examples/termFinderClient.pl` still prints that term through its 0.05 cutoff because the missing field compares numerically as zero: actual example output. Princeton initializes `CORRECTED_PVALUE` to the raw value when building each result; my comparison run supplies the missing field. This existing fix is public in the same 2017 commit. The resolved RT zero-hypothesis crash is a different case.

**GTF-004.** `TermFinder.pm:1977–2012` uses the result's array rank instead of the number of real hypotheses at or below its p-value. Two terms annotate exactly v1/v2/v3 in a six-gene population; each p=1/20. The unchanged random sampler's 50 recorded draws produce a mean of 1/5 null hypotheses at that cutoff, independently recomputed from those draws. Both real hypotheses are at that cutoff, so the documented estimator is (1/5)/2=1/10 for both. Actual FDRs are 1/5 and 1/10. `EXPECTED_FALSE_POSITIVES` is already 1/5 for both in this repro; that field is not independently wrong here. The relevant public POD is `TermFinder.pm:567–578`, and `termFinderClient.pl:75–76` enables this option. This is the package's simulated FDR, not Benjamini–Hochberg. No matching prior fix was found.

**GTF-005.** `TermFinder.pm:1774` returns the raw supplied population names for sampling, while construction resolves duplicates. My population is `[v1, first_alias, v2, v3, v4, v5, v6]`, with `first_alias` resolving to v1. The six distinct genes form two disjoint three-gene annotation sets. With a three-gene query, uniform distinct-gene sampling has two extreme subsets among C(6,3)=20, hence probability 1/10. Sampling the seven raw slots has three extreme subsets among C(7,3)=35, hence 3/35; some draws also collapse to fewer than three genes. The same standard seed yields simulation p-values 0.076 for redundant names and 0.092 for canonical names; neither finite estimate is asserted to equal its limiting probability. Of 1,050 recorded draws in the redundant case, 176 collapse after alias resolution. Public POD `TermFinder.pm:501–507` promises deduplication, and constructor POD documents `population`. Changes 0.83 fixes random-index selection; that fix remains present here and does not fix duplicate-name weighting. No matching prior normalization fix was found.

**GTF-006.** The claimed numerical effect reproduces at `TermFinder.pm:379`: with three explicit direct-aspect annotations among six known genes and `totalNumGenes=12`, unpatched M=9 gives C(9,3)/C(12,3)=21/55. Under the hunter's direct-records-only definition, M=3 instead gives 1/220. However, public POD `TermFinder.pm:509–516` expressly assigns entirely unannotated genes to the root, its aspect child, and an unannotated dummy node. Under that virtual-annotation convention, the six anonymous genes belong in M and **21/55 is the correct hand calculation**. Changes 0.80 and `__buildHashRefOfAnnotations` instead emphasize direct annotations; the equivalent explicit-population input returns M=3, p=1/220. Thus the release is internally inconsistent, and the anonymous-gene behavior looks intended under public documentation. **INTENDED is narrowly about the alleged invention of annotations and the claimed uniquely correct replacement p-value; it does not certify the broader consistency of aspect handling.** I would not send this as a settled wrong-result report or endorse the hunter's patch without resolving that definition. The option is normal use: the interactive example explicitly asks for organism gene count.

**GTF-007.** `OboParser.pm:310,320` sets validity from tag order. A stanza with `is_obsolete: true` preceding `namespace: biological_process`, no relationships, and a following live term retains the obsolete node. Collecting the stanza's tags independently requires its exclusion; swapping only these two tags excludes it. This is a legal layout under the [OBO 1.2 specification](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html), which also defines equivalent alternate IDs and permits typedefs before terms. The public constructor accepts OBO files without an order restriction. Nonetheless this differs from the conventional term-tag order, and source lines 324–325 already acknowledge the ordering assumption. No separate matching issue or fix was located. Treat as a minor compatibility defect, not an established new discovery.

**GTF-008.** `TermFinder.pm:1111–1123,1176–1198` leaves the previous database ID in scope and then pops a gene that was never pushed for the ambiguous alias. My query `[v1,v2,v3,collision]`, with `collision` naming v5/v6, retains only v1/v2; correct behavior retains v1/v2/v3 and excludes only collision. Actual p=1/22; correct p=1/220. Moving collision first restores all three genes. Public ambiguity policy `TermFinder.pm:489–496` describes ignoring the ambiguous name. Princeton's [2017 source](https://github.com/princeton-genomics/GO-Tools/blob/8635ca70c79eb2c526062eeba90a9428a89fc325/lib/GO/TermFinder.pm#L1125) explicitly explains the accidental pop and inserts `next`, plus a later reset. The same independent input succeeds with those libraries. RT #77197 concerns a different case-insensitive standard-name return value. **KNOWN.**

**GTF-009.** `OboParser.pm:285` stops at the first `[Typedef]`. My leading `part_of` typedef is followed by the aspect and two valid child terms; all three `nodeFromId` calls return absent. Independently scanning the term stanzas finds all three. Moving the same typedef after the terms restores all three nodes. This obeys the OBO serializer's suggested typedef-before-term order, so it is not malformed input. The API, README and tutorials support OBO ontology input; the bundled test ontology happens to place typedefs after terms. No matching fix was found in CPAN, the mirror or Princeton's published parser. I did not establish the layout used by every current GO data release or live web service.

**GTF-010.** `OboParser.pm:616–630` recursively follows ancestors without checking revisits. The independent edge list is A→B→A, which DFS identifies as a cycle and a GO DAG parser should reject. The unpatched parser warns of deep recursion, emits no result, and is killed by the RSS watchdog after 0.669 seconds; peak observed RSS was 895,712 KiB. This is an observed sample, not a precise maximum. Removing one cycle edge gives a valid chain and returns immediately. The OBO constructor is a normal entry point, but the triggering graph violates the DAG assumption. No matching issue or fix was found; downgrade to malformed-input robustness.

**Known/fixed search and limits.** Fresh read-only `gh api` requests checked all open/closed issues, all branches, and commit history in `gitpan/GO-TermFinder` and `princeton-genomics/GO-Tools`, plus targeted global issue searches. Both repositories have only `master` and returned no issues. The gitpan head `414c6cd22b8ec6eec90a2f22f3b7f83d26d94ba6` has identical relevant modules to CPAN. Princeton head is `a55e5845cbe169745dc0accfec0f35aed052717e`; its three fixes above were already published in commit `8635ca70c79eb2c526062eeba90a9428a89fc325`, dated 2017-12-15. Its README explicitly says its modified modules override the CPAN files. The comparison runs use these published modules and the locally built CPAN native library, without modifying either source. Global issue search also found [CGD PR #48](https://github.com/candidagenome/cgd-backend/pull/48), which describes integration tests, not these defects.

MetaCPAN's [latest-release endpoint](https://fastapi.metacpan.org/v1/release/GO-TermFinder) still names `GO-TermFinder-0.86` and the same archive; its numeric version field inconsistently says 0.85, whereas archive VERSION and module say 0.86. All of the fresh CPAN Changes file was read, including the 0.80 Bonferroni fix, 0.81 zero-hypothesis fix, and 0.83 sampling fix. None supplies the four shortlisted fixes.

Live [CPAN RT](https://rt.cpan.org/Public/Dist/Display.html?Name=GO-TermFinder) returned HTTP 202 with `x-amzn-waf-action: challenge`; this job cannot certify current ticket contents. I independently retrieved the [2021 active queue](https://web.archive.org/web/20210519024220/https://rt.cpan.org/Public/Dist/Display.html?Name=GO-TermFinder) and resolved queue, read the four active ticket bodies (#102758 long-double tests; #102757 compiler selection; #77197 standard-name lookup; #13361 visualization clipping), and compared the three resolved subjects (#33010 zero-hypothesis crash; #30861 native tests; #6779 typo). They do not establish prior reports of the four shortlisted defects. MetaCPAN distribution metadata reports the same four active/three resolved counts, but is not a substitute for readable live ticket contents. Raw API replies, archived pages, module comparisons and WAF headers are under evidence/upstream. **Previously unreported is not proven.**

**NEW: no** under the Friends scientific-result definition. This referee report establishes software behaviors and identifies existing fixes; it does not beat a printed scientific number, settle a paper's open problem, or test a scientific prediction on new data. No predictive metric was evaluated, so trivial/simple/model baselines and SBS do not apply. No hunter patch was tested or endorsed. All work stayed local; no issues, PRs, comments, forks, uploads or messages were created.

## Bugs: pre-referee report; final dispositions above

_Source: [friends/sherlock-go-termfinder/BUGS.md](friends/sherlock-go-termfinder/BUGS.md)_

## Confirmed defects in GO::TermFinder 0.86

Ten local fixes, each with a failing input, captured original output, independently computed correct output, an isolated patch, and an unchanged normal control. The original source is untouched in `sources/GO-TermFinder-0.86/`; locations below refer to that source. `all-fixes.patch` combines the fixes. Nothing was submitted publicly.

No overlap was found with Changes, the four archived active RT tickets, the three archived resolved-ticket subjects, or the checked mirror history. **Previously unreported is not established:** live RT returned an AWS challenge; the accessible queue snapshot is from 2021. See [PRIOR_ART.md](friends/sherlock-go-termfinder/PRIOR_ART.md).

### GTF-001 — Compound NOT qualifiers become positive annotations

- **Location:** `lib/GO/AnnotationProvider/AnnotationParser.pm:583`.
- **Wrong behavior:** skips only a field equal to `NOT`, retaining valid pipe-separated fields such as `NOT|contributes_to` and `NOT|involved_in`.
- **Repro:** repro/GTF-001/run.sh. Two negated annotations to GO:0000011 produce a positive enrichment result, p = 1/190 = 0.00526315789473685. Correct output contains no result for that term. The two genes also have positive annotations to a different term, so their background membership is unchanged.
- **Fix:** match `NOT` as a complete pipe-delimited token. Positive annotations and bare NOT controls retain their behavior. This is a modern-GAF compatibility defect; the release's POD predates those formats.
- **Reason / independent check:** [GAF 2.1, column 4](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/#qualifier-column-4), [GAF 2.2, relation/negation](https://geneontology.org/docs/go-annotation-file-gaf-format-2.2/#relation-column-4). Python splits the field into tokens before constructing annotation sets. Both qualifier orders and GAF 2.2 negation were checked.
- **Effect:** negative biological evidence can become apparently significant positive enrichment. **Confidence: high.**

### GTF-002 — Alternate GO IDs split a single term's counts

- **Location:** `lib/GO/TermFinder.pm:1353–1361`.
- **Wrong behavior:** `nodeFromId` resolves an alternate ID, but annotation counting keeps the original string rather than the node's primary ID. Genes annotated under primary and alternate IDs are counted separately.
- **Repro:** repro/GTF-002/run.sh. Query genes use GO:0000099 (alternate) and GO:0000011 (primary). Original: no tested term. Correct: one term with x = 2, M = 3, n = 2, N = 20, p = C(3,2)/C(20,2) = 3/190 = 0.0157894736842105.
- **Fix:** canonicalize the ID before storing annotations, including direct aspect annotations.
- **Reason / independent check:** [OBO 1.2, alt_id](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html): alternate IDs refer to the same term. Python maps alternate IDs to primary IDs before set union and exact combinatorics.
- **Effect:** missed enrichment, split counts, and potentially mismatched returned gene membership. **Confidence: high.**

### GTF-003 — One-hypothesis Bonferroni result omits its corrected p-value

- **Location:** `lib/GO/TermFinder.pm:1578`.
- **Wrong behavior:** only assigns `CORRECTED_PVALUE` when more than one hypothesis is tested, despite the documented result contract.
- **Repro:** repro/GTF-003/run.sh. Original: field absent. Correct: `CORRECTED_PVALUE = PVALUE = 1/190`.
- **Fix:** run the assignment for one or more hypotheses. Zero hypotheses still produce an empty list. The normal control exercises multiple hypotheses and the usual multiplier.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf), and local `TermFinder.pm:456–463`: adjusted p = min(1, m p), including m = 1. Python computes this formula independently.
- **Effect:** API clients receive missing data for a legitimate result; clients relying on the documented field can mis-handle the result. This is an output-contract bug, not an incorrect raw p-value. **Confidence: high.**

### GTF-004 — Tied p-values have different FDR estimates at the same cutoff

- **Location:** `lib/GO/TermFinder.pm:1977–2012`.
- **Wrong behavior:** divides expected null discoveries by array rank `i+1`; a cutoff at a tied p-value includes every tied hypothesis, not just the first members of the tie.
- **Repro:** repro/GTF-004/run.sh. Two identical annotation sets yield p = 1/6. With 50 explicitly enumerated draws, average null discoveries = 0.5. Original FDRs: 0.5 and 0.25. Correct: 0.25 and 0.25. With the unchanged standard sampler and seed 17: original 0.44/0.22, corrected 0.22/0.22 (`standard.*.json`).
- **Fix:** use the last rank of the tie for both the FDR denominator and the reported expected false positives; scan tie endpoints once. Non-tied FDR control is unchanged.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf), local POD `TermFinder.pm:473–480, 573–578`: count real hypotheses as good or better than the cutoff. Python recomputes all null p-values from each recorded draw, then counts all real hypotheses at the cutoff.
- **Effect:** reported FDR depends on GO-ID tie ordering and can be inflated for early members of a tie. **Confidence: high.** This package implements a simulation estimator, not BH; replacing it with BH would change the method. A separate BH comparison is in `checks/coverage.json`.

### GTF-005 — Duplicate background names/aliases bias simulation sampling

- **Location:** `lib/GO/TermFinder.pm:1774`.
- **Wrong behavior:** background counts resolve and de-duplicate gene IDs, but the simulation pool uses the raw supplied names. A gene listed by ID and alias occupies two sampling slots; nominal two-gene draws can collapse to one gene.
- **Repro:** repro/GTF-005/run.sh. Four biological genes, but raw population `[g1, alias1, g2, g3, g4]`, where alias1 = g1. Under exhaustive index-subset cycles, corrected p changes from 300/1000 = 0.300 to 333/1000 = 0.333; FDR changes from 0.300 to 0.340 for the prescribed 50 draws. Exact uniform-subset null probability is 2/C(4,2) = 1/3. The finite 50/1000-draw values are not claimed to equal the limiting probability.
- **Fix:** build the sampling pool using the same ID resolution and de-duplication used for background counts.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf): simulations sample gene sets from the background. Python independently enumerates subsets of four distinct genes. With the unchanged random sampler and seed 17, corrected p is 0.308 before and 0.329 after; the patched output exactly matches the canonical unique-ID population. Unique-background normal control is unchanged.
- **Effect:** simulation-corrected p-values and FDR can depend on redundant spellings in the background. This differs from the index-sampling algorithm bias fixed in 0.83. **Confidence: high.**

### GTF-006 — Extra anonymous genes inflate direct aspect annotations

- **Location:** `lib/GO/TermFinder.pm:379`.
- **Wrong behavior:** after replacing aspect counts with direct annotations, adds every extra gene implied by `totalNumGenes` back to that direct count.
- **Repro:** repro/GTF-006/run.sh. Two explicit annotations to biological_process among four known genes; client supplies total N = 20. Original M = 18, p = 153/190 = 0.805263157894736. Correct direct M = 2, p = 1/190 = 0.00526315789473685.
- **Fix:** retain extra genes in population and unannotated counts, without inventing direct annotations to the aspect.
- **Reason / independent check:** 0.80 Changes and local `TermFinder.pm:1227–1232, 1288–1297, 1304–1320` specify that only direct aspect annotations are tested. [GAF, GO ID](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/#go-id-column-5) identifies the annotated term; no annotation row exists for these anonymous genes. Python counts direct rows and independently expands the denominator with unannotated entities.
- **Effect:** direct aspect enrichment can disappear when the user correctly supplies a larger total gene count. Other term counts in the normal input remain unchanged. **Confidence: high for inconsistency with the implemented direct-annotation definition.**

### GTF-007 — Obsolete status depends on tag order

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:310, 320`.
- **Wrong behavior:** `namespace` resets validity to true, resurrecting a term whose earlier tag was `is_obsolete: true`.
- **Repro:** repro/GTF-007/run.sh. Original `nodeFromId('GO:0000011')` returns an obsolete node. Correct: absent; the live root and other term remain present.
- **Fix:** retain a separate obsolete flag until the next term stanza. Conventionally ordered obsolete terms continue to be excluded.
- **Reason / independent check:** [OBO 1.2, is_obsolete and serializer conventions](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html). Parser acceptance must not depend on suggested serializer tag order. Python collects all stanza tags before filtering obsolete terms.
- **Effect:** obsolete terms can enter the graph and enrichment analysis with valid alternative tag layouts. **Confidence: high.**

### GTF-008 — Ignoring an ambiguous alias deletes the preceding valid gene

- **Location:** `lib/GO/TermFinder.pm:1111–1123, 1176–1198`.
- **Wrong behavior:** ambiguous-alias branch neither resets the previous `$databaseId` nor skips subsequent duplicate handling. That handling pops the most recently accepted gene.
- **Repro:** repro/GTF-008/run.sh. Query `[g1, g2, shared]`, with `shared` an alias for two other genes. Original accepted genes: `[g1]`, no result. Correct: `[g1,g2]`, p = 1/190; only `shared` is ignored.
- **Fix:** immediately continue after excluding an ambiguous alias.
- **Reason / independent check:** the documented ambiguity policy in local `TermFinder.pm:1109–1118` excludes the ambiguous alias; it does not authorize deleting another gene. Python constructs the name-to-ID relation independently and excludes names with multiple targets.
- **Effect:** list-order-dependent sample size, lost enrichment, and wrong gene membership. Distinct from RT #77197, which concerns case-insensitive standard-name lookup. **Confidence: high.**

### GTF-009 — Typedef stanzas terminate the entire ontology parse

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:285`.
- **Wrong behavior:** stops at the first `[Typedef]`, ignoring all later terms.
- **Repro:** repro/GTF-009/run.sh. Put a valid `part_of` definition before the terms. Original: all three queried nodes absent. Correct: all three present, with the same GO graph as when the definition is last.
- **Fix:** finish the preceding term and skip non-term stanza contents, then resume at the next term; do not stop parsing the file.
- **Reason / independent check:** [OBO 1.2, stanza conventions](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) actually recommends typedefs before terms. Python discovers term stanzas independently of typedef placement.
- **Effect:** a correctly formatted ontology can load as an empty or incomplete graph. **Confidence: high.**

### GTF-010 — Cyclic ontology input causes uncontrolled recursion

- **Location:** `lib/GO/OntologyProvider/OboParser.pm:616–630`.
- **Wrong behavior:** recursively extends paths without detecting revisited nodes.
- **Repro:** repro/GTF-010/run.sh. GO:0000011 is_a GO:0000012 and vice versa. Original warns of deep recursion and returns no result before the 0.5-second watchdog kills it; output is in `before.txt`. Patched: promptly exits nonzero with `Cycle in ontology involving ...` (`after.txt`).
- **Fix:** reject a path that revisits its originating node or an existing ancestor.
- **Reason / independent check:** [Boyle et al. 2004](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf) requires a DAG; [OBO parser requirements](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html) require graceful failure. A separate Python DFS detects the cycle directly from the edge list. The valid diamond-DAG output is byte-identical.
- **Effect:** malformed user ontologies can hang or exhaust resources instead of producing a useful rejection. This is an invalid-input robustness defect, not a wrong p-value on a valid GO DAG. **Confidence: high.**

### Suspected / not promoted to bugs

- Native boundary validation beyond feasible observed count tables is incomplete by inspection (negative arguments, N larger than the constructor cache, and a zero-sized cache). No demonstrated valid enrichment call reaches these cases; no additional correctness claim or patch is made.
- General OBO escaping, imports, trailing modifiers, and relation types beyond is_a/part_of were not exhaustively tested. No failure is claimed without a repro.
- No representable-tail numerical failure was found in the tested grid and extreme cases. `checks/numeric.json` records 23,761 exact-reference comparisons; worst relative error was 4.86e-9. Four true tails below binary64 range return zero. This is a floating-point range limitation, not a new bug claim.

### Known issues excluded

- RT #102758: long-double Perl test comparisons; #102757: compiler detection; #77197: case-insensitive standard-name lookup (ticket body concerns `databaseIdByStandardName`, despite its title); #13361: GO::View clipping. Archived ticket bodies were read and stored locally.
- Resolved RT #33010: zero-hypothesis crash; #30861: native test failure; #6779: capitalization typo. These are excluded; GTF-003 concerns one hypothesis, not zero.
- Changes 0.86 p-value ceiling; 0.84 invalid-observation checks; 0.83 random-index bias; 0.81 casing fixes and cross-aspect error diagnostics; 0.80 earlier Bonferroni multiplier bug. None is claimed as a new discovery here.
- Flight and Wentzell (2009), [Potential Bias in GO::TermFinder](https://doi.org/10.1093/bib/bbn054), reports the sampling-algorithm bias fixed in 0.83. GTF-005 instead concerns inconsistent normalization of the supplied population in 0.86.
- Evidence-code inclusion/exclusion is explicitly a TODO in `AnnotationParser.pm:116–129`; the parser includes IEA by default and has no implemented evidence-filter API. This is not reported as a newly discovered defect. Filtering must be performed on the input annotations.
- BH is not implemented or promised by this version. BH and the documented simulated FDR differ by design; that difference is not a bug. Bonferroni's data-dependent family/filtering choices are described by the authors; this job does not claim a new FWER guarantee for them.

## Prior Art

_Source: [friends/sherlock-go-termfinder/PRIOR_ART.md](friends/sherlock-go-termfinder/PRIOR_ART.md)_

## Source and prior-report check

Checked locally on 2026-11-06. No public changes or communications were made.

### Canonical source

The [paper's Sherlock-lab copy](https://web.stanford.edu/group/sherlocklab/pdfs/TERMFINDER_BOYLE_BIOINFORMATICS_2004.pdf) identifies CPAN as the distribution location. [MetaCPAN's latest release API](https://fastapi.metacpan.org/v1/release/GO-TermFinder) selects SHERLOCK's GO-TermFinder-0.86 archive, released 2009-11-19. Used that author's archive rather than a downstream modified installation. The archive, original Changes, API response, and module hashes are retained in `sources/` and `SOURCE.json`.

The API's `version` field is stale at 0.85; `name`, download URL, distribution `VERSION`, module version, and Changes identify 0.86. This metadata inconsistency is not reported as a software correctness bug.

GitHub repository search for GO-TermFinder found [gitpan/GO-TermFinder](https://github.com/gitpan/GO-TermFinder), a read-only release-history mirror, and an unrelated experiment repository. No Sherlock-lab-maintained GitHub mirror was found. Recorded gitpan HEAD `414c6cd22b8ec6eec90a2f22f3b7f83d26d94ba6`; its TermFinder.pm is byte-identical to the CPAN file. It is not treated as an independently maintained newer release.

Also inspected the three relevant downstream modules in [princeton-genomics/GO-Tools](https://github.com/princeton-genomics/GO-Tools), which explicitly depends on 0.86 and carries modified copies. Their source still contains the relevant NOT equality test, raw alternate-ID counting, one-hypothesis Bonferroni guard, raw population sampling, rank denominator, ambiguity fall-through, obsolete-order dependence, and early typedef termination. This downstream project is not identified as a Sherlock-lab mirror. Its downloaded source and HEAD metadata are retained in `prior-art/`.

### Changes read before correctness experiments

The entire `sources/GO-TermFinder-0.86/Changes` was read. Excluded fixes already described there: 0.86 rounding ceiling; 0.84 invalid hypergeometric observations; 0.83 random-index sampling bias; 0.81 case-sensitive/case-insensitive ambiguity handling and diagnostics; 0.80 earlier Bonferroni correction and zero-hypothesis handling; older annotation API capitalization typos. GTF-005 concerns the supplied sampling population, not the random-index algorithm already repaired in 0.83.

### RT and GitHub issues

[Live RT queue](https://rt.cpan.org/Public/Dist/Display.html?Name=GO-TermFinder) and public/REST alternatives returned HTTP 202, zero bytes, `x-amzn-waf-action: challenge`. This prevented reading the live tickets before experimentation; the limitation was recorded in STATUS.md before tests. Gitpan's all-state issue API returned an empty list (`prior-art/gitpan-issues.json`).

Recovered the [2021 active queue snapshot](https://web.archive.org/web/20210519024220/https://rt.cpan.org/Public/Dist/Display.html?Name=GO-TermFinder) and archived bodies of all four active tickets. Read them before finalizing the bug list:

| Ticket | Existing report | Treatment |
| --- | --- | --- |
| [102758](https://rt.cpan.org/Public/Bug/Display.html?id=102758) | Native tests compare Perl long-double values with C++ double results too strictly | Excluded |
| [102757](https://rt.cpan.org/Public/Bug/Display.html?id=102757) | FreeBSD ships clang++ but build searches for g++ | Excluded |
| [77197](https://rt.cpan.org/Public/Bug/Display.html?id=77197) | Case-insensitive standard-name lookup; body identifies wrong final return in `databaseIdByStandardName` | Excluded; GTF-008 is a separate stale-ID/pop bug |
| [13361](https://rt.cpan.org/Public/Bug/Display.html?id=13361) | GO::View arbitrarily limits displayed top nodes | Excluded |

Bodies: `prior-art/rt-<ID>.html` and readable `.txt`. The archived resolved queue lists #33010 (zero hypotheses), #30861 (native test), #6779 (capitalization typo); excluded those subjects too. Live MetaCPAN's distribution response reports four active and three closed tickets, matching the archived counts, but matching counts do not establish current ticket identity or freshness.

### Literature / format references

- Boyle et al. (2004), [GO::TermFinder](https://doi.org/10.1093/bioinformatics/bth456): hypergeometric tail, gene sampling, and simulated correction definitions. Official lab PDF retained as `prior-art/Boyle-2004.pdf`.
- Flight & Wentzell (2009), [Potential Bias in GO::TermFinder](https://doi.org/10.1093/bib/bbn054): existing incorrect random-index sampling, repaired in 0.83. Excluded as an already reported finding.
- [GAF 2.1](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/) and [GAF 2.2](https://geneontology.org/docs/go-annotation-file-gaf-format-2.2/): pipe-separated NOT qualifiers/relations and annotation columns. Copies retained locally.
- [OBO 1.2 specification](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html): alternate IDs, obsolete status, stanza order, and graceful parser failure. Copy retained locally.

Targeted web searches for GO-TermFinder with NOT qualifiers, alternate IDs, FDR ties, supplied gene totals, and existing bugs found the original papers, Changes, and downstream documentation, but no matching report for these ten repros. This is a bounded check, not proof of absence from all prior literature or tickets. No NOTE-track paper or scientific novelty claim is made; a cited-by literature audit for a new paper was not attempted.

---

# Marcel Salathé — COVID-Twitter-BERT and lab repos

Folder: [friends/salathe-covid-twitter-bert](friends/salathe-covid-twitter-bert)

## Verdicts

_Source: [friends/salathe-covid-twitter-bert/VERDICTS.md](friends/salathe-covid-twitter-bert/VERDICTS.md)_

## Referee verdicts

All six failures reproduced from independently downloaded, unpatched pinned source. Three are **CONFIRMED**, two **CONFIRMED-MINOR**, and one **KNOWN** because its EOF-loss mechanism and empty-list crash have upstream history. The five non-KNOWN findings survive as software defects within the limits below. **NEW: no** under Ricardo's paper-result definition: no printed score was beaten, open scientific problem settled, or prediction tested on new data.

| ID | Verdict | My repro | Effect on users' results |
|---|---|---|---|
| CT001 | **CONFIRMED** | driver, result, batch input | Text exceeding the sequence budget produces inconsistent tensor lengths; an ordinary mixed text-file batch fails before prediction. |
| CT002 | **CONFIRMED-MINOR** | driver, result | The documented, default-enabled So-removal option leaves residual non-emoji symbols in model inputs; downstream prediction changes are unmeasured. |
| CT003 | **CONFIRMED** | driver, result, traceback | Numeric TSV labels make fine-tuning data generation crash before any training records are written. |
| FR001 | **CONFIRMED** | driver, result | Product-detail calls, including the bundled demo's call, omit the ID and cannot select the requested product resource. |
| FR002 | **CONFIRMED-MINOR** | driver, result | A scalar include option throws before any request; arrays work, and scalar support is described only in a helper comment in this alpha example. |
| PV001 | **KNOWN** | driver, result, current upstream comparison | A one-iteration log loses both output rows and crashes CSV export; this is an inherited Caffe EOF-loss edge case with prior reports, and the archived full log exports normally. |

### Ranked for Ricardo to read before any author contact

1. **CT001 — prediction input construction.** A single over-budget line can abort a whole mixed prediction batch. Reproduced at the shipped 96-token setting, not just an artificial small budget. It also appears unchanged in the README-linked TensorFlow notebook's prediction helper. This affects the repository's TensorFlow input code; it does not establish a failure of Hugging Face's tokenizer or model.
2. **CT003 — numeric-label data preparation.** Numeric class labels are a normal representation in the documented TSV schema, which imposes no alphabetic-label restriction. The actual main/processor/converter fails with `KeyError`, whereas the matching textual-label control writes valid records. This blocks preparing a user's dataset, rather than silently changing a paper score.
3. **FR001 — product IDs discarded.** Every nonempty-ID detail call takes the same path, including the demo linked from the API docs. This is a direct failure of the example's principal lookup operation. Its reach is limited to this bundled alpha JavaScript client; no server-side API defect is established.
4. **CT002 — ineffective default cleaning option.** The promise to remove Unicode category So is explicit in CLI help and the README command. The comparison is always false. Common emoji are converted earlier, so the independently demonstrated residual symbols are a narrower case; no checkpoint-quality improvement is asserted.
5. **FR002 — scalar include throws.** Reproducible through the public `Endpoint.product` method, consistent with the helper's stated value-or-list contract, but absent from the bundled demo and with a simple array workaround. Report alongside FR001 if the example is to be maintained.

**PV001 is not on the author shortlist.** Its one-iteration failure is real and would otherwise be CONFIRMED-MINOR, but known upstream EOF-loss and empty-list-export reports must accompany it. No inference is made about whether Marcel would care; Ricardo reads first, then the friend decides. Nobody has been contacted.

### Independent observations and normal-use checks

**CT001.** At [run_predict.py:77](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/run_predict.py#L77), the slice adds two to the sequence budget before two special tokens are added. The correct 96-position layout is `[CLS]`, at most 94 wordpieces, `[SEP]`, then padding if needed. My independent vocabulary-line oracle uses the word `patient`: 3 and 94 words give correct lengths `[96,96,96]`; 95 give `[97,97,96]`; 140 give `[100,100,96]`. The original file generator with a short and long line throws TensorFlow `InvalidArgumentError` while stacking word IDs. CLI help explicitly supports arbitrary `--input_text`, one-example-per-line `--input_txt_files`, and interactive input; the preparation default and README example use 96. The notebook helper has the same AST. No model weights or full classifier run were needed to demonstrate the malformed inputs and batch crash.

**CT002.** At [utils/preprocess.py:69](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/utils/preprocess.py#L69), a one-character category prefix is compared with the two-character `So`. By hand, `Near⌂home ∑ $ 12 café!` must become `Nearhome ∑ $ 12 café!`; the helper returns it unchanged. Actual default preprocessing produces `near⌂home ∑ $ 12 café!`, still retaining HOUSE, and retains BLANK SYMBOL in `A␢B`. Both characters have category So and survive the preceding emoji conversion. A plain accented/math/currency/punctuation control agrees with its manually specified expected output. CLI help at create_finetune_data.py:176 explicitly promises So removal, with default True. This is a real contract violation, not evidence that removing these symbols improves a trained model; training/inference cleaning would need to stay consistent.

**CT003.** At [create_finetune_data.py:145](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/preprocess/create_finetune_data.py#L145), pandas infers numeric labels. My three training rows use labels `2,7,2`, with two development rows. Stdlib CSV independently yields the label names `["2","7"]` and training IDs `[0,1,0]`; the original main instead writes mapping `[2,7]`, and the pinned converter looks up string `'2'` in an integer-keyed map and crashes. The training TFRecord is empty. A textual control with `class_a,class_b,class_a` succeeds and its real serialized labels are `[0,1,0]`. The README documents this id/label/text TSV layout and arbitrary custom datasets. No documented requirement rules out numeric class names. The provided COVID Category dataset uses text names; there is no claim that its paper experiment crashed or used this numeric representation.

**FR001.** At [foodrepo_api_v3.js:114](https://github.com/digitalepidemiologylab/foodrepo_api/blob/61b437d948e6c21acfedcc49aa8ff6dde2a1b945/v3/code/javascript/foodrepo_api_v3.js#L114), a nonempty ID appends only `/`. My independent calls for IDs 731 and 902 both record `/api/v3/products/?`; the cloned curl docs specify `/api/v3/products/{ID}`, so their requested resources differ. A normal listing still records page number and page size. The v3 README links the JavaScript example; index.html loads this file; helper_v3.js:73 calls `endpoint.product(product0.id, null, ...)`. Thus the trigger is in the bundled normal demo, not just a speculative caller. Transport was recorded locally; whether the live server answers this malformed detail call with a collection or an error remains untested.

**FR002.** At [foodrepo_api_v3.js:27](https://github.com/digitalepidemiologylab/foodrepo_api/blob/61b437d948e6c21acfedcc49aa8ff6dde2a1b945/v3/code/javascript/foodrepo_api_v3.js#L27), scalar normalization is assigned to an unused variable. `product(731, 'nutrients', callback)` throws `TypeError: values.map is not a function` and sends zero requests; `['nutrients']` sends a request with `include=nutrients`, matching an independent URLSearchParams construction. The helper comment explicitly says value or list; the exposed Endpoint accepts includes, but has no separate scalar-form docs and the demo passes null. The file labels itself a draft/ALPHA. This warrants a minor classification. FR001 is independent and still affects the array-form detail URL.

**PV001.** At [parse_log.py:132](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis/blob/90dd7555352a77e427918c124306780e0951f46d/googLeNet/color-80-20/finetune/results/parse_log.py#L132), parsing finishes without appending pending train/test rows. The hand-written four-line fixture explicitly contains a solver start, an iteration/lr line, a training output and a test output: expected 1/1 rows, observed 0/0; CSV export then raises `IndexError` at line 219. Adding a second iteration yields 2/2 rows and valid CSVs. All 62 parser copies are byte-identical by independently computed SHA-256. The README's normal result workflow invokes this parser, whose help imposes no minimum-iteration restriction, so a short/interrupted run is a legitimate edge case. The shipped full log yields 602/31 rows and exports normally; this is not evidence of an error in the published results.

The parser's stated upstream source has a [2014 EOF-row-loss report](https://github.com/BVLC/caffe/pull/1547#issuecomment-67324321) and [maintainer acknowledgement](https://github.com/BVLC/caffe/pull/1547#issuecomment-67342408). The later fix handles normal multi-row logs but leaves this single-iteration remainder. That precise fixture was not shown in the old discussion, so KNOWN here means an inherited, already-reported mechanism, not proof that the lab received this exact report. Current Caffe reproduces the same 0/0 row loss; [Caffe #3292](https://github.com/BVLC/caffe/pull/3292) separately fixed empty-list CSV crashing upstream. The lab copy lacks that guard. Calling the combination a fresh lab discovery would omit material prior history.

### Current status, authorship, and limits

Source and paper references establish Salathé as coauthor for all three associated papers and the paper-to-repository connections. The affected file:line statements above were checked against fresh pinned source; numbered excerpts are in cited-source-lines.txt.

Read-only `gh api` checks covered all visible open/closed issues and PRs with discussions, recent commits, every current repository branch's affected files, and every open PR's changed files. All three tested pins remain default-branch heads. None of the five non-KNOWN defects is described or fixed in those retrieved histories/branches; none of the repos publishes a newer GitHub release. Full details and scope limits are in SOURCES.md; private knowledge is untestable.

The documented CT-BERT TensorFlow 2.2 install fails on this Mac. The independent tests use real TensorFlow 2.16.2 with the original pinned models converter/tokenizer; full preprocessing restores only a removed HTML-unescape API. PlantVillage/Caffe source uses Python 2, so only print syntax and tab indentation were adapted in memory. No source patch was applied. Reproduction instructions describe every substitution and expected-answer construction. These observations support local correctness verdicts, not an unqualified reproduction of the historical cloud/TPU/Caffe environments. No model training, checkpoint download, authenticated API call, public write, or contact occurred.

## Repositories

_Source: [friends/salathe-covid-twitter-bert/REPOSITORIES.md](friends/salathe-covid-twitter-bert/REPOSITORIES.md)_

## Public-repository survey — 2026-11-06

Surveyed all 93 public repositories returned by the GitHub organization endpoint (one page of 100). Screened repository descriptions and available READMEs, and inspected paper/manuscript links. Historical `salathegroup` repository URLs resolve into `digitalepidemiologylab`; both old account listing endpoints return 404. See the saved API responses in `survey/`.

“Most used” is operationalized as GitHub stars, with forks shown as supporting context; these are popularity proxies, not download or active-user counts. Last commit means the default-branch HEAD committer date, not `pushed_at` (which can reflect PR activity). Dates are UTC. Inventory snapshots include hashes in `survey/inventory.json`.

### Selected runnable projects

1. **COVID-Twitter-BERT — 184 stars, 28 forks.** Highest-starred qualifying project; ships tokenization, preprocessing, training and inference code. Test input preparation and label handling without downloading the large model.
2. **PlantVillage analysis — 107 stars, 78 forks.** Runnable Caffe configurations and analysis scripts, explicitly the paper’s code release. Test analysis on tiny logs/HDF5 data without training Caffe.
3. **FoodRepo API — 63 stars, 6 forks.** The paper cites this repository’s executable client examples. It includes runnable JavaScript, Python, R and Ruby, in addition to dumps; it is not a data-only repository. Test request construction with a local XHR recorder, requiring no API account.

VaxGame has 85 stars/40 forks but its README identifies an outreach game developed by Ellsworth Campbell, and the paper search did not establish a Salathé-authored paper tied to this code. It is excluded on that evidence limit, not because of a guess about interest. The 59-star PlantVillage dataset is a data release. Neither outranks FoodRepo among established runnable paper-linked candidates.

### Established paper links (Salathé is a coauthor)

| Repository | Paper | Stars | Last commit | Role |
|---|---|---:|---|---|
| [covid-twitter-bert](https://github.com/digitalepidemiologylab/covid-twitter-bert) | [COVID-Twitter-BERT: A Natural Language Processing Model to Analyse COVID-19 Content on Twitter](https://arxiv.org/abs/2005.07503) | 184 | 2022-06-20 | model / training / preprocessing / inference code; SELECTED |
| [plantvillage_deeplearning_paper_analysis](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis) | [Using Deep Learning for Image-Based Plant Disease Detection](https://doi.org/10.3389/fpls.2016.01419) | 107 | 2016-08-15 | training configurations and executable analysis; SELECTED |
| [foodrepo_api](https://github.com/digitalepidemiologylab/foodrepo_api) | [FoodRepo: An Open Food Repository of Barcoded Food Products](https://doi.org/10.3389/fnut.2018.00057) | 63 | 2020-08-24 | runnable JS/Python/R/Ruby API clients and examples, plus data; SELECTED |
| [plantvillage_deeplearning_paper_dataset](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_dataset) | [Using Deep Learning for Image-Based Plant Disease Detection](https://doi.org/10.3389/fpls.2016.01419) | 59 | 2016-09-02 | image dataset; excluded from runnable-code selection |
| [crowdbreaks](https://github.com/digitalepidemiologylab/crowdbreaks) | [Crowdbreaks: Tracking Health Trends Using Public Social Media Data and Crowdsourcing](https://doi.org/10.3389/fpubh.2019.00081) | 12 | 2023-05-25 | platform code |
| [crowdbreaks-paper](https://github.com/digitalepidemiologylab/crowdbreaks-paper) | [Crowdbreaks: Tracking Health Trends Using Public Social Media Data and Crowdsourcing](https://doi.org/10.3389/fpubh.2019.00081) | 12 | 2020-05-19 | paper-specific code and data |
| [vaccine-sentiment](https://github.com/digitalepidemiologylab/vaccine-sentiment) | [Assessing Vaccination Sentiments with Online Social Media: Implications for Infectious Disease Dynamics and Control](https://doi.org/10.1371/journal.pcbi.1002199) | 12 | 2011-10-17 | paper-specific collection / classification code |
| [concept_drift_paper](https://github.com/digitalepidemiologylab/concept_drift_paper) | [Addressing machine learning concept drift reveals declining vaccine sentiment during the COVID-19 pandemic](https://arxiv.org/abs/2012.02197) | 6 | 2020-12-07 | paper code; README uses the earlier title How machine learning concept drift can negatively affect social media analysis |
| [experts-covid19-twitter](https://github.com/digitalepidemiologylab/experts-covid19-twitter) | [Experts and Authorities Receive Disproportionate Attention on Twitter During the COVID-19 Crisis](https://arxiv.org/abs/2008.08364) | 4 | 2020-11-10 | annotation data, model references and inference examples |
| [swisscovid_efficacy](https://github.com/digitalepidemiologylab/swisscovid_efficacy) | [Early Evidence of Effectiveness of Digital Contact Tracing for SARS-CoV-2 in Switzerland](https://doi.org/10.1101/2020.09.07.20189274) | 4 | 2020-09-19 | manuscript repository; not runnable code |
| [aerosol](https://github.com/digitalepidemiologylab/aerosol) | [Assessing the Dynamics and Control of Droplet- and Aerosol-Transmitted Influenza Using an Indoor Positioning System](https://doi.org/10.1038/s41598-019-38825-y) | 3 | 2020-01-13 | simulation / analysis code and data |
| [postprandial-glucose-traits-analyses](https://github.com/digitalepidemiologylab/postprandial-glucose-traits-analyses) | [Short-term postprandial glucose monitoring reveals stable traits from noisy free-living meals](https://doi.org/10.64898/2026.09.14.26362991) | 3 | 2026-09-09 | analysis notebooks / prepared inputs |
| [SocialContagion](https://github.com/digitalepidemiologylab/SocialContagion) | [Complex social contagion makes networks more vulnerable to disease outbreaks](https://arxiv.org/abs/1211.0518) | 2 | 2013-03-01 | simulation code and manuscript |
| [llm_crowd_experts_annotation](https://github.com/digitalepidemiologylab/llm_crowd_experts_annotation) | [Use of large language models as a scalable approach to understanding public health discourse](https://doi.org/10.1371/journal.pdig.0000631) | 2 | 2024-11-25 | analysis code and partial public annotation data |
| [vaccinationcontagionEPJDataScience](https://github.com/digitalepidemiologylab/vaccinationcontagionEPJDataScience) | [The dynamics of health behavior sentiments on a large online social network](https://doi.org/10.1140/epjds16) | 2 | 2013-04-04 | Java/SAS analysis code and data |
| [Collocation](https://github.com/digitalepidemiologylab/Collocation) | [A low-cost method to assess the epidemiological importance of individuals in controlling infectious disease outbreaks](https://doi.org/10.1186/1741-7015-11-35) | 1 | 2012-12-05 | simulation / collocation ranking scripts and matching input files |
| [FoodAndYou-PLOSDigitalHealth](https://github.com/digitalepidemiologylab/FoodAndYou-PLOSDigitalHealth) | [Food & You: A digital cohort on personalized nutrition](https://doi.org/10.1371/journal.pdig.0000389) | 1 | 2023-10-30 | R/Quarto figure code and aggregate data |
| [dietary-consistency-and-quality-associated-with-gut-microbiota-diversity-paper](https://github.com/digitalepidemiologylab/dietary-consistency-and-quality-associated-with-gut-microbiota-diversity-paper) | [Temporal nutrition analysis associates dietary regularity and quality with gut microbiome diversity: insights from the Food & You digital cohort](https://doi.org/10.1038/s41467-025-63799-z) | 1 | 2026-05-12 | analysis code and available data |
| [global-commons](https://github.com/digitalepidemiologylab/global-commons) | [Governing the Global Commons with Local Institutions](https://doi.org/10.1371/journal.pone.0034051) | 1 | 2012-04-17 | Java simulation code; paper named in repo description |
| [meal-pattern-analysis-paper](https://github.com/digitalepidemiologylab/meal-pattern-analysis-paper) | [Meal timing associations on dietary quality and glucose response](https://doi.org/10.1038/s44528-026-00033-2) | 1 | 2026-07-14 | analysis notebooks; README retains working title |
| [w3cRio](https://github.com/digitalepidemiologylab/w3cRio) | [Validating Models for Disease Detection Using Twitter](https://citeseerx.ist.psu.edu/document?doi=ef0f25bad89a16a43912a3296a36501b7bf9ad4c&repid=rep1&type=pdf) | 1 | 2014-01-28 | analysis material; README calls it Validating Methods |
| [UHS-Analysis](https://github.com/digitalepidemiologylab/UHS-Analysis) | [On the Ground Validation of Online Diagnosis with Twitter and Medical Records](https://doi.org/10.1145/2567948.2579272) | 0 | 2014-02-14 | analysis code and included manuscript source |
| [content_changes_paper](https://github.com/digitalepidemiologylab/content_changes_paper) | [Dynamics of social media behavior before and after SARS-CoV-2 infection](https://doi.org/10.3389/fpubh.2022.1069931) | 0 | 2023-01-17 | analysis / text-processing code |
| [covid-sources-timeliness](https://github.com/digitalepidemiologylab/covid-sources-timeliness) | [Timeliness of online COVID-19 reports from official sources](https://doi.org/10.3389/fpubh.2022.1027812) | 0 | 2022-11-07 | analysis code and data |
| [food-additives-gut-microbiota-public](https://github.com/digitalepidemiologylab/food-additives-gut-microbiota-public) | [Food additive exposure associated with reduction in gut microbiota diversity](https://doi.org/10.64898/2026.06.22.26356234) | 0 | 2026-01-22 | analysis code |
| [llm_benchmarking](https://github.com/digitalepidemiologylab/llm_benchmarking) | [Open-source solution for evaluation and benchmarking of large language models for public health](https://doi.org/10.1101/2025.03.20.25324040) | 0 | 2025-05-18 | R/Shiny benchmarking code and data |
| [mindays-estimation-paper](https://github.com/digitalepidemiologylab/mindays-estimation-paper) | [Minimum days estimation for reliable dietary intake information: findings from a digital cohort](https://doi.org/10.1038/s41430-025-01644-8) | 0 | 2025-03-27 | analysis notebooks |
| [network_assortativity_paper](https://github.com/digitalepidemiologylab/network_assortativity_paper) | [Positive Network Assortativity of Influenza Vaccination at a High School: Implications for Outbreak Risk and Herd Immunity](https://doi.org/10.1371/journal.pone.0087042) | 0 | 2017-06-29 | raw network data; not runnable-code target |
| [vaccine_sentiment_england](https://github.com/digitalepidemiologylab/vaccine_sentiment_england) | [Keep calm and carry on vaccinating: Is anti-vaccination sentiment contributing to declining vaccine coverage in England?](https://graphsearch.epfl.ch/en/publication/007ebfac-e128-41dc-9275-48da96ff935b) | 0 | 2019-12-23 | analysis code and aggregate data |

The UHS manuscript is saved at `survey/UHS-Analysis/paper.tex`; its title/authors and DOI are in that source. The Collocation association uses the named collocation method, the matching released scripts/data, and the source paper. Missing root READMEs are preserved as API 404 responses, not treated as evidence of absence of code.

### Related code/components — indirect paper associations

These project links are weaker than explicit paper data/code citations and do not alter the top-three selection.

| Repository | Related paper project | Stars | Last commit | Evidence / role |
|---|---|---:|---|---|
| [crowdbreaks-streamer-v1](https://github.com/digitalepidemiologylab/crowdbreaks-streamer-v1) | crowdbreaks | 6 | 2021-02-28 | platform stream processor; project association, not separately cited paper code |
| [caffe](https://github.com/digitalepidemiologylab/caffe) | plantvillage_deeplearning_paper_analysis | 4 | 2016-03-09 | framework fork referenced in paper; master is not proof of historical experiment branch |
| [PlantVillage-Analysis-Caffe](https://github.com/digitalepidemiologylab/PlantVillage-Analysis-Caffe) | plantvillage_deeplearning_paper_analysis | 3 | 2016-03-16 | earlier PlantVillage configuration repository; association inferred from project/files |
| [crowdbreaks-streamer](https://github.com/digitalepidemiologylab/crowdbreaks-streamer) | crowdbreaks | 2 | 2022-11-29 | platform stream processor; later implementation |
| [text-classification](https://github.com/digitalepidemiologylab/text-classification) | concept_drift_paper | 2 | 2022-02-24 | classification component; the paper repo has this as a submodule |
| [crowdbreaks-welcome](https://github.com/digitalepidemiologylab/crowdbreaks-welcome) | crowdbreaks | 1 | 2020-10-26 | project documentation, not runnable code |
| [plantvillage-analysis-env](https://github.com/digitalepidemiologylab/plantvillage-analysis-env) | plantvillage_deeplearning_paper_analysis | 1 | 2016-02-19 | Vagrant environment; project association inferred |
| [covid-scraper](https://github.com/digitalepidemiologylab/covid-scraper) | covid-sources-timeliness | 0 | 2022-08-23 | web scraper explicitly linked from the paper repository |
| [llm-prediction-tool](https://github.com/digitalepidemiologylab/llm-prediction-tool) | llm_benchmarking | 0 | 2025-03-20 | prediction prototype explicitly linked from the paper repository |
| [myfoodrepo_project](https://github.com/digitalepidemiologylab/myfoodrepo_project) | foodrepo_api | 0 | 2022-04-05 | link index also linking The Food Recognition Benchmark (10.3389/fnut.2022.875143); not executable analysis |
| [preprocess](https://github.com/digitalepidemiologylab/preprocess) | crowdbreaks | 0 | 2022-04-29 | platform data-processing component |

### Remaining repositories

No qualifying paper link/Salathé authorship was established for these within the survey. This is not a claim that none exists. The project descriptions are retained in the organization API snapshot. In particular, `brazil-vaccine-uptake` names a study topic but does not cite a paper, and `population-memetics` describes research in progress.

| Repository | Stars | Last commit |
|---|---:|---|
| [VaxGame](https://github.com/digitalepidemiologylab/VaxGame) | 85 | 2021-11-18 |
| [nodular.js](https://github.com/digitalepidemiologylab/nodular.js) | 12 | 2017-01-18 |
| [mkondo](https://github.com/digitalepidemiologylab/mkondo) | 5 | 2012-10-26 |
| [react-native-scandit](https://github.com/digitalepidemiologylab/react-native-scandit) | 5 | 2017-08-21 |
| [tweepy](https://github.com/digitalepidemiologylab/tweepy) | 4 | unavailable (fork/empty; not selected) |
| [covid-stream](https://github.com/digitalepidemiologylab/covid-stream) | 3 | 2020-05-06 |
| [openbeacon-case](https://github.com/digitalepidemiologylab/openbeacon-case) | 3 | 2016-02-01 |
| [population-memetics](https://github.com/digitalepidemiologylab/population-memetics) | 3 | 2012-03-22 |
| [COVID-documents](https://github.com/digitalepidemiologylab/COVID-documents) | 2 | 2020-04-22 |
| [MOOCnet](https://github.com/digitalepidemiologylab/MOOCnet) | 2 | 2013-08-16 |
| [google-images](https://github.com/digitalepidemiologylab/google-images) | 2 | unavailable (fork/empty; not selected) |
| [keyword_streamer](https://github.com/digitalepidemiologylab/keyword_streamer) | 2 | 2012-07-09 |
| [rails_ar_encryption](https://github.com/digitalepidemiologylab/rails_ar_encryption) | 2 | 2022-04-22 |
| [reverse-geocoder](https://github.com/digitalepidemiologylab/reverse-geocoder) | 2 | 2012-03-16 |
| [Minimal-Bag-of-Visual-Words-Image-Classifier](https://github.com/digitalepidemiologylab/Minimal-Bag-of-Visual-Words-Image-Classifier) | 1 | unavailable (fork/empty; not selected) |
| [VCFpreprocess](https://github.com/digitalepidemiologylab/VCFpreprocess) | 1 | 2016-10-03 |
| [Weighted_Network_Analysis](https://github.com/digitalepidemiologylab/Weighted_Network_Analysis) | 1 | unavailable (fork/empty; not selected) |
| [brazil-vaccine-uptake](https://github.com/digitalepidemiologylab/brazil-vaccine-uptake) | 1 | 2026-03-10 |
| [deep-height](https://github.com/digitalepidemiologylab/deep-height) | 1 | 2016-11-21 |
| [fuel](https://github.com/digitalepidemiologylab/fuel) | 1 | unavailable (fork/empty; not selected) |
| [pydeepgenomics](https://github.com/digitalepidemiologylab/pydeepgenomics) | 1 | 2017-01-26 |
| [sent2vec](https://github.com/digitalepidemiologylab/sent2vec) | 1 | unavailable (fork/empty; not selected) |
| [snakes](https://github.com/digitalepidemiologylab/snakes) | 1 | unavailable (fork/empty; not selected) |
| [twitter-visual](https://github.com/digitalepidemiologylab/twitter-visual) | 1 | 2012-08-25 |
| [2016_TwitterEpi](https://github.com/digitalepidemiologylab/2016_TwitterEpi) | 0 | 2017-09-20 |
| [Food-Repo-DNA-analysis-WIMF](https://github.com/digitalepidemiologylab/Food-Repo-DNA-analysis-WIMF) | 0 | 2021-10-04 |
| [JavaScriptAPIs_FoodRepo](https://github.com/digitalepidemiologylab/JavaScriptAPIs_FoodRepo) | 0 | 2019-11-27 |
| [JavaScriptAPIs_MyFoodRepo](https://github.com/digitalepidemiologylab/JavaScriptAPIs_MyFoodRepo) | 0 | 2019-10-28 |
| [JavaScriptAPIs_common](https://github.com/digitalepidemiologylab/JavaScriptAPIs_common) | 0 | 2019-09-03 |
| [Semester_Project](https://github.com/digitalepidemiologylab/Semester_Project) | 0 | 2018-01-11 |
| [Tweet_Filt](https://github.com/digitalepidemiologylab/Tweet_Filt) | 0 | 2017-09-13 |
| [barcode_test_swift](https://github.com/digitalepidemiologylab/barcode_test_swift) | 0 | 2016-02-11 |
| [coco-ui](https://github.com/digitalepidemiologylab/coco-ui) | 0 | unavailable (fork/empty; not selected) |
| [covid-stream-analysis](https://github.com/digitalepidemiologylab/covid-stream-analysis) | 0 | 2020-11-02 |
| [deepdetect](https://github.com/digitalepidemiologylab/deepdetect) | 0 | unavailable (fork/empty; not selected) |
| [deepimputation](https://github.com/digitalepidemiologylab/deepimputation) | 0 | 2016-11-07 |
| [django-tastypie](https://github.com/digitalepidemiologylab/django-tastypie) | 0 | unavailable (fork/empty; not selected) |
| [fastText](https://github.com/digitalepidemiologylab/fastText) | 0 | unavailable (fork/empty; not selected) |
| [grippenet](https://github.com/digitalepidemiologylab/grippenet) | 0 | 2017-01-23 |
| [hub](https://github.com/digitalepidemiologylab/hub) | 0 | unavailable (fork/empty; not selected) |
| [ladder](https://github.com/digitalepidemiologylab/ladder) | 0 | unavailable (fork/empty; not selected) |
| [lstm-char-cnn-tensorflow](https://github.com/digitalepidemiologylab/lstm-char-cnn-tensorflow) | 0 | unavailable (fork/empty; not selected) |
| [mini-challenges](https://github.com/digitalepidemiologylab/mini-challenges) | 0 | 2018-05-20 |
| [multi-lang-vaccine-sentiment](https://github.com/digitalepidemiologylab/multi-lang-vaccine-sentiment) | 0 | 2020-03-25 |
| [myfoodrepo-mask-rcnn](https://github.com/digitalepidemiologylab/myfoodrepo-mask-rcnn) | 0 | unavailable (fork/empty; not selected) |
| [nutrition-tracking-platform-v2](https://github.com/digitalepidemiologylab/nutrition-tracking-platform-v2) | 0 | 2025-04-16 |
| [paranoia](https://github.com/digitalepidemiologylab/paranoia) | 0 | unavailable (fork/empty; not selected) |
| [react-native-camera](https://github.com/digitalepidemiologylab/react-native-camera) | 0 | unavailable (fork/empty; not selected) |
| [rog-rl](https://github.com/digitalepidemiologylab/rog-rl) | 0 | 2024-04-08 |
| [swagger_engine](https://github.com/digitalepidemiologylab/swagger_engine) | 0 | unavailable (fork/empty; not selected) |
| [tensorflow_models_tf21](https://github.com/digitalepidemiologylab/tensorflow_models_tf21) | 0 | unavailable (fork/empty; not selected) |
| [twiprocess](https://github.com/digitalepidemiologylab/twiprocess) | 0 | 2022-08-16 |
| [vega-react-minimal-example](https://github.com/digitalepidemiologylab/vega-react-minimal-example) | 0 | 2018-05-29 |

### Pinned shallow clones

| Repository | Commit | Last commit |
|---|---|---|
| covid-twitter-bert | `86909698f104525b13d8ab0e22ae666e264ac5c6` | 2022-06-20T17:13:52+02:00 |
| foodrepo_api | `61b437d948e6c21acfedcc49aa8ff6dde2a1b945` | 2020-08-24T17:16:36+02:00 |
| plantvillage_deeplearning_paper_analysis | `90dd7555352a77e427918c124306780e0951f46d` | 2016-08-15T18:03:19+02:00 |

### Issues and PRs read before cloning

Fetched all open issues/PRs and up to 30 recent closed issues/PRs, sorted by last update, with issue comments and PR review comments/reviews. All selected projects have fewer than 30 closed entries, so this covers their complete visible histories. No open page reached the 100-entry limit. Raw responses are in `survey/<repo>/`.

| Repo | Open issues | Closed issues | Open PRs | Closed PRs |
|---|---:|---:|---:|---:|
| covid-twitter-bert | 6 | 12 | 2 | 10 |
| plantvillage_deeplearning_paper_analysis | 2 | 0 | 1 | 0 |
| foodrepo_api | 4 | 6 | 2 | 15 |

Dependency-bump PR release notes were screened by title/package/version; human issue bodies and discussion were read. Known issues excluded from the bug count are listed in `BUGS.md`.

## Bugs: pre-referee report; final dispositions above

_Source: [friends/salathe-covid-twitter-bert/BUGS.md](friends/salathe-covid-twitter-bert/BUGS.md)_

## Confirmed correctness bugs

Six defects, six private fixes. The three selected repositories, paper links, stars, issue histories and pinned commits are in [REPOSITORIES.md](friends/salathe-covid-twitter-bert/REPOSITORIES.md). Every repro runs the pinned source, records its failing output, applies its own minimal Git patch in a temporary local checkout, and compares the result against a separately written reference check. Ordinary inputs are compared before/after. The reference checks are separate implementations, not another person's review.

These are software-correctness findings. **NEW: no** under the stated paper-result definition: no printed benchmark number was beaten, open research problem settled, or scientific prediction tested on new data. No claim is made that the original paper results change. No training, large checkpoint download, authenticated FoodRepo request, or public write occurred.

### CT001 — prediction truncation reserves the special tokens with the wrong sign

- **Repo / pin:** `digitalepidemiologylab/covid-twitter-bert` @ `86909698f104525b13d8ab0e22ae666e264ac5c6`.
- **File:line:** [`run_predict.py:77`](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/run_predict.py#L77).
- **Wrong:** the branch for an overlong token sequence slices at `max_seq_length + 2`, then adds `[CLS]` and `[SEP]`. It must reserve two positions by slicing at `max_seq_length - 2`.
- **Repro:** repro/CT001/, run `./repro/CT001/run.sh`.
- **Before → after:** with a six-position configuration, five wordpieces yield word-ID/mask lengths 7 and segment-ID length 6; ten wordpieces yield lengths 10/10/6. After the one-line fix all three inputs have length 6 and the expected four-wordpiece prefix plus special tokens. Two- and four-wordpiece normal/boundary inputs are byte-for-byte unchanged.
- **Independent check:** a standard-library reference constructs expected token IDs from the shipped vocabulary and the six-position budget; it does not call the repo's tokenizer or input builder.
- **Effect:** overlength single-text, interactive and text-file prediction inputs violate the classifier's configured shapes. This can prevent predictions; it is not a measured change to a paper score. Real TensorFlow tensors and the exact pinned BERT tokenizer were used, with no model weights.
- **Confidence:** high for the input-construction defect. Full BERT/cloud inference was not run.

### CT002 — the Unicode-symbol removal option silently removes nothing

- **Repo / pin:** `covid-twitter-bert` @ `86909698f104525b13d8ab0e22ae666e264ac5c6`.
- **File:line:** [`utils/preprocess.py:69`](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/utils/preprocess.py#L69).
- **Wrong:** `unicodedata.category(ch)[0]` is one character, so it never equals the two-character category `So`. The CLI help explicitly says this option removes category `So`.
- **Repro:** repro/CT002/, run `./repro/CT002/run.sh`.
- **Before → after:** the helper returns `A℗B` and `A⏣B` unchanged before; after it returns `AB`. With default preprocessing options the corresponding results change from `a℗b` / `a⏣b` to `ab`. These non-emoji symbols survive the preceding emoji conversion. Ordinary text, accented letters, numbers, math signs and punctuation remain unchanged.
- **Independent check:** a separate character-by-character Unicode-category reference agrees with both the helper and the complete preprocessing function.
- **Effect:** users requesting symbol removal receive different model input text from the documented cleaning policy. Fixing this changes affected preprocessing and requires keeping training and inference preprocessing consistent; no benefit to an existing trained checkpoint is asserted.
- **Confidence:** high. The repro imports the actual preprocessing module; it restores only the documented Python-3.8 HTML-unescape API on the host Python 3.9.

### CT003 — numeric TSV class labels crash TFRecord generation

- **Repo / pin:** `covid-twitter-bert` @ `86909698f104525b13d8ab0e22ae666e264ac5c6`.
- **File:line:** [`preprocess/create_finetune_data.py:145`](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/preprocess/create_finetune_data.py#L145), feeding the mapping at lines 150–155 and `TextClassificationProcessor._create_examples`.
- **Wrong:** pandas infers numeric labels as integers, while the processor reads the emitted TSV labels as strings. The pinned TensorFlow-models converter indexes an integer-keyed label map with a string.
- **Repro:** repro/CT003/, run `./repro/CT003/run.sh`. Each train/dev split has only two rows in the documented `id / label / text` format.
- **Before → after:** labels `0,1` fail with `KeyError: '0'`; after requesting string dtype for the label column, the real writer emits two training TFRecords with label IDs `[0,1]` and label mapping `["0","1"]`. Normal `label_a,label_b` mapping and TFRecord label IDs are unchanged.
- **Independent check:** Python's CSV reader independently derives the textual label vocabulary and IDs, without pandas, TensorFlow or repo code.
- **Effect:** a common binary/numeric classification dataset cannot reach fine-tuning through the supplied preparation script. This is a data-preparation crash, not proof that the published datasets or scores were affected.
- **Confidence:** high. The repro runs the actual `main`, processor and pinned converter, and reads the serialized TFRecords. Runtime substitutions are documented in the repro README.

### FR001 — JavaScript product-detail requests omit the requested product ID

- **Repo / pin:** `digitalepidemiologylab/foodrepo_api` @ `61b437d948e6c21acfedcc49aa8ff6dde2a1b945`.
- **File:line:** [`v3/code/javascript/foodrepo_api_v3.js:114`](https://github.com/digitalepidemiologylab/foodrepo_api/blob/61b437d948e6c21acfedcc49aa8ff6dde2a1b945/v3/code/javascript/foodrepo_api_v3.js#L114).
- **Wrong:** a nonempty ID adds only `/` to `products`, never the ID. The bundled page itself calls `endpoint.product(product0.id, null, ...)`.
- **Repro:** repro/FR001/, run `./repro/FR001/run.sh`. A local XHR recorder captures the real client's outgoing request; no network request occurs.
- **Before → after:** `product(2663, null, callback)` targets `/api/v3/products/?` before and `/api/v3/products/2663?` after. The ordinary `products(2,5,callback)` listing request is identical before/after.
- **Independent check:** a separate Python REST-path check verifies the requested ID against the API's documented single-product resource pattern (also used by the bundled Python example).
- **Effect:** callers and the bundled demo fail to retrieve the requested product detail and may receive a collection or an error instead. The observed defect is request construction; live server behavior and any paper-level effect were not tested.
- **Confidence:** high.

### FR002 — a scalar include option crashes the JavaScript client

- **Repo / pin:** `foodrepo_api` @ `61b437d948e6c21acfedcc49aa8ff6dde2a1b945`.
- **File:line:** [`v3/code/javascript/foodrepo_api_v3.js:27`](https://github.com/digitalepidemiologylab/foodrepo_api/blob/61b437d948e6c21acfedcc49aa8ff6dde2a1b945/v3/code/javascript/foodrepo_api_v3.js#L27).
- **Wrong:** the helper promises a value or list of values. Its scalar branch stores `[values]` in an unused `includes` variable, then calls `.map` on the original scalar.
- **Repro:** repro/FR002/, run `./repro/FR002/run.sh`.
- **Before → after:** `product(2663, 'images', callback)` raises `TypeError: values.map is not a function`; after normalizing `values` itself, it constructs exactly the same query as `['images']`. Existing array/null calls are unchanged.
- **Independent check:** Python independently parses the recorded URL query and checks `include=images` plus scalar/list equivalence.
- **Effect:** a supported option form aborts before any request, preventing data retrieval. This patch is intentionally independent of FR001: its detail URL still has FR001's separate defect unless both patches are applied.
- **Confidence:** high for the helper's explicitly stated scalar/list contract. The JavaScript file describes itself as an alpha draft; no official deployed-client usage is asserted.

### PV001 — a one-iteration Caffe log loses its output rows and crashes CSV export

- **Repo / pin:** `digitalepidemiologylab/plantvillage_deeplearning_paper_analysis` @ `90dd7555352a77e427918c124306780e0951f46d`.
- **File:line:** [`googLeNet/color-80-20/finetune/results/parse_log.py:132`](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis/blob/90dd7555352a77e427918c124306780e0951f46d/googLeNet/color-80-20/finetune/results/parse_log.py#L132) (missing EOF flush); CSV export fails at line 219. The same parser is copied into 62 experiment folders, listed in the repro.
- **Wrong:** the first train/test row is retained in a local variable until another iteration establishes the row schema. EOF never flushes those remaining rows. A log containing one train and one test output at one iteration consequently returns two empty lists.
- **Repro:** repro/PV001/, run `./repro/PV001/run.sh`.
- **Before → after:** a valid four-line log returns 0 train / 0 test rows, and CSV export raises `IndexError: list index out of range`. After flushing pending rows at EOF, it writes 1 train / 1 test row. The ordinary two-iteration case is identical. The archived full Caffe log still produces 602 train / 31 test rows, with identical CSV bytes before/after.
- **Independent check:** a separate EOF/CSV check derives the expected iteration rows directly from the fixture's records. It imports no repo code. The patch changes only the same EOF handling in all 62 parser copies.
- **Effect:** short/debug/interrupted single-iteration runs cannot produce their analysis CSVs through the bundled parser. No effect on the published full-run results is demonstrated; the full archived run is explicitly unchanged.
- **Confidence:** high for the parser defect. Python-2 print syntax is converted in memory; the parsing logic is unchanged. Caffe itself and model training were not run.

## Suspected — not included in the confirmed count

- **CT-BERT training versus direct-text inference preprocessing:** `create_finetune_data.py` calls `preprocess_bert`, while `run_predict.py`'s text paths tokenize their input directly. This suggests that raw handles/URLs may be represented differently unless the caller already preprocesses them. No matched small trained checkpoint with an established raw-input contract was available under the checkpoint limit; no prediction failure or numerical effect was demonstrated, and no patch is supplied.
- **PlantVillage external-image preprocessing:** `googLeNet/segmented-80-20/test_bing/test_bing.prototxt` references an external-test mean file, while its training configuration references the PlantVillage mean. The means, original HDF5 predictions and weights are not released here. Different file paths alone do not prove different means or changed predictions. No confirmed bug or paper correction is claimed.

## Known issues and rejected candidates excluded

- **CT-BERT:** open issues [17](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/17) and [30](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/30) already concern dataset download / Colab errors. Closed [6](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/6) fixed malformed tweet IDs; [10](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/10) and [11](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/11) concern model conversion / historical Hugging Face weights; [5](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/5) concerns lowercasing; [12](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/12) concerns GPU memory. [21](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/21)'s multi-token COVID words are normal WordPiece behavior. Dependency bump PRs and the README's known TF 2.3 incompatibility are excluded.
- **PlantVillage:** [issue 1](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis/issues/1) already reports standard-Caffe HDF5Output incompatibility; [issue 2](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis/issues/2) reports broken external-image links. PR 3 changes the README. The suspected divisible-batch loss did **not** reproduce: unchanged constants 32,400 / 24 / 1,351 retain all 32,400 rows and discard only the extra repeated batch. Its speculative patch was withdrawn before application; the investigation is retained under `survey/suspected-PV-batch/`.
- **FoodRepo:** open [20](https://github.com/digitalepidemiologylab/foodrepo_api/issues/20) concerns nutrient/unit naming, [1](https://github.com/digitalepidemiologylab/foodrepo_api/issues/1) requests brand fields, [23](https://github.com/digitalepidemiologylab/foodrepo_api/issues/23) requests a new dump, and [28](https://github.com/digitalepidemiologylab/foodrepo_api/issues/28) requests an API key. Historical pagination [17](https://github.com/digitalepidemiologylab/foodrepo_api/issues/17), CORS [15](https://github.com/digitalepidemiologylab/foodrepo_api/issues/15), sorting [10](https://github.com/digitalepidemiologylab/foodrepo_api/issues/10), malformed-request [11](https://github.com/digitalepidemiologylab/foodrepo_api/issues/11) / [12](https://github.com/digitalepidemiologylab/foodrepo_api/issues/12), and deprecated-v2 problems are excluded. Python 3 conversion (PR 24) and dependency bumps are not new findings.

None of the six confirmed failures was described in the selected repositories' saved visible issue/PR histories. This is a scoped duplicate check, not a claim of worldwide priority.

---

# Victor Garcia — the NK-CTL model, VB10

Folder: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb10](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb10)

## Claim

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb10/CLAIM.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb10/CLAIM.md)_

## Claim victor_VB10 — sharp hyperbolic stable-equilibrium capacity

Status: exact within-run checks PASS; separate referee and Fable/Opus TASTE pending. This is a mathematical claim about a Garcia coauthored paper, not a priority or biological claim.

**Published starting point and location.** Garcia, Bonhoeffer and Fu2020, [DOI10.1016/j.jtbi.2020.110185](https://doi.org/10.1016/j.jtbi.2020.110185), printed Eqs21–23, Section2.3 and AppendixC. The paper already gives a quintic residual, up to5 additional fixed points and numerical bistability; it warns that projected nullcline stability does not guarantee full3D stability. Those facts are credited, not claimed new. No sharp attained full-system capacity is asserted as a published number here.

**Our number and exact domain.** The maximum is **3 hyperbolic asymptotically stable nonnegative equilibria**, over all strictly positive constants in the printed model. A global degree/crossing argument supplies the upper bound; a rational assignment attains it, with stable states at T=0, approximately1.56314789924 and13.99709358253. Two other positive equilibria are unstable. The general bound excludes nonhyperbolic stable states and other attractors. With the non-coupling constants fixed to printed Table3, the sharper maximum is2, attained within the printed variable ranges.

**Code/data.** Kept in a private working copy, not in this repository:

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

## Verdict

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb10/VERDICT.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb10/VERDICT.md)_

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

## Prior Art

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb10/PRIOR_ART.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb10/PRIOR_ART.md)_

## Independent referee source log — 2026-11-02

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

### Completed independent checks

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

---

# Victor Garcia — the NK-CTL model, VB25

Folder: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb25](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb25)

## Claim

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb25/CLAIM.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb25/CLAIM.md)_

## VB25 — global dynamics at the printed fixed rates

Candidate claim, 2026-11-02T17:29:54Z. Please independently audit the analytic proof as well as rebuilding the certificates. No novelty, physiological, treatment or author-interest judgement is requested from the mechanical referee. Opus/Fable TASTE separately decides those questions. This is the harder target explicitly selected in victor_VB10/TASTE.md; the old count claim stays closed NON-SEND.

Published baseline: Garcia, Bonhoeffer and Fu2020, DOI10.1016/j.jtbi.2020.110185, printed Eqs21–23 and Table3, AppendixC. The paper gives a quintic/nullcline and numerical bistability; no numerical global-convergence bound is printed. Identity is checked on PMC7079339 itself; official Figshare11536824 files and primary XML remained byte/catalog identical on final recheck. Original equation/equilibrium and native-R finite-difference/Jacobian controls are frozen in the parent directory. Legacy R differs in a denominator/misses helpers, so this claim concerns the printed model only, with that limitation explicit.

Our candidate result: with every non-coupling constant fixed to Table3, for all U=c*sigma>0,V=k*sigma*omega>0 and every finite nonnegative initial state, the printed three-dimensional system converges to one equilibrium. Thus there are no nonconstant periodic or other recurrent non-equilibrium limit sets. At hyperbolic bistable parameters the common boundary of the two sink basins is the interior saddle stable manifold. The exact fold is V=e(T)^2[f(T)n'(T)-ab*n(T)]/[e(T)-T*e'(T)], U=f(T)n(T)-T*V/e(T), for0<T<Tcrit; Tcrit is the unique positive root of (1-bT)n'-bn in(0,2200). The proof covers degeneracies for convergence but confines the basin assertion to hyperbolic bistability.

Private working files, not in this repository: vb25_global_convergence/GLOBAL_PROOF.md (complete proof), REPORT.md (commands), PRIOR_ART.md, CLAIM_MANIFEST.json (payload hashes), construct_energy_certificate.py, construct_fold_certificate.py, verify_exact_polynomials.py, verify_differential_identities.py. Certificates and logs are in final_backup/vb25, final_backup/results, pod_backup/vb25, checkpoint_1726/vb25 and run5_backup/checkpoint_1719/vb25/ENERGY_CONSTRUCTION.json in the job root. Primary public inputs are in run5_backup/results/run5_first_sources.tar.xz with its manifest; parent printed-equation/native controls and independently checked root lemma are in vb10_global_dynamics. No new observation dataset or holdout is involved.

Verification: independent standard-library Fraction checker reconstructs n,e from printed summands; proves the two degree13 energy polynomials have strictly positive rational coefficients on T>=0; verifies rate/g bounds, the unique fold endpoint, strict Vprime<0 by positive Bernstein coefficients and Uprime identity; independently rechecks the at-most-two-positive-root Descartes lemma. Separate Sympy checker differentiates the original normalized ODE for arbitrary smooth n,e and reconstructs the full Jacobian/cubic. Both PASS. The exact absorbing-tail matrix margin is125/7757. The construction is not imported by either checker; the Fraction checker compares independently reconstructed coefficient hashes with the frozen construction.

Controls: original printed-equation/native-R source baseline, full3D rather than projected slope stability, exact half-line rather than finite-grid damping, separate treatment of T=0,U>=3a/2,U=a and possible energy divergence at T=0. No ODE scan is used to prove no cycles; no fitting or retuning. Classical Descartes, Routh–Hurwitz and Barbashin–Krasovskii–LaSalle methods are credited.

What to worry about: the executable identities do not verify compactness/LaSalle/manifold reasoning. Audit especially the absorbing limsup estimate, U>a energy dichotomy, U=a removable singularity and the complete-bounded-trajectory step excluding a homoclinic saddle branch. Eventual damping alone would not exclude such a branch; the proof explicitly strengthens the bound to all times on complete bounded trajectories. Fold classification relies on its exact monotonicity plus the independently rechecked multiplicity bound. The rates must remain frozen; the theorem is not asserted for arbitrary biological constants. Original printed equations versus legacy R are distinguished. Final public search is bounded and some endpoints fail; absence of a match is not a priority claim. No author-ready summary will be sent or added until both review stages clear.

NEXT BAR is for the external reviewers, not a reason to polish the closed VB10 count. Please return a mechanical HOLDS/false-step verdict; TASTE remains Opus/Fable only.

## Verdict

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb25/VERDICT.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb25/VERDICT.md)_

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

## Prior Art

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb25/PRIOR_ART.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb25/PRIOR_ART.md)_

## Independent referee source ledger

Started 2026-11-02 before referee code or construction.
Claim: fixed-rate global convergence and fold/basin classification for the printed Garcia–Bonhoeffer–Fu model, DOI 10.1016/j.jtbi.2020.110185, PMC7079339.
The claimed source baseline is a quintic equilibrium equation and numerical bistability; there is no competition scoreboard specified. This is being independently checked, not assumed.
Primary source attempted: https://pmc.ncbi.nlm.nih.gov/articles/PMC7079339/ (browser challenge); DOI resolver failed in browsing tool. Will inspect primary XML/public publisher data and frozen public-source archive.
Read claim and candidate proof as objects of audit, not as independent verification.
Public code, recent papers, named agent repositories and community checks: pending, to be recorded below before any novelty statement. No novelty or priority judgment is requested.
Baseline reproduction: reconstruct printed rates/equations independently on the shared ref pod; never import candidate construction or verifier code.

Independent source pass completed on authorized ref pod before mathematical construction:
- Europe PMC full-text XML fetched successfully, 352197 bytes, SHA256 44a73bed7dbeaef770b73c291dc2fe5319b99ed578be4796e3afa165685500f8; identical to frozen input. The live source names Victor Garcia, Sebastian Bonhoeffer and Feng Fu.
- Official public code catalog https://api.figshare.com/v2/articles/11536824 fetched (6845 bytes). Printed Eqs.21–23 and Table 3 extracted directly; rates match the claimed normalization. Appendix C and source R audit continue.
- GitHub repository search sorted updated: `110185` (four irrelevant repositories), `cancer immunosuppression bistability` (zero), `tumor global stability 2026` (zero), `awesome mathematical biology` (zero). Repository search is not a code-content search.
- Trees checked: BakeLab/Epi-results, google-deepmind/alphaevolve_results, kisonecat/openai-math: no model-specific path matches. plasma-ai/erdos has only unrelated Garcia number-theory paths. Wrong DeepMind repository spelling returned 404 and openai/math response exceeded the explicit 12 MB read limit; follow-up required. EinsteinArena repository discovery succeeded.
- arXiv past-year tumor/stability query succeeded (30 entries); content inspection pending. Community exact-title queries on Reddit/X returned no relevant hit in browsing search. No community account or communication used.
- Related prior result encountered: Vithanage, Wei and Jang (2023), DOI https://doi.org/10.1002/mma.9152, gives global results for a different model (four variables with a two-variable subsystem); not established as this three-variable fixed-rate theorem. Do not treat negative bounded searches as priority evidence.
- Current baseline remains the primary paper's numerical NK/CTL bistability and quintic/nullcline reduction. There is no published numerical global-convergence bound being beaten. Referee must test an analytic extension, not a statistical gain.

Follow-up and final refresh, 2026-11-02 17:42 UTC:
- Independently read the complete primary NK/CTL section and Appendix C, including its explicit warning that projected slope is not sufficient for full stability. The five-positive-root discussion is a generic quintic bound, not a demonstrated five-root instance at the frozen rates.
- Correct DeepMind tree (`alphaevolve_repository_of_problems`) and vinid/einstein-arena tree checked with no topic path matches. openai/math CONTENTS.md fetched (640943 bytes); no topic-term line matches. These bounded tree/index checks cannot establish absence from all file contents.
- Final source XML and Figshare catalog match the initial downloads byte for byte. Four checked agent-tree heads remained identical; final EinsteinArena/plasma/kisonecat head requests hit HTTP 403 rate limits, so their earlier successful snapshots are the latest observations here.
- Exact-title GitHub repository search: zero. Exact-title GitHub issue search: one match, https://github.com/monarch-initiative/dismech/pull/528, titled "Add cancer disease knowledge base and research documentation". HTML retrieval via browsing failed; it is not evidence of a competing theorem and has not been exhaustively reviewed. An earlier DOI-number issue query returned 69 noisy matches and was superseded by this title query.
- Exact-title arXiv query restricted to the last year returned zero. Broad recent query returned 30 titles, primarily unrelated imaging/PDE studies; no same-model theorem was identified. These searches are incomplete and are not a priority finding.
- The publisher abstract of Vithanage/Wei/Jang (2023), DOI 10.1002/mma.9152, confirms global asymptotic-stability results and a three-interior-equilibrium classification in a different model. This is a related prior result for the taste reviewer to know, not a novelty verdict on this claim.
- Reproduced the printed fixed-rate bistability independently at U=0.6, V=2e-9 (positive roots approximately 257.90864 and 9720.51043). Full Jacobian analysis agrees with saddle/sink classification. Supplied R does not reproduce the same normalized function because its NK denominator contains T^2; directly downloaded official file matches frozen public code.

---

# Victor Garcia — the NK-CTL model, VB31

Folder: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb31](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb31)

## Claim

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb31/CLAIM.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb31/CLAIM.md)_

## VB31 — global convergence through growth2

Submitted 2026-11-02T20:08:43.997540+00:00. Internal exact/source/archive checks PASS; separate mechanical VERDICT and Opus5.5/Fable5.1TASTE requested. This is the externalVB28/VB30harderbar, not a novelty/priority judgment bySol.

Published anchor: Garcia, Bonhoeffer and Fu2020, DOI10.1016/j.jtbi.2020.110185, printed Eqs21–23/Table3. Its growth parameter is a=.514; no published global-convergence score exists to beat. FreshprimaryXMLSHA25644a73bed7dbeaef770b73c291dc2fe5319b99ed578be4796e3afa165685500f8 pins authorship/constants. Source/nativebaseline was independently audited inVB10/VB25/VB28. The releasedNKhelper differs fromEq22 and does not establish historical3Dsimulation identity.

Our statement: fixing exactly the Table3immune rates, every finite nonnegative trajectory converges to one equilibrium for every0<a<=2 and everyb,U,V>0. The equilibrium may depend on its initialstate. This excludes all nonconstant periodic or other recurrentlimitsets, includes a=U and repeatedroots, and uses unchanged time/growth under y=N/sigma,z=E/(sigma*omega),U=c*sigma,V=k*sigma*omega. Endpoint2 is sufficient, not a sharp threshold or biologicalparameter estimate.

Code/data/proof are in a private working copy (vb31_table3_global_growth), not in this repository.
GLOBAL_PROOF.md gives the full analytic argument; REPORT.md gives commands/limits. CLAIM_MANIFEST.json freezes 21files. Canonical replayresults: verified_backup/vb31_portable_replay; complete coefficient arrays: VARIABLE_SHIFT_POLYNOMIALS.json.gz there. PUBLIC_VERIFIER_REPLAY.tar.gz contains only portable scientificcode/rationalconstants. Currentpriorreceipts: verified_backup/vb31_prior_final.

How verified: a direct checker differentiates the proposedenergy in the actual sourceT,y,z field; another checks the genericvariableshift, including its derivative. A separate Bernsteinidentity checker covers the wholegrowthinterval. The mainFraction/Sturm verifier independently reconstructs rational sourcefunctions/potentialderivatives without NumPy/searchmatrices and certifies31distinct positivepolynomials over everyT>=0. Positive denominators, sourcebounds and a uniform leadingdampingbound193/360 are exact. Proofweights are q=32,kappa(T)=(T+3420000)/(30(T+200000)); no biologicalrateschange. Absorbing-domain, extinction/coercivity, C1boundary and LaSalle steps are written explicitly. This is executableexactarithmetic plus analyticreasoning, not a proof-assistant artifact.

An isolatedpodreplay unpacked the portablearchive into an emptyfolder, returned0and matched allscientificcertificatefields and the entirecompressedpolynomialarchive. PortableverifierSHA25672adaaf21c74816c0735d6098c32f02c090fc0466323a5d43bbab7a433552d0f; Python3.12.3,SymPy1.13.3. Allscientificcompute stayed on authorizedevo; mainchecker isstdlib, identities additionallyuseSymPy. No empiricaldata/holdout applies.

Controls: at a=2,b=51/50000000000,U=11/5,V=11/100000000000, an independentexactcontrol finds two simplepositiveequilibria, besides theboundary. Thus the theorem doesnotassumeequilibriumuniqueness or reduce to U>=3a/2automaticextinction. The earlier constant-q/coarse-bound argument fails exactly at a=2; the new functional contains a restoring-force cross term and allshiftderivatives. The2520trajectoryscan is exploratoryonly, with no role in this proof. Initialnumericalfixes and its12workerresourceviolation are preserved in NUMERICAL_AUDIT.md/RUN_COMPLIANCE.md; proofjobsuseoneworker.

Worries: the complete analyticdomain/boundary/LaSalle reasoning needs independent audit, not just a polynomialrerun; literalTable3rates rather than a quantified uncertaintyregion; no historicalsimulation/physiology/clinicalclaim;2notsharp; methods are classical and model-specific novelty/usefulness belongs only toTASTE. Final16-sourcecheck had one503keywordquery followedby200retry, with currentunchangedprimary/catalog and successfulGitHub/agentchecks; priors remainbounded. Nothing sent to anyone.

## Verdict

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb31/VERDICT.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb31/VERDICT.md)_

HOLDS
Referee: gpt-6.1-sol

The stated convergence theorem survives independent reconstruction and audit: literal Table 3 immune rates, every 0<a<=2, all b,U,V>0, and every finite nonnegative initial state. Equilibria need not be unique. No counterexample or proof gap was found.

Primary source: [Garcia, Bonhoeffer and Fu (2020)](https://doi.org/10.1016/j.jtbi.2020.110185), Eqs. 21–23/Table 3. Fresh MathML parsing confirms Victor Garcia's authorship and a=.514 per day. The normalization changes neither time nor growth. The endpoint 2 is a sufficient theorem bound, not a published performance number or a sharp threshold.

What I ran: independently written source parser, full-field energy differentiation, parameter-affinity/Bernstein reconstruction, and exact positivity checks for all 36 control matrices. No claimant search/verifier code was imported. An additional integer Bernstein checker independently proves all 40 referee-derived polynomials positive without root-counting software. See independent_result.json and bernstein_result.json.

I also audited finite-time domain entry, extinction, the a=U boundary extension, LaSalle, and repeated equilibria; details are in ANALYTIC_AUDIT.md. These steps establish convergence of each orbit, rather than merely excluding Hopf bifurcations.

Sceptic's control: the supplied a=2 example independently has exactly two simple positive equilibria besides the boundary, and U<3a/2. Uniqueness or automatic extinction therefore does not explain the result. No empirical data or hold-out exists; exploratory trajectory scans contribute no proof evidence.

Relative to the paper: its stationary-root/bistability analysis at a=.514 is supplemented by an all-orbit convergence guarantee through a=2 for arbitrary positive couplings. Prior encountered: Clotilda et al. (2024), DOI 10.37394/232023.2024.4.15, proves global stability for a different chemotherapy subsystem. Bounded searches and their limitations are recorded in PRIOR_ART.md; no priority judgment is made.

Scope: this establishes the printed ODE. The public R NK helper uses hg+T_w^2 instead of Eq. 22's linear denominator; historical simulation identity remains unestablished. Evidence is copied back, all tracked workers exited, and the pod referee directory ends at 448 KB.

Strongest author objection: the ten literal immune constants have no quantified uncertainty allowance, so this theorem alone does not establish robustness to rate variation.

NEXT BAR: certify the same convergence statement throughout an explicit ±1% box around all ten fixed immune constants.

## Prior Art

_Source: [friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb31/PRIOR_ART.md](friends/victor-garcia-nk-ctl/nk-ctl-note/referee-vb31/PRIOR_ART.md)_

## Prior-art/source audit — 2026-11-02

Scope: independent referee of the stated fixed-Table-3 global convergence theorem, not a novelty judgment.

Primary anchor supplied by claim: Garcia, Bonhoeffer and Fu (2020), Journal of Theoretical Biology, DOI https://doi.org/10.1016/j.jtbi.2020.110185, equations 21–23 and Table 3. Claim says published a=0.514 and no published global-convergence score. This is unverified pending source retrieval.

Before writing test code, audit plan:
1. Read current primary paper/catalog and any official results/code, including issues/PRs if applicable; identify what quantity is actually claimed.
2. Search public GitHub, recently updated results, and relevant agent result repositories.
3. Search recent papers and public community summaries for this exact model/theorem.
4. Independently reconstruct source equations and proof identities; exact arithmetic is the baseline for this analytic claim. There is no empirical hold-out or numerical leaderboard claimed.

No claim of novelty or record will be made. Receipts and search limitations will be added below.

### Completed independent source checks

Retrieved on 2026-11-02, then rechecked before closing:

- Fresh primary XML: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7079339/fullTextXML . SHA256 `44a73bed7dbeaef770b73c291dc2fe5319b99ed578be4796e3afa165685500f8`. MathML and Table 3 parsed by the referee's own code. Authors Victor Garcia, Sebastian Bonhoeffer, Feng Fu; source growth a=257/500 per day. Original paper is a stationary-root/bistability analysis of the NK/CTL extension, with an explicit Appendix C warning that a stabilizing root in the reduced tumor equation does not guarantee full stability. It supplies no global-convergence score or numerical record of this kind.
- Public code baseline: https://doi.org/10.6084/m9.figshare.11536824.v1 ; version metadata https://api.figshare.com/v2/articles/11536824/versions/1 . All ten released R files read. In `analysis_FengNKCTL.R`, `N.stab.nomut` uses `g*T_w/(hg+T_w^2)`, whereas printed Eq. 22 uses `bn*T/(kappa_bn+T)`. The release also calls absent `params_FengNKCTL.R`. Thus it is not a faithful executable baseline for the exact printed 3D field. The referee instead reconstructs that field directly, which is the baseline relevant to this theorem. Historical simulation identity remains unestablished.
- GitHub repository searches were sorted by updated date for exact title phrase, Bonhoeffer/Fu, 110185, and tumor-immune/2026. The exact-title and author pair returned zero repositories. Numeric queries were noisy. Exact-title issue/PR search returned one disease-documentation PR, not a convergence proof; the numeric issue query mostly matches issue numbers. Raw receipts are in `public/github_*.json`. No claim of exhaustive GitHub code search is made.
- Agent repositories inspected via README and available tree paths: https://github.com/BakeLab/Epi-results , https://github.com/google-deepmind/alphaevolve_results , https://github.com/openai/math , https://github.com/togethercomputer/EinsteinArena-new-SOTA , https://github.com/plasma-ai/erdos , https://github.com/kisonecat/openai-math . The original `google-deepmind/repository_of_problems` URL returned 404; a repository search resolved it to https://github.com/google-deepmind/alphaevolve_repository_of_problems and that source was subsequently checked. A full `openai/math` tree exceeded the 12 MB bounded read; its README and manuscript catalogue were inspected instead. No matching model/theorem was identified in those bounded inspections. Unrelated Garcia number-theory filenames occurred in the Erdos tree.
- Recent literature: EuropePMC exact-title phrase, publication dates 2025-11-02 through 2026-11-02, returned zero; arXiv Garcia AND immunosuppression sorted by submitted date returned zero. Web searches of DOI/title with global stability, LaSalle, periodic, and convergence found the primary and citations, not a same-model theorem. Public X/Reddit/blog searches likewise yielded no relevant theorem in the returned results; no private community access or contact was attempted.
- A prior result encountered and read: Clotilda, Vithanage and Lakshika, *A Mathematical Model to Treat for a Cancer Using Chemotherapy and Immunotherapy under Mass Action Kinetics for Immunotherapy* (2024), https://doi.org/10.37394/232023.2024.4.15 ; source https://wseas.com/journals/msa/2024/a30msa-012%282024%29.pdf . Its Theorem 2 gives global stability for a different two-state chemotherapy subsystem, using Poincare–Bendixson; the full model includes a chemotherapy compartment and one immune compartment. It does not establish this fixed-rate NK/CTL theorem. The paper was extracted on the pod using the public pypdf wheel after pdftotext proved unavailable.

The best applicable baseline in the primary source is the printed field and its bistability/root analysis at a=.514. The submitted theorem adds a universal, all-initial-state convergence conclusion for the literal fixed immune rates over 0<a<=2, arbitrary positive b,U,V, including multiple equilibria. This describes the difference from the paper; it is not a judgment about novelty, priority, or usefulness. Classical energy/LaSalle, polynomial positivity and Bernstein convexity are the methods used in the submitted argument. There is no empirical hold-out to reproduce.

Final source rechecks and their limitations are recorded in `final_public_receipts.json` and `close_sources.json`. These bounded searches cannot establish priority.

---

# Victor Garcia — the R script, line 35

Folder: [friends/victor-garcia-nk-ctl/script-line-35](friends/victor-garcia-nk-ctl/script-line-35)

## Bugs

_Source: [friends/victor-garcia-nk-ctl/script-line-35/BUGS.md](friends/victor-garcia-nk-ctl/script-line-35/BUGS.md)_

## Confirmed bugs in analysis_FengNKCTL.R

Five confirmed defects, grouped by cause. The target script is unchanged in `source/`; its MD5 matches the supplied frozen copy. INVENTORY.md lists all ten files. COMPARISON.md gives the paper comparison, parameter ambiguities, figure evidence and scientific limits. Original line numbers are used throughout. Reproduce one bug with `sh repro/<ID>/run.sh` from this directory; the saved R/Python outputs and minimal patch are in each folder.

### B03 — Squared NK stimulation denominator changes the model and Fig. A2

**Line:** 35, `parameters$hg + T_w^2`. **Paper:** Eqs. 22 and 76 require κbn+T, as does the script's own comment at line 31.

**Wrong:** The extra square changes N(T), CTL recruitment through N(T), all reduced tumor equilibria and the numerator degree assumed in Appendix C.

**Repro:** [repro/B03/run.sh](friends/victor-garcia-nk-ctl/script-line-35/repro/B03/run.sh), [R output](friends/victor-garcia-nk-ctl/script-line-35/repro/B03/r_output.txt), [Python output](friends/victor-garcia-nk-ctl/script-line-35/repro/B03/python_output.txt), [patch](friends/victor-garcia-nk-ctl/script-line-35/repro/B03/patch.diff). Direct ODE residual, root coordinates, full-Jacobian stability and folds are independently recomputed. Plot: Fig. A2 comparison.

**Before → after** (σ=1000,k=10⁻⁵, other constants Table 3):

- At T=100000, N=502.491349620 → **1596.264367816**. Substitution in printed dN/dt gives residual +685.207939392 → approximately zero.
- At c=0.001, roots [0,17404.7359,19762510.0178] → **[0]**. Full stability: two stable states plus one saddle → **one stable state**.
- Upper bistability fold c=0.00102628890913 → **0.000728393687513** (29.03% lower); lower boundary c₀=0.000514 is unchanged.
- At c=10⁻⁷, positive root 726310343.496 → **408558364.138**. c=1 has no positive root in either case.

**Which does the paper follow?** Appendix C/Eq. 81 follow the printed linear denominator. **Fig. A2 follows the squared denominator:** with σ=1000,k=10⁻⁴, its A peak (~2.8×10⁷), A root (~2.2×10⁸) and B roots (~1.7×10⁴ and ~5.9×10⁶) are reproduced. Printed Eq. 22 has no B positive roots at those parameters. Irrespective of σ,k within their printed ranges, the smaller positive root of the printed equations must be below 2133 cells, incompatible with the displayed ~10⁴ root. Exact original k remains uncertain; see COMPARISON.md.

**Effect on paper:** Quantitative figure and bistability region change. The broad claim of possible NK–CTL bistability survives: the corrected equations have two stable equilibria at σ=1000,c=0.0006,k=10⁻⁵. Because Table 3 gives σ as a range, c=0.001 is also bistable at σ=600, with different roots. No unique printed numerical NK upper fold exists to replace; these fold values are explicit recomputations. No effect on separate base-model treatment thresholds is established.

**Confidence:** High for model error, recomputations and figure's denominator; moderate for the specific k=10⁻⁴ provenance inference.

## Verdicts

_Source: [friends/victor-garcia-nk-ctl/script-line-35/referee/VERDICTS.md](friends/victor-garcia-nk-ctl/script-line-35/referee/VERDICTS.md)_

## Referee verdicts: NK-CTL script

B03's numerical headline survives independent recomputation. The exact Fig. A2 settings remain uncertain, and correction does not eliminate the model's ability to be bistable. These are software/reproducibility findings: **NEW: no** under the friends lane's novel scientific-result definition.

| Bug | Verdict |
|---|---|
| B03 — squared NK denominator | CONFIRMED WITH CAVEATS |

### B03 — CONFIRMED WITH CAVEATS (priority)

**Call sentence:** “The archived NK formula uses T² where both printed equations use T, and at σ=1000, k=10⁻⁵, c=0.001 that change creates a stable tumor state absent from the printed model.”

**Strongest objection Victor could raise:** The paper never uniquely specifies σ and k for Fig. A2, the T² code could be an exploratory variant, and the printed model still supports bistability elsewhere—including at c=0.001 if σ=600—so this does not refute the general biological conclusion or the separate base-model treatment results.

**What survived:** Independently read line 35 and primary Eqs. 22/76; the script's own comments agree with the linear denominator. The paper describes a maximum proliferation rate and saturation coefficient, not a declining T/(κ+T²) response. Our exact-rational root isolation and full Jacobians reproduce T=17404.7359049 (saddle), T=19762510.0178169 (stable), and T=0 (stable) for the squared version; the printed model has only stable T=0 at the specified point. The lower boundary is 0.000514 in both; upper folds are 0.00102628890913447 (squared) and 0.000728393687513285 (printed), a 29.02645% decrease.

**Figure qualification:** Fig. A2 uses c=10⁻⁷,10⁻³,1; Table 3 supplies ranges rather than exact σ,k. Squared T with σ=1000,k=10⁻⁴ closely reproduces its A peak and A/B zeros; k=10⁻⁵ from line 355 does not. That is strong parameter evidence, not a recovered execution record. With fixed Table 3 constants, the printed model can never have two positive roots both above 2132.602201 cells for any positive σ,k, whereas panel B displays two above that size. Thus the displayed roots conflict with the printed equations even after allowing the stated σ,k ranges. The headline k=10⁻⁵ roots should not be described as the exact plotted roots.

---

# Victor Garcia — codon-rate preprint, Fig 2B

Folder: [friends/victor-garcia-nk-ctl/nmds-fig2b](friends/victor-garcia-nk-ctl/nmds-fig2b)

## Claim

_Source: [friends/victor-garcia-nk-ctl/nmds-fig2b/CLAIM.md](friends/victor-garcia-nk-ctl/nmds-fig2b/CLAIM.md)_

NEW: yes
Printed: 34.8 percent Kruskal NMDS stress, Figure 2B caption, page 5, https://doi.org/10.1101/2025.06.03.657573 .
Ours: 16.9693901688774 percent, on the same 23 sequences, 253 pairs, two dimensions, Euclidean raw Shah rate profiles, and MASS stress objective. Numerical certificate PASS; separate referee verdict HOLDS.
Standard method: Native R/MASS::isoMDS with all defaults gives 34.8056749, reproducing the printed 34.8; the cited Shah–Gilchrist Table S2 column Rc and original DC3 sequences are used.
Deviations: standard failed: results/standard.log shows immediate default convergence at 34.8056749, reproducing but not improving the printed value. STATUS.md records the change before execution: maxit=1000, tol=1e-10, then 100 standard Gaussian starts with seed 1104, otherwise unchanged MASS settings.

Verification: `verify_stress.py` independently re-extracts all 61 printed rates
with a different PDF parser, hashes the fresh original sequences, reconstructs
profile dissimilarities exactly as integers, confirms native R's pair ordering,
and certifies the actual isotonic least-squares fit and stress with 384-bit Arb
interval arithmetic. The upper bound is below 34.75, the lower edge of the
printed number's rounding bin. Certificate: `results/shah_certificate.json`;
coordinates: `results/shah_best_coords.csv` in the working directory.

This is a new feasible numerical value for a printed objective under the job's
definition. It uses routine documented software settings and restarts. It is
not a new optimizer, a global optimum or a biological discovery. It does not
change the expression measurements or epistasis analysis. This unsupervised
objective has no predictive split; SBS is inapplicable (see BASELINES.json).
Prior art: `PRIOR_ART.md`; final live recheck completed 2026-11-04 22:56–22:57 UTC, no later comparable result located in the bounded search.

Referee: HOLDS. Independently rebuilt the original profiles, recovered the
actual published PDF configuration, checked native MASS::Shepard and wrote a
separate 320-bit Arb certificate proving stress below 16.970. The producing
384-bit certificate encloses the value in [16.9693901688773, 16.9693901688775].
See the [referee verdict](friends/victor-garcia-nk-ctl/nmds-fig2b/VERDICT.md) and [full review](friends/victor-garcia-nk-ctl/nmds-fig2b/REFEREE.md).

Internal claim only; no publication or contact. Original analysis script is
unavailable; native defaults and published PDF coordinates identify the
objective convention. No exhaustive-priority claim is made.

## Referee

_Source: [friends/victor-garcia-nk-ctl/nmds-fig2b/REFEREE.md](friends/victor-garcia-nk-ctl/nmds-fig2b/REFEREE.md)_

HOLDS

Both printed numerical objectives are improved on the same released sequence
set, cited codon-rate tables, Euclidean profile distances, dimension and
MASS/Kruskal Stress-1 convention:

- Shah (Figure 2B caption): 34.8 → 16.9693901688774.
- Rudorf (Figure 2C caption): 23.4 → 13.4830828456807.

Independent primary-table reconstruction, native MASS::Shepard, 90-digit
evaluation and a separately written Arb upper-bound certificate agree.
The actual plotted configurations give 34.80635 and 23.39684, supporting
the claimed objective identity beyond matching two rounded numbers.

These are new feasible numerical values under the user's stated definition.
They arise from routine solver convergence settings and restarts; no new
optimizer, global optimum or biological discovery is established. The original
analysis script is unavailable, so its implementation is identified by the
native-default and plotted-configuration match. No judgment is made about
whether Victor would care. Final prior-art checking is handled by the parent.

## Verdict

_Source: [friends/victor-garcia-nk-ctl/nmds-fig2b/VERDICT.md](friends/victor-garcia-nk-ctl/nmds-fig2b/VERDICT.md)_

HOLDS
Referee: gpt-6.1-sol
NEW confirmed: yes

The claim beats a number actually printed in Victor Garcia's own paper.
I opened the primary PDF: page 1 names Garcia; Figure 2B's caption on
page 5 prints 34.8. Pages 13–15 specify Shah–Gilchrist Table S2's Rc
column, raw elongation-rate profiles, Euclidean distances and Kruskal NMDS.
Paper: https://doi.org/10.1101/2025.06.03.657573

I independently parsed all 61 rates and rebuilt the 23 released sequences'
387 translated-codon profiles and all 253 pairs. Native R/MASS defaults
return 34.8056748605161%, reproducing 34.8. The actual PDF circles,
calibrated against the axes, give approximately 34.80624%; their coordinates
match the native result within 0.014 units. This supports objective identity.

My own isotonic-regression implementation recomputes the supplied witness
as 16.969390168877389…%, also confirmed by native MASS::Shepard.
My separate 320-bit Arb checker certifies the actual isotonic least-squares
fit and stress strictly inside [16.9693901688773, 16.9693901688775]%,
well below 34.75, the printed value's rounding-bin lower edge.
Ran recompute.py, standard_referee.R, certify.py and check_plot.py locally
at nice 10; no claimant search or verifier code was imported.
Evidence: results/recomputed.json, independent_interval.json, native_R.log,
pdf_plot_check.json. SBS and untouched hold-outs do not apply to this exact
unsupervised objective; BASELINES.json explains why.

Strongest objection: the original analysis script is unavailable; convention
identity rests on the methods, default reproduction and matching plotted map.
Fresh bioRxiv PDF/CSV fetches returned 429; archived public inputs were used.
Relative to the paper, this is a better feasible visualization via routine
MASS settings/restarts, with no global optimum or biological result shown.
Final public-source recheck found no comparable later value in bounded searches.
NEXT BAR: release the original Figure 2B script and evaluate this witness
through its original preprocessing and stress calculation.

## Prior Art

_Source: [friends/victor-garcia-nk-ctl/nmds-fig2b/PRIOR_ART.md](friends/victor-garcia-nk-ctl/nmds-fig2b/PRIOR_ART.md)_

## Prior art

Started 2026-11-04 22:46 UTC. This file precedes research code.

Read first: `../friends_queue/GOAL.md`; also read `_codex/RULES.md`,
`_codex/FRONT.md`, the Victor scoreboard and queue. Only Victor's own papers
are eligible. No outreach, uploads or remote compute. Resource cap: Mini,
four cores, 4 GB, nice 10; total deadline 2026-11-05 04:46 UTC.

### Selection and inherited results

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

### Public source checks, 2026-11-04

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

### Completed source checks and reproduction

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

### Final recheck, 2026-11-04 22:56–22:57 UTC

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

### Independent t2 referee, 2026-11-04

The material above was supplied by the claimant and is unverified input. This
review will open the primary PDF and rate supplement, reconstruct the released
sequences and Euclidean rate-profile distances independently, run standard
MASS defaults first, then evaluate the supplied witness with independent code.
The claim concerns an unsupervised finite objective, not predictive accuracy.
Live DOI opening in the web tool failed (internal access error); read-only HTTP
and the archived public PDF will be used. The printed 34.8 is the baseline to
check, not a presumed record. No improvement search is planned by this referee.

Independent live checks: exact-title/DOI/stress/GitHub and value-prefix searches
returned the preprint, bibliographic mirrors and an institutional talk; no later
comparable number was established. Read the official CRAN MASS source:
https://raw.githubusercontent.com/cran/MASS/master/R/isoMDS.R and
https://raw.githubusercontent.com/cran/MASS/master/src/MASS.c .
Its defaults and percentage Stress-1 formula support the convention, but do not
establish that the claimant computed it correctly. Fresh bioRxiv API metadata
and fresh PLOS S2 downloaded; evidence/fetch_receipts.json records provenance.
This review makes no priority claim; it cannot finish the numerical baseline
reproduction because the prescribed pod is unavailable. No substitute compute
or restricted mathematical variant was used.

### Resumed independent review, 2026-11-04
The current instruction explicitly authorizes light computation on the Mini
(4 cores, 4 GB, nice 10). Prior pod unavailability is therefore not a blocker.
I opened the archived primary PDF directly: page 1 names Victor Garcia,
page 5 Figure 2B prints 34.8, pages 14–15 specify Euclidean raw rate profiles
and Kruskal NMDS. Live title/DOI searches again locate the same preprint.
The existing prepared scripts have not been accepted as numerical evidence.
I will run native MASS defaults before evaluating the proposed coordinates,
and independently implement and certify the objective from the primary data.
No predictor is being evaluated: SBS and held-out splits are inapplicable.

### Final independent result and live recheck
Native R 4.6.2 / MASS 7.3-66 reproduced 34.8056748605161; independent
PAVA and Arb certify the submitted map at 16.969390168877389… percent.
The PDF's actual vector circles also reproduce that native default map.
Public metadata, updated-sorted GitHub title/DOI searches, issue search and
seven agent-result trees were rechecked; receipts are in
`evidence/final_public_recheck.json`. GitHub title/DOI results were unrelated;
the broad numeric issue query also returned unrelated results. No original
analysis repository or comparable later objective value was located.
No relevant paths were found in the seven result trees; openai/math's tree
is truncated. Final exact-title/DOI/value web searches again found the
preprint and listings, not a comparable later value. This bounded check is
not an exhaustive priority claim, and the verdict judges the printed-value
comparison only. Established Kruskal/MASS methods receive full credit.

---

# Victor Garcia — codon-rate preprint, Fig 2C

Folder: [friends/victor-garcia-nk-ctl/nmds-fig2c](friends/victor-garcia-nk-ctl/nmds-fig2c)

## Claim

_Source: [friends/victor-garcia-nk-ctl/nmds-fig2c/CLAIM.md](friends/victor-garcia-nk-ctl/nmds-fig2c/CLAIM.md)_

NEW: yes
Printed: 23.4 percent Kruskal NMDS stress, Figure 2C caption, page 5, https://doi.org/10.1101/2025.06.03.657573 .
Ours: 13.4830828456807 percent, on the same 23 sequences, 253 pairs, two dimensions, Euclidean raw Rudorf rate profiles, and MASS stress objective. Numerical certificate PASS; separate referee verdict HOLDS.
Standard method: Native R/MASS::isoMDS with all defaults gives 23.396544, reproducing the printed 23.4; the cited Rudorf–Lipowsky Table S2, growth 0.7 h^-1 and 2-1-2 pathway, and original DC3 sequences are used.
Deviations: standard failed: results/standard.log shows immediate default convergence at 23.396544, reproducing but not improving the printed value at its precision. STATUS.md records the change before execution: maxit=1000, tol=1e-10, then 100 standard Gaussian starts with seed 1104, otherwise unchanged MASS settings.

Verification: `verify_stress.py` independently re-extracts all 61 printed rates
with a different PDF parser, hashes the fresh original sequences, reconstructs
profile dissimilarities exactly as integers, confirms native R's pair ordering,
and certifies the actual isotonic least-squares fit and stress with 384-bit Arb
interval arithmetic. The upper bound is below 23.35, the lower edge of the
printed number's rounding bin. Certificate: `results/rudorf_certificate.json`;
coordinates: `results/rudorf_best_coords.csv` in the working directory.

This is a new feasible numerical value for a printed objective under the job's
definition. It uses routine documented software settings and restarts. It is
not a new optimizer, a global optimum or a biological discovery. It does not
change the expression measurements or epistasis analysis. This unsupervised
objective has no predictive split; SBS is inapplicable (see BASELINES.json).
Prior art: `PRIOR_ART.md`; final live recheck completed 2026-11-04 22:56–22:57 UTC, no later comparable result located in the bounded search.

Referee: HOLDS. Independently rebuilt the original profiles, recovered the
actual published PDF configuration, checked native MASS::Shepard and wrote a
separate 320-bit Arb certificate proving stress below 13.484. The producing
384-bit certificate encloses the value in [13.4830828456806, 13.4830828456809].
See the [referee verdict](friends/victor-garcia-nk-ctl/nmds-fig2c/VERDICT.md) and [full review](friends/victor-garcia-nk-ctl/nmds-fig2c/REFEREE.md).

Internal claim only; no publication or contact. Original analysis script is
unavailable; native defaults and published PDF coordinates identify the
objective convention. No exhaustive-priority claim is made.

## Referee

_Source: [friends/victor-garcia-nk-ctl/nmds-fig2c/REFEREE.md](friends/victor-garcia-nk-ctl/nmds-fig2c/REFEREE.md)_

HOLDS

Both printed numerical objectives are improved on the same released sequence
set, cited codon-rate tables, Euclidean profile distances, dimension and
MASS/Kruskal Stress-1 convention:

- Shah (Figure 2B caption): 34.8 → 16.9693901688774.
- Rudorf (Figure 2C caption): 23.4 → 13.4830828456807.

Independent primary-table reconstruction, native MASS::Shepard, 90-digit
evaluation and a separately written Arb upper-bound certificate agree.
The actual plotted configurations give 34.80635 and 23.39684, supporting
the claimed objective identity beyond matching two rounded numbers.

These are new feasible numerical values under the user's stated definition.
They arise from routine solver convergence settings and restarts; no new
optimizer, global optimum or biological discovery is established. The original
analysis script is unavailable, so its implementation is identified by the
native-default and plotted-configuration match. No judgment is made about
whether Victor would care. Final prior-art checking is handled by the parent.

## Verdict

_Source: [friends/victor-garcia-nk-ctl/nmds-fig2c/VERDICT.md](friends/victor-garcia-nk-ctl/nmds-fig2c/VERDICT.md)_

HOLDS
Referee: gpt-6.1-sol
NEW confirmed: yes
The claimed lower feasible stress is confirmed under the stated printed-number rule.
[The paper](https://doi.org/10.1101/2025.06.03.657573), Figure 2C caption,
PDF page 5, actually prints 23.4; page 1 lists Victor Garcia as a coauthor.
Pages 13 and 15 specify Rudorf's 0.7 h^-1, 2-1-2 rates, Euclidean rate-profile
distances and Kruskal nonmetric MDS. The caption itself does not print “percent”.

I independently rebuilt all 23 profiles (387 sense codons each), all 253
pairwise dissimilarities, and evaluated the submitted two-dimensional witness.
Own PAVA code, checked against SciPy isotonic regression, gives
13.48308284568073 percent Stress-1 using the documented MASS convention.
Own 384-bit Arb evaluation certifies 13.48308284568072855, with enclosure
radius below 3e-112, strictly below 23.35, the printed rounding-bin threshold.
PAVA optimality conditions also pass. Enforcing equal disparities for tied
input distances gives the same value. No producer/referee code was imported.
Evidence: results/independent_audit.json; code: audit.py.
To check objective identity, I extracted all 23 plotted PDF vector marks,
corrected the axis scales using printed ticks, and recomputed 23.396468%.
All marks match the supplied default configuration within 0.008 PDF points;
that configuration independently evaluates to 23.396544%. See plot_audit.py
and results/published_plot_audit.json. I did not rerun the original optimizer.
Run both scripts with the shared .venv Python, nice 10 and one BLAS thread.
These local checks completed successfully; no pod was needed.

New relative to this paper: a lower feasible value of its Figure 2C objective;
no global optimum, new optimizer, or changed biological conclusion is shown.
SBS/trivial/simple predictive scores: inapplicable; this is an unsupervised
finite geometric objective with no prediction labels or held-out split.

Strongest objection: the original analysis script is unavailable, so MASS
implementation identity is inferred from the methods and plotted-configuration
match. Fresh Rudorf PDF matches the archived hash; bioRxiv HTTP 429 required
archived primary paper/sequence files. No comparable later value was found
in bounded exact-title/DOI searches; this is not an exhaustive priority search.

NEXT BAR: release the original Figure 2C distance matrix and analysis script
so the implementation and preprocessing can be compared directly.

## Prior Art

_Source: [friends/victor-garcia-nk-ctl/nmds-fig2c/PRIOR_ART.md](friends/victor-garcia-nk-ctl/nmds-fig2c/PRIOR_ART.md)_

## Prior art

Started 2026-11-04 22:46 UTC. This file precedes research code.

Read first: `../friends_queue/GOAL.md`; also read `_codex/RULES.md`,
`_codex/FRONT.md`, the Victor scoreboard and queue. Only Victor's own papers
are eligible. No outreach, uploads or remote compute. Resource cap: Mini,
four cores, 4 GB, nice 10; total deadline 2026-11-05 04:46 UTC.

### Selection and inherited results

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

### Public source checks, 2026-11-04

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

### Completed source checks and reproduction

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

### Final recheck, 2026-11-04 22:56–22:57 UTC

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

### Independent referee intake (2026-11-04)
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

### Resumed independent audit (2026-11-04)
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

---

# Victor Garcia — the Danish forecast

Folder: [friends/victor-garcia-nk-ctl/danish-forecast](friends/victor-garcia-nk-ctl/danish-forecast)

## Claim

_Source: [friends/victor-garcia-nk-ctl/danish-forecast/CLAIM.md](friends/victor-garcia-nk-ctl/danish-forecast/CLAIM.md)_

NEW: yes
Kind: note
Builds on: Cadosch, Garcia, Jensen, Low & Althaus (2020), Understanding the spread of de novo and transmitted macrolide-resistance in Mycoplasma genitalium, https://doi.org/10.7717/peerj.8913.
Ours: A new retrospective empirical test of the unchanged Danish forecast against later SSI 2021–2022 and national MiBa 2021–2024 reported surveillance fractions, with historical constant/logistic baselines and source/rounding audits. The new contribution is the external forecast comparison, not a new model, new surveillance measurements, or a completed 2025 endpoint test.
Prior art: Chua et al. (2025), https://doi.org/10.1016/j.lanmic.2024.101047, already synthesize resistance prevalence and population heterogeneity; Riou et al. (2023), https://doi.org/10.1186/s12879-023-08200-4, develop related gonococcal forecasting; Bolaji et al. (2026), https://doi.org/10.1371/journal.pgph.0006834, analyze a theoretical M. genitalium model. No inspected prior work performs this frozen Danish forecast/baseline comparison. See PRIOR_ART.md for access limits and search records.
Cited by: 17 papers since 2020 (OpenAlex W3015720582, checked 2026-11-04; citing query exposes 12 records, all inventoried); closest: Riou et al. 2023, Projecting the development of antimicrobial resistance in Neisseria gonorrhoeae from antimicrobial surveillance data. No direct earlier Danish forecast validation found in the bounded search.
Standard method: Unchanged official R code, last changed October 2019, with deSolve default ODE integration, bbmle Nelder–Mead fitting, published initial conditions/fixed parameters, seed 71309 and 10,000 parameter draws per country. All three published rounded 2025 forecasts and confidence intervals reproduce. Linear-time binomial logistic regression uses only the original four Danish training rows; the trivial predictor holds the last historical fraction constant without fitting.
Deviations: standard failed: the current bbmle 1.0.26 on pod R 4.3.3 called an unavailable %||% runtime operator (results/standard/first_failed_run.log). STATUS.md records the failure and planned change before retry. Pinned archived bbmle 1.0.23.1 and reran the original source unchanged; no scientific setting, model, data or optimizer was altered.

Metric: unweighted MAE in percentage points across the stated external year cells; all three predictors use identical outcomes within each series.

| Split | Trivial | Simple logistic | Original model | SBS |
|---|---:|---:|---:|---:|
| SSI, 2021–2022 | 24.87319185 | 13.91936772 | 10.86405197 | 0.781906 |
| MiBa, 2021–2024 | 21.02951542 | 19.94675090 | 16.83106330 | 0.257896 |

The SBS script output is preserved in BASELINES.json (fraction-scale scores, identical split/metric); raw outputs are results/sbs_SSI.json and results/sbs_MiBa.json. Both SBS values are below one. The original model improves over the specified simple baseline by 3.0553 and 3.1157 percentage points of MAE. This is a finite external comparison, not a new predictive method or a claim of general superiority.

Referee: independent computational referee, HOLDS WITH CAVEATS. A separate implementation refitted the logistic score equations and source likelihood, integrated all four source compartments, and recomputed every evaluated observation, prediction, metric, SBS and rounding range. See referee/REFEREE.md and referee/recomputation.json.

Limits: historical specimens, later SSI episodes and MiBa case fractions have different sampling and typing definitions. The original forecasts assume continued treatment practices; actual changes prevent causal or counterfactual refutation. Every evaluated point lies inside the original broad parameter confidence band. The two aggregate scores cover different year sets and cannot isolate a source effect. The 2021 SSI denominator is inferred; MiBa 2024 is rounded. No 2025 endpoint, French/Swedish validation, intervention effect, or all-infected-population calibration is claimed. Literature searches are bounded; five citations implied by OpenAlex's headline count were not returned by its query.

Artifacts: NOTE.md (short manuscript), REPORT.md (reproduction), DATA.md, PROPOSAL.md, IDEAS.md, PRIOR_ART.md, BASELINES.json, code/, data/, results/, sources/ and referee/ in a private working copy, not in this repository.

Disposition at the time: unpublished; the author is the judge.

## Verdict

_Source: [friends/victor-garcia-nk-ctl/danish-forecast/VERDICT.md](friends/victor-garcia-nk-ctl/danish-forecast/VERDICT.md)_

HOLDS WITH CAVEATS
Referee: gpt-6.1-sol
NEW confirmed: yes

The note adds a later-data comparison that survives independent recomputation. It supports the frozen model beating the specified constant/logistic baselines on these reported fractions, with no claim of a new model, causal refutation or completed 2025 test.

Primary source: Victor Garcia is a coauthor. The abstract and Results genuinely print conditional 2025 resistance forecasts of France 25% (9–30), Denmark 84% (36–98), Sweden 62% (48–76). Equations 1–6 and Tables 1–2 were read in the [paper](https://doi.org/10.7717/peerj.8913). No later-surveillance MAE is printed there.

Independent code: `fresh_recompute.py` reconstructs the four compartments and likelihood, refits with Nelder–Mead, fits binomial logistic IRLS using only the original four Danish rows, and recomputes six outcomes, MAEs, rounding bounds and SBS. No claimant or earlier verifier code was imported. ODE/scalar solutions agree within 3.36e-11 in fraction.

Same-split unweighted MAE, percentage points; lower is better:

| Series | Trivial | Simple logistic | Frozen model | SBS |
|---|---:|---:|---:|---:|
| SSI 2021–2022 | 24.873192 | 13.919368 | 10.869207 | 0.782193 |
| MiBa 2021–2024 | 21.029515 | 19.946751 | 16.837261 | 0.258277 |

SBS was computed with the required sbs.py (`BASELINES.json`). This is mechanistic forecasting, not deep learning. The note's default-solver MAEs differ by only 0.0052/0.0062 points; independent refitting and published rounding do not reverse the advantage.

Primary surveillance checks confirm SSI 274 at 62.6% in 2021 (unique integer denominator 438), 311/436 in 2022; MiBa 60.6%, 63.2%, 63.6%, and rounded 65% in 2024. The 2022 source contrast is 8.1303 points. Sources: [SSI](https://en.ssi.dk/surveillance-and-preparedness/surveillance-in-denmark/annual-reports-on-disease-incidence/m/mycoplasma-genitalium), [MiBa 2023](https://en.ssi.dk/surveillance-and-preparedness/surveillance-in-denmark/annual-reports-on-disease-incidence/m/mycoplasma-genitalium-2011-2023), [2024](https://en.ssi.dk/surveillance-and-preparedness/surveillance-in-denmark/annual-reports-on-disease-incidence/m/mycoplasma-genitalium-2024).

The original model predates the outcomes; baseline fitting uses historical data only. The worker saw some later percentages before fixing its protocol, so researcher selection is not prospectively sealed. Kind: note is honest for the added empirical comparison; source reproduction alone is a rerun.

I ran cited-by myself for 10.7717/peerj.8913 and 10.1101/321216, opened potentially overlapping titles and relevant sections, and directly searched this question. No inspected work already contains this comparison. Riou concerns gonorrhoea; Bolaji uses another theoretical model; Almeida's open accepted manuscript additionally fits English 2016–2017 diagnoses. Details: PRIOR_ART.md.

Access caveats: Chua 2025 [10.1016/j.lanmic.2024.101047](https://doi.org/10.1016/j.lanmic.2024.101047) is gold OA, but Discussion/supplement remain unread after publisher/API, SSRN, Bern and Melbourne attempts. Kenyon 2021 [10.1097/OLQ.0000000000001404](https://doi.org/10.1097/OLQ.0000000000001404) was abstract-only; its PrEP cohort question excludes this comparison. The 2019 clinical item [10.1007/s15011-019-2392-x](https://doi.org/10.1007/s15011-019-2392-x) remains unread and predates the outcomes. OpenAlex reports 17 citations but returns 12 records. These are coverage limits, not evidence of an earlier result.

The authorized pod name is unavailable to its launcher (KeyError: fnew), so I did not repeat the full official R bootstrap. All light claimed comparisons were independently recomputed locally, one thread, nice 10.

Strongest author objection / weakest point: changed treatment, laboratory coverage, episode definitions and typing denominators make these fractions an imperfect target for the original conditional all-infection forecast. The note discloses this and every point remains inside its broad parameter band; only its limited transport comparison holds.

NEXT BAR: Obtain and inspect Chua's Discussion and supplement for any earlier comparison of the frozen Danish forecast with later surveillance.

## Prior Art

_Source: [friends/victor-garcia-nk-ctl/danish-forecast/PRIOR_ART.md](friends/victor-garcia-nk-ctl/danish-forecast/PRIOR_ART.md)_

## Independent prior-art audit (2026-11-04)

Scope: retrospective validation of the unchanged Cadosch et al. (2020), DOI 10.7717/peerj.8913, Danish macrolide-resistance forecast against later SSI/MiBa summaries.

Audit started before writing recomputation code. The source model and ordinary binomial logistic trend are the standard methods to reproduce. There is no identified official leaderboard for this epidemiological validation question.

Pending: independently open the primary paper, its public repository, SSI reports, all potentially overlapping forward citations returned by `cited-by`, and direct question searches. Check public code and AI result repositories and community sources. The claimant's prior-art assertions are unverified input.

This is an exact reconstruction and retrospective forecasting audit, not a new model search. No improvement or novelty is assumed.

### Initial independent findings
- Primary full text downloaded independently from Europe PMC (`primary.xml`, PMCID PMC7147432). The abstract and Results print the treatment-conditional 2025 values 25% (9–30), 84% (36–98), 62% (48–76); Victor Garcia is a coauthor. Table 2 supplies the four Danish rows.
- Official code: https://github.com/calthaus/MG-resistance; archived commit 95fd31a6af5a94d287be07b2d199c38ae86149fe downloaded as `official.R`. Reproduction will use the authors' ODE, optimizer, initial state, parameter transforms, seed and 10,000 simulations unchanged on the authorized pod. Independent recalculation will use separately written Python, not the claimant's code or existing referee.
- Ran `cited-by 10.7717/peerj.8913 --limit 200` myself: `cited_by.txt`. OpenAlex headline count 17; independent raw query returns 12 (`citing_works.json`); abstracts and primary locations inventoried in `citation_inventory.txt`. Overlapping papers are being opened in full, with access failures recorded.
- Opened the three current SSI primary reports (2003–2022, 2011–2023, 2024). They document episodes, source changes and treatment changes. Figures require visual checking.
- Direct searches: "Mycoplasma genitalium" "forecast validation"; "Cadosch" "forecast" "Denmark" resistance validation; "Mycoplasma genitalium" "forecast" "MiBa"; "MG-resistance" "validation" github; source DOI + Denmark + 2026. No earlier same comparison located in the returned material; search results were noisy, so this is a bounded search, not proof of absence.
- arXiv, public-code, community and AI-repository scoped searches returned no relevant validation. There is no numerical record/leaderboard for this retrospective question. Additional primary-paper and GitHub issue/PR checks remain pending.

### Completed source and code checks
- Independent official run succeeded on fnew, using unchanged source, deSolve 1.42 and archived bbmle 1.0.23.1, seed 71309 and all 30,000 draws. `official_pod_result.txt` reproduces all three printed point estimates and intervals. This is the reconstructed standard baseline, not a new result.
- Live GitHub API: latest commit remains 95fd31a6af5a94d287be07b2d199c38ae86149fe (2020-07-22), code change 2019-10-23. The all-state issue/PR query is empty (`github_issues.json`). Repository search sorted by updated (`github_search.json`) finds the official repository and five unrelated name matches; no relevant newer validation code.
- arXiv exact-species search sorted newest (`arxiv_search.xml`) returns zero records; no directly relevant recent arXiv paper located. Web-scoped searches for the question in BakeLab, Google DeepMind, OpenAI/math, X and Reddit yielded no earlier comparison. These are search-result checks, not complete audits of all repository contents or private community discussions.

### Forward-citation screening
Ran the required helper independently for published DOI 10.7717/peerj.8913, then independently for its preprint DOI 10.1101/321216 after a reference in Braam 2020 revealed it. Raw inventories are retained.

| Citing work | Independent inspection and relevance |
|---|---|
| Bolaji 2026, 10.1371/journal.pgph.0006834 | Abstract and full text from Europe PMC; especially numerical simulations and conclusion. Different theoretical model and qualitative comparisons to aggregate resistance ranges; no frozen Danish forecast scored against SSI/MiBa. |
| Tenney et al. 2026, 10.1093/ofid/ofag031 | Abstract and full text; resistance prevalence, surveillance gaps and conclusion. Treatment review, not this forecast/baseline test. |
| Carvajal-Garcia 2024, 10.1093/narmme/ugae001 | Abstract and full text downloaded; small-molecule experiments, not national forecast validation. |
| Riou 2023, 10.1186/s12879-023-08200-4 | Abstract and full Methods/Results/Discussion, primary Springer and Europe PMC. Gonococcal models fitted to GRASP, not this Danish M. genitalium comparison. |
| Nowack 2023, 10.1007/s00105-022-05099-x | Abstract and full text; M. genitalium subsection. Pandemic/clinical review, no this forecast test. |
| De Baetselier 2022, 10.1093/ofid/ofac615 | Abstract, cohort methods, resistance results and discussion; West African MSM study, not Danish annual validation. |
| Recombinant-protein diagnostic review, 10.33448/rsd-v11i10.32970 | Abstract excludes forecasting; diagnostic serology meta-analysis. |
| Yonathan 2022, 10.36452/jkdoktmeditek.v28i2.2264 | Primary PDF abstract and macrolide section, p.241. Repeats the original 25/84/62% forecasts; does not test them with the later Danish series. |
| Wood 2021, 10.1128/jcm.00819-21 | Abstract, results and discussion; U.S. treatment outcomes. Repeats original forecasts as conditional predictions, no Danish external test. |
| Xu 2021, 10.1038/s41598-021-90627-3 | Abstract, calibration and output methods, results/discussion; Australian anatomical-site model, not this validation. |
| Kenyon 2021, 10.1097/OLQ.0000000000001404 | Primary abstract and institutional metadata read. Full text unavailable: DOI payment/subscription response and LWW access failures. Describes 179 PrEP participants, 70 infections, and treated/untreated comparison; no indication of Danish forecast validation in the abstract. Relevant full section NOT inspected. |
| Ong 2021, 10.1016/j.eclinm.2021.100779 | Full text; Australian MSM screening-model methods/discussion. Cites source mechanistic conclusion, not the Danish forecast/baseline comparison. |

Additional checks:
- Europe PMC forward citations (11) add Waters 2026, 10.1097/olq.0000000000002369: primary abstract reports Seattle cohort (2014–2018), sequential sex practices; no Danish forecast test. Full XML endpoint returned HTTP 500.
- Braam 2020 (PMC7575077) found by direct search: full abstract/results/discussion checked; Dutch 2018 assay/prevalence data, not the later Danish test. References the 2018 source preprint, explaining why checking only the final paper DOI can miss citations.
- Source preprint helper returns four works: Tenney 2026 (full text inspected above), a 2021 qualitative model (10.1002/cmm4.1199), Cina 2019 natural-history systematic review (10.1136/sextrans-2018-053823), and a short 2019 clinical item (10.1007/s15011-019-2392-x). Abstracts of the first two new titles describe equilibrium/optimal control and natural history rather than this test. Wiley/other full-text access was unsuccessful; the 2019 clinical item could not be inspected beyond bibliographic information.
- Chua 2025 (10.1016/j.lanmic.2024.101047): primary abstract/core metadata and Monash institutional abstract inspected. Includes surveillance sampled through 2021 and searched through April 2023. Full text unavailable from Lancet/ScienceDirect (403), Elsevier API, or the temporarily restricted Bern repository. No full relevant-section review claimed.

### Coverage limits and facts for the verdict
OpenAlex's headline is 17 but its raw indexed citation query returns 12; Semantic Scholar returns 11; Crossref's count is 11; Europe PMC returns 11, one additional title. The discrepancy is unresolved and does not prove five actual unidentified papers exist. No inspected material contains the exact frozen Danish forecast/baseline test. This bounded negative search does not complete the requested full-text exclusion of prior work. No priority conclusion is asserted from inaccessible material.

What differs from the 2020 source: later SSI/MiBa surveillance fractions and a historical constant/logistic error comparison. Source reproduction, equations, optimizer, surveillance observations themselves, and the general warning about changed ascertainment are not new. Kind: note is honest for the additional empirical comparison; the source reconstruction by itself is a rerun.

### Fresh referee pass, 2026-11-05
The directory contains an earlier incomplete referee pass; its reports and code are not accepted as verification. I have rerun cited-by (cited_by_current.txt) and direct public searches. They show the same 12 returned citing titles and a headline count of 17. I will reconstruct the numerical comparison anew from the primary paper, inspect the potentially overlapping papers, and specifically try the open Chua copies identified in OPEN_ACCESS.md. No forecast-validation leaderboard is applicable. Prior code will not be imported or copied.

#### Fresh pass conclusions (2026-11-05)
- Independently ran both cited-by commands again: `cited_by_current.txt` (published DOI) and `cited_by_preprint_current.txt`. The raw OpenAlex query in `fresh_citations.json` again returns 12 versus the headline 17. A count mismatch does not establish either missing papers or prior overlap.
- Fresh primary XML (`primary_current.xml`) was fetched from Europe PMC. Read equations 1–6, Tables 1–2, fitting section, Results and Discussion; Victor Garcia is a named coauthor, and the three conditional 2025 projections are genuinely printed. The source prints no later-surveillance MAE.
- Reopened the SSI 2003–2022, MiBa 2011–2023 and MiBa 2024 primary reports. Freshly downloaded and visually read SSI Table 4 (`fresh_ssi2022.png`) and MiBa Figure 2 (`fresh_miba2023.png`): 274 at 62.6% in 2021, 311/436 in 2022, and MiBa 60.6/63.2/63.6. The 2024 report says 65% in each sex; the pooled rate is bounded by their common rounding interval. The 2022 MiBa/SSI difference is 8.1303 points, not an independent biological replication.
- Read the abstracts and relevant full-text sections in the primary XMLs for Bolaji (numerical simulation/conclusion), Riou (methods/results/discussion), Ong (methods/discussion), Xu (Australian anatomical-site model), Wood (treatment outcomes/discussion), De Baetselier (West African cohort), Tenney (resistance/surveillance/conclusion), Nowack (M. genitalium subsection), and Carvajal-Garcia (experimental results/discussion). These describe other analyses, not the frozen Danish annual forecast comparison. Yonathan's primary PDF abstract and macrolide section repeat the 25/84/62 forecasts, without testing them. Recombinant-protein review's primary abstract concerns diagnostic test sensitivity/specificity and excludes this question.
- Fresh Kenyon core abstract (`fresh_kenyon_core.json`) describes 179 PrEP participants and treated/untreated infection clearance/resistance. It settles that this is a different cohort question. Full text remains unread; fresh OpenAlex locations list only DOI and PubMed, with no repository/PDF copy.
- CMM 2021 (10.1002/cmm4.1199) abstract describes equilibrium/stability/optimal control, not Danish forecast validation. Tried the Wiley/public repository locations returned by OpenAlex: Turin is restricted; Minho/Aveiro attempts retained. Full text remains unread. Cina 2019's abstract concerns natural history using studies searched through March 2018; it cannot contain these later outcomes. The 2019 clinical item 10.1007/s15011-019-2392-x has no readable full text here and likewise predates the scored surveillance.
- Chua 2025 is gold open access, NOT asserted paywalled. Fresh OpenAlex (`chua_openalex_current.json`) lists the publisher, SSRN, Bern BORIS/CRIS, Melbourne and PubMed. Lancet full text returns 403; ScienceDirect PDF paths return HTML challenge pages, not PDFs; Elsevier API returns only 1,994 bytes of core metadata, no body; SSRN DOI and direct delivery return challenge pages; Bern fetches time out/fail; Melbourne loads but its public item/bundles endpoint reports zero bundles. Europe PMC has no PMCID/full-text copy. The primary abstract covers samples through 2021, searches through April 2023, and regional prevalence meta-analysis, but Discussion/supplement remain unread. No exclusion of a forecast comparison from that unseen text is asserted.
- Direct searches for Cadosch + Danish forecast/validation, M. genitalium + MiBa + forecast, and the note's baseline question found no earlier same comparison. Scoped public-code, AI-result-repository, X/Reddit and recent-paper searches found none; these are bounded searches, not exhaustive exclusions. Fresh official GitHub API checks show latest commit 95fd31a6af5a94d287be07b2d199c38ae86149fe and zero issues/PRs. No applicable live leaderboard exists.
- Independent code `fresh_recompute.py` imports no claimant or previous referee code. It reconstructs all four compartments, refits the original likelihood with Nelder–Mead, fits ordinary binomial logistic IRLS to the four historical rows, recomputes all six later observations and same-split MAEs, calls sbs.py, and checks all rounding corners. The scalar resistance-ratio identity agrees with ODE integration within 3.36e-11. `fresh_recomputation.json` and `BASELINES.json` contain results. The original model's advantage survives independent fitting, numerical tolerance and outcome rounding.
- Attempt to rerun the unchanged official R source on the specifically authorized shared pod failed before remote execution: friends_podsh.py raises KeyError: fnew. No alternate pod was used and no files left the Mini. The complete light recomputation ran locally, one thread, nice 10, well below the 4 GB/4-core limit; the earlier official bootstrap output is archival evidence only.

The factual addition relative to the source is a later-data comparison and two historical-baseline scores. It is not a source optimizer restart, so Kind: note is honest. The weakest point remains the changed surveillance target/treatment exposure. No inspected work already has the comparison; unread full texts and citation coverage are caveats, not evidence that the result is false. The bounded literature check does not prove absolute priority.
- Access update: the Minho open accepted manuscript for Almeida et al. CMM 2021 was successfully downloaded and read (`fresh_cmm.pdf`, 16 pages; `fresh_cmm.txt`). Its numerical illustrations and final discussion use country-parameter theoretical/optimal-control scenarios; they do not use the later SSI/MiBa observations or this frozen-forecast error comparison. Remove CMM from the unread-full-text caveats above. This is why repository copies were tried before declaring access unavailable.

---

# Contributions to AI-bio companies and open-source tools

Pull requests to AI-for-biology companies' public code, with their live status: [README](README.md#contributions-to-ai-bio-companies-and-open-source-tools).

---

# References

Nothing here is from scratch. Each repository carries its own references; this list covers the hub.

- Brian Armstrong, [publicly funded science as open source](https://x.com/brian_armstrong/status/2119150702446420027), November 7, 2026.
- Arc Institute, [Virtual Cell Challenge](https://virtualcellchallenge.org/).
- Anthropic and Adaptyv Bio, [the protein design competition](https://proteinbase.com/competitions/anthropic-adaptyv-2026).
- [Virtual Embryo Challenge](https://virtualembryo.ai/challenge).
- Márquez et al., ExOrthist, *Genome Biology* 2021, [doi:10.1186/s13059-021-02441-9](https://doi.org/10.1186/s13059-021-02441-9).
- Tapial et al., vast-tools / VastDB, *Genome Research* 2017, [doi:10.1101/gr.220962.117](https://doi.org/10.1101/gr.220962.117).
- Boyle et al., GO::TermFinder, *Bioinformatics* 2004, [doi:10.1093/bioinformatics/bth456](https://doi.org/10.1093/bioinformatics/bth456).
- Müller, Salathé and Kummervold, COVID-Twitter-BERT, [arXiv:2005.07503](https://arxiv.org/abs/2005.07503).
- Garcia, Bonhoeffer and Fu, *J. Theor. Biol.* 2020, [doi:10.1016/j.jtbi.2020.110185](https://doi.org/10.1016/j.jtbi.2020.110185).
- pyglmnet, [glm-tools/pyglmnet](https://github.com/glm-tools/pyglmnet); multimedia, structSSI and miniLNM on CRAN.
- Anthropic Economics, [AI for scientific discovery: how researchers use Claude](https://www.anthropic.com/research/how-researchers-use-claude), November 5, 2026 — the per-field numbers the retro uses.
- Pinho, Garcia and Feldman, *PLOS ONE* 2015, [doi:10.1371/journal.pone.0119972](https://doi.org/10.1371/journal.pone.0119972); Pinho, Garcia, Irimia and Feldman, *PLoS Comput Biol* 2014, [doi:10.1371/journal.pcbi.1003916](https://doi.org/10.1371/journal.pcbi.1003916).

Thanks to Arc Institute, to Adaptyv Bio and Anthropic for funding experimental validation, and to the scientists above for letting an outsider's agents read their code.
