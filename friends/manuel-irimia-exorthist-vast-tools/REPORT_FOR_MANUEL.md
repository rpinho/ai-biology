# ExOrthist and vast-tools: bug report, Nov 6 2026

AI agents found these bugs; a separate independent check reproduced each. Pins: ExOrthist `83185dcf04c4bda7c765a6bcf87fb1b48b36f329`; vast-tools `5598e1f1b0067611dc9e5abb285b4eacaf543ee3`.

## How to use

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

## ExOrthist

The D2 same-species count bug (lines 62/69) is the one I sent on 11-05, so it isn't repeated here.

### A3-01: Families split across chunks

At batch size 1,000, species ordering splits 1,000 of 1,001 families across chunks. Split families are not aligned across species.
May already be fixed in your new version; it is still present on public master 83185dc (no newer branch or release).

`bin/A3_split_clusters_in_chunks.pl:179`  
Repro: `bash repro/A3-01/run.sh <repo>`  
Patch: `patches/ExOrthist/01-A3-01.patch`

### A1-03: Transcript IDs replace gene IDs

This triggers when transcript_id comes before gene_id in the GTF (some GTF writers use that order). Transcript IDs are written where the gene IDs belong, the input check still passes, and those proteins can't be matched to their genes in the clusters.

`bin/A1_generate_annotations.pl:109`  
Repro: `bash repro/A1-03/run.sh <repo>`  
Patch: `patches/ExOrthist/02-A1-03.patch`

### A1-01: CDS rows reuse the preceding gene ID

With CDS-only input, all six exon rows are lost. With all exons listed before the CDS lines, one gene's protein is attached to another gene and its exon rows are lost.

`bin/A1_generate_annotations.pl:1108`  
Repro: `bash repro/A1-01/run.sh <repo>`  
Patch: `patches/ExOrthist/03-A1-01.patch`

### A1-05: CDS ordering changes strand translation

This triggers when minus-strand CDS records are in ascending order. The protein sequence changes and the exon numbering is reversed.

`bin/A1_generate_annotations.pl:163`  
Repro: `bash repro/A1-05/run.sh <repo>`  
Patch: `patches/ExOrthist/04-A1-05.patch`

### A1-02: Exon endpoints include a neighboring residue

Exon end positions include one residue from the next exon: 22 instead of 21, and 11 instead of 10. Neighboring exons overlap by one residue.

`bin/A1_generate_annotations.pl:1291`  
Repro: `bash repro/A1-02/run.sh <repo>`  
Patch: `patches/ExOrthist/05-A1-02.patch`

### B1-02: Gene IDs collide between species

This triggers when two species reuse the same gene ID. Two families collapse into one, and all four cross-species pairs are scored instead of the two specified ones.

`bin/B1_parse_IPA_prot_aln.pl:135`  
Repro: `bash repro/B1-02/run.sh <repo>`  
Patch: `patches/ExOrthist/06-B1-02.patch`

### B06: Cluster totals omit reintroduced exons

A four-exon cluster is reported as three exons. Its hub exon's membership score is 1.12 instead of 0.90.

`bin/D2_cluster_EXs.R:80`  
Repro: `bash repro/B06/run.sh <repo>`  
Patch: `patches/ExOrthist/07-B06.patch`

### B11: The dPSI option is ignored

Requesting a dPSI of 40 still applies 15. Two exons are called regulated instead of one.

`bin/compare_exon_sets.pl:45`  
Repro: `bash repro/B11/run.sh <repo>`  
Patch: `patches/ExOrthist/09-B11.patch`

### B4-01: Header filter drops any row containing CID

The header is removed with `grep -v 'CID'`, so every row whose gene ID contains CID (CIDEA, PCID2) is deleted too. In the test, two of four rows are removed from each merged feature table.

`bin/B4_merge_PROT_EX_INT_aln_info.pl:15`  
Repro: `bash repro/B4-01/run.sh <repo>`  
Patch: `patches/ExOrthist/10-B4-01.patch`

### A1-04: Lowercase bases translate to X

Twelve lowercase CDS bases translate to XXXX instead of MAAA.

`bin/A1_generate_annotations.pl:83`  
Repro: `bash repro/A1-04/run.sh <repo>`  
Patch: `patches/ExOrthist/11-A1-04.patch`

### B1-01: Protein labels erase intron matches

This triggers when protein IDs have five characters or fewer. Four intron matches are erased.

`bin/B1_parse_IPA_prot_aln.pl:571`  
Repro: `bash repro/B1-01/run.sh <repo>`  
Patch: `patches/ExOrthist/12-B1-01.patch`

### B2-01: Table splitting changes identifiers

Cluster IDs lose their leading zeros before exon realignment: CID 007300 becomes 7300, and null becomes NA, so the IDs passed on no longer match.

`bin/B2_split_EX_pairs_to_realign.py:18`  
Repro: `bash repro/B2-01/run.sh <repo>`  
Patch: `patches/ExOrthist/13-B2-01.patch`

### B08: Contig hyphens change exon lengths

A pair of 90-nt exons passes on contig7 but disappears on contig-7. A hyphen in the contig name changes the result.

`bin/C2_filter_and_select_best_EX_matches_by_targetgene.pl:84`  
Repro: `bash repro/B08/run.sh <repo>`  
Patch: `patches/ExOrthist/14-B08.patch`

### B03: Reclustering consumes data as headers

The first data row is read as a header. Six genes in three pairs become two genes in one component. Patch shared with B16.

`bin/D3.1_recluster_genes_by_species_pair.py:24`  
Repro: `bash repro/B03/run.sh <repo>`  
Patch: `patches/ExOrthist/15-B16-B03.patch`

### B04: Exons without clusters acquire nan labels

Two pairs that are absent from the exon clusters merge into Family.01nan. Patch shared with B13.

`bin/D3.2_recluster_EXs_by_species_pair.py:44`  
Repro: `bash repro/B04/run.sh <repo>`  
Patch: `patches/ExOrthist/17-B04-B13.patch`

### B13: Coordinate lookup crosses genes

The lookup uses the coordinate only. An exon from an unrelated species at the same coordinate overwrites the pair's suffix .003 with .009. Patch shared with B04.

`bin/D3.2_recluster_EXs_by_species_pair.py:42`  
Repro: `bash repro/B13/run.sh <repo>`  
Patch: `patches/ExOrthist/17-B04-B13.patch`

### B07: Zero cutoffs are replaced by defaults

Similarity and length cutoffs set to zero are replaced by the defaults, so a pair that passes zero cutoffs is dropped.

`bin/C2_filter_and_select_best_EX_matches_by_targetgene.pl:45`  
Repro: `bash repro/B07/run.sh <repo>`  
Patch: `patches/ExOrthist/18-B07.patch`

### R6-02: FASTA descriptions prevent canonical-site lookup

This triggers with -canonical_ss when the FASTA headers have a description. A known canonical exon pair is no longer found (one pair becomes zero).

`bin/get_liftovers.pl:140`  
Repro: `bash repro/R6-02/run.sh <repo>`  
Patch: `patches/ExOrthist/19-R6-02.patch`

### S1-01: Numeric cluster selection returns no data

Selecting cluster 42 for plotting leaves the annotation, overlap and protein inputs empty.

`bin/subset_inputs.py:24`  
Repro: `bash repro/S1-01/run.sh <repo>`  
Patch: `patches/ExOrthist/20-S1-01.patch`

### B09: OG categories miscount species multiplicity

An orthogroup with six genes in one species and one in the other (6:1) misses both the >=3 and >=4 categories. A 3:4 orthogroup gives Other=-1.

`bin/get_cluster_stats.pl:204`  
Repro: `bash repro/B09/run.sh <repo>`  
Patch: `patches/ExOrthist/21-B09.patch`

### Crashes and failed runs

These stop with an error instead of giving wrong results.

#### B05: Singleton reassignment aborts clustering

With input generated by D1, D2 stops with "the condition has length > 1". The whole chunk is aborted.

`bin/D2_cluster_EXs.R:33`  
Repro: `bash repro/B05/run.sh <repo>`  
Patch: `patches/ExOrthist/08-B05.patch`

#### B16: Reclustering rejects the cluster format

The three-column, headerless gene file described in the README raises ParserError. Patch shared with B03.

`bin/D3.1_recluster_genes_by_species_pair.py:27`  
Repro: `bash repro/B16/run.sh <repo>`  
Patch: `patches/ExOrthist/15-B16-B03.patch`

#### B02: The module passes unsupported flags

The --orthopairs exon-reclustering command exits with code 2. It passes -sp1/-sp2 where -s1/-s2 are expected.

`modules/local/exorthist/recluster_exs.nf:26`  
Repro: `bash repro/B02/run.sh <repo>`  
Patch: `patches/ExOrthist/16-B02.patch`

### Minor

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

## vast-tools

- **VT-001**: combine replaces a count of 3 with 0 when cRPKM rounds to 0.00. `bin/MakeTableRPKMs.pl:79`. Repro: `bash repro/VT-001/run.sh <repo>`. Patch: `patches/vast-tools/01-VT-001.patch`.
- **VT-002**: Missing microexon (MIC) counts become numbers in the merged table: renaming samples turns NA into 10/10 and PSI 50. `bin/MergeOutputs.pl:451`. Repro: `bash repro/VT-002/run.sh <repo>`. Patch: `patches/vast-tools/03-VT-002.patch`.
- **VT-004**: diff aborts when a chunk holds one event. The output has only a header, or two of three events. `R/vastdiff.R:226`. Repro: `bash repro/VT-004/run.sh <repo>`. Patch: `patches/vast-tools/02-VT-004.patch`.
- **VT-006**: Minor. When a filter keeps no events, tidy exits 255 with a division by zero (the header-only table it writes is correct). `bin/Filter_and_clean_Combine.pl:520`. Repro: `bash repro/VT-006/run.sh <repo>`. Patch: `patches/vast-tools/04-VT-006.patch`.
- **VT-005**: Minor. With group identifier 0, tidy reports an existing sample as absent. `bin/Filter_and_clean_Combine.pl:221`. Repro: `bash repro/VT-005/run.sh <repo>`. Patch: `patches/vast-tools/05-VT-005.patch`.

### If anyone uses diff --paired

- **VT-003**: Column order overrides the named pairing. One eligible event is lost and one is scored without a pair. `R/vastdiff.R:176`. Repro: `bash repro/VT-003/run.sh <repo>`. Patch: `patches/vast-tools/06-VT-003.patch`.
