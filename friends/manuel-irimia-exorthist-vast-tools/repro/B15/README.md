# B15

Run `bash repro/B15/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The two A/B components remain {ash,birch} and {oak,elm} for all seeds. Compare gene-to-label dictionaries across seeds, ignoring row order. C/D sentinel records isolate this from header loss; see ../README.md. Biological membership is unchanged by the original defect.

Patch: `patches/ExOrthist/28-B15.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
