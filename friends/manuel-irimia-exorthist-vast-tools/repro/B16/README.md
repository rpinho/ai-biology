# B16

Run `bash repro/B16/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The README documents three gene-cluster columns with no header. Four supplied genes in two disjoint pairs must parse and all four must be returned. Orthopairs are also headerless.

Patch: `patches/ExOrthist/15-B16-B03.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
