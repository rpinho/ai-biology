# B01

Run `bash repro/B01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The oak intervals 980-1120 and 1010-1070 overlap. The long interval has two targets and must represent both pairs; the headerless C5 output must contain exactly two pairs.

Patch: `patches/ExOrthist/23-B01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
