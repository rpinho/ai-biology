# B08

Run `bash repro/B08/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Both exons are 90 nt long. Their ratio is 1, exceeding 0.8, with or without the contig-name hyphen.

Patch: `patches/ExOrthist/14-B08.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
