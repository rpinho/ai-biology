"""Locked model definitions: FullMol-LGBM, SynFactor CP16 (imported directly), Neural Additive, and Ridge ID Additive."""

from __future__ import annotations

import copy
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn

# Import SynFactor directly from the cloned repository
SYNFACTOR_DIR = Path(__file__).resolve().parents[1] / "synfactor"
if str(SYNFACTOR_DIR) not in sys.path:
    sys.path.insert(0, str(SYNFACTOR_DIR))
from model import SynFactor  # noqa: E402

LGBM_WORKER = Path(__file__).with_name("lgbm_worker.py")


@dataclass
class IsolatedLGBMTeacher:
    """LightGBM teacher trained in an isolated subprocess (prevents dual-libomp deadlock with PyTorch)."""

    task: str
    best_iteration_: int
    model_str: str


class NeuralAdditiveSynthon(nn.Module):
    """Representation-matched additive synthon control with identical trunk to SynFactor."""

    def __init__(self, input_dim: int, tasks: int = 1, hidden: int = 64):
        super().__init__()
        self.tasks = tasks
        self.trunk = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.GELU(),
            nn.LayerNorm(hidden),
            nn.Dropout(0.1),
            nn.Linear(hidden, hidden),
            nn.GELU(),
        )
        self.heads = nn.ModuleList([nn.Linear(hidden, tasks) for _ in range(3)])
        self.output_scale = nn.Parameter(torch.ones(tasks))
        self.output_bias = nn.Parameter(torch.zeros(tasks))
        self.register_buffer("x_mean", torch.zeros(input_dim))
        self.register_buffer("x_scale", torch.ones(input_dim))
        self.register_buffer("y_mean", torch.zeros(tasks))
        self.register_buffer("y_scale", torch.ones(tasks))

    def slot_score(self, embeddings: torch.Tensor, slot: int) -> torch.Tensor:
        x = ((embeddings - self.x_mean) / self.x_scale).clamp(-8, 8)
        return self.heads[slot](self.trunk(x))

    def forward(self, components: torch.Tensor, present: torch.Tensor) -> torch.Tensor:
        s0 = self.slot_score(components[:, 0], 0)
        s1 = self.slot_score(components[:, 1], 1)
        total = s0 + s1
        if present[:, 2].any():
            s2 = self.slot_score(components[:, 2], 2)
            total = total + torch.where(present[:, 2, None], s2, 0.0)
        return (total * self.output_scale + self.output_bias) * self.y_scale + self.y_mean


def fit_lgbm_teacher(
    X_tr: np.ndarray,
    y_tr: np.ndarray,
    X_va: np.ndarray,
    y_va: np.ndarray,
    task: str,
    seed: int = 42,
) -> IsolatedLGBMTeacher:
    """Fit locked FullMol-LGBM teacher/baseline in an isolated subprocess (exact n_jobs=4)."""
    with tempfile.TemporaryDirectory(prefix="lgbm_fit_") as tmp:
        tmp_dir = Path(tmp)
        in_npz = tmp_dir / "in.npz"
        out_npz = tmp_dir / "out.npz"
        model_txt = tmp_dir / "model.txt"
        np.savez(in_npz, X_tr=X_tr, y_tr=y_tr, X_va=X_va, y_va=y_va)
        subprocess.run(
            [
                sys.executable,
                str(LGBM_WORKER),
                "--mode",
                "fit",
                "--task",
                task,
                "--seed",
                str(seed),
                "--input-npz",
                str(in_npz),
                "--output-npz",
                str(out_npz),
                "--model-txt",
                str(model_txt),
            ],
            check=True,
        )
        res = np.load(out_npz, allow_pickle=False)
        best_iter = int(res["best_iteration"])
        model_str = model_txt.read_text()
    return IsolatedLGBMTeacher(task=task, best_iteration_=best_iter, model_str=model_str)


def predict_lgbm_scores(
    model: IsolatedLGBMTeacher, X: np.ndarray, task: str
) -> tuple[np.ndarray, np.ndarray]:
    """Return (eval_score, distill_target) via isolated LightGBM subprocess.

    For classification: eval_score = probability of class 1, distill_target = raw log-odds.
    For regression: both are continuous predictions.
    """
    with tempfile.TemporaryDirectory(prefix="lgbm_pred_") as tmp:
        tmp_dir = Path(tmp)
        in_npz = tmp_dir / "in.npz"
        out_npz = tmp_dir / "out.npz"
        model_txt = tmp_dir / "model.txt"
        model_txt.write_text(model.model_str)
        np.savez(in_npz, X=X, best_iteration=np.array(model.best_iteration_, dtype=np.int64))
        subprocess.run(
            [
                sys.executable,
                str(LGBM_WORKER),
                "--mode",
                "predict",
                "--task",
                task,
                "--input-npz",
                str(in_npz),
                "--output-npz",
                str(out_npz),
                "--model-txt",
                str(model_txt),
            ],
            check=True,
        )
        res = np.load(out_npz, allow_pickle=False)
        return res["eval_score"].astype(np.float64), res["distill_target"].astype(np.float64)


def fit_synthon_neural(
    arch: str,
    x_emb: np.ndarray,
    tuples_tr: np.ndarray,
    y_tr: np.ndarray,
    tuples_va: np.ndarray,
    y_va: np.ndarray,
    tuples_eval: np.ndarray,
    loss_mode: str,
    seed: int,
    rank: int = 16,
    hidden: int = 64,
    epochs: int = 300,
    patience: int = 35,
    batch_size: int = 256,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Train SynFactor (cp16) or NeuralAdditiveSynthon (additive) with SynFactor's exact schedule.

    loss_mode: 'huber' (exact synfactor/train.py standardized Huber + val MSE) or 'bce' (BCEWithLogitsLoss).
    """
    torch.set_num_threads(4)
    torch.manual_seed(seed + (rank if arch == "cp16" else 0))

    x = torch.tensor(x_emb, dtype=torch.float32)
    t_tr = torch.tensor(tuples_tr, dtype=torch.long)
    p_tr = t_tr >= 0
    y_tr_t = torch.tensor(y_tr[:, None], dtype=torch.float32)

    t_va = torch.tensor(tuples_va, dtype=torch.long)
    p_va = t_va >= 0
    y_va_t = torch.tensor(y_va[:, None], dtype=torch.float32)

    t_ev = torch.tensor(tuples_eval, dtype=torch.long)
    p_ev = t_ev >= 0

    if arch == "cp16":
        model = SynFactor(x.shape[1], tasks=1, rank=rank, hidden=hidden)
    elif arch == "additive":
        model = NeuralAdditiveSynthon(x.shape[1], tasks=1, hidden=hidden)
    else:
        raise ValueError(f"Unknown arch: {arch}")

    with torch.no_grad():
        occurrences = x[t_tr[p_tr]]
        model.x_mean.copy_(occurrences.mean(0))
        std = occurrences.std(0, correction=0)
        model.x_scale.copy_(torch.where(std > 1e-5, std, torch.ones_like(std)))
        if loss_mode == "huber":
            model.y_mean.copy_(y_tr_t.mean(0))
            model.y_scale.copy_(y_tr_t.std(0).clamp_min(1e-6))
        else:
            model.y_mean.zero_()
            model.y_scale.fill_(1.0)

    optimizer = torch.optim.AdamW(model.parameters(), lr=0.002, weight_decay=0.002)
    best, stale, best_epoch, state = float("inf"), 0, 0, None
    n_tr = len(t_tr)

    for epoch in range(epochs):
        model.train()
        perm = torch.randperm(n_tr)
        for ids in perm.split(batch_size):
            pred = model(x[t_tr[ids].clamp_min(0)], p_tr[ids])
            if loss_mode == "huber":
                loss = torch.nn.functional.huber_loss(
                    (pred - model.y_mean) / model.y_scale,
                    (y_tr_t[ids] - model.y_mean) / model.y_scale,
                )
            else:
                loss = torch.nn.functional.binary_cross_entropy_with_logits(pred, y_tr_t[ids])
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            optimizer.step()

        model.eval()
        with torch.no_grad():
            va_preds = []
            for start in range(0, len(t_va), 2048):
                sl = slice(start, start + 2048)
                va_preds.append(model(x[t_va[sl].clamp_min(0)], p_va[sl]))
            va_pred = torch.cat(va_preds, dim=0)
            if loss_mode == "huber":
                val_loss = (((va_pred - y_va_t) / model.y_scale) ** 2).mean().item()
            else:
                val_loss = torch.nn.functional.binary_cross_entropy_with_logits(
                    va_pred, y_va_t
                ).item()

        if val_loss < best - 1e-5:
            best, stale, best_epoch = val_loss, 0, epoch + 1
            state = copy.deepcopy(model.state_dict())
        else:
            stale += 1
        if stale >= patience:
            break

    if state is None:
        raise RuntimeError(f"Training did not produce finite validation loss ({arch}, seed={seed})")
    model.load_state_dict(state)
    model.eval()

    with torch.inference_mode():
        ev_preds = []
        for start in range(0, len(t_ev), 2048):
            sl = slice(start, start + 2048)
            ev_preds.append(model(x[t_ev[sl].clamp_min(0)], p_ev[sl]))
        raw_out = torch.cat(ev_preds, dim=0).squeeze(-1).cpu().numpy().astype(np.float64)

    return raw_out, {"best_epoch": int(best_epoch), "best_val_loss": float(best)}


def fit_additive_id_ridge(
    y: np.ndarray, tuples: np.ndarray, split: np.ndarray
) -> tuple[np.ndarray, dict[str, Any]]:
    """Exact train-only ridge slot-ID lookup from synfactor/experiments/compare.py:additive_fit.

    Uses sparse/dense design matrix over unique (slot, synthon_id) observed in train.
    Unseen synthons receive zero slot contribution -> global train mean + intercept.
    """
    train_mask = split == "train"
    val_mask = split == "validation"

    # Build slot-specific ID vocabulary from train only so unseen IDs get 0 weight
    vocab: dict[tuple[int, int], int] = {}
    for row in tuples[train_mask]:
        for slot in (0, 1):
            sid = int(row[slot])
            if sid >= 0 and (slot, sid) not in vocab:
                vocab[(slot, sid)] = len(vocab)

    n_cols = len(vocab) + 1  # last column is intercept
    n_rows = len(tuples)

    from scipy import sparse
    from scipy.sparse.linalg import lsqr

    rr, cc, vv = [], [], []
    for i, row in enumerate(tuples):
        for slot in (0, 1):
            col = vocab.get((slot, int(row[slot])))
            if col is not None:
                rr.append(i)
                cc.append(col)
                vv.append(1.0)
        rr.append(i)
        cc.append(n_cols - 1)
        vv.append(1.0)
    design = sparse.csr_matrix((vv, (rr, cc)), shape=(n_rows, n_cols), dtype=np.float64)

    mean = float(y[train_mask].mean())
    scale = float(max(y[train_mask].std(), 1e-6))
    y_tr_std = (y[train_mask] - mean) / scale
    y_va_std = (y[val_mask] - mean) / scale
    X_tr = design[train_mask]
    X_va = design[val_mask]

    best_loss = float("inf")
    chosen_penalty = None
    best_pred = None
    for penalty in (1e-6, 1e-3, 0.1, 1.0, 10.0):
        # Solve min ||X w - y||^2 + penalty * ||w||^2 via damped least squares
        sol = lsqr(X_tr, y_tr_std, damp=np.sqrt(penalty), atol=1e-10, btol=1e-10, iter_lim=5000)
        w = sol[0]
        pred_va = X_va @ w
        loss = float(np.mean((pred_va - y_va_std) ** 2))
        if loss < best_loss:
            best_loss = loss
            chosen_penalty = penalty
            best_pred = (design @ w) * scale + mean

    assert best_pred is not None
    return best_pred.astype(np.float64), {
        "ridge_penalty": float(chosen_penalty),
        "validation_nmse": float(best_loss),
        "n_train_slot_ids": int(len(vocab)),
    }
