Shipped: an independent finding that the note's limited Danish forecast/baseline comparison holds with caveats; model MAEs are 10.8692 and 16.8373 percentage points, and unread prior-work text limits an unconditional priority conclusion.

The decision is in VERDICT.md. I independently reconstructed the primary paper's equations, historical counts and likelihood in fresh_recompute.py; the claimant's code and previous referee code were not imported. Ordinary binomial logistic IRLS used only the original four historical rows. Six later outcomes were checked against primary SSI reports and images. The unchanged frozen model beats the stated logistic baseline by 3.0502 points on SSI and 3.1095 on MiBa. Independent refitting, a scalar identity and all outcome-rounding corners preserve the comparison. This is a finite retrospective comparison, not general forecasting superiority or causal validation.

Reproduce locally from this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 \
  .venv/bin/python fresh_recompute.py
nice -n 10 cited-by 10.7717/peerj.8913 --limit 200
nice -n 10 cited-by 10.1101/321216 --limit 200
```

The local recomputation took under one second and used one thread. Outputs are fresh_recomputation.json, fresh_recomputation.log and BASELINES.json. Scores are unweighted annual MAEs on identical observations for all three predictors. The mechanistic method is not a published deep-learning score; the general predictive-baseline requirement was applied with MAE's documented --lower-is-better flag.

Primary definitions and the genuine printed conditional 2025 endpoints were read in the newly downloaded primary_current.xml. Fresh SSI Table 4 and MiBa Figure 2 are fresh_ssi2022.png and fresh_miba2023.png. The note's last decimal places depend on deSolve's default tolerances; independent accurate ODE integration changes MAEs by only 0.0052/0.0062 percentage points. Refitted treatment/introduction parameters are 0.1291884/year and 1995.59234, close to the unchanged source's 0.1290696 and 1995.58036. The fit and predictions use no later outcome labels.

The initial SBS call omitted --lower-is-better and failed. I reverted the new scripts to Trash before diagnosis and recreated the corrected local script. The official R rerun could not start because the helper no longer has POD.txt's fnew name configured. No alternate pod was used; no files left the Mini. Earlier official-bootstrap artifacts were read as archived data, not presented as a fresh run. All six light comparisons were recomputed locally.

PRIOR_ART.md records fresh cited-by runs, direct question searches, the 12-returned/17-headline citation discrepancy, relevant primary full-text sections and open-copy attempts. The closest unresolved text is Chua 2025, a gold-OA regional prevalence meta-analysis, whose Discussion and supplement could not be fetched. Its primary abstract was read. Kenyon's abstract settles its different PrEP cohort question. Almeida's 16-page accepted manuscript was recovered from Minho: besides theoretical/optimal-control analysis, section 7 fits English 2016–2017 diagnoses, not this later Danish forecast comparison. No inspected work already contains the note's comparison. No absolute priority or taste judgment is asserted.

The weakest scientific point is target alignment under changed ascertainment and treatment. The historical specimen data, SSI episodes and MiBa case fractions are not interchangeable population observations. The note honestly limits itself to transport to those reporting systems and does not claim the unchanged-treatment mechanism has been refuted. Some outcomes were seen before the retrospective protocol, so absence of researcher selection cannot be independently guaranteed.

Next concrete step: read Chua's Discussion and supplement for an earlier frozen Danish forecast comparison. This access limit warrants HOLDS WITH CAVEATS, not FAILS. The empirical addition relative to the source is the later-data comparison; reproduction and the source model are not new.
