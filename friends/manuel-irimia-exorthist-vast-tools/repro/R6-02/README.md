# R6-02

Run `bash repro/R6-02/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The target sequence has a known AG/GT splice site. The same one identity-lifted pair must survive whether chr1 has a FASTA description or not.

Patch: `patches/ExOrthist/19-R6-02.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
