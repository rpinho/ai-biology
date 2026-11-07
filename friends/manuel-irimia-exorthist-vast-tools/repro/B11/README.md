# B11

Run `bash repro/B11/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Absolute dPSI values 24 and 65 yield exactly one regulated exon at threshold 40 and two at default threshold 15. Both the announced threshold and counted set are checked.

Patch: `patches/ExOrthist/09-B11.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
