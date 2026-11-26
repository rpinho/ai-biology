# Prior Art & Baseline Reproduction

**Date:** 2026-11-24  
**Target:** `mireklzicar/synfactor` @ `1eaee906` (MIT license)

## 1. Target System Under Test: `mireklzicar/synfactor`
- **Repository:** `https://github.com/mireklzicar/synfactor` (MIT License, author: Miroslav Lžičař)
- **Pinned commit audited:** `1eaee90610d1a54654c0ec22544154676df4f8fa` (2026-11-16, *"Report matched-budget TYK2 docking and diverse portfolio improvements"*)
- **Method:** Neural rank-16 Canonical Polyadic (CP16) tensor factorization over capped synthons (`synfactor/model.py`, class `SynFactor`). Each capped synthon embedding passes through a shared `input_dim -> 64 -> GELU -> LayerNorm -> Dropout(0.1) -> 64 -> GELU` trunk and slot-specific linear heads producing rank-$R=16$ vectors $u, v$ (and optionally $w$). Two-synthon prediction is $\alpha \langle u, v \rangle / \sqrt{16} + \beta$ scaled by train target mean/std, trained with AdamW (`lr=0.002`, `weight_decay=0.002`), batch size 256, gradient clip 5.0, Huber loss on standardized targets, and validation-MSE early stopping (`patience=35`).
- **Published claims in repository (`synfactor/README.md`, `synfactor/benchmarks/paper_model_summary.csv`, `synfactor/benchmarks/comparison_pilot/README.md`):**
  - On a 993-route research split over 18 OpenADMET/CheMeleon teacher outputs, **12 of 18 CP16 outputs exceed test Spearman 0.8** (e.g., hERG `0.8417`, LogD MiniMol `0.9445`, LogD CheMeleon `0.8900`, HLM clearance `0.8130`), while CYP outputs are weaker (CYP1A2 `0.6939`, CYP2C9 `0.7189`, CYP2D6 `0.6534`, CYP3A4 `0.6659`).
  - On an 8-reaction dense Cartesian grid pilot (`4,400` products, `805` test products; all synthons seen in train, `2026-11-13`), CP16 achieved hERG teacher Spearman `0.970` vs `0.934` for a synthon-ID ridge additive lookup (`learned_additive`) and `0.816` for Shi et al. (2000) Eq. 11; median teacher Spearman across 18 ADMET outputs was `0.983` (CP16) vs `0.976` (fitted additive lookup).
  - **Explicitly stated limitations in `synfactor/README.md`:**
    1. All reported ADMET correlations are agreement with **teacher model predictions**, not experimental ADMET measurements (lines 22–23, 270).
    2. Splits share synthons/reactions across train and test (not a scaffold holdout; lines 257–258).
    3. The repo's `learned_additive` control (`experiments/compare.py:additive_fit`) is an embedding-free synthon-ID ridge lookup, so it changes both interaction order and input representation (lines 264–266).

## 2. Related Prior Art
- **Shi et al. (2000)** basis-product additive equation (cited and implemented in `synfactor/experiments/baselines.py`): exact for additive descriptors (`MolWt`, `HAC`, `HBA`, `HBD`, `TPSA`, `CrippenLogP`), approximate for nonlinear ADMET teachers.
- **SpaceProp / combinatorial property distribution methods** and **APEX factorized surrogates** (benchmarked in `synfactor/benchmarks/comparison_pilot/`).
- **Therapeutics Data Commons (TDC) ADMET Benchmark Group** (`https://tdcommons.ai/benchmark/admet_group/overview/`, Huang et al., NeurIPS 2021 / Nature Chemical Biology 2022): standard experimental ADMET benchmarks evaluated on Bemis-Murcko scaffold splits. Reported top public leaderboard scores (full-molecule models, scaffold split):
  - `hERG` (classification, AUROC, n≈648): MapLight+GNN ~`0.880` AUROC.
  - `CYP3A4_Veith` (classification, AUPRC, n=12,328): MapLight+GNN ~`0.916` AUPRC, ContextPred ~`0.904`, Chemprop ~`0.862`.
  - `Lipophilicity_AstraZeneca` (regression, MAE, n=4,200): MiniMol ~`0.456` MAE.
  - `Solubility_AqSolDB` (regression, MAE, n=9,982): MiniMol ~`0.741` MAE, Chemprop-RDKit ~`0.761` MAE.
- **BRICS retrosynthetic fragmentation** (Degen et al., *ChemMedChem* 2008, implemented in `rdkit.Chem.BRICS`): standard synthetically-motivated bond cleavage into building blocks/synthons.

## 3. Honest Reproduction of `mireklzicar/synfactor` Baseline
Before running any TDC experiments, we executed `synfactor`'s own test suite and bundled RDKit demo in `./.venv` (Python 3.12.13, PyTorch 2.15.0 CPU, RDKit 2026.9.2):
- **Unit tests:** `cd ./synfactor && ../.venv/bin/python -m unittest discover -s tests -v` -> **86 tests run in 4.30s: 80 OK, 6 skipped** (optional pyarrow/xgboost docking tests).
- **Bundled CrippenLogP demo (`prepare.py` + `train.py`, seed 38026, 3,000 products, 614 test products):**
  - Reported in `synfactor/README.md`: test Spearman `0.977` (~7 s CPU training).
  - Our reproduction (`results/synfactor_demo/metrics.json`): **test Spearman `0.9774`** (n=614; 2-component `0.9784` on n=584, 3-component `0.9270` on n=30; MAE `0.3026`; best epoch 266; training `8.44 s` on CPU; max float16 cache diff `0.00217`).
  - Reproduction matches upstream faithfully.

## 4. Gap Addressed by This Sealed Study
No public evaluation in `mireklzicar/synfactor` tests CP16 against **real experimental ADMET measurements** (e.g., TDC), nor isolates rank-16 bilinear interactions from a **representation-matched neural additive synthon control** under realistic **scaffold splits** and **unseen-synthon** prevalence. This study tests that gap under a pre-committed protocol (`SEALED.md`).
