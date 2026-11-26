"""Locked chemistry preprocessing, BRICS 1-cut decomposition, splits, and featurization."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import BRICS, Crippen, Descriptors, Lipinski, rdFingerprintGenerator, rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.model_selection import train_test_split

RDLogger.DisableLog("rdApp.*")


def _largest_fragment(mol: Chem.Mol) -> Chem.Mol:
    frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
    if len(frags) == 1:
        return frags[0]
    scored = [
        (f.GetNumHeavyAtoms(), Chem.MolToSmiles(f, isomericSmiles=True, canonical=True), f)
        for f in frags
    ]
    # Pick largest heavy-atom count; break ties deterministically by smallest canonical SMILES
    scored.sort(key=lambda item: (-item[0], item[1]))
    return scored[0][2]


def standardize_dataset(df: pd.DataFrame, task: str) -> tuple[pd.DataFrame, dict[str, int]]:
    """Standardize SMILES (largest fragment, canonical isomeric) and deduplicate."""
    n_raw = len(df)
    n_invalid = 0
    rows = []
    for smi, y in zip(df["Drug"], df["Y"]):
        if not isinstance(smi, str) or pd.isna(y):
            n_invalid += 1
            continue
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            n_invalid += 1
            continue
        try:
            frag = _largest_fragment(mol)
            Chem.SanitizeMol(frag)
            canon = Chem.MolToSmiles(frag, isomericSmiles=True, canonical=True)
            if Chem.MolFromSmiles(canon) is None or frag.GetNumHeavyAtoms() < 1:
                n_invalid += 1
                continue
        except Exception:
            n_invalid += 1
            continue
        rows.append((canon, float(y)))

    work = pd.DataFrame(rows, columns=["smiles", "Y"])
    grouped = work.groupby("smiles", sort=True)["Y"]
    clean_rows = []
    n_dedup_merged = 0
    n_conflicts = 0
    for smi, vals in grouped:
        arr = vals.to_numpy(dtype=np.float64)
        if len(arr) > 1:
            if task == "classification":
                uniq = np.unique(arr)
                if len(uniq) > 1:
                    n_conflicts += 1
                    continue
                n_dedup_merged += len(arr) - 1
                clean_rows.append((smi, float(uniq[0])))
            else:
                n_dedup_merged += len(arr) - 1
                clean_rows.append((smi, float(arr.mean())))
        else:
            clean_rows.append((smi, float(arr[0])))

    clean_df = pd.DataFrame(clean_rows, columns=["smiles", "Y"])
    stats = {
        "n_raw": int(n_raw),
        "n_invalid": int(n_invalid),
        "n_dedup_merged": int(n_dedup_merged),
        "n_label_conflicts_dropped": int(n_conflicts),
        "n_clean": int(len(clean_df)),
    }
    return clean_df, stats


def _cap_dummy_fragment(frag: Chem.Mol) -> tuple[int, str, str, int] | None:
    """Extract single dummy isotope label, dummy SMILES, and H-capped canonical SMILES."""
    dummies = [a.GetIdx() for a in frag.GetAtoms() if a.GetAtomicNum() == 0]
    if len(dummies) != 1:
        return None
    d_idx = dummies[0]
    d_atom = frag.GetAtomWithIdx(d_idx)
    if d_atom.GetDegree() != 1:
        return None
    btype = int(d_atom.GetIsotope())
    dummy_smi = Chem.MolToSmiles(frag, isomericSmiles=True, canonical=True)

    rw = Chem.RWMol(frag)
    neighbor = rw.GetAtomWithIdx(d_idx).GetNeighbors()[0]
    neighbor.SetNumExplicitHs(neighbor.GetNumExplicitHs() + 1)
    rw.RemoveAtom(d_idx)
    capped = rw.GetMol()
    try:
        Chem.SanitizeMol(capped)
        capped_smi = Chem.MolToSmiles(capped, isomericSmiles=True, canonical=True)
        rt = Chem.MolFromSmiles(capped_smi)
        if rt is None:
            return None
        n_heavy = rt.GetNumHeavyAtoms()
        if n_heavy < 1:
            return None
        return btype, capped_smi, dummy_smi, int(n_heavy)
    except Exception:
        return None


def brics_one_cut(smiles: str) -> dict[str, Any] | None:
    """Deterministic balanced BRICS 1-cut into 2 valid capped synthons (SEALED.md Sec. 2)."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    candidates = []
    for (a1, a2), (t1, t2) in BRICS.FindBRICSBonds(mol):
        bond = mol.GetBondBetweenAtoms(a1, a2)
        if bond is None or bond.IsInRing() or bond.GetBondType() != Chem.BondType.SINGLE:
            continue
        labels = (int(t1), int(t2)) if bond.GetBeginAtomIdx() == a1 else (int(t2), int(t1))
        try:
            frag_mol = Chem.FragmentOnBonds(
                mol, [bond.GetIdx()], addDummies=True, dummyLabels=[labels]
            )
            frags = Chem.GetMolFrags(frag_mol, asMols=True, sanitizeFrags=True)
        except Exception:
            continue
        if len(frags) != 2:
            continue
        c0 = _cap_dummy_fragment(frags[0])
        c1 = _cap_dummy_fragment(frags[1])
        if c0 is None or c1 is None:
            continue
        # Orient canonically: (btype, capped_smiles, dummy_smiles) ascending
        pair = sorted([c0, c1], key=lambda item: (item[0], item[1], item[2]))
        s0, s1 = pair[0], pair[1]
        key = (
            abs(s0[3] - s1[3]),
            -min(s0[3], s1[3]),
            (s0[0], s0[1], s0[2]),
            (s1[0], s1[1], s1[2]),
        )
        candidates.append((key, s0, s1))

    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0])
    _, s0, s1 = candidates[0]
    return {
        "btype_0": s0[0],
        "capped_0": s0[1],
        "dummy_0": s0[2],
        "heavy_0": s0[3],
        "btype_1": s1[0],
        "capped_1": s1[1],
        "dummy_1": s1[2],
        "heavy_1": s1[3],
    }


def join_brics_frags(dummy_0: str, dummy_1: str) -> str | None:
    """Reassemble two single-dummy BRICS fragments into a canonical product SMILES."""
    m0 = Chem.MolFromSmiles(dummy_0)
    m1 = Chem.MolFromSmiles(dummy_1)
    if m0 is None or m1 is None:
        return None
    comb = Chem.CombineMols(m0, m1)
    rw = Chem.RWMol(comb)
    dummies = [a.GetIdx() for a in rw.GetAtoms() if a.GetAtomicNum() == 0]
    if len(dummies) != 2:
        return None
    n0_list = rw.GetAtomWithIdx(dummies[0]).GetNeighbors()
    n1_list = rw.GetAtomWithIdx(dummies[1]).GetNeighbors()
    if len(n0_list) != 1 or len(n1_list) != 1:
        return None
    n0, n1 = n0_list[0].GetIdx(), n1_list[0].GetIdx()
    if n0 == n1 or rw.GetBondBetweenAtoms(n0, n1) is not None:
        return None
    try:
        rw.AddBond(n0, n1, Chem.BondType.SINGLE)
        for idx in sorted(dummies, reverse=True):
            rw.RemoveAtom(idx)
        mol = rw.GetMol()
        Chem.SanitizeMol(mol)
        if any(a.GetAtomicNum() == 0 for a in mol.GetAtoms()):
            return None
        canon = Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)
        if Chem.MolFromSmiles(canon) is None:
            return None
        return canon
    except Exception:
        return None


def featurize_smiles(smiles_list: list[str] | np.ndarray) -> np.ndarray:
    """Locked 2,058-dim float32 featurizer: log1p(Morgan2 count 2048) + 10 RDKit descriptors."""
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    out = np.empty((len(smiles_list), 2058), dtype=np.float32)
    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            raise ValueError(f"Invalid SMILES in featurizer: {smi}")
        fp = np.log1p(gen.GetCountFingerprintAsNumPy(mol).astype(np.float32))
        out[i, :2048] = fp
        out[i, 2048:] = [
            float(Crippen.MolLogP(mol)),
            float(Descriptors.MolWt(mol)),
            float(Descriptors.TPSA(mol)),
            float(mol.GetNumHeavyAtoms()),
            float(Lipinski.NumHAcceptors(mol)),
            float(Lipinski.NumHDonors(mol)),
            float(Lipinski.NumRotatableBonds(mol)),
            float(rdMolDescriptors.CalcNumRings(mol)),
            float(rdMolDescriptors.CalcFractionCSP3(mol)),
            float(Crippen.MolMR(mol)),
        ]
    if not np.isfinite(out).all():
        raise ValueError("Non-finite descriptor values encountered")
    return out


def make_scaffold_split(smiles_list: list[str] | np.ndarray) -> np.ndarray:
    """Deterministic 70/10/20 Bemis-Murcko scaffold split (largest scaffolds first)."""
    scaffolds: dict[str, list[int]] = defaultdict(list)
    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        scaf = MurckoScaffold.MurckoScaffoldSmiles(mol=mol, includeChirality=False)
        scaffolds[scaf].append(i)
    groups = sorted(scaffolds.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    n = len(smiles_list)
    train_cut = 0.70 * n
    val_cut = 0.80 * n
    split = np.empty(n, dtype=object)
    train_n = 0
    val_n = 0
    for _, idxs in groups:
        if train_n + len(idxs) <= train_cut:
            split[idxs] = "train"
            train_n += len(idxs)
        elif train_n + val_n + len(idxs) <= val_cut:
            split[idxs] = "validation"
            val_n += len(idxs)
        else:
            split[idxs] = "test"
    return split.astype(str)


def make_random_split(
    smiles_list: list[str] | np.ndarray, y: np.ndarray, task: str, seed: int = 42
) -> np.ndarray:
    """Deterministic 70/10/20 random split (stratified on Y for classification)."""
    n = len(smiles_list)
    idx = np.arange(n)
    strat = y.astype(int) if task == "classification" else None
    tr, tmp = train_test_split(idx, test_size=0.30, random_state=seed, stratify=strat)
    strat_tmp = y[tmp].astype(int) if task == "classification" else None
    va, te = train_test_split(tmp, test_size=2.0 / 3.0, random_state=seed, stratify=strat_tmp)
    split = np.empty(n, dtype=object)
    split[tr] = "train"
    split[va] = "validation"
    split[te] = "test"
    return split.astype(str)


def generate_cartesian_pairs(
    train_df: pd.DataFrame,
    forbidden_smiles: set[str],
    max_pairs: int,
    seed: int = 42,
) -> pd.DataFrame:
    """Sample leak-free BRICS-compatible Cartesian products from train-only synthons."""
    rng = np.random.default_rng(seed)
    # Group unique train synthons by (btype_0, btype_1)
    pair_types = train_df.groupby(["btype_0", "btype_1"], sort=True)
    type_keys = []
    type_weights = []
    slot0_pools: dict[tuple[int, int], list[tuple[str, str]]] = {}
    slot1_pools: dict[tuple[int, int], list[tuple[str, str]]] = {}

    for (b0, b1), grp in pair_types:
        s0 = sorted(set(zip(grp["capped_0"].tolist(), grp["dummy_0"].tolist())))
        s1 = sorted(set(zip(grp["capped_1"].tolist(), grp["dummy_1"].tolist())))
        if len(s0) * len(s1) <= len(grp):
            continue
        type_keys.append((int(b0), int(b1)))
        type_weights.append(len(grp))
        slot0_pools[(int(b0), int(b1))] = s0
        slot1_pools[(int(b0), int(b1))] = s1

    if not type_keys or max_pairs <= 0:
        return pd.DataFrame(columns=["smiles", "capped_0", "capped_1", "btype_0", "btype_1"])

    probs = np.asarray(type_weights, dtype=np.float64)
    probs /= probs.sum()

    seen_smiles = set(forbidden_smiles)
    seen_pairs: set[tuple[str, str]] = set(zip(train_df["capped_0"], train_df["capped_1"]))
    records = []
    max_attempts = max_pairs * 8
    attempts = 0
    while len(records) < max_pairs and attempts < max_attempts:
        attempts += 1
        t_idx = int(rng.choice(len(type_keys), p=probs))
        key = type_keys[t_idx]
        p0 = slot0_pools[key]
        p1 = slot1_pools[key]
        c0, d0 = p0[int(rng.integers(len(p0)))]
        c1, d1 = p1[int(rng.integers(len(p1)))]
        if (c0, c1) in seen_pairs:
            continue
        prod = join_brics_frags(d0, d1)
        if prod is None or prod in seen_smiles:
            continue
        seen_smiles.add(prod)
        seen_pairs.add((c0, c1))
        records.append(
            {
                "smiles": prod,
                "capped_0": c0,
                "capped_1": c1,
                "btype_0": key[0],
                "btype_1": key[1],
            }
        )

    out = pd.DataFrame(records)
    # Mandatory anti-leakage assertion
    if len(out) > 0:
        assert not set(out["smiles"]).intersection(forbidden_smiles), "Leakage detected in Cartesian generation!"
    return out
