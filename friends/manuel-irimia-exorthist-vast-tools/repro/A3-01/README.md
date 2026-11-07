# A3-01

Run `bash repro/A3-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: A family must occupy one chunk. The 1,001 one-to-one families require both species together at batch size 1,000; all must survive. The family-ordered three-family control is unchanged.

Patch: `patches/ExOrthist/01-A3-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
