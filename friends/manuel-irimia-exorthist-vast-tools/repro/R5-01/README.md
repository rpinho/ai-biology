# R5-01

Run `bash repro/R5-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Both known alignment sequences must appear in the isolated Fern/Moss display. Sharing six accession-prefix characters must not empty Moss. The IPA file was constructed in B0 format.

Patch: `patches/ExOrthist/25-R5-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
