# A1-04

Run `bash repro/A1-04/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The known codons translate to M + A*9 + E*11 + F*9 for oak and M + K*9 + D*10 + W*10 for elm, regardless of masking case.

Patch: `patches/ExOrthist/11-A1-04.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
