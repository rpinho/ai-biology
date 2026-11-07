# A1-07

Run `bash repro/A1-07/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The second transcript shares the protein and CDS and differs in UTR. It must not concatenate another coding sequence: oak remains 30 residues and three CDS exons.

Patch: `patches/ExOrthist/22-A1-07.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
