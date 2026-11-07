# B1-01

Run `bash repro/B1-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The supplied aligned proteins have two matching introns in both query directions, for four intron-match rows. Protein label length must not erase those matches.

Patch: `patches/ExOrthist/12-B1-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
