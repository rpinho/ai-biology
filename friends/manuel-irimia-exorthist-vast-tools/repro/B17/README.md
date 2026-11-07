# B17

Run `bash repro/B17/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Both fixtures have one 1:1 OG and differ only in its identifier, 0 versus Family. Both must finish and print the same statistics.

Patch: `patches/ExOrthist/29-B17.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
