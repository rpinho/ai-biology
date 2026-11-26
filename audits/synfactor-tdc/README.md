# TDC ADMET check on `mireklzicar/synfactor` (`1eaee906`)

Pre-registered empirical check of [`mireklzicar/synfactor`](https://github.com/mireklzicar/synfactor) pinned at commit `1eaee906` (MIT) across four experimental TDC ADMET endpoints (`hERG`, `Lipophilicity_AstraZeneca`, `Solubility_AqSolDB`, `CYP3A4_Veith`) on `scaffold` and `random` splits.

The full protocol was frozen in [SEALED.md](SEALED.md) before any TDC model training or evaluation. A separate AI referee on a different model family (`GPT-6.2 Astra`) then rebuilt the entire pipeline from the raw Harvard Dataverse TDC files and [SEALED.md](SEALED.md) alone, with zero access to the first agent's code or outputs (162 independent fits, including a planted false claim `C6` that was caught and refuted). No human has checked this yet, so treat it as a candidate.

## Refereed results (clean-room rebuild)

| Claim | Verdict | Independent referee result |
|---|---|---|
| **C2 (H1 Distilled-Cartesian)** | **CONFIRMED-WITH-CAVEATS** | `CP16-Distilled-Cartesian` beats representation-matched `NeuralAdditive` on **3/4 scaffold** (`Lipophilicity` +0.0256 p=0.0020; `Solubility` +0.0253 p=0.0015; `CYP3A4` +0.0192 AUROC p=0.0001; `hERG` +0.0019 n.s.) and **3/4 random** (+0.0251, +0.0213, +0.0189; `hERG` +0.0111 n.s.), with 0 significant degradations. Overall H1 = PASS. 0 exact-product overlaps across 112,330 synthetic products (caveat: some synthetic products share held-out test scaffolds, which is allowed under exact-product exclusion). |
| **C3 (Unseen synthons)** | **CONFIRMED-WITH-CAVEATS** | The Cartesian-distilled CP16 gain over matched `NeuralAdditive` persists inside `unseen_any` across all three large scaffold sets: `Lipophilicity` (n=766) +0.0243 (p=0.0035), `Solubility` (n=1,239) +0.0256 (p=0.0012), `CYP3A4` (n=2,016) +0.0178 (p=0.0003). |
| **C4 (Teacher fidelity vs experimental gap)** | **CONFIRMED-WITH-CAVEATS** | All 8 splits clear 0.80 teacher Spearman (0.8208 to 0.8931 scaffold; 0.8902 to 0.9595 random; hERG scaffold CI [0.728, 0.887] includes 0.80), yet `CP16-Distilled-Cartesian` still trails `FullMol-LGBM` on real experimental labels across all three large scaffold sets (`Lipophilicity` -0.0760, `Solubility` -0.1088, `CYP3A4` -0.0274, all p=0.0001). |
| **C5 (Coverage & overlap)** | **CONFIRMED-WITH-CAVEATS** | 1-cut BRICS covers 92.96% to 95.88% on `hERG`, `Lipophilicity`, and `CYP3A4`, and 66.76% (6,397/9,582; 66.85% under opposite equal-size salt tie-break) on `Solubility_AqSolDB`. Scaffold `both_seen` is 2.52% to 12.58%. |
| **C1 (Direct training & ID confound)** | **REFUTED (count); overall direct H1 still FAILS** | First run reported 0/4 scaffold and 0/4 random passes for `CP16-Direct`; referee found 1/4 scaffold (`Lipophilicity` +0.0689, p=0.0002) and 1/4 random (`Solubility` +0.0147, p=0.0167). Overall direct H1 still fails the pre-registered bar (>=2/4 scaffold or >=3/4 random). Against `synfactor`'s embedding-free `Additive-ID` baseline, the direct edge reproduced at +0.1083 to +0.3336 (p=0.0001) on the three large scaffold sets, confirming the representation confound. |
| **C6 (Planted false claim)** | **REFUTED** | Caught cleanly: `Solubility` coverage is 66.76% (not >90%) and distilled CP16 trailed `FullMol-LGBM` by -0.1088 Spearman (not +0.02). |

## Files

- Protocol & context: [SEALED.md](SEALED.md) · [DEVIATIONS.md](DEVIATIONS.md) · [PRIOR_ART.md](PRIOR_ART.md)
- First run (builder): [builder/RESULTS.md](builder/RESULTS.md) · [builder/REPORT.md](builder/REPORT.md) · [builder/CLAIMS.json](builder/CLAIMS.json) · [`builder/src/`](builder/src/)
- Independent rebuild (referee): [referee/VERDICT.md](referee/VERDICT.md) · [referee/verdict.json](referee/verdict.json) · [referee/REPORT.md](referee/REPORT.md) · [`referee/src/`](referee/src/)
