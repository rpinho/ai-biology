# B4-01

Run `bash repro/B4-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: All four supplied rows satisfy the merge rule; CIDEA and PCID2 are data identifiers, not headers. Each of the three feature tables must retain four data rows.

Patch: `patches/ExOrthist/10-B4-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
