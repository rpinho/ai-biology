"""Deterministic full-molecule and fragment identities."""
from functools import lru_cache

import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import BRICS, Crippen, Descriptors, Lipinski, rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold
RDLogger.DisableLog("rdApp.*")

def smiles(mol):
    return Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)

def standard(s):
    mol = Chem.MolFromSmiles(s)
    if mol is None:
        return None
    pieces = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
    return max((p.GetNumHeavyAtoms(), smiles(p)) for p in pieces)[1]

def identity(frag):
    atoms = [a for a in frag.GetAtoms() if a.GetAtomicNum()==0]
    if len(atoms)!=1 or atoms[0].GetDegree()!=1:
        return None
    dummy = atoms[0]
    edit = Chem.RWMol(frag)
    neighbor = edit.GetAtomWithIdx(dummy.GetNeighbors()[0].GetIdx())
    neighbor.SetNumExplicitHs(neighbor.GetNumExplicitHs()+1)
    edit.RemoveAtom(dummy.GetIdx())
    Chem.SanitizeMol(edit)
    capped = smiles(edit)
    if not edit.GetNumHeavyAtoms() or Chem.MolFromSmiles(capped) is None:
        return None
    return (dummy.GetIsotope(), capped, smiles(frag)), edit.GetNumHeavyAtoms()

def cuts(mol):
    options = set()
    for (a,b),(ta,tb) in BRICS.FindBRICSBonds(mol):
        bond = mol.GetBondBetweenAtoms(a,b)
        if bond.IsInRing() or bond.GetBondType()!=Chem.BondType.SINGLE:
            continue
        labels = (int(ta),int(tb))
        if a != bond.GetBeginAtomIdx():
            labels = labels[::-1]
        try:
            cut = Chem.FragmentOnBonds(mol,[bond.GetIdx()],dummyLabels=[labels])
            frags = Chem.GetMolFrags(cut, asMols=True, sanitizeFrags=True)
            parts = [identity(f) for f in frags]
        except (RuntimeError, ValueError):
            continue
        if len(parts)!=2 or None in parts:
            continue
        (s,x),(t,y) = sorted(parts)
        options.add((abs(x-y),-min(x,y),s,t))
    return sorted(options)

@lru_cache(10000)
def tagged(s):
    mol = Chem.MolFromSmiles(s)
    [d] = [a for a in mol.GetAtoms() if not a.GetAtomicNum()]
    d.SetAtomMapNum(999)
    return mol

def join(left, right):
    # RDKit molzip preserves tetrahedral neighbor permutations at the splice.
    mol = Chem.molzip(tagged(left), tagged(right))
    Chem.SanitizeMol(mol)
    return smiles(mol)

fp = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
def features(s):
    m = Chem.MolFromSmiles(s)
    ds = [Crippen.MolLogP, Descriptors.MolWt, Descriptors.TPSA, Lipinski.HeavyAtomCount,
          Lipinski.NumHAcceptors,Lipinski.NumHDonors,Lipinski.NumRotatableBonds,
          Lipinski.RingCount, Lipinski.FractionCSP3, Crippen.MolMR]
    return np.r_[np.log1p(fp.GetCountFingerprintAsNumPy(m)), [d(m) for d in ds]].astype("f4")
