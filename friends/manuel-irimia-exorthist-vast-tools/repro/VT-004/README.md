# VT-004

Run `bash repro/VT-004/run.sh /path/to/vast-tools` from the extracted bundle.

Correct answer: Every supplied event passes coverage. Single-event input must finish with one result, tail input with chunk size 2 must finish with three results, and the two-event control with two. Paired/unpaired modes and default PDF singleton are exercised.

Patch: `patches/vast-tools/02-VT-004.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
