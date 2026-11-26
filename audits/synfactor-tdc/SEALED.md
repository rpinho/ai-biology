# Sealed Experimental Protocol: SynFactor CP16 vs Additive & Full-Molecule Baselines on Experimental TDC ADMET Benchmarks

**Frozen on:** 2026-11-24 (committed BEFORE any TDC model training or test-set evaluation)  
**Target repo under test:** `https://github.com/mireklzicar/synfactor` @ `1eaee90610d1a54654c0ec22544154676df4f8fa`  
**Environment:** Python 3.12.13 (`./.venv`), PyTorch 2.15.0 (CPU), RDKit 2026.9.2, LightGBM 4.7.0, scikit-learn 1.9.1, SciPy 1.18.1, NumPy 2.5.5, pandas 3.1.1.

---

## 1. Endpoints & Frozen Data Provenance

Four public experimental Therapeutics Data Commons (TDC) ADMET datasets fetched directly from Harvard Dataverse (IDs from official `mims-harvard/TDC/tdc/metadata.py`), spanning classification and regression, plus strong-teacher/additive (hERG, Lipophilicity) and weaker/non-additive (CYP3A4, Solubility) regimes:

| Endpoint (`key`) | TDC Name | Task | Raw Rows | Dataverse URL | SHA-256 (`data/<key>.tab`) |
| --- | --- | --- | ---: | --- | --- |
| `herg` | `hERG` | Binary classification | 655 | `https://dataverse.harvard.edu/api/access/datafile/4259588` | `dfce97b6a89b710d20c93cf211f005fbee0d8445a60ca7df584cac430798a379` |
| `cyp3a4_veith` | `CYP3A4_Veith` | Binary classification | 12,328 | `https://dataverse.harvard.edu/api/access/datafile/4259582` | `4c85a4cea9ffadd36fdd188f96b866d1d8db5d333a6d423172cf4363a585565a` |
| `lipophilicity_astrazeneca` | `Lipophilicity_AstraZeneca` | Regression (logD pH 7.4) | 4,200 | `https://dataverse.harvard.edu/api/access/datafile/4259595` | `14add1edb356e62f78256ff964c0cbba03c007be3ff48d6d4c18679f307f1d4c` |
| `solubility_aqsoldb` | `Solubility_AqSolDB` | Regression (logS mol/L) | 9,982 | `https://dataverse.harvard.edu/api/access/datafile/4259610` | `0b593f7b55abbe477ba4284aefd7b5450551f4ed21ac4aed80a097931141c9a4` |

### Standardization & Deduplication (Deterministic, Pre-Split)
1. Parse `Drug` SMILES with `Chem.MolFromSmiles`; drop unparseable molecules (logged).
2. If multi-fragment (salts/mixtures), retain the single largest fragment by `(num_heavy_atoms, canonical_smiles)` via `Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)`.
3. Canonicalize with `Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)`.
4. Deduplicate by canonical SMILES:
   - **Regression:** average `Y` across duplicate SMILES.
   - **Classification:** keep one row if all duplicates share the same binary label; drop canonical SMILES with conflicting labels (`0` and `1`).
   - Exact counts (`n_raw`, `n_invalid`, `n_dedup_merged`, `n_label_conflicts_dropped`, `n_clean`) are recorded.

---

## 2. Exact BRICS 1-Cut / 2-Synthon Decomposition Protocol

For each standardized single-fragment molecule `mol` in `N_clean`:
1. Enumerate all candidate bonds `(a1, a2)` with BRICS environment types `(t1, t2)` returned by `rdkit.Chem.BRICS.FindBRICSBonds(mol)` that satisfy `not bond.IsInRing()` and `bond.GetBondType() == Chem.BondType.SINGLE`.
2. For each candidate bond:
   - Align dummy labels with the bond's `(begin, end)` orientation: `labels = (int(t1), int(t2))` if `bond.GetBeginAtomIdx() == a1` else `(int(t2), int(t1))`.
   - Cut with `Chem.FragmentOnBonds(mol, [bond.GetIdx()], addDummies=True, dummyLabels=[labels])` and split with `Chem.GetMolFrags(..., asMols=True, sanitizeFrags=True)`. Require exactly 2 fragments.
   - For each fragment, locate its single dummy atom (`atomicNum == 0`, degree 1), record its dummy isotope label `btype = dummy.GetIsotope()`, record `dummy_smiles = Chem.MolToSmiles(frag, isomericSmiles=True, canonical=True)`, and produce `capped_smiles` by incrementing `neighbor.SetNumExplicitHs(neighbor.GetNumExplicitHs() + 1)` and removing the dummy atom (mirroring `synfactor/chemistry.py:cap_synthon`), sanitizing (`Chem.SanitizeMol`), verifying round-trip parsing (`Chem.MolFromSmiles`), and requiring `num_heavy_atoms >= 1`.
   - Orient the two synthons canonically as `(slot_0, slot_1)` by sorting the two tuples `(btype, capped_smiles, dummy_smiles)` ascending.
3. **Deterministic tie-breaking:** Among all valid 2-synthon BRICS 1-cuts of `mol`, select the unique cut minimizing:
   `(|heavy_atoms(slot_0) - heavy_atoms(slot_1)|, -min(heavy_atoms(slot_0), heavy_atoms(slot_1)), (btype_0, capped_0, dummy_0), (btype_1, capped_1, dummy_1))`.
   This selects the most balanced synthetically-cleavable 2-synthon split with atom-order-independent deterministic tie-breaking.
4. Molecules with zero valid cuts are recorded as non-decomposable.

### Coverage & Synthon-Overlap Metrics Reported
- **Decomposition coverage:** `n_decomp / n_clean` (% of valid unique molecules admitting a valid BRICS 1-cut 2-synthon decomposition).
- **Test synthon overlap (per split):** for each decomposable test molecule `(s0, s1)`:
  - `both_seen`: `s0` observed in `train` slot 0 AND `s1` observed in `train` slot 1 (primary, matching SynFactor's slot-indexed heads; we also report slot-agnostic `both_seen_any_slot`).
  - `one_seen`: exactly one of `(0, s0)` or `(1, s1)` observed in `train`.
  - `neither_seen`: neither observed in `train`.
  - `unseen_any = one_seen + neither_seen`.

---

## 3. Splits & Seeds (Locked)

All models are evaluated on the **exact same decomposable molecule splits** per endpoint (we also log `FullMol-LGBM` on all `N_clean` vs `N_decomp` to audit any coverage selection bias):

1. **Scaffold Split (`scaffold`, 70/10/20, deterministic):**
   - Compute Bemis-Murcko scaffold `MurckoScaffold.MurckoScaffoldSmiles(mol=mol, includeChirality=False)`.
   - Group molecules by scaffold, sort groups by `(-len(group), scaffold_smiles)` (standard deterministic TDC/DeepChem greedy packing).
   - Assign groups in order to `train` until adding the next group would exceed `0.70 * N`, then to `validation` until `0.80 * N`, and remaining groups to `test`. Zero scaffold overlap across splits.
2. **Random / Pair-Overlap Split (`random`, 70/10/20, fixed seed `42`):**
   - `sklearn.model_selection.train_test_split` with `random_state=42`: first 70% `train` vs 30% `temp`, then `temp` split 1/3 `validation` (10%) vs 2/3 `test` (20%). Stratified on `Y` for classification endpoints; unstratified for regression endpoints.

Every neural model is trained across **3 fixed initialization seeds (`42, 43, 44`)**, matching SynFactor's 3-initialization protocol (`synfactor/README.md` line 263). Primary test predictions are the **3-seed ensemble mean** (for paired bootstrap/permutation tests on the fixed test set); we also report mean ± SD across the 3 individual seeds.

---

## 4. Shared Featurization & Locked Models

### Featurizer (Identical for Full Molecules and Capped Synthons)
Every molecule or capped synthon SMILES is mapped to a **2,058-dimensional `float32` vector**:
- 2,048-dim Morgan count fingerprint (`rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048).GetCountFingerprintAsNumPy(mol)`), transformed via `np.log1p(counts)`.
- 10 RDKit physicochemical descriptors: `MolLogP`, `MolWt`, `TPSA`, `NumHeavyAtoms`, `NumHAcceptors`, `NumHDonors`, `NumRotatableBonds`, `RingCount`, `FractionCSP3`, `MolMR`.

Using identical `2058`-dim capped-synthon embeddings for both `Additive` and `CP16` eliminates the representation confound noted in `synfactor/README.md` lines 264–266.

### Models Compared

1. **`FullMol-LGBM` (Model 1: Full-Molecule Baseline & Teacher)**
   - LightGBM (`LGBMClassifier` / `LGBMRegressor`) on the 2,058-dim full-molecule feature vector.
   - Locked hyperparameters: `n_estimators=2000`, `learning_rate=0.03`, `num_leaves=31`, `min_child_samples=20`, `subsample=0.8`, `subsample_freq=1`, `colsample_bytree=0.5`, `reg_lambda=1.0`, `random_state=42`, `n_jobs=4`, early stopping on validation set (`early_stopping_rounds=50`; logloss for classification, RMSE for regression).
   - Distillation targets emitted by the frozen teacher: continuous `y_hat` for regression; continuous raw margin (log-odds `predict(..., raw_score=True)`) for classification.

2. **`Additive-Direct` & `Additive-Distilled-*` (Model 2a: Representation-Matched Neural Additive Synthon Control)**
   - Exact same `SynFactor` trunk (`2058 -> 64 -> GELU -> LayerNorm(64) -> Dropout(0.1) -> 64 -> GELU`), input standardization (`x_mean`, `x_scale` from train synthon occurrences, clamped `[-8, 8]`), and slot-specific heads, EXCEPT each slot head outputs a single scalar $s_0(x_0), s_1(x_1)$ combined purely additively:
     $$\hat{y} = \big((s_0(x_0) + s_1(x_1)) \cdot \alpha + \beta\big) \cdot y_{\text{scale}} + y_{\text{mean}}.$$
   - Identical training schedule as CP16 (`AdamW(lr=0.002, weight_decay=0.002)`, batch size `256`, `clip_grad_norm_(5.0)`, max `300` epochs, early-stopping `patience=35`, seeds `42, 43, 44`).
   - Trained in all three regimes matched to CP16: `Additive-Direct` (experimental labels), `Additive-Distilled-Train` (teacher predictions on train molecules), and `Additive-Distilled-Cartesian` (teacher predictions on train + synthetic train-only Cartesian pairs).

   **`Additive-ID-Ridge` (Model 2b: Exact SynFactor Repo Control)**
   - Exact `additive_fit` from `synfactor/experiments/compare.py`: train-only ridge slot-ID lookup (no embeddings; validation-selected $\lambda \in \{10^{-6}, 10^{-3}, 0.1, 1.0, 10.0\}$; unseen synthons receive zero slot contribution -> global intercept). Evaluated in both Direct and Distilled-Train regimes for exact traceability to `synfactor`.

3. **`CP16-Direct` (Model 3: SynFactor CP16 Trained on Experimental TDC Labels)**
   - Exact `SynFactor(input_dim=2058, tasks=1, rank=16, hidden=64)` imported directly from `./synfactor/model.py` (`present = [True, True, False]`).
   - Exact `synfactor/train.py` optimization (`AdamW(lr=0.002, weight_decay=0.002)`, batch size `256`, `clip_grad_norm_(5.0)`, `epochs=300`, `patience=35`, seeds `42, 43, 44`).
   - Loss: exact `synfactor/train.py` Huber loss on standardized targets (validation early-stopping on standardized MSE) for regression; `BCEWithLogitsLoss` on raw logit output (`y_mean=0, y_scale=1`, validation early-stopping on BCE) for binary classification.

4. **`CP16-Distilled-Train` & `CP16-Distilled-Cartesian` (Model 4: SynFactor CP16 Distilled from `FullMol-LGBM`)**
   - Exact `SynFactor` class imported from `./synfactor/model.py` (`rank=16, hidden=64`), trained with exact `synfactor/train.py` Huber loss on standardized continuous teacher targets (`y_hat` for regression; `logit_hat` for classification), validation early-stopping on standardized MSE against teacher predictions on the `validation` split (`y_val` experimental labels are NEVER used during distillation).
   - **`CP16-Distilled-Train`:** distilled on `(train_pairs, teacher_pred(train_mol))`.
   - **`CP16-Distilled-Cartesian` (SynFactor's Cartesian workflow):** augments train pairs with up to `M = min(20_000, 5 * N_train)` synthetic BRICS-compatible Cartesian combinations of **train-only** synthons:
     1. Collect unique `(slot_0, slot_1)` synthons from `train`, grouped by BRICS dummy-type pairs `(btype_0, btype_1)` observed in `train`.
     2. Sample pairs proportional to train `(btype_0, btype_1)` counts (fixed seed `42`), join dummy neighbors by a single bond, remove dummy atoms, sanitize, and canonicalize.
     3. **Anti-leakage check (mandatory assertion):** drop any assembled product whose canonical SMILES appears in `train`, `validation`, OR `test`. Deduplicate assembled SMILES.
     4. Score synthetic products with frozen `FullMol-LGBM` and distill both `CP16-Distilled-Cartesian` and `Additive-Distilled-Cartesian` on `train + synthetic_cartesian`.

---

## 5. Evaluation Metrics, Stratification & Pre-Registered Pass/Fail Rules

### Metrics
- **Classification (`hERG`, `CYP3A4_Veith`):** Primary = **AUROC**; Secondary = **AUPRC** (TDC official CYP metric).
- **Regression (`Lipophilicity_AstraZeneca`, `Solubility_AqSolDB`):** Primary = **Spearman $\rho$** and **RMSE**; Secondary = **MAE** (TDC official metric).
- **Teacher Fidelity (distilled models):** **Spearman $\rho$** (and Pearson $r$) between student and `FullMol-LGBM` predictions on the held-out test set.

### Stratification
Evaluated on:
1. `all` (all decomposable test molecules)
2. `both_seen` (both `(slot, capped_smiles)` observed in `train`)
3. `unseen_any` (at least one synthon unseen in `train`)

Strata with `n < 20` (or `< 2` samples of either class for classification) are reported as `N/A (n=...)` rather than noisy estimates.

### Uncertainty & Paired Hypothesis Tests (Fixed Seed `20261124`)
- **95% Bootstrap CIs:** 2,000 paired nonparametric bootstrap resamples of test molecules (for both point metrics and model differences $\Delta$).
- **Two-Sided Paired Permutation Test:** 10,000 random per-molecule swaps between two models' predictions (for scale-sensitive RMSE, raw predictions swapped; for rank metrics AUROC/Spearman, rank-standardized or raw score swap — specifically, exact paired prediction swap of the two models' test prediction arrays on the same test molecules), yielding exact two-sided $p = (1 + \#\{|\Delta_{\text{perm}}| \ge |\Delta_{\text{obs}}|\}) / 10001$.
  - *Note on scale alignment for paired swaps:* Because AUROC and Spearman are invariant to strictly monotone increasing transforms, before computing paired permutation swaps for AUROC/Spearman we z-score each model's test predictions (zero mean, unit std) so swapping predictions across models tests rank-order differences rather than arbitrary offset/scale differences! For RMSE, raw predictions (in native target units) are swapped directly.

### Pre-Registered Pass/Fail Criteria

1. **H1 — Non-Additive CP16 Gain over Matched Neural Additive Control on Real Experimental ADMET Labels:**
   - **Per-cell PASS** (for an endpoint $\times$ split $\times$ training regime):
     - Classification: $\Delta\text{AUROC}(\text{CP16} - \text{Additive}) \ge +0.010$ AND two-sided paired permutation $p < 0.05$ AND 95% bootstrap CI strictly $> 0$.
     - Regression: ($\Delta\rho(\text{CP16} - \text{Additive}) \ge +0.010$ OR $\Delta\text{RMSE}(\text{CP16} - \text{Additive}) \le -0.020$) AND two-sided paired permutation $p < 0.05$ AND 95% bootstrap CI excludes $0$ in the favorable direction.
   - **Overall H1 PASS:** $\ge 2/4$ endpoints pass on **Scaffold split** OR $\ge 3/4$ endpoints pass on **Random split** (in either Direct or Distilled-Cartesian regime), with zero statistically significant degradations ($\Delta \le -0.010$ / $\Delta\text{RMSE} \ge +0.020$ at $p < 0.05$) on other endpoints. Otherwise **FAIL** (no robust non-additive experimental advantage).

2. **H2 — Distillation Fidelity vs Experimental Accuracy Gap:**
   - Check whether `CP16-Distilled-Cartesian` reaches SynFactor's benchmark teacher Spearman $\ge 0.80$ on non-CYP endpoints on real TDC splits, AND measure the exact experimental gap $\Delta = \text{metric}(\text{CP16-Distilled-Cartesian}) - \text{metric}(\text{FullMol-LGBM})$ (with 95% CI and paired $p$).

3. **H3 — Real-World Synthon Coverage & Overlap Audit:**
   - Quantify exact BRICS 2-synthon coverage (`n_decomp / n_clean`) and `both_seen` fraction under Scaffold vs Random splits across all 4 TDC benchmarks.

---

## 6. No-Deviation Commitment

No hyperparameter, feature, split, metric, or model architecture in Sections 1–5 may be modified after committing `SEALED.md`. If any unforeseen technical failure forces a change, it will be logged verbatim in `DEVIATIONS.md`.
