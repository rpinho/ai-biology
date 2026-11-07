# VT-005

Run `bash repro/VT-005/run.sh /path/to/vast-tools` from the extracted bundle.

Correct answer: The input assigns existing sample A to group 0 and B to group 1. Both numeric and named group configurations must complete with one retained event.

Patch: `patches/vast-tools/05-VT-005.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
