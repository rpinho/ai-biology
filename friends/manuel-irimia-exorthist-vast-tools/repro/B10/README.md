# B10

Run `bash repro/B10/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Annotated exon numbers 1,2,3 and CDS phases 0,1,2 determine fake starts 0,30,60 and downstream phases 1,2,last. Coordinate text order must not change them.

Patch: `patches/ExOrthist/24-B10.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
