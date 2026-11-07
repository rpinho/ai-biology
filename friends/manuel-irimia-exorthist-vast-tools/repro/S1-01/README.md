# S1-01

Run `bash repro/S1-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Selecting the only cluster yields two GTF rows, one overlap row and a reference-protein file with a header plus one protein, for both numeric and textual cluster IDs.

Patch: `patches/ExOrthist/20-S1-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
