# B1-02

Run `bash repro/B1-02/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: clusters.tsv specifies familyAlpha=Fern seed/Moss spore and familyBeta=Fern spore/Moss seed. Exactly those two protein pairs must be aligned, independently of gene IDs reused between species.

Patch: `patches/ExOrthist/06-B1-02.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
