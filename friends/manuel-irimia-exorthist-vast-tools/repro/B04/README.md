# B04

Run `bash repro/B04/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Only the first supplied pair has an existing exon cluster, Family.003. The other two pairs must not form a fabricated shared nan cluster. The supplied repair omits pairs without a cluster.

Patch: `patches/ExOrthist/17-B04-B13.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
