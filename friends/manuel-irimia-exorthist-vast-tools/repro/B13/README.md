# B13

Run `bash repro/B13/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: The oak/elm pair explicitly belongs to Family.003 and must become Family.01.003. The unrelated birch coordinate collision must not change its suffix to .009.

Patch: `patches/ExOrthist/17-B04-B13.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
