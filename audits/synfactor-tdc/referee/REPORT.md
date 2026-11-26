Shipped: Independent C1–C6 referee audit from the four raw TDC files and pinned SynFactor source.
C1 and C6 are REFUTED. C2–C5 are CONFIRMED-WITH-CAVEATS. See [VERDICT.md](VERDICT.md) for the claim comparisons, paired intervals, p-values and control audits. [verdict.json](verdict.json) retains full precision.
Direct CP16 passed the matched-control rule on 1/4 scaffold and 1/4 random endpoints. Cartesian-distilled CP16 passed on 3/4 and 3/4. Its teacher fidelity exceeded 0.80 on 8/8 tests.
Solubility coverage was 6,397/9,582 (66.76%). Its scaffold experimental Δρ against the teacher was −0.10885 [−0.13365, −0.08442], p=1/10001. The opposite salt tie reproduced C5’s 6,400/9,574 and 42/1,280 scaffold overlap. The gap under that convention was −0.10758, p=1/10001.
Four SHA-256 values matched the manifest and the seal. The eight synthetic training sets contained 112,330 products in total, with zero exact product overlap with their experimental splits. Some shared scaffolds or capped inputs. No external publication or contact.
Verified harvest covers 144 primary and 18 sensitivity fits. Maximum sampled aggregate worker RSS was 1.005 GB against the 6 GB limit. All guarded stages exited 0.
Sources and limitations are in [PRIOR_ART.md](PRIOR_ART.md), [SEALED.md](SEALED.md), [DEVIATIONS.md](DEVIATIONS.md) and [the upstream commit](https://github.com/mireklzicar/synfactor/tree/1eaee90610d1a54654c0ec22544154676df4f8fa).
Reproduce from this job root in a fresh output tree with the supplied src, data and protocol files. Set a new authorized deadline for a later rerun. The worker guard defaults to the original job deadline.
```sh
export UV_CACHE_DIR="$PWD/.cache/uv" UV_PYTHON_INSTALL_DIR="$PWD/.cache/python" TMPDIR="$PWD/.tmp"
mkdir -p audit "$TMPDIR"
printf '%s\n' 'You asked: Independently reproduce the sealed benchmark.' > STATUS.md
git clone --no-checkout https://github.com/mireklzicar/synfactor ./synfactor && git -C synfactor checkout --detach 1eaee90610d1a54654c0ec22544154676df4f8fa
uv venv --python 3.12.13 .venv && uv pip install --python .venv/bin/python -r audit/environment.txt
pgrep -f ref-synfactor-tdc-1125 | wc -l
set -e
for stage in prepare run evaluate salt_sensitivity; do .venv/bin/python src/guard.py .venv/bin/python "src/$stage.py"; done
.venv/bin/python src/render.py && .venv/bin/python src/harvest.py
```
Retain audit/environment.txt, audit/decisions.json and this report for those commands. AUDIT_DEADLINE is a Unix timestamp. Raw files, checkpoints and resource receipts stay local.
Inference conditions on one split and the fixed ensembles. Score variation across seeds, random-split row order and same-size salt ties limits numerical replication. To make the benchmark exactly replayable, the next protocol should seal the row order, fragment tie direction and split/product identity hashes.
