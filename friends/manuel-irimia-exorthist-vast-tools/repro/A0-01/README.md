# A0-01

Run `bash repro/A0-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: For the fixed date 2026-11-06 the run date must read 2026-11-06, not 2026-06-11. Only the clock call is stubbed.

Patch: `patches/ExOrthist/30-A0-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
