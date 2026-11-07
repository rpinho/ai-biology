# A1-05

Run `bash repro/A1-05/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Reverse-complementing the three minus-strand CDS pieces in transcript order gives M + K*9 + D*10 + W*10. Exons 1,2,3 are 701-730,601-630,501-530 for both GTF orderings.

Patch: `patches/ExOrthist/04-A1-05.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
