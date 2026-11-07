# A1-01

Run `bash repro/A1-01/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Both oak and elm have three CDS exons. Both protein IDs must retain their own gene suffix, and all six exon rows must exist for CDS-only, exons-first and interleaved inputs.

Patch: `patches/ExOrthist/03-A1-01.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
