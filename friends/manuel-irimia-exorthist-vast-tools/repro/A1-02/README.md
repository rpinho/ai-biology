# A1-02

Run `bash repro/A1-02/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: CDS lengths 31,32,27 give cumulative ends 31,63,90 and amino-acid endpoints ceil(n/3)=11,21,30. Lengths 30,30,30 give endpoints 10,20,30. This case checks endpoints only; partial-codon start conventions are outside this claim.

Patch: `patches/ExOrthist/05-A1-02.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
