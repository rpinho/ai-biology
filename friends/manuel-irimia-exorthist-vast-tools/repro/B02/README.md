# B02

Run `bash repro/B02/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The flags extracted from recluster_exs.nf must be accepted by its D3.2 script. The known oak/elm pair must produce two exon rows. This is a direct module-command test, not a Nextflow run.

Patch: `patches/ExOrthist/16-B02.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
