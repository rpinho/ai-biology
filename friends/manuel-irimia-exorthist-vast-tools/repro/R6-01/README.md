# R6-01

Run `bash repro/R6-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: All three spellings refer to the same Fern annotation and must return the same one identity-lifted pair. A directory component must not become part of the species ID.

Patch: `patches/ExOrthist/26-R6-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
