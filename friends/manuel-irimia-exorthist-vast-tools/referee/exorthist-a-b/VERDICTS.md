# ExOrthist A/B referee verdicts

**12 CONFIRMED; 4 CONFIRMED-MINOR.** All sixteen mechanisms reproduced independently on unpatched 83185dcf04c4bda7c765a6bcf87fb1b48b36f329. “Minor” reflects limited exposure or a helper/cosmetic effect; it does not mean the output is correct. The suspected list was excluded.

Each linked note supplies the minimal inputs, independently computed correct answer, actual output, cited source lines, normal-use assessment and known/fixed status. [Methods and rerun commands](repro/README.md). The final runs used a separate pristine pinned clone for each claim.

| ID | Verdict | My repro path | Effect on users' results |
|---|---|---|---|
| A0-01 | CONFIRMED-MINOR | [repro/A0-01](repro/A0-01/README.md) | Prints 2026-06-11 on November 6; cosmetic run-date error. |
| A1-01 | CONFIRMED | [repro/A1-01](repro/A1-01/README.md) | CDS-only input loses all six exon rows; exons-first input attaches oak's protein to elm and loses oak's three rows. |
| A1-02 | CONFIRMED | [repro/A1-02](repro/A1-02/README.md) | Exon endpoints include a residue from the next exon: observed 22 instead of 21, and 11 instead of 10, on ordinary CDS input. |
| A1-03 | CONFIRMED | [repro/A1-03](repro/A1-03/README.md) | Transcript-first GTF writes transcripts into gene slots, preventing matching under the real gene IDs used in clusters. |
| A1-04 | CONFIRMED | [repro/A1-04](repro/A1-04/README.md) | Twelve lowercase known CDS bases become four X residues rather than MAAA. |
| A1-05 | CONFIRMED | [repro/A1-05](repro/A1-05/README.md) | Ascending negative-strand CDS rows produce the wrong protein and reversed coding-exon numbering. |
| A1-07 | CONFIRMED-MINOR | [repro/A1-07](repro/A1-07/README.md) | Shared protein IDs concatenate CDSs: 30 aa/three exons become 60 aa/six exons; claimed RefSeq prevalence unsubstantiated. |
| A3-01 | CONFIRMED | [repro/A3-01](repro/A3-01/README.md) | Species-sorted rows split 1000 of 1001 families at the documented 1000-alignment batch size; B1 requires both species in one chunk. |
| B1-01 | CONFIRMED | [repro/B1-01](repro/B1-01/README.md) | Short protein IDs erase four known directional intron matches; real B5 reports all four as NO_INTRON. † |
| B1-02 | CONFIRMED | [repro/B1-02](repro/B1-02/README.md) | Reused gene IDs collapse two families into one and score all four cross-species pairs rather than the two specified pairs. † |
| B2-01 | CONFIRMED | [repro/B2-01](repro/B2-01/README.md) | Table splitting changes CID 007300 to 7300 and null to NA, corrupting identifiers forwarded to realignment. |
| B4-01 | CONFIRMED | [repro/B4-01](repro/B4-01/README.md) | CIDEA and PCID2 disappear from all three merged feature tables; four eligible rows become two. |
| R5-01 | CONFIRMED-MINOR | [repro/R5-01](repro/R5-01/README.md) | Shared six-character accession prefixes label both alignment rows as one species and leave the other species empty; viewer only. ‡ |
| R6-01 | CONFIRMED-MINOR | [repro/R6-01](repro/R6-01/README.md) | ./Fern.gtf or data.v1/Fern.gtf causes an explicit species-name failure before any liftover; plain Fern.gtf succeeds. |
| R6-02 | CONFIRMED | [repro/R6-02](repro/R6-02/README.md) | With canonical_ss, adding a normal FASTA description changes one known canonical exon pair to zero pairs. § |
| S1-01 | CONFIRMED | [repro/S1-01](repro/S1-01/README.md) | Numeric cluster selection returns empty annotation/overlap/protein data instead of 2/1/1 rows, breaking plot inputs. |

† Real B0/B1 (and B5 for B1-01), with an independently written equal-length pass-through MAFFT stand-in. No real MAFFT/Nextflow run is certified. ‡ Newly hand-built B0-format alignment, as permitted for this claim. § Identity liftOver and small BED6 intersection stand-ins; genomic remapping is not certified. R6-01's failure occurs before those tools. All other rows use real scripts directly without stand-ins. Python checks used pandas 1.5.3 (repository container: 1.5.2).

**Known/fixed:** no exact matching public report or later fix found in 42 issue/PR records, 102 comments, recent and relevant historical commits, the other branch, or current release. Current master and release v2.0.0 are the pinned version; the other branch has the same files. A1-02 has related 2021 phase-handling history, explicitly discussed in its note. No exact-name CRAN/PyPI/Bioconda distribution was found (404 responses). [Sources and limits](prior_art/README.md). Absence in this search does not establish private awareness or scientific novelty.

The five author candidates below are ranked by demonstrated effect on results and normal input reachability, without estimating population prevalence or whether Manuel would care. Ricardo reads them first; nothing has been sent.

1. **A3-01 — entire families lost at chunk boundaries.** The real A2→A3 reproduction at the documented batch size splits 1000 of 1001 one-to-one families; B1's same-chunk condition then excludes those families. Input ordering is not restricted in the README.
2. **A1-03 — real gene identities replaced by transcript IDs.** A routine GTF writer emits this attribute order; A0 accepts it. B1's gene-cluster lookup consequently cannot select these proteins under their real genes. This downstream consequence follows from B1 source; no full pipeline run was claimed.
3. **A1-01 — annotation loss from row-order dependence.** Correct gene attributes on CDS rows are ignored in Part 2; exons-first input demonstrably loses oak, and CDS-only input loses both genes' exon rows. No interleaving requirement is documented.
4. **A1-05 — wrong negative-strand protein on ascending rows.** This changes the sequence and exon numbering, not just metadata. The equal-length wrong output demonstrates that normal length checks would miss it.
5. **A1-02 — ordinary exon coordinates include a neighboring residue.** Direct nucleotide arithmetic proves it, and the downstream residue assignment/extraction uses those coordinates. The hunter's genome-wide percentages and final-score deltas were not independently recomputed and are not endorsed.

**NEW: no** under the lane's scientific definition. This ships an independent bug-referee conclusion, not a novel scientific result, a published-number improvement, or a new-data prediction test. No predictive-model performance claim is made; SBS is not applicable. No hunter patch was applied or certified. No public actions or contacts occurred.
