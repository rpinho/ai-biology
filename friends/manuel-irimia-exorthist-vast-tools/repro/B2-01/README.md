# B2-01

Run `bash repro/B2-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Table partitioning must round-trip the exact CID strings 007300, null and fam7300. No inference about numeric values or missingness is appropriate for those identifiers.

Patch: `patches/ExOrthist/13-B2-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
