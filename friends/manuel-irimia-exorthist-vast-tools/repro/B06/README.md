# B06

Run `bash repro/B06/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: For each final cluster, the reported exon total must equal its number of rows. Every fixture gene/species is distinct. Membership is (out-degree+in-degree+reciprocal neighbors)/(2*(final cluster size-1)+(number of genes-1)). The four-member hub must score 9/10=0.90, not 9/8=1.12.

Patch: `patches/ExOrthist/07-B06.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
