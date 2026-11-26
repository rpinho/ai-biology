# Independent referee verdict

Four raw TDC files, eight fixed test sets, 144 neural fits and 48 seed ensembles. Differences below are CP16 minus the named comparator. AUROC applies to hERG and CYP3A4, Spearman ρ to the two regression endpoints. Brackets give paired 95% bootstrap intervals. All p-values are two-sided Monte Carlo tests. Full-precision results are in verdict.json and the per-split statistics files.

| Claim | Claimed result | Independent verdict and result |
|---|---|---|
| C1 | Direct H1 0/4 on each split despite +0.11 to +0.32 gains against ID. | REFUTED. Direct training passed on 1/4 scaffold and 1/4 random endpoints. Scaffold lipophilicity reversed direction (Δρ +0.0689, p=0.00020), and random solubility also passed (+0.0147, p=0.01670). Overall direct H1 still failed. The three large scaffold ID gains reproduced at +0.1083 to +0.3336, all p=0.00010. |
| C2 | Cartesian H1 3/4 scaffold, 3/4 random, no significant degradation. | CONFIRMED-WITH-CAVEATS. Cartesian H1 passed on the same 3/4 endpoints on each split, with zero significant degradations. Scaffold gains were +0.0256, +0.0253 and +0.0192 on lipophilicity, solubility and CYP3A4. Random lipophilicity was +0.0251 versus the claimed +0.0352. Exact-product leakage checks passed. |
| C3 | Three significant unseen-synthon gains of +0.0248, +0.0252 and +0.0203. | CONFIRMED-WITH-CAVEATS. All three large scaffold unseen-synthon gains reproduced. Lipophilicity gained +0.0243 (p=0.00350), solubility +0.0256 (p=0.00120), and CYP3A4 +0.0178 (p=0.00030). The primary solubility stratum contained 1,239 molecules versus 1,238 claimed. |
| C4 | 8/8 fidelity scores above 0.80, significant experimental deficits on all three large scaffold sets. | CONFIRMED-WITH-CAVEATS. All 8 fidelity point estimates exceeded 0.80. The ranges were 0.8208–0.8931 scaffold and 0.8902–0.9595 random. The hERG scaffold CI included 0.80. Experimental gaps on the large scaffold sets were −0.0760, −0.1088 and −0.0274, all p=0.00010. |
| C5 | Coverage 92.96%–95.88% on three endpoints and 66.85% on solubility, with 2.52%–12.58% scaffold both-seen. | CONFIRMED-WITH-CAVEATS. All four claimed coverage fractions and all four scaffold overlap counts reproduced when equal-size salt fragments kept the lexicographically first canonical SMILES. The frozen primary run kept the last and gave 6,397/9,582 for solubility, 41/1,280 both seen, and 11,527/12,299 for CYP3A4. |
| C6 | Solubility coverage >90% and CP16 experimental Δρ >+0.02 at p<0.05 against FullMol-LGBM. | REFUTED. Both components failed. Solubility coverage was 66.76% in the primary analysis and 66.85% with the opposite salt tie. Primary experimental ρ was 0.6449 for distilled CP16 and 0.7537 for FullMol-LGBM (Δ −0.1088, 95% CI −0.1337 to −0.0844, p=0.00010). |

## C1. Direct experimental training

The large-endpoint scaffold ID comparisons were claimed to span +0.11 to +0.32, all p < 0.001. The claim supplies no individual random-split deltas.

| Cell | Claimed matched Δ (p) | Matched Δ [CI], p | Matched ΔRMSE [CI], p | CP16 − ID Δ [CI], p | H1 pass |
|---|---|---|---|---|---|
| hERG scaffold | −.0065 (.863) | -0.0487 [-0.1131, +0.0189], p=0.12819 | — | +0.0928 [-0.0199, +0.2037], p=0.17208 | no |
| Lipophilicity scaffold | −.0068 (.647) | +0.0689 [+0.0360, +0.1009], p=0.00020 | -0.0506 [-0.0771, -0.0233], p=0.00020 | +0.2305 [+0.1711, +0.2897], p=0.00010 | yes |
| Solubility scaffold | +.0032 (.832) | +0.0224 [-0.0083, +0.0511], p=0.14509 | +0.0053 [-0.0471, +0.0614], p=0.84642 | +0.3336 [+0.2783, +0.3888], p=0.00010 | no |
| CYP3A4 scaffold | +.0020 (.639) | -0.0051 [-0.0130, +0.0035], p=0.23858 | — | +0.1083 [+0.0872, +0.1302], p=0.00010 | no |
| hERG random | no pass | -0.0215 [-0.0671, +0.0240], p=0.35576 | — | +0.1081 [+0.0083, +0.2107], p=0.04360 | no |
| Lipophilicity random | no pass | +0.0058 [-0.0158, +0.0279], p=0.60144 | -0.0027 [-0.0296, +0.0231], p=0.83622 | +0.1700 [+0.1260, +0.2137], p=0.00010 | no |
| Solubility random | no pass | +0.0147 [+0.0029, +0.0270], p=0.01670 | -0.0468 [-0.0865, -0.0091], p=0.02230 | +0.2065 [+0.1752, +0.2404], p=0.00010 | yes |
| CYP3A4 random | no pass | +0.0032 [-0.0035, +0.0097], p=0.36456 | — | +0.0786 [+0.0624, +0.0955], p=0.00010 | no |

## C2. Distilled-Cartesian training

| Cell | Claimed Δ | Independent primary Δ [CI], p | Other Δ [CI], p | H1 pass | Significant harm |
|---|---|---|---|---|---|
| hERG scaffold | +.0104 (n.s.) | +0.0019 [-0.0291, +0.0325], p=0.90371 | AUPRC +0.0021 [-0.0154, +0.0215], p=0.82342 | no | no |
| Lipophilicity scaffold | +.0255 / −.0430 RMSE | +0.0256 [+0.0113, +0.0407], p=0.00200 | RMSE -0.0447 [-0.0605, -0.0287], p=0.00010 | yes | no |
| Solubility scaffold | +.0247 / −.0756 RMSE | +0.0253 [+0.0103, +0.0407], p=0.00150 | RMSE -0.0758 [-0.1141, -0.0398], p=0.00010 | yes | no |
| CYP3A4 scaffold | +.0209 / +.0429 AP | +0.0192 [+0.0120, +0.0265], p=0.00010 | AUPRC +0.0368 [+0.0241, +0.0497], p=0.00010 | yes | no |
| hERG random | +.0094 (n.s.) | +0.0111 [-0.0192, +0.0427], p=0.46715 | AUPRC +0.0093 [-0.0089, +0.0296], p=0.38346 | no | no |
| Lipophilicity random | +.0352 | +0.0251 [+0.0100, +0.0410], p=0.00140 | RMSE -0.0408 [-0.0622, -0.0199], p=0.00010 | yes | no |
| Solubility random | +.0220 | +0.0213 [+0.0125, +0.0300], p=0.00010 | RMSE -0.1053 [-0.1349, -0.0759], p=0.00010 | yes | no |
| CYP3A4 random | +.0161 | +0.0189 [+0.0134, +0.0246], p=0.00010 | AUPRC +0.0277 [+0.0187, +0.0365], p=0.00010 | yes | no |

## C3. Unseen synthons on the scaffold split

| Endpoint | Claimed n, Δ, p | Independent n | Independent Δ [CI], p |
|---|---|---|---|
| hERG | n/a | 116 | +0.0020 [-0.0315, +0.0363], p=0.91241 |
| Lipophilicity | 766, +.0248, .0070 | 766 | +0.0243 [+0.0079, +0.0398], p=0.00350 |
| Solubility | 1238, +.0252, .0028 | 1239 | +0.0256 [+0.0093, +0.0421], p=0.00120 |
| CYP3A4 | 2016, +.0203, .0001 | 2016 | +0.0178 [+0.0090, +0.0269], p=0.00030 |

## C4. Teacher fidelity and experimental accuracy

Claimed fidelity ranges were 0.822–0.903 on scaffold splits and 0.899–0.961 on random splits. The three large scaffold experimental gaps were claimed at p < 0.001.

| Cell | Teacher Spearman [CI] | CP16 experimental | Teacher experimental | Claimed gap | Independent gap [CI], p |
|---|---|---|---|---|---|
| hERG scaffold | 0.8208 [0.7280, 0.8870] | 0.8665 | 0.8960 | — | -0.0296 [-0.0873, +0.0238], p=0.32517 |
| Lipophilicity scaffold | 0.8647 [0.8416, 0.8853] | 0.6523 | 0.7284 | −.0875 | -0.0760 [-0.1066, -0.0445], p=0.00010 |
| Solubility scaffold | 0.8626 [0.8428, 0.8801] | 0.6449 | 0.7537 | −.1085 | -0.1088 [-0.1337, -0.0844], p=0.00010 |
| CYP3A4 scaffold | 0.8931 [0.8817, 0.9033] | 0.8464 | 0.8739 | −.0262 | -0.0274 [-0.0378, -0.0177], p=0.00010 |
| hERG random | 0.9071 [0.8526, 0.9457] | 0.9032 | 0.9183 | — | -0.0151 [-0.0503, +0.0178], p=0.36006 |
| Lipophilicity random | 0.8902 [0.8694, 0.9082] | 0.7558 | 0.8286 | — | -0.0728 [-0.0983, -0.0486], p=0.00010 |
| Solubility random | 0.9595 [0.9526, 0.9653] | 0.8550 | 0.8745 | — | -0.0196 [-0.0305, -0.0096], p=0.00030 |
| CYP3A4 random | 0.9441 [0.9378, 0.9494] | 0.9013 | 0.9180 | — | -0.0168 [-0.0232, -0.0101], p=0.00010 |

## C5 and C6. Coverage and overlap

| Endpoint | Claimed coverage | Independent coverage | Claimed scaffold both | Scaffold both, one, neither, both-any-slot | Random both, one, neither, both-any-slot |
|---|---|---|---|---|---|
| hERG | 594/639 | 594/639 (92.958%) | 3/119 | 3/119 (2.52%), 39, 77, 3 | 13/120 (10.83%), 59, 48, 14 |
| Lipophilicity | 4027/4200 | 4027/4200 (95.881%) | 40/806 | 40/806 (4.96%), 494, 272, 59 | 127/806 (15.76%), 544, 135, 141 |
| Solubility | 6400/9574 | 6397/9582 (66.761%) | 42/1280 | 41/1280 (3.20%), 707, 532, 69 | 521/1280 (40.70%), 619, 140, 557 |
| CYP3A4 | 11528/12299 | 11527/12299 (93.723%) | 290/2306 | 290/2306 (12.58%), 1384, 632, 349 | 669/2306 (29.01%), 1265, 372, 752 |

With the opposite largest-fragment tie, the solubility scaffold sensitivity rerun gave 6400/9574 coverage, experimental ρ=0.6593 for CP16 and 0.7669 for the teacher, and Δρ -0.1076 [-0.1314, -0.0845], p=0.00010. These 18 extra fits are reported separately from the primary H1 counts.
C6 requires coverage >90% and a scaffold experimental Δρ >+0.020 at p <0.05. Independent coverage was 66.761%. The experimental Δρ was -0.1088 [-0.1337, -0.0844], p=0.00010.

## CONTROLS:

No. H1 decisions in src/summary.py use the matched comparator and both registered regression metrics. The ID result never supplies an H1 pass. Direct H1 passed 1/4 scaffold and 1/4 random endpoints.

The paired comparisons use the same held-out rows, three seeds, descriptor normalization fitted on training occurrences and stopping rule for both neural heads. The 2×2 interaction check in audit/cp-control.json gives 6e-08 for the additive control and 0.145 for CP16. The upstream masked-third-slot and product-over-four checks both give 0 maximum formula error and 0 mask error. Parameter counts including the unused third heads are 136,261 and 139,186, respectively. The matched comparison isolates the choice of head and combination as a package. Width and parameter count of the heads differ.

The 100-row upstream ridge control in src/verify_controls.py selected λ=10.0 with maximum prediction difference 1.1e-16. The ID comparison changes both representation and architecture. Only the matched comparison decides H1. The upstream README reports >0.8 on 12/18 teacher outputs on another product set. That result supplies a reference for fidelity, not an experimental-label score.

Direct and distilled students use validation labels and validation teacher margins, respectively. Teacher early stopping itself uses experimental validation labels. Thus the distilled checkpoint depends indirectly on those labels. The neural worker receives no experimental test labels. The split and evaluation programs can read the raw targets. These are code-level controls within a shared filesystem.

The independently replayed synthetic stream checks ordered dummy identities against real training-slot membership, observed ordered type pairs, unique products, and all original canonical SMILES. The table also checks stronger forms of molecular similarity. Scaffold sharing and capped-feature collisions can make the augmented test prediction problem easier. They do not violate the sealed exact-product exclusion.

| Cell | Synthetic products | Exact overlap | Reparsed overlap | Val/test connectivity hits¹ | Test scaffolds represented | Test capped pairs in synthetic² |
|---|---|---|---|---|---|---|
| hERG scaffold | 2075 | 0 | 0 | 0 | 3/119 | 0 |
| hERG random | 2075 | 0 | 0 | 2 | 30/91 | 1 |
| Lipophilicity scaffold | 14090 | 0 | 0 | 0 | 60/806 | 0 |
| Lipophilicity random | 14090 | 0 | 0 | 0 | 182/636 | 2 |
| Solubility scaffold | 20000 | 0 | 0 | 0 | 23/1119 | 2 |
| Solubility random | 20000 | 0 | 0 | 6 | 204/450 | 18 |
| CYP3A4 scaffold | 20000 | 0 | 0 | 1 | 145/2306 | 0 |
| CYP3A4 random | 20000 | 0 | 0 | 3 | 496/1847 | 9 |

¹ Count of synthetic products matching val/test after removing stereo and isotope distinctions in non-isomeric SMILES. ² Count of test molecules with a matching ordered capped pair. Source molecules and chemical products can differ. num_threads=4 for each numerical worker. LightGBM and Torch ran in separate processes.

## CONTRADICTING:

No. src/harvest.py checks all 144 primary fit files, including significant direct gains that contradict C1 and the solubility loss against the teacher that contradicts C6. All 8 cells, 3 strata, and 3 seeds are present in audit/*-stats.json. Ineligible strata retain their molecule counts. The following ranges show the three single-initialization CP16 minus matched-control differences. The sealed decision uses the three-seed ensemble.

| Cell | Direct Δ, seeds 42/43/44 | Cartesian Δ, seeds 42/43/44 | Both seen | Decomp / all-clean teacher scores³ |
|---|---|---|---|---|
| hERG scaffold | -0.0010, -0.1023, -0.0799 | +0.0130, -0.0136, +0.0010 | 3 (N/A) | 0.8960 / 0.8935 |
| hERG random | -0.0420, -0.0013, -0.0672 | -0.0030, +0.0158, +0.0084 | 13 (N/A) | 0.9183 / 0.8668 |
| Lipophilicity scaffold | +0.0537, +0.0459, +0.0131 | +0.0236, +0.0280, +0.0069 | 40 (scored) | 0.7284 / 0.7484 |
| Lipophilicity random | +0.0129, +0.0014, -0.0227 | +0.0269, +0.0210, +0.0139 | 127 (scored) | 0.8286 / 0.8260 |
| Solubility scaffold | +0.0399, +0.0026, -0.0080 | +0.0133, +0.0279, +0.0280 | 41 (scored) | 0.7537 / 0.7799 |
| Solubility random | +0.0105, +0.0188, +0.0133 | +0.0142, +0.0184, +0.0236 | 521 (scored) | 0.8745 / 0.8978 |
| CYP3A4 scaffold | -0.0149, -0.0116, -0.0071 | +0.0185, +0.0166, +0.0178 | 290 (scored) | 0.8739 / 0.8751 |
| CYP3A4 random | -0.0039, -0.0019, -0.0044 | +0.0168, +0.0173, +0.0160 | 669 (scored) | 0.9180 / 0.9152 |

³ All-clean and decomposable populations were independently split. Differences mix population and split effects. See audit/*-stats.json for AP, RMSE, MAE, distilled-train controls, fidelity, intervals and seed SDs. Bootstrap intervals and permutation p-values condition on one split and fixed trained ensembles. Molecules sharing a scaffold are resampled individually under the sealed rule. The p-values are unadjusted for multiple comparisons.

## LABELS:

No. src/crosscheck.py independently re-read each Drug and numeric Y, regrouped standardized molecules, recomputed means or conflict exclusions, and verified every surviving target. Source assay annotations and physical measurements have no independent assay replicate in the allowed inputs. The check establishes agreement with the tabulated targets. Assay units and endpoint names come from the seal.

| Endpoint | Raw rows | Label counts or range | Invalid | Redundant valid rows merged | Conflicting keys dropped | Verified clean labels | Maximum absolute discrepancy |
|---|---|---|---|---|---|---|---|
| hERG | 655 | {'1.0': 451, '0.0': 204} | 0 | 10 | 3 | 639 | 0 |
| Lipophilicity | 4200 | [-1.5, 4.5] | 0 | 0 | 0 | 4200 | 0 |
| Solubility | 9982 | [-13.1719, 2.1376816201] | 2 | 398 | 0 | 9582 | 1.8e-15 |
| CYP3A4 | 12328 | {'0': 7218, '1': 5110} | 0 | 27 | 1 | 12299 | 0 |

## Tie-breaking and reproducibility

For all equal-balance candidates, the verifier reversed atom order and reran cut enumeration. It also replaced the sealed lexicographically first equal-balance cut with the last as a sensitivity check. This changes inputs while holding the test molecules fixed. The primary fits all retain the sealed winner.

| Endpoint | Distinct tied cuts (molecules) | Winner changes after atom reversal | Reverse-tie both seen, scaffold | Reverse-tie both seen, random | Original cut/join string mismatches | Of which same non-isomeric graph |
|---|---|---|---|---|---|---|
| hERG | 62 | 0 | 2 | 13 | 0 | 0 |
| Lipophilicity | 387 | 0 | 43 | 134 | 41 | 41 |
| Solubility | 626 | 0 | 40 | 510 | 0 | 0 |
| CYP3A4 | 1279 | 0 | 269 | 655 | 0 | 0 |

Two further checks hold the raw files fixed. The first rebuilds single-component SMILES without fragment extraction and reverses the lexical tie among equal-sized salt fragments in a separate variant. The second changes only the input ordering before the seeded random split.

| Endpoint | Literal single-component clean count | Single-component strings changed | Opposite salt tie, decomp/clean | Opposite salt tie, scaffold both | Random test overlap, raw vs canonical order |
|---|---|---|---|---|---|
| hERG | 639 | 0 | 594/639 | 3 | 28/120 |
| Lipophilicity | 4200 | 0 | 4027/4200 | 40 | 169/806 |
| Solubility | 9582 | 0 | 6400/9574 | 42 | 260/1280 |
| CYP3A4 | 12299 | 0 | 11528/12299 | 290 | 461/2306 |

All 41 initial cut/join string discrepancies on lipophilicity resolved to the same isomeric canonical SMILES on reparsing. The extra canonicalization check on accepted synthetic products is reported above.

The seal fixes seeds but leaves row order, sampling enumeration order, and some implementation conventions unspecified. The rebuild sorts canonical molecules and dummy identities, applies greedy scaffold packing, uses the three stated seeds literally, and averages raw scores. Upstream train.py adds rank to its CLI seed. Its defaults, original teacher losses and connector vocabulary differ from the sealed experimental adaptations. None of these ambiguities was tuned using reference results.

All 240 scalar comparisons for ties against SciPy/scikit-learn or direct arithmetic passed (maximum error 4.4e-16). All five metric-specific permutation p-values matched the exhaustive tiny-example swap lookup, and the paired RMSE bootstrap interval matched the scalar reference. The hash and version receipts are in audit/protocol.sha256, audit/environment.txt and audit/crosscheck.json. Sampling-related outputs are rerun evidence. They cannot establish what an inaccessible implementation actually did.

Methods and sources are in SEALED.md, DEVIATIONS.md, PRIOR_ART.md, src/, and the pinned public repository. REPORT.md gives reproduction commands.
