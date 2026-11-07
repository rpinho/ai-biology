# B14

Run `bash repro/B14/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The reciprocal triangle always has three exons. Changing oak to oak#extra must not change the four-column tabular parse or abort the cluster.

Patch: `patches/ExOrthist/27-B14.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
