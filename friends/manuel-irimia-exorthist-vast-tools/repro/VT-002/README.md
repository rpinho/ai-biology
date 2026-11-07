# VT-002

Run `bash repro/VT-002/run.sh /path/to/vast-tools` from the extracted bundle.

Correct answer: A missing plus known contribution remains unknown, as in the existing last-NA policy. Renaming sample files must not change the result. Numeric-only control sums 10+10 to 20 for each count and gives PSI 50.

Patch: `patches/vast-tools/03-VT-002.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
