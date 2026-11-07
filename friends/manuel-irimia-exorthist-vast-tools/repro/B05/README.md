# B05

Run `bash repro/B05/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Real D1 computes reciprocal flags from the supplied directed edges. D2 must complete and return exon rows rather than fail with a vector condition. Community partitioning can depend on igraph version.

Patch: `patches/ExOrthist/08-B05.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
