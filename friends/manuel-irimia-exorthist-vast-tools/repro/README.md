# Reproductions

Run `bash repro/<ID>/run.sh /absolute/path/to/repository`. Use ExOrthist for A/B/R/S IDs and vast-tools for VT IDs. The caller-selected repository is never copied or patched by the runner.

Each runner prints a JSON observation followed on stderr by `CORRECT` or `WRONG OUTPUT / FAILURE REPRODUCED`. Exit zero means the reproduction completed, including when it demonstrated the upstream bug. Compare stdout to `expected-before.json` or `expected-after.json`. A harness/dependency error exits nonzero. New run files and upstream stdout/stderr are retained under that case's `runs/` directory; those generated directories are excluded from the bundle.

Dependencies are the tools' normal dependencies: bash, Perl and Python 3; pandas 1.5.x for the Python ExOrthist stages; R with igraph and hashmap for D2, and optparse for vast-tools diff. The supplied Python harness itself uses only the standard library. `PYTHON` and `RSCRIPT` can select interpreters; otherwise they are found on PATH. Verification used Python 3.11.18/pandas 1.5.3, R 4.5.3/igraph 2.3.4, and system Perl. There is no Nextflow, database download, compiled test program or network operation in these runners.

External-tool substitutions, all under `_shared/stubs/`:

- B1-01 and B1-02 use a MAFFT stand-in that passes through the supplied equal-length aligned sequences. Real B0 and B1 execute. This tests parsing and protein selection conditional on these alignments; it does not test MAFFT scoring or a whole Nextflow run.
- R6-01 and R6-02 use identity liftOver and a BED6 `bedtools intersect -wao` stand-in. The fixtures include a known AG/GT target splice site. This tests the helper's filename and FASTA parsing, not chain remapping. The R6-01 failures precede either external tool.
- R5-01 uses a hand-built single-block B0-format IPA file, not an aligner output produced in this job.
- A0-01 fixes Perl's `localtime` to noon on 2026-11-06 using a wrapper, so its calendar test remains reproducible on other dates. The upstream file is unchanged.

B02 extracts and executes the species flags from the actual Nextflow module; it does not run Nextflow. B04/B13 run D3.2 directly; B16/B02 block that optional workflow on the unpatched repository. B15 prepends an out-of-pair C/D component to the referee's two A/B components, in headerless form. Both parsers exclude C/D, leaving the same four A/B genes on both sides, so the comparison isolates hash-seed label dependence from B03's first-row loss.

Expected summaries are recorded from this job's reruns. Their `correct` field is computed against the arithmetic, identifiers, or error-free completion described in each case README, rather than obtained by accepting the patched output as the oracle. `expected/before/` and `expected/after/` retain relevant program outputs and logs. Paths in logs are replaced by `<repo>` and `<run>` for readability. No prevalence or scientific benchmark claim is made.
