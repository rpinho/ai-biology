# VT-001

Run `bash repro/VT-001/run.sh /path/to/vast-tools` from the extracted bundle.

Correct answer: The input supplies raw count 3 beside rounded expression 0.00. All three count exports must retain 3. The expression field and genuine NA remain as supplied; the nonzero-expression control is retained.

Patch: `patches/vast-tools/01-VT-001.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
