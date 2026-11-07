Independent referee result: HOLDS; NEW confirmed: yes.
The primary paper's Figure 2B value 34.8 is reproduced as 34.8056748605161%
by native all-default R/MASS. Independently evaluated witness stress is
16.969390168877389…%; a separate 320-bit Arb KKT/objective certificate
proves it lies in [16.9693901688773,16.9693901688775]%. See VERDICT.md.

Primary evidence:
- Opened evidence/paper.pdf directly, read pages 1, 5, 13–15, and inspected
  Figure 2 visually. Its axis-calibrated vector circles match native default
  coordinates within 0.014 units and independently recover stress 34.80624%.
- Fresh PLOS Table S2 fetched and parsed; all 61 Rc values reconstructed.
- Released DC3 CSV: 23 sequences, 1164 bases each, terminal stop omitted
  because Rc describes elongation, yielding 387 translated codons each.
- Exact integer squared dissimilarities agree with native R's pair ordering,
  including its six excess ties (253 pairs, 247 distinct dissimilarities).
- Archived paper and CSV hashes match source receipts in the claim; fresh
  bioRxiv paper and CSV downloads were throttled with HTTP 429. This input
  provenance limitation is retained in the verdict.

Reproduce from this directory on arm64 macOS:
  zsh setup_reproduction.sh
This downloads public CRAN R 4.6.2 into a job-local temporary runtime,
extracts it without a system installation, and runs the following scripts:
  nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python recompute.py
  nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python certify.py
  nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python check_plot.py
Python dependencies: pypdf, python-flint, numpy, pymupdf. R/MASS is bundled.
No coordinate search is performed. No claimant code is imported.
Retained data and logs are under results/ and evidence/.
The earlier independent_check.py and pod notes are superseded by these runs.
The large temporary R runtime was moved to Trash after verification.

Prior-art checks and limitations are in PRIOR_ART.md and
 evidence/final_public_recheck.json. Bounded exact-title/DOI/value queries,
updated-sorted GitHub repository queries and seven agent-result trees found
no same-data successor. openai/math's tree is truncated, so no exhaustive
priority conclusion follows. No novelty-of-method judgment is made.

Next: the original author analysis script would directly settle the remaining
preprocessing and tie-convention provenance caveat. No pod or GPU is needed.
