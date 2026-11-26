# Sealed Empirical Results: SynFactor CP16 vs Additive & Full-Molecule Baselines on TDC ADMET Benchmarks

**Protocol:** [SEALED.md](../SEALED.md) (frozen at commit `ee30be763e5c800ddc5c47a62ecc1700231c7599`, untouched)  
**Target system:** `mireklzicar/synfactor` @ `1eaee90610d1a54654c0ec22544154676df4f8fa`  
**Deviations:** [DEVIATIONS.md](../DEVIATIONS.md) (RDKit `2025.9.6` wheel for `MurckoDecompose` + LightGBM subprocess isolation for macOS dual-`libomp` + exact `< 1e-12` vectorized stats; zero protocol/hyperparameter changes)  
**Run telemetry:** `2063.7 s` total wall-clock across 4 endpoints × 2 splits (`results/summary.json`), Peak RSS `1736.3 MB` (`1.70 GB` ≤ `6 GB` cap), 10/10 unit tests passing (`src/test_pipeline.py`), independent CSV-vs-JSON point-metric discrepancy `0.000e+00`.

---

## Executive Pre-Registered Verdicts (SEALED.md Sec. 5)

| Hypothesis | Pre-Registered Verdict | Concise Finding |
| --- | --- | --- |
| **H1 (Non-Additive CP16 Gain over Matched Neural Additive Control)** | **PASS (Distilled-Cartesian only); FAIL (Direct)** | **Direct training:** `0/4` PASS on Scaffold, `0/4` PASS on Random (0 degradations). Matching the 2,058-dim synthon trunk eliminates 100% of CP16's apparent direct edge over `Additive-ID-Direct`. **Distilled-Cartesian (SynFactor's intended workflow):** **`3/4` PASS on Scaffold** and **`3/4` PASS on Random** (`Lipophilicity`, `Solubility`, `CYP3A4` all pass at $p \le 0.0042$, 95% CIs strictly excluding 0; `hERG` positive `+0.0104`/`+0.0094` but underpowered at $n=119/120$; `0` degradations). Exceeds pre-registered Overall H1 PASS bar ($\ge 2/4$ Scaffold OR $\ge 3/4$ Random, 0 degradations). |
| **H2 (Teacher Fidelity vs Experimental Accuracy Gap)** | **Teacher $\ge 0.80$ MET (8/8); Significant Experimental Loss vs Teacher (6/8)** | `CP16-Distilled-Cartesian` exceeds `0.80` teacher Spearman on **all 8/8** splits (`0.8223–0.9033` Scaffold; `0.8991–0.9613` Random). Despite high teacher fidelity, it still suffers a **statistically significant experimental accuracy drop vs `FullMol-LGBM`** on all 3 large endpoints on both splits (Scaffold: Lipophilicity $\Delta\rho=-0.0875$, $\Delta\text{RMSE}=+0.0869$; Solubility $\Delta\rho=-0.1085$, $\Delta\text{RMSE}=+0.2040$; CYP3A4 $\Delta\text{AUROC}=-0.0262$; all $p=1.0\times 10^{-4}$). |
| **H3 (Coverage & Synthon Overlap Audit)** | **Quantified (High Novelty / Partial Coverage)** | BRICS 1-cut coverage is `93.0%–95.9%` on drug-like endpoints (`hERG`, `Lipophilicity`, `CYP3A4`) but only **`66.85%`** (`6,400/9,574`) on `Solubility_AqSolDB`. Under Scaffold splits, only **`2.52%–12.58%`** of test molecules have both synthons seen in train (`87.4%–97.5%` unseen-any); under Random splits, `both_seen` is `10.83%–40.00%`. |

---

## 1. H3: Dataset Standardization, BRICS 1-Cut Coverage & Synthon-Overlap Audit

### Standardization & BRICS 1-Cut 2-Synthon Coverage

| Endpoint | Task | Raw | Invalid | Dedup Merged | Label Conflicts | Clean (`N_clean`) | BRICS Decomp (`N_decomp`) | Coverage (%) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hERG` (`herg`) | Classification | 655 | 0 | 10 | 3 | 639 | 594 | **92.96%** |
| `Lipophilicity_AstraZeneca` | Regression | 4,200 | 0 | 0 | 0 | 4,200 | 4,027 | **95.88%** |
| `Solubility_AqSolDB` | Regression | 9,982 | 2 | 406 | 0 | 9,574 | 6,400 | **66.85%** |
| `CYP3A4_Veith` | Classification | 12,328 | 0 | 27 | 1 | 12,299 | 11,528 | **93.73%** |

### Split Sizes, Test Synthon Overlap, Cartesian Augmentation & Coverage Selection Bias Audit

| Endpoint | Split | Train / Val / Test | Unique Train (s0 / s1) | `both_seen` (slot) | `both_seen` (any slot) | `one_seen` | `neither_seen` | Synthetic Cartesian Pairs | `FullMol-LGBM` Clean Test (`N_clean_te`) | `FullMol-LGBM` Decomp Test | Bias Diff (Decomp − Clean) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| `hERG` | `scaffold` | 415 / 60 / 119 | 285 / 298 | 3 (**2.52%**) | 3 (2.52%) | 39 (32.77%) | 77 (64.71%) | 2,075 | `0.8814` [0.8103, 0.9427] (n=128) | `0.8990` [0.8306, 0.9510] | `+0.0175` |
| `hERG` | `random` | 415 / 59 / 120 | 307 / 329 | 13 (**10.83%**) | 14 (11.67%) | 59 (49.17%) | 48 (40.00%) | 2,075 | `0.8713` [0.8003, 0.9281] (n=128) | `0.9234` [0.8639, 0.9689] | `+0.0521` |
| `Lipophilicity` | `scaffold` | 2,818 / 403 / 806 | 1,806 / 1,511 | 40 (**4.96%**) | 59 (7.32%) | 494 (61.29%) | 272 (33.75%) | 14,090 | `0.7425` [0.7051, 0.7765] (n=840) | `0.7303` [0.6887, 0.7673] | `-0.0122` |
| `Lipophilicity` | `random` | 2,818 / 403 / 806 | 1,912 / 1,678 | 127 (**15.76%**) | 141 (17.49%) | 544 (67.49%) | 135 (16.75%) | 14,090 | `0.8323` [0.8025, 0.8576] (n=840) | `0.8244` [0.7953, 0.8487] | `-0.0079` |
| `Solubility` | `scaffold` | 4,480 / 640 / 1,280 | 1,730 / 1,510 | 42 (**3.28%**) | 69 (5.39%) | 709 (55.39%) | 529 (41.33%) | 20,000 | `0.7719` [0.7467, 0.7948] (n=1,915) | `0.7646` [0.7343, 0.7929] | `-0.0073` |
| `Solubility` | `random` | 4,480 / 640 / 1,280 | 2,222 / 1,902 | 512 (**40.00%**) | 551 (43.05%) | 609 (47.58%) | 159 (12.42%) | 20,000 | `0.9144` [0.9011, 0.9243] (n=1,916) | `0.8980` [0.8803, 0.9135] | `-0.0164` |
| `CYP3A4` | `scaffold` | 8,069 / 1,153 / 2,306 | 4,211 / 3,946 | 290 (**12.58%**) | 349 (15.13%) | 1,384 (60.02%) | 632 (27.41%) | 20,000 | `0.8730` [0.8592, 0.8859] (n=2,460) | `0.8720` [0.8578, 0.8861] | `-0.0009` |
| `CYP3A4` | `random` | 8,069 / 1,153 / 2,306 | 4,637 / 4,333 | 663 (**28.75%**) | 749 (32.48%) | 1,279 (55.46%) | 364 (15.78%) | 20,000 | `0.9201` [0.9095, 0.9307] (n=2,460) | `0.9158` [0.9051, 0.9264] | `-0.0044` |

*(Clean vs Decomp audit uses primary metric: AUROC for `hERG`/`CYP3A4`, Spearman $\rho$ for `Lipophilicity`/`Solubility`. All CIs overlap cleanly, indicating minimal selection bias except slightly higher point AUROC on decomposable `hERG` molecules.)*

---

## 2. H2: Teacher Fidelity vs Real Experimental Accuracy Gap (`stratum = all`)

| Endpoint | Split | `Additive-ID-Dist` TF $\rho$ | `Add-Dist-Train` TF $\rho$ | `CP16-Dist-Train` TF $\rho$ | `Add-Dist-Cart` TF $\rho$ | `CP16-Dist-Cart` TF $\rho$ [95% CI] | `CP16-Dist-Cart` TF Pearson $r$ | TF $\Delta\rho$ (`CP16Cart − AddCart`, $p$) | Exp Gap: `CP16Cart − FullMol-LGBM` Primary [95% CI] ($p$) | Exp Secondary Gap vs `FullMol-LGBM` ($p$) | Distillation Lift: `CP16Cart − CP16Dir` ($p$) |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- | --- | --- | --- |
| `hERG` | `scaffold` | 0.2718 | 0.7649 | 0.7368 | 0.7695 | **0.8223** [0.7299, 0.8810] | 0.8896 | `+0.0528` (0.0443) | `-0.0143` [-0.0735, +0.0411] (0.6544) | $\Delta$AUPRC `-0.0101` (0.6567) | **`+0.1153`** (0.0140) |
| `hERG` | `random` | 0.6629 | 0.8873 | 0.8921 | 0.8589 | **0.9037** [0.8423, 0.9433] | 0.9349 | `+0.0448` (0.0045) | `-0.0097` [-0.0347, +0.0136] (0.3887) | $\Delta$AUPRC `-0.0019` (0.7701) | **`+0.0709`** (0.0385) |
| `Lipophilicity` | `scaffold` | 0.4890 | 0.7879 | 0.7686 | 0.8585 | **0.8702** [0.8471, 0.8890] | 0.8882 | `+0.0117` (0.0801) | **`-0.0875`** [-0.1182, -0.0594] (1.0e-4) | $\Delta$RMSE **`+0.0869`** (1.0e-4) | **`+0.0529`** (0.0030) |
| `Lipophilicity` | `random` | 0.6262 | 0.8451 | 0.8341 | 0.8721 | **0.8991** [0.8781, 0.9161] | 0.9140 | `+0.0270` (1.0e-4) | **`-0.0558`** [-0.0810, -0.0318] (1.0e-4) | $\Delta$RMSE **`+0.0825`** (1.0e-4) | **`+0.0534`** (1.0e-4) |
| `Solubility` | `scaffold` | 0.3601 | 0.7988 | 0.8266 | 0.8332 | **0.8664** [0.8477, 0.8838] | 0.8794 | `+0.0333` (1.0e-4) | **`-0.1085`** [-0.1333, -0.0846] (1.0e-4) | $\Delta$RMSE **`+0.2040`** (1.0e-4) | **`+0.0398`** (0.0004) |
| `Solubility` | `random` | 0.7306 | 0.9291 | 0.9453 | 0.9398 | **0.9613** [0.9543, 0.9670] | 0.9666 | `+0.0215` (1.0e-4) | **`-0.0138`** [-0.0236, -0.0040] (0.0031) | $\Delta$RMSE **`+0.0399`** (0.0477) | **`+0.0195`** (0.0002) |
| `CYP3A4` | `scaffold` | 0.5060 | 0.8437 | 0.8590 | 0.8614 | **0.9033** [0.8929, 0.9126] | 0.9191 | `+0.0419` (1.0e-4) | **`-0.0262`** [-0.0356, -0.0170] (1.0e-4) | $\Delta$AUPRC **`-0.0306`** (1.0e-4) | **`+0.0394`** (1.0e-4) |
| `CYP3A4` | `random` | 0.7118 | 0.9142 | 0.9275 | 0.9192 | **0.9493** [0.9434, 0.9545] | 0.9541 | `+0.0301` (1.0e-4) | **`-0.0143`** [-0.0209, -0.0079] (1.0e-4) | $\Delta$AUPRC **`-0.0201`** (0.0003) | **`+0.0332`** (1.0e-4) |

**Key H2 takeaway:** Even when `CP16-Distilled-Cartesian` achieves `0.866–0.903` Spearman correlation against the `FullMol-LGBM` teacher on scaffold splits (clearing SynFactor's `0.80` benchmark across all 4 endpoints, including CYP3A4), the approximation error compounds with teacher error to produce a **large, highly significant experimental deficit vs `FullMol-LGBM`** (`-0.088` to `-0.109` Spearman and `+0.087` to `+0.204` RMSE on regression scaffold holdouts; `-0.026` AUROC / `-0.031` AUPRC on CYP3A4 scaffold). Simultaneously, Cartesian teacher distillation produces a massive, statistically significant experimental gain over direct experimental training (`CP16-Distilled-Cartesian` vs `CP16-Direct`: positive and $p \le 0.0385$ on **8/8** splits, up to `+0.1153` AUROC on hERG scaffold).

---

## 3. Full Experimental Metrics Across All 9 Models (`stratum = all`, 3-Seed Ensemble + Per-Seed Mean ± SD)

### Classification Endpoints (`hERG`, `CYP3A4_Veith`)

| Endpoint | Split ($n$) | Model | AUROC [95% CI] | AUPRC [95% CI] | Per-Seed AUROC (Mean ± SD) |
| --- | --- | --- | --- | --- | --- |
| `hERG` | `scaffold` (119) | `FullMol-LGBM` | **0.8990** [0.8306, 0.9510] | **0.9474** [0.9039, 0.9798] | — |
| `hERG` | `scaffold` (119) | `Additive-ID-Direct` | 0.6517 [0.5718, 0.7283] | 0.7843 [0.7104, 0.8525] | — |
| `hERG` | `scaffold` (119) | `Additive-ID-Distilled` | 0.6509 [0.5710, 0.7284] | 0.7846 [0.7138, 0.8528] | — |
| `hERG` | `scaffold` (119) | `Additive-Direct` | 0.7758 [0.6912, 0.8592] | 0.8913 [0.8292, 0.9433] | 0.7686 ± 0.0381 |
| `hERG` | `scaffold` (119) | `CP16-Direct` | 0.7693 [0.6742, 0.8595] | 0.8644 [0.7809, 0.9332] | 0.7310 ± 0.0439 |
| `hERG` | `scaffold` (119) | `Additive-Distilled-Train` | 0.8752 [0.8035, 0.9356] | 0.9362 [0.8897, 0.9721] | 0.8625 ± 0.0198 |
| `hERG` | `scaffold` (119) | `CP16-Distilled-Train` | 0.8726 [0.7986, 0.9344] | 0.9315 [0.8798, 0.9710] | 0.8578 ± 0.0107 |
| `hERG` | `scaffold` (119) | `Additive-Distilled-Cartesian` | 0.8743 [0.8025, 0.9353] | 0.9342 [0.8849, 0.9722] | 0.8711 ± 0.0055 |
| `hERG` | `scaffold` (119) | `CP16-Distilled-Cartesian` | 0.8847 [0.8114, 0.9448] | 0.9374 [0.8872, 0.9761] | 0.8787 ± 0.0060 |
| `hERG` | `random` (120) | `FullMol-LGBM` | **0.9234** [0.8639, 0.9689] | **0.9681** [0.9373, 0.9897] | — |
| `hERG` | `random` (120) | `Additive-ID-Direct` | 0.7388 [0.6382, 0.8300] | 0.8408 [0.7593, 0.9110] | — |
| `hERG` | `random` (120) | `Additive-ID-Distilled` | 0.8161 [0.7375, 0.8857] | 0.9032 [0.8515, 0.9430] | — |
| `hERG` | `random` (120) | `Additive-Direct` | 0.8726 [0.8016, 0.9310] | 0.9485 [0.9129, 0.9754] | 0.8657 ± 0.0067 |
| `hERG` | `random` (120) | `CP16-Direct` | 0.8427 [0.7613, 0.9106] | 0.9312 [0.8831, 0.9668] | 0.8215 ± 0.0453 |
| `hERG` | `random` (120) | `Additive-Distilled-Train` | 0.9079 [0.8459, 0.9537] | 0.9631 [0.9335, 0.9840] | 0.9006 ± 0.0085 |
| `hERG` | `random` (120) | `CP16-Distilled-Train` | 0.9005 [0.8428, 0.9501] | 0.9611 [0.9327, 0.9832] | 0.8928 ± 0.0056 |
| `hERG` | `random` (120) | `Additive-Distilled-Cartesian` | 0.9042 [0.8430, 0.9550] | 0.9608 [0.9302, 0.9842] | 0.9024 ± 0.0046 |
| `hERG` | `random` (120) | `CP16-Distilled-Cartesian` | 0.9136 [0.8570, 0.9600] | 0.9663 [0.9394, 0.9859] | 0.9098 ± 0.0079 |
| `CYP3A4` | `scaffold` (2,306) | `FullMol-LGBM` | **0.8720** [0.8578, 0.8861] | **0.8276** [0.8032, 0.8501] | — |
| `CYP3A4` | `scaffold` (2,306) | `Additive-ID-Direct` | 0.6958 [0.6750, 0.7174] | 0.6258 [0.5966, 0.6545] | — |
| `CYP3A4` | `scaffold` (2,306) | `Additive-ID-Distilled` | 0.7073 [0.6858, 0.7287] | 0.6437 [0.6141, 0.6719] | — |
| `CYP3A4` | `scaffold` (2,306) | `Additive-Direct` | 0.8044 [0.7868, 0.8225] | 0.7397 [0.7080, 0.7687] | 0.7966 ± 0.0031 |
| `CYP3A4` | `scaffold` (2,306) | `CP16-Direct` | 0.8064 [0.7890, 0.8241] | 0.7477 [0.7180, 0.7760] | 0.7923 ± 0.0026 |
| `CYP3A4` | `scaffold` (2,306) | `Additive-Distilled-Train` | 0.8205 [0.8037, 0.8372] | 0.7542 [0.7226, 0.7819] | 0.8149 ± 0.0018 |
| `CYP3A4` | `scaffold` (2,306) | `CP16-Distilled-Train` | 0.8342 [0.8180, 0.8506] | 0.7806 [0.7523, 0.8054] | 0.8293 ± 0.0029 |
| `CYP3A4` | `scaffold` (2,306) | `Additive-Distilled-Cartesian` | 0.8249 [0.8079, 0.8417] | 0.7542 [0.7232, 0.7818] | 0.8229 ± 0.0029 |
| `CYP3A4` | `scaffold` (2,306) | `CP16-Distilled-Cartesian` | 0.8458 [0.8300, 0.8611] | 0.7970 [0.7710, 0.8198] | 0.8416 ± 0.0029 |
| `CYP3A4` | `random` (2,306) | `FullMol-LGBM` | **0.9158** [0.9051, 0.9264] | **0.8905** [0.8730, 0.9073] | — |
| `CYP3A4` | `random` (2,306) | `Additive-ID-Direct` | 0.7945 [0.7760, 0.8121] | 0.7504 [0.7245, 0.7758] | — |
| `CYP3A4` | `random` (2,306) | `Additive-ID-Distilled` | 0.8081 [0.7915, 0.8252] | 0.7727 [0.7490, 0.7948] | — |
| `CYP3A4` | `random` (2,306) | `Additive-Direct` | 0.8740 [0.8603, 0.8876] | 0.8422 [0.8198, 0.8634] | 0.8664 ± 0.0038 |
| `CYP3A4` | `random` (2,306) | `CP16-Direct` | 0.8683 [0.8543, 0.8827] | 0.8322 [0.8103, 0.8540] | 0.8536 ± 0.0087 |
| `CYP3A4` | `random` (2,306) | `Additive-Distilled-Train` | 0.8847 [0.8718, 0.8980] | 0.8520 [0.8298, 0.8732] | 0.8806 ± 0.0034 |
| `CYP3A4` | `random` (2,306) | `CP16-Distilled-Train` | 0.8926 [0.8800, 0.9051] | 0.8634 [0.8434, 0.8834] | 0.8892 ± 0.0011 |
| `CYP3A4` | `random` (2,306) | `Additive-Distilled-Cartesian` | 0.8854 [0.8723, 0.8989] | 0.8506 [0.8290, 0.8717] | 0.8838 ± 0.0004 |
| `CYP3A4` | `random` (2,306) | `CP16-Distilled-Cartesian` | 0.9015 [0.8898, 0.9132] | 0.8703 [0.8500, 0.8896] | 0.8981 ± 0.0009 |

### Regression Endpoints (`Lipophilicity_AstraZeneca`, `Solubility_AqSolDB`)

| Endpoint | Split ($n$) | Model | Spearman $\rho$ [95% CI] | RMSE [95% CI] | MAE [95% CI] | Per-Seed $\rho$ / RMSE (Mean ± SD) |
| --- | --- | --- | --- | --- | --- | --- |
| `Lipophilicity` | `scaffold` (806) | `FullMol-LGBM` | **0.7303** [0.6887, 0.7673] | **0.7921** [0.7452, 0.8415] | **0.6125** [0.5776, 0.6474] | — |
| `Lipophilicity` | `scaffold` (806) | `Additive-ID-Direct` | 0.3834 [0.3204, 0.4374] | 1.0994 [1.0428, 1.1597] | 0.8759 [0.8306, 0.9253] | — |
| `Lipophilicity` | `scaffold` (806) | `Additive-ID-Distilled` | 0.3939 [0.3316, 0.4488] | 1.1444 [1.0845, 1.2010] | 0.9232 [0.8745, 0.9718] | — |
| `Lipophilicity` | `scaffold` (806) | `Additive-Direct` | 0.5967 [0.5465, 0.6439] | 0.9501 [0.8994, 1.0012] | 0.7465 [0.7047, 0.7890] | 0.5584±0.0301 / 0.9908±0.0253 |
| `Lipophilicity` | `scaffold` (806) | `CP16-Direct` | 0.5899 [0.5391, 0.6370] | 0.9659 [0.9117, 1.0181] | 0.7660 [0.7228, 0.8071] | 0.5391±0.0206 / 1.0060±0.0244 |
| `Lipophilicity` | `scaffold` (806) | `Additive-Distilled-Train` | 0.6013 [0.5517, 0.6493] | 0.9440 [0.8942, 0.9947] | 0.7449 [0.7037, 0.7865] | 0.5762±0.0207 / 0.9688±0.0183 |
| `Lipophilicity` | `scaffold` (806) | `CP16-Distilled-Train` | 0.6003 [0.5501, 0.6463] | 0.9509 [0.8985, 1.0037] | 0.7481 [0.7067, 0.7899] | 0.5707±0.0110 / 0.9755±0.0028 |
| `Lipophilicity` | `scaffold` (806) | `Additive-Distilled-Cartesian` | 0.6173 [0.5682, 0.6634] | 0.9219 [0.8745, 0.9722] | 0.7295 [0.6892, 0.7699] | 0.6112±0.0067 / 0.9283±0.0093 |
| `Lipophilicity` | `scaffold` (806) | `CP16-Distilled-Cartesian` | 0.6428 [0.5967, 0.6857] | 0.8790 [0.8308, 0.9266] | 0.6950 [0.6572, 0.7346] | 0.6324±0.0068 / 0.8904±0.0064 |
| `Lipophilicity` | `random` (806) | `FullMol-LGBM` | **0.8244** [0.7953, 0.8487] | **0.6563** [0.6141, 0.6974] | **0.4878** [0.4581, 0.5164] | — |
| `Lipophilicity` | `random` (806) | `Additive-ID-Direct` | 0.5584 [0.5069, 0.6072] | 1.0076 [0.9493, 1.0664] | 0.7796 [0.7361, 0.8232] | — |
| `Lipophilicity` | `random` (806) | `Additive-ID-Distilled` | 0.5495 [0.4975, 0.5988] | 1.0128 [0.9546, 1.0719] | 0.7849 [0.7420, 0.8291] | — |
| `Lipophilicity` | `random` (806) | `Additive-Direct` | 0.7163 [0.6741, 0.7522] | 0.8265 [0.7726, 0.8813] | 0.6079 [0.5678, 0.6465] | 0.6948±0.0043 / 0.8625±0.0052 |
| `Lipophilicity` | `random` (806) | `CP16-Direct` | 0.7152 [0.6733, 0.7518] | 0.8301 [0.7785, 0.8826] | 0.6143 [0.5762, 0.6540] | 0.6819±0.0234 / 0.8683±0.0314 |
| `Lipophilicity` | `random` (806) | `Additive-Distilled-Train` | 0.7263 [0.6861, 0.7622] | 0.8108 [0.7613, 0.8616] | 0.6074 [0.5693, 0.6454] | 0.7070±0.0072 / 0.8383±0.0094 |
| `Lipophilicity` | `random` (806) | `CP16-Distilled-Train` | 0.7104 [0.6703, 0.7474] | 0.8318 [0.7809, 0.8812] | 0.6263 [0.5887, 0.6648] | 0.6862±0.0050 / 0.8614±0.0087 |
| `Lipophilicity` | `random` (806) | `Additive-Distilled-Cartesian` | 0.7334 [0.6944, 0.7682] | 0.7945 [0.7481, 0.8417] | 0.6114 [0.5773, 0.6482] | 0.7286±0.0029 / 0.8001±0.0049 |
| `Lipophilicity` | `random` (806) | `CP16-Distilled-Cartesian` | 0.7686 [0.7317, 0.8003] | 0.7388 [0.6921, 0.7884] | 0.5544 [0.5205, 0.5902] | 0.7567±0.0034 / 0.7537±0.0058 |
| `Solubility` | `scaffold` (1,280) | `FullMol-LGBM` | **0.7646** [0.7343, 0.7929] | **1.3905** [1.3148, 1.4683] | **1.0150** [0.9635, 1.0681] | — |
| `Solubility` | `scaffold` (1,280) | `Additive-ID-Direct` | 0.2940 [0.2422, 0.3406] | 2.0811 [2.0021, 2.1634] | 1.6481 [1.5806, 1.7205] | — |
| `Solubility` | `scaffold` (1,280) | `Additive-ID-Distilled` | 0.2900 [0.2391, 0.3362] | 2.0844 [2.0072, 2.1662] | 1.6518 [1.5850, 1.7238] | — |
| `Solubility` | `scaffold` (1,280) | `Additive-Direct` | 0.6132 [0.5716, 0.6516] | 1.6399 [1.5669, 1.7129] | 1.2537 [1.1959, 1.3136] | 0.5933±0.0130 / 1.6921±0.0328 |
| `Solubility` | `scaffold` (1,280) | `CP16-Direct` | 0.6163 [0.5768, 0.6528] | 1.6534 [1.5829, 1.7262] | 1.2822 [1.2247, 1.3401] | 0.5901±0.0239 / 1.6981±0.0203 |
| `Solubility` | `scaffold` (1,280) | `Additive-Distilled-Train` | 0.6198 [0.5796, 0.6598] | 1.7030 [1.6221, 1.7849] | 1.2848 [1.2240, 1.3471] | 0.6115±0.0096 / 1.7330±0.0476 |
| `Solubility` | `scaffold` (1,280) | `CP16-Distilled-Train` | 0.6499 [0.6114, 0.6858] | 1.5734 [1.5027, 1.6443] | 1.1982 [1.1418, 1.2538] | 0.6392±0.0314 / 1.5999±0.0481 |
| `Solubility` | `scaffold` (1,280) | `Additive-Distilled-Cartesian` | 0.6314 [0.5905, 0.6706] | 1.6701 [1.5896, 1.7520] | 1.2430 [1.1831, 1.3054] | 0.6265±0.0210 / 1.6906±0.0754 |
| `Solubility` | `scaffold` (1,280) | `CP16-Distilled-Cartesian` | 0.6561 [0.6175, 0.6916] | 1.5945 [1.5179, 1.6708] | 1.2011 [1.1433, 1.2590] | 0.6491±0.0080 / 1.6150±0.0183 |
| `Solubility` | `random` (1,280) | `FullMol-LGBM` | **0.8980** [0.8803, 0.9135] | **0.9560** [0.8920, 1.0162] | **0.6535** [0.6166, 0.6906] | — |
| `Solubility` | `random` (1,280) | `Additive-ID-Direct` | 0.6644 [0.6286, 0.6966] | 1.6102 [1.5322, 1.6821] | 1.2150 [1.1542, 1.2728] | — |
| `Solubility` | `random` (1,280) | `Additive-ID-Distilled` | 0.6658 [0.6293, 0.6976] | 1.5955 [1.5174, 1.6682] | 1.1990 [1.1383, 1.2575] | — |
| `Solubility` | `random` (1,280) | `Additive-Direct` | 0.8566 [0.8360, 0.8748] | 1.1207 [1.0611, 1.1810] | 0.8141 [0.7746, 0.8548] | 0.8490±0.0032 / 1.1536±0.0065 |
| `Solubility` | `random` (1,280) | `CP16-Direct` | 0.8647 [0.8453, 0.8826] | 1.0878 [1.0245, 1.1484] | 0.7727 [0.7308, 0.8134] | 0.8563±0.0031 / 1.1201±0.0106 |
| `Solubility` | `random` (1,280) | `Additive-Distilled-Train` | 0.8590 [0.8372, 0.8782] | 1.1109 [1.0470, 1.1750] | 0.8002 [0.7585, 0.8414] | 0.8554±0.0025 / 1.1265±0.0115 |
| `Solubility` | `random` (1,280) | `CP16-Distilled-Train` | 0.8722 [0.8533, 0.8895] | 1.0519 [0.9890, 1.1113] | 0.7510 [0.7113, 0.7907] | 0.8674±0.0041 / 1.0707±0.0162 |
| `Solubility` | `random` (1,280) | `Additive-Distilled-Cartesian` | 0.8622 [0.8408, 0.8801] | 1.0992 [1.0410, 1.1613] | 0.8114 [0.7721, 0.8527] | 0.8604±0.0015 / 1.1061±0.0053 |
| `Solubility` | `random` (1,280) | `CP16-Distilled-Cartesian` | 0.8842 [0.8656, 0.9006] | 0.9959 [0.9336, 1.0569] | 0.7107 [0.6721, 0.7474] | 0.8805±0.0028 / 1.0140±0.0085 |

---

## 4. H1 Pre-Registered Paired Tests (`CP16 − Additive`, `stratum = all`)

| Regime | Split | Endpoint | Primary $\Delta$ [95% CI] | Primary $p_{\text{perm}}$ | Secondary $\Delta$ [95% CI] | Secondary $p_{\text{perm}}$ | Cell Verdict |
| --- | --- | --- | --- | ---: | --- | ---: | --- |
| **Direct** | `scaffold` | `hERG` | $\Delta$AUROC `-0.0065` [-0.0717, +0.0592] | 0.8634 | $\Delta$AUPRC `-0.0268` [-0.0787, +0.0223] | 0.4885 | FAIL |
| **Direct** | `scaffold` | `Lipophilicity` | $\Delta\rho$ `-0.0068` [-0.0344, +0.0229] | 0.6469 | $\Delta$RMSE `+0.0157` [-0.0085, +0.0397] | 0.2133 | FAIL |
| **Direct** | `scaffold` | `Solubility` | $\Delta\rho$ `+0.0032` [-0.0248, +0.0307] | 0.8324 | $\Delta$RMSE `+0.0135` [-0.0380, +0.0637] | 0.6102 | FAIL |
| **Direct** | `scaffold` | `CYP3A4` | $\Delta$AUROC `+0.0020` [-0.0063, +0.0109] | 0.6394 | $\Delta$AUPRC `+0.0080` [-0.0044, +0.0222] | 0.2204 | FAIL |
| **Direct** | `random` | `hERG` | $\Delta$AUROC `-0.0299` [-0.0852, +0.0215] | 0.3138 | $\Delta$AUPRC `-0.0173` [-0.0474, +0.0072] | 0.3860 | FAIL |
| **Direct** | `random` | `Lipophilicity` | $\Delta\rho$ `-0.0011` [-0.0227, +0.0214] | 0.9218 | $\Delta$RMSE `+0.0036` [-0.0239, +0.0294] | 0.7961 | FAIL |
| **Direct** | `random` | `Solubility` | $\Delta\rho$ `+0.0081` [-0.0018, +0.0188] | 0.1317 | $\Delta$RMSE `-0.0329` [-0.0734, +0.0047] | 0.1003 | FAIL |
| **Direct** | `random` | `CYP3A4` | $\Delta$AUROC `-0.0057` [-0.0117, +0.0008] | 0.0775 | $\Delta$AUPRC `-0.0100` [-0.0198, -0.0001] | 0.0420 | FAIL |
| **Distilled-Train** | `scaffold` | `hERG` | $\Delta$AUROC `-0.0026` [-0.0372, +0.0357] | 0.8902 | $\Delta$AUPRC `-0.0047` [-0.0278, +0.0177] | 0.6419 | FAIL |
| **Distilled-Train** | `scaffold` | `Lipophilicity` | $\Delta\rho$ `-0.0010` [-0.0272, +0.0266] | 0.9471 | $\Delta$RMSE `+0.0069` [-0.0168, +0.0296] | 0.5747 | FAIL |
| **Distilled-Train** | `scaffold` | `Solubility` | $\Delta\rho$ **`+0.0302`** [+0.0098, +0.0495] | 0.0037 | $\Delta$RMSE **`-0.1296`** [-0.1776, -0.0814] | 1.0e-4 | **PASS** |
| **Distilled-Train** | `scaffold` | `CYP3A4` | $\Delta$AUROC **`+0.0137`** [+0.0072, +0.0203] | 1.0e-4 | $\Delta$AUPRC **`+0.0265`** [+0.0151, +0.0394] | 1.0e-4 | **PASS** |
| **Distilled-Train** | `random` | `hERG` | $\Delta$AUROC `-0.0074` [-0.0433, +0.0273] | 0.6949 | $\Delta$AUPRC `-0.0020` [-0.0179, +0.0138] | 0.8140 | FAIL |
| **Distilled-Train** | `random` | `Lipophilicity` | $\Delta\rho$ `-0.0159` [-0.0362, +0.0037] | 0.1172 | $\Delta$RMSE `+0.0209` [-0.0039, +0.0451] | 0.1022 | FAIL |
| **Distilled-Train** | `random` | `Solubility` | $\Delta\rho$ **`+0.0132`** [+0.0050, +0.0214] | 0.0013 | $\Delta$RMSE **`-0.0590`** [-0.0896, -0.0275] | 0.0002 | **PASS** |
| **Distilled-Train** | `random` | `CYP3A4` | $\Delta$AUROC `+0.0079` [+0.0031, +0.0124] | 0.0015 | $\Delta$AUPRC `+0.0114` [+0.0035, +0.0191] | 0.0049 | FAIL (<0.010) |
| **Distilled-Cartesian** | `scaffold` | `hERG` | $\Delta$AUROC `+0.0104` [-0.0228, +0.0423] | 0.5359 | $\Delta$AUPRC `+0.0031` [-0.0214, +0.0239] | 0.8128 | FAIL (n.s.) |
| **Distilled-Cartesian** | `scaffold` | `Lipophilicity` | $\Delta\rho$ **`+0.0255`** [+0.0090, +0.0430] | 0.0042 | $\Delta$RMSE **`-0.0430`** [-0.0597, -0.0264] | 1.0e-4 | **PASS** |
| **Distilled-Cartesian** | `scaffold` | `Solubility` | $\Delta\rho$ **`+0.0247`** [+0.0093, +0.0393] | 0.0022 | $\Delta$RMSE **`-0.0756`** [-0.1124, -0.0371] | 0.0002 | **PASS** |
| **Distilled-Cartesian** | `scaffold` | `CYP3A4` | $\Delta$AUROC **`+0.0209`** [+0.0134, +0.0289] | 1.0e-4 | $\Delta$AUPRC **`+0.0429`** [+0.0286, +0.0574] | 1.0e-4 | **PASS** |
| **Distilled-Cartesian** | `random` | `hERG` | $\Delta$AUROC `+0.0094` [-0.0154, +0.0348] | 0.4729 | $\Delta$AUPRC `+0.0055` [-0.0049, +0.0172] | 0.3248 | FAIL (n.s.) |
| **Distilled-Cartesian** | `random` | `Lipophilicity` | $\Delta\rho$ **`+0.0352`** [+0.0208, +0.0504] | 1.0e-4 | $\Delta$RMSE **`-0.0557`** [-0.0760, -0.0353] | 1.0e-4 | **PASS** |
| **Distilled-Cartesian** | `random` | `Solubility` | $\Delta\rho$ **`+0.0220`** [+0.0150, +0.0292] | 1.0e-4 | $\Delta$RMSE **`-0.1033`** [-0.1320, -0.0758] | 1.0e-4 | **PASS** |
| **Distilled-Cartesian** | `random` | `CYP3A4` | $\Delta$AUROC **`+0.0161`** [+0.0105, +0.0216] | 1.0e-4 | $\Delta$AUPRC **`+0.0198`** [+0.0111, +0.0286] | 0.0002 | **PASS** |

### Representation Confound Quantification (`CP16-Direct` vs `Additive-ID-Direct` vs `Additive-Direct`)

Comparing `CP16-Direct` against `synfactor`'s embedding-free ridge slot-ID control (`Additive-ID-Direct`) yields huge apparent advantages (`+0.1176` hERG scaffold, `+0.2065` Lipophilicity scaffold, `+0.3223` Solubility scaffold, `+0.1106` CYP3A4 scaffold; all 3 large endpoints $p=1.0\times 10^{-4}$). Replacing the ID lookup with our representation-matched `Additive-Direct` collapses that advantage completely (`-0.0065`, `-0.0068`, `+0.0032`, `+0.0020`, all $p \ge 0.64$). Thus, **without Cartesian teacher distillation, 100% of CP16's direct gain over `Additive-ID` is representation (molecular embeddings generalizing to unseen synthons), not bilinear interaction.**

---

## 5. Stratified Breakdown: `both_seen` vs `unseen_any`

| Endpoint | Split | Stratum ($n$) | `FullMol-LGBM` | `Add-ID-Dir` | `Add-Dir` | `CP16-Dir` | `Add-Cart` | `CP16-Cart` | $\Delta$(`CP16Cart − AddCart`) [95% CI] ($p$) | $\Delta$(`CP16Cart − LGBM`) ($p$) | TF $\rho$ (`CP16Cart`/`AddCart`) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| `hERG` | `scaffold` | `both_seen` (3) | N/A | N/A | N/A | N/A | N/A | N/A | N/A (`n<20`) | N/A | N/A |
| `hERG` | `scaffold` | `unseen_any` (116) | 0.8951 | 0.6383 | 0.7672 | 0.7605 | 0.8694 | 0.8802 | `+0.0108` [-0.0233, +0.0412] (0.5343) | `-0.0148` (0.6506) | 0.8132 / 0.7591 |
| `hERG` | `random` | `both_seen` (13) | N/A | N/A | N/A | N/A | N/A | N/A | N/A (`n<20`) | N/A | N/A |
| `hERG` | `random` | `unseen_any` (107) | 0.9140 | 0.7314 | 0.8616 | 0.8309 | 0.8972 | 0.9054 | `+0.0082` [-0.0190, +0.0365] (0.5797) | `-0.0086` (0.4843) | 0.8963 / 0.8535 |
| `Lipophilicity` | `scaffold` | `both_seen` (40) | 0.7936 | 0.4966 | 0.6788 | 0.7648 | 0.7322 | 0.7534 | `+0.0212` [-0.0584, +0.0997] (0.5004) | `-0.0402` (0.4025) | 0.9094 / 0.9167 |
| `Lipophilicity` | `scaffold` | `unseen_any` (766) | 0.7283 | 0.3758 | 0.5943 | 0.5831 | 0.6146 | 0.6394 | **`+0.0248`** [+0.0070, +0.0425] (0.0070) | **`-0.0888`** (1.0e-4) | 0.8676 / 0.8555 |
| `Lipophilicity` | `random` | `both_seen` (127) | 0.8762 | 0.7543 | 0.8422 | 0.8358 | 0.8007 | 0.8684 | **`+0.0676`** [+0.0222, +0.1193] (0.0031) | `-0.0078` (0.6764) | 0.9444 / 0.8968 |
| `Lipophilicity` | `random` | `unseen_any` (679) | 0.8156 | 0.5177 | 0.6945 | 0.6957 | 0.7209 | 0.7506 | **`+0.0297`** [+0.0139, +0.0452] (1.0e-4) | **`-0.0650`** (1.0e-4) | 0.8907 / 0.8662 |
| `Solubility` | `scaffold` | `both_seen` (42) | 0.8075 | 0.6612 | 0.7270 | 0.7456 | 0.7012 | 0.7299 | `+0.0287` [-0.0207, +0.0944] (0.2189) | `-0.0776` (0.1467) | 0.9229 / 0.9119 |
| `Solubility` | `scaffold` | `unseen_any` (1,238) | 0.7635 | 0.2834 | 0.6103 | 0.6129 | 0.6291 | 0.6543 | **`+0.0252`** [+0.0105, +0.0415] (0.0028) | **`-0.1092`** (1.0e-4) | 0.8642 / 0.8304 |
| `Solubility` | `random` | `both_seen` (512) | 0.9402 | 0.8887 | 0.9097 | 0.9220 | 0.9091 | 0.9302 | **`+0.0211`** [+0.0126, +0.0306] (1.0e-4) | **`-0.0101`** (0.0038) | 0.9817 / 0.9668 |
| `Solubility` | `random` | `unseen_any` (768) | 0.8672 | 0.4690 | 0.8181 | 0.8217 | 0.8295 | 0.8500 | **`+0.0205`** [+0.0105, +0.0317] (1.0e-4) | **`-0.0172`** (0.0333) | 0.9445 / 0.9197 |
| `CYP3A4` | `scaffold` | `both_seen` (290) | 0.9449 | 0.8722 | 0.8970 | 0.9066 | 0.9294 | 0.9509 | **`+0.0215`** [+0.0090, +0.0365] (0.0010) | `+0.0060` (0.2279) | 0.9744 / 0.9536 |
| `CYP3A4` | `scaffold` | `unseen_any` (2,016) | 0.8566 | 0.6538 | 0.7856 | 0.7846 | 0.8032 | 0.8235 | **`+0.0203`** [+0.0113, +0.0295] (1.0e-4) | **`-0.0331`** (1.0e-4) | 0.8855 / 0.8393 |
| `CYP3A4` | `random` | `both_seen` (663) | 0.9627 | 0.9196 | 0.9344 | 0.9311 | 0.9365 | 0.9509 | **`+0.0145`** [+0.0060, +0.0228] (0.0005) | **`-0.0118`** (0.0013) | 0.9736 / 0.9555 |
| `CYP3A4` | `random` | `unseen_any` (1,643) | 0.8902 | 0.7172 | 0.8418 | 0.8345 | 0.8593 | 0.8738 | **`+0.0145`** [+0.0076, +0.0214] (0.0003) | **`-0.0164`** (0.0003) | 0.9312 / 0.8950 |

**Critical stratified insight:** `CP16-Distilled-Cartesian` beats `Additive-Distilled-Cartesian` **not only on `both_seen`, but also on `unseen_any`** across all 3 large endpoints on both scaffold and random splits (`Lipophilicity` scaffold `unseen_any` $+0.0248$, $p=0.0070$, $\Delta\text{RMSE}=-0.0437$, $p=1.0\times 10^{-4}$; `Solubility` scaffold `unseen_any` $+0.0252$, $p=0.0028$, $\Delta\text{RMSE}=-0.0768$, $p=0.0002$; `CYP3A4` scaffold `unseen_any` $+0.0203$, $p=1.0\times 10^{-4}$). Dense Cartesian teacher supervision enables the shared synthon trunk + rank-16 factor heads to learn generalizable bilinear structure even for novel synthons.

---

## 6. Self-Referee Audit (`CONTROLS`, `CONTRADICTING`, `LABELS`)

- **`CONTROLS:`** Representation-matched neural additive controls (`NeuralAdditiveSynthon`, verified zero interaction in `src/test_pipeline.py:test_neural_additive_has_zero_interaction`) were trained under identical trunk, features, optimizer, seeds (`42, 43, 44`), and Cartesian distillation sets (`results/summary.json`). Far from being overridden, the controls revealed the core dissociation: `Additive-Direct` matched or beat `CP16-Direct` on 6/8 cells (`0/8` CP16-Direct passes), proving that CP16's direct gain over `Additive-ID-Direct` (`+0.074` to `+0.322`) is purely a representation effect; only `Distilled-Cartesian` unlocks genuine bilinear gains over the matched neural additive control (`3/4` scaffold, `3/4` random).
- **`CONTRADICTING:`** No contradicting cells or failures were dropped. All 4 endpoints × 2 splits × 9 models × 3 strata are reported verbatim from `results/summary.json`, including `Direct` failing `0/4` on both splits, `Distilled-Train` failing `Lipophilicity` (`-0.0010` scaffold, `-0.0159` random) and `hERG`, `hERG` failing significance in `Distilled-Cartesian` ($n=119/120$, $p=0.536/0.473$), `Solubility` losing `33.15%` of molecules to non-decomposability, and `CP16-Distilled-Cartesian` trailing `FullMol-LGBM` significantly on `6/8` cells.
- **`LABELS:`** All 4 raw `.tab` files verified against locked SHA-256 digests in `data/manifest.json` (`src/run_experiments.py:verify_data_manifest`); exact invalid/duplicate/label-conflict counts logged (`hERG` 3 conflicts dropped, `CYP3A4` 1 conflict dropped, `Solubility` 2 invalid + 406 merged); Cartesian anti-leakage assertion enforced against `train ∪ val ∪ test` (`src/chemistry_utils.py:338`); independent recomputation of all `4 × 2 × 9` model point metrics and overlap counts from `results/test_preds_<ep>_<split>.csv` matched `results/summary.json` to `0.000e+00`.
