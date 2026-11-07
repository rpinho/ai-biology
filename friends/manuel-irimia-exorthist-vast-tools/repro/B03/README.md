# B03

Run `bash repro/B03/run.sh /path/to/ExOrthist` from the extracted bundle.

Correct answer: Three disjoint edges fix components {alpha,beta}, {gamma,delta}, {epsilon,zeta}. All six genes must be returned from the documented headerless inputs.

Patch: `patches/ExOrthist/15-B16-B03.patch`. Shared patch files are applied once. Runtime dependencies and substitutions: [shared instructions](../README.md).

`expected-before.json` is the observed failure on the pinned clean source; `expected-after.json` is the observation after applying the report's patch set. Both were rerun for this bundle.
