# VT-003

Run `bash repro/VT-003/run.sh /path/to/vast-tools` from the extracted bundle.

Correct answer: Named A1/B1 has coverage for event HsaEX0000001 only. Event HsaEX0000002 has coverage in A1/B2 only and has no eligible named pair. Both input column orders must return event 1 only. No Monte Carlo value is used as a benchmark.

Patch: `patches/vast-tools/06-VT-003.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
