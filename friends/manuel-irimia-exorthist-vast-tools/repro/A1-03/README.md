# A1-03

Run `bash repro/A1-03/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The explicit gene_id attributes are oak and elm regardless of attribute order. Both exint headers and the headerless reference-protein table must retain those gene IDs.

Patch: `patches/ExOrthist/02-A1-03.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
