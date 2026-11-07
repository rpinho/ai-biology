# B07

Run `bash repro/B07/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Exon lengths 120 and 40 have ratio 1/3; similarity 0.001 exceeds a zero threshold. Both zero and tiny-positive similarity/length minima must retain the pair.

Patch: `patches/ExOrthist/18-B07.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
