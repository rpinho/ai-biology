# B09

Run `bash repro/B09/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Each fixture has one OG. Counts 6:1 and 3:4 each satisfy >=3 and >=4, and have Other=0. The 1:1 control is one 1:1 OG. Categories must not produce a negative remainder.

Patch: `patches/ExOrthist/21-B09.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
