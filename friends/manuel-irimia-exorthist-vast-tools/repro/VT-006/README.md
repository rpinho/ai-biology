# VT-006

Run `bash repro/VT-006/run.sh /path/to/vast-tools` from the extracted bundle.

Correct answer: The equal-PSI event has SD zero and should be filtered out. tidy must finish successfully with the header-only result; the varying-PSI control must retain one event.

Patch: `patches/vast-tools/04-VT-006.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
