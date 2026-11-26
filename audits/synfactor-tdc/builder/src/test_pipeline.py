"""Unit tests validating pipeline invariants on synthetic data before running sealed TDC experiments."""

import unittest

import numpy as np
import pandas as pd
import torch
from rdkit import Chem

from chemistry_utils import (
    brics_one_cut,
    featurize_smiles,
    generate_cartesian_pairs,
    join_brics_frags,
    make_scaffold_split,
)
from models import (
    NeuralAdditiveSynthon,
    SynFactor,
    fit_additive_id_ridge,
    fit_lgbm_teacher,
    predict_lgbm_scores,
)
from stats_utils import _batch_metric, _metric_val, paired_comparison


class PipelineInvariantTests(unittest.TestCase):
    def test_brics_one_cut_deterministic_and_roundtrips(self):
        # Atom-order permutation invariance for aspirin
        smi1 = "CC(=O)Oc1ccccc1C(=O)O"
        mol = Chem.MolFromSmiles(smi1)
        smi2 = Chem.MolToSmiles(mol, doRandom=True)
        c1 = brics_one_cut(smi1)
        c2 = brics_one_cut(smi2)
        self.assertIsNotNone(c1)
        self.assertEqual(c1, c2)
        rebuilt = join_brics_frags(c1["dummy_0"], c1["dummy_1"])
        canon = Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)
        self.assertEqual(rebuilt, canon)

    def test_neural_additive_has_zero_interaction(self):
        torch.manual_seed(0)
        model = NeuralAdditiveSynthon(input_dim=8, tasks=1, hidden=16)
        model.eval()
        a1, a2 = torch.randn(1, 8), torch.randn(1, 8)
        b1, b2 = torch.randn(1, 8), torch.randn(1, 8)
        z = torch.zeros(1, 8)
        pres = torch.tensor([[True, True, False]])
        y11 = model(torch.stack([a1, b1, z], dim=1), pres).item()
        y12 = model(torch.stack([a1, b2, z], dim=1), pres).item()
        y21 = model(torch.stack([a2, b1, z], dim=1), pres).item()
        y22 = model(torch.stack([a2, b2, z], dim=1), pres).item()
        # Strictly additive: (y22 - y21) == (y12 - y11)
        self.assertAlmostEqual(y22 - y21, y12 - y11, places=5)

    def test_synfactor_imported_runs_two_slot(self):
        torch.manual_seed(0)
        model = SynFactor(input_dim=8, tasks=1, rank=16, hidden=16)
        model.eval()
        comp = torch.randn(4, 3, 8)
        pres = torch.tensor([[True, True, False]] * 4)
        out = model(comp, pres)
        self.assertEqual(tuple(out.shape), (4, 1))
        self.assertTrue(torch.isfinite(out).all())

    def test_cartesian_anti_leakage(self):
        mols = [
            "CC(=O)Oc1ccccc1C(=O)O",
            "CC(=O)Oc1ccc(C)cc1",
            "CCC(=O)Oc1ccccc1",
            "CC(=O)Oc1ccc(F)cc1",
            "CCCC(=O)Oc1ccc(Cl)cc1",
        ]
        recs = []
        for s in mols:
            c = brics_one_cut(s)
            if c:
                recs.append({"smiles": Chem.MolToSmiles(Chem.MolFromSmiles(s), isomericSmiles=True), **c})
        df = pd.DataFrame(recs)
        forbidden = set(df["smiles"])
        cart = generate_cartesian_pairs(df, forbidden_smiles=forbidden, max_pairs=20, seed=42)
        self.assertGreater(len(cart), 0)
        self.assertFalse(set(cart["smiles"]).intersection(forbidden))

    def test_scaffold_split_disjoint_scaffolds(self):
        from rdkit.Chem.Scaffolds import MurckoScaffold

        smis = [
            "c1ccccc1C", "c1ccccc1CC", "c1ccccc1CCC", "c1ccccc1O",
            "c1ccncc1C", "c1ccncc1CC", "c1ccncc1O",
            "c1ccc2ccccc2c1C", "c1ccc2ccccc2c1CC",
            "C1CCCCC1C", "C1CCCCC1CC",
            "c1ccoc1C", "c1ccsc1C",
        ]
        split = make_scaffold_split(smis)
        scafs = [MurckoScaffold.MurckoScaffoldSmiles(mol=Chem.MolFromSmiles(s), includeChirality=False) for s in smis]
        tr_scaf = {sc for sc, sp in zip(scafs, split) if sp == "train"}
        va_scaf = {sc for sc, sp in zip(scafs, split) if sp == "validation"}
        te_scaf = {sc for sc, sp in zip(scafs, split) if sp == "test"}
        self.assertFalse(tr_scaf & va_scaf)
        self.assertFalse(tr_scaf & te_scaf)
        self.assertFalse(va_scaf & te_scaf)

    def test_paired_comparison_sanity(self):
        rng = np.random.default_rng(0)
        y = rng.normal(size=100)
        p1 = y + rng.normal(scale=0.2, size=100)
        p2 = y + rng.normal(scale=1.5, size=100)
        res_same = paired_comparison(y, p1, p1, "spearman", n_boot=200, n_perm=500)
        self.assertEqual(res_same["delta"], 0.0)
        self.assertGreater(res_same["p_perm"], 0.99)
        res_diff = paired_comparison(y, p1, p2, "spearman", n_boot=200, n_perm=500)
        self.assertGreater(res_diff["delta"], 0.1)
        self.assertLess(res_diff["p_perm"], 0.01)

    def test_featurizer_shape(self):
        X = featurize_smiles(["CCO", "c1ccccc1"])
        self.assertEqual(X.shape, (2, 2058))
        self.assertEqual(X.dtype, np.float32)

    def test_additive_id_ridge_runs(self):
        rng = np.random.default_rng(0)
        tuples = np.column_stack([rng.integers(0, 5, 50), rng.integers(5, 10, 50), np.full(50, -1)])
        w = rng.normal(size=10)
        y = w[tuples[:, 0]] + w[tuples[:, 1]] + rng.normal(scale=0.05, size=50)
        split = np.array(["train"] * 35 + ["validation"] * 5 + ["test"] * 10)
        pred, info = fit_additive_id_ridge(y, tuples, split)
        self.assertEqual(len(pred), 50)
        self.assertLess(np.sqrt(np.mean((pred[40:] - y[40:]) ** 2)), 0.3)

    def test_vectorized_metrics_match_scalar_reference_including_ties(self):
        rng = np.random.default_rng(123)
        n = 80
        # Classification: both continuous and heavily tied predictions (e.g. Ridge ID unseen intercept)
        y_cls = rng.integers(0, 2, size=n).astype(np.float64)
        s_cont = rng.normal(size=(6, n))
        s_tied = np.round(rng.normal(size=(6, n)) * 2.0) / 2.0
        s_tied[:, :25] = 0.0  # heavy constant tie block
        S_cls = np.vstack([s_cont, s_tied])

        for metric in ("auroc", "auprc"):
            vec_1d = _batch_metric(y_cls, S_cls, metric)
            ref_1d = np.array([_metric_val(y_cls, row, metric) for row in S_cls])
            self.assertLess(float(np.max(np.abs(vec_1d - ref_1d))), 1e-12)

            Y2 = np.stack([y_cls[rng.integers(0, n, size=n)] for _ in range(len(S_cls))])
            vec_2d = _batch_metric(Y2, S_cls, metric)
            ref_2d = np.array([_metric_val(y_row, s_row, metric) for y_row, s_row in zip(Y2, S_cls)])
            self.assertLess(float(np.max(np.abs(vec_2d - ref_2d))), 1e-12)

        # Regression: continuous + tied
        y_reg = rng.normal(size=n)
        S_reg = np.vstack([rng.normal(size=(5, n)), np.round(rng.normal(size=(5, n)), 1)])
        for metric in ("spearman", "pearson", "rmse", "mae"):
            vec_1d = _batch_metric(y_reg, S_reg, metric)
            ref_1d = np.array([_metric_val(y_reg, row, metric) for row in S_reg])
            self.assertLess(float(np.max(np.abs(vec_1d - ref_1d))), 1e-12)

            Y2 = np.stack([y_reg[rng.integers(0, n, size=n)] for _ in range(len(S_reg))])
            vec_2d = _batch_metric(Y2, S_reg, metric)
            ref_2d = np.array([_metric_val(y_row, s_row, metric) for y_row, s_row in zip(Y2, S_reg)])
            self.assertLess(float(np.max(np.abs(vec_2d - ref_2d))), 1e-12)

    def test_isolated_lgbm_coexists_with_pytorch(self):
        rng = np.random.default_rng(7)
        X_tr = rng.normal(size=(120, 32)).astype(np.float32)
        y_tr = (X_tr[:, 0] + rng.normal(scale=0.5, size=120) > 0).astype(np.float64)
        X_va = rng.normal(size=(40, 32)).astype(np.float32)
        y_va = (X_va[:, 0] + rng.normal(scale=0.5, size=40) > 0).astype(np.float64)
        teacher = fit_lgbm_teacher(X_tr, y_tr, X_va, y_va, task="classification", seed=42)
        probs, logits = predict_lgbm_scores(teacher, X_va, task="classification")
        self.assertEqual(probs.shape, (40,))
        self.assertTrue(np.all((probs >= 0.0) & (probs <= 1.0)))
        self.assertLess(float(np.max(np.abs(probs - 1.0 / (1.0 + np.exp(-logits))))), 1e-6)
        # Verify PyTorch multi-threaded backward pass still runs cleanly afterward
        torch.set_num_threads(4)
        lin = torch.nn.Linear(32, 8)
        out = lin(torch.tensor(X_tr))
        out.sum().backward()


if __name__ == "__main__":
    unittest.main()
