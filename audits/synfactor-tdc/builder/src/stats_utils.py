"""Statistical evaluation, bootstrap 95% CIs, and paired permutation tests (SEALED.md Sec. 5).

Vectorized implementations are mathematically equivalent (<1e-12) to scalar sklearn/scipy reference
functions, including exact tie handling for AUROC, AUPRC, and Spearman.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.stats import pearsonr, rankdata, spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score


def _metric_val(y_true: np.ndarray, y_pred: np.ndarray, metric_name: str) -> float:
    if metric_name == "auroc":
        return float(roc_auc_score(y_true, y_pred))
    if metric_name == "auprc":
        return float(average_precision_score(y_true, y_pred))
    if metric_name == "spearman":
        if np.std(y_true) == 0 or np.std(y_pred) == 0:
            return float("nan")
        return float(spearmanr(y_true, y_pred).statistic)
    if metric_name == "pearson":
        if np.std(y_true) == 0 or np.std(y_pred) == 0:
            return float("nan")
        return float(pearsonr(y_true, y_pred).statistic)
    if metric_name == "rmse":
        return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    if metric_name == "mae":
        return float(np.mean(np.abs(y_true - y_pred)))
    raise ValueError(f"Unknown metric: {metric_name}")


def _zscore(arr: np.ndarray) -> np.ndarray:
    s = float(np.std(arr))
    if s < 1e-12:
        return np.zeros_like(arr, dtype=np.float64)
    return (arr - float(np.mean(arr))) / s


def valid_stratum(y_true: np.ndarray, task: str, min_n: int = 20) -> bool:
    if len(y_true) < min_n:
        return False
    if task == "classification":
        n_pos = int(np.sum(y_true == 1))
        n_neg = int(np.sum(y_true == 0))
        return n_pos >= 2 and n_neg >= 2
    return float(np.std(y_true)) > 0


def _batch_auroc(Y: np.ndarray, S: np.ndarray) -> np.ndarray:
    """Exact vectorized AUROC for 2D (B, n) or broadcast 1D Y against (B, n) S, including ties."""
    ranks = rankdata(S, axis=1)
    if Y.ndim == 1:
        pos = Y == 1
        n1 = float(np.sum(pos))
        n0 = float(Y.shape[0] - n1)
        if n1 == 0 or n0 == 0:
            return np.full(S.shape[0], np.nan, dtype=np.float64)
        return (ranks[:, pos].sum(axis=1) - n1 * (n1 + 1.0) * 0.5) / (n1 * n0)
    pos = Y == 1
    n1 = pos.sum(axis=1).astype(np.float64)
    n0 = Y.shape[1] - n1
    valid = (n1 > 0) & (n0 > 0)
    out = np.full(S.shape[0], np.nan, dtype=np.float64)
    if np.any(valid):
        r_sum = np.sum(ranks[valid] * pos[valid], axis=1)
        n1v = n1[valid]
        out[valid] = (r_sum - n1v * (n1v + 1.0) * 0.5) / (n1v * n0[valid])
    return out


def _auprc_sorted_with_ties(y_sorted: np.ndarray, s_sorted: np.ndarray, n_pos: float) -> float:
    """Exact sklearn average_precision_score from descending-sorted arrays when ties are present."""
    n = len(y_sorted)
    distinct = np.flatnonzero(s_sorted[:-1] != s_sorted[1:])
    idx = np.empty(len(distinct) + 1, dtype=np.int64)
    idx[:-1] = distinct
    idx[-1] = n - 1
    tp = np.cumsum(y_sorted, dtype=np.float64)[idx]
    prec = tp / (idx + 1.0)
    dtp = np.empty_like(tp)
    dtp[0] = tp[0]
    if len(tp) > 1:
        dtp[1:] = tp[1:] - tp[:-1]
    return float(np.sum((dtp / n_pos) * prec))


def _batch_auprc(Y: np.ndarray, S: np.ndarray) -> np.ndarray:
    """Exact vectorized AUPRC for 1D or 2D Y and 2D (B, n) S, matching sklearn including ties."""
    bs, n = S.shape
    order = np.argsort(-S, axis=1)
    S_ord = np.take_along_axis(S, order, axis=1)
    if Y.ndim == 1:
        y_bin = (Y == 1).astype(np.float64)
        n_pos_scalar = float(y_bin.sum())
        if n_pos_scalar == 0 or n_pos_scalar == n:
            return np.full(bs, np.nan, dtype=np.float64)
        Y_ord = y_bin[order]
        n_pos = np.full(bs, n_pos_scalar, dtype=np.float64)
        valid = np.ones(bs, dtype=bool)
    else:
        Y_bin = (Y == 1).astype(np.float64)
        n_pos = Y_bin.sum(axis=1)
        valid = (n_pos > 0) & (n_pos < n)
        Y_ord = np.take_along_axis(Y_bin, order, axis=1)

    out = np.full(bs, np.nan, dtype=np.float64)
    if not np.any(valid):
        return out

    has_tie = np.any(S_ord[:, :-1] == S_ord[:, 1:], axis=1)
    fast = valid & (~has_tie)
    if np.any(fast):
        Yf = Y_ord[fast]
        tp = np.cumsum(Yf, axis=1)
        denom = np.arange(1, n + 1, dtype=np.float64)
        out[fast] = np.sum((tp / denom) * Yf, axis=1) / n_pos[fast]

    slow = np.flatnonzero(valid & has_tie)
    for i in slow:
        out[i] = _auprc_sorted_with_ties(Y_ord[i], S_ord[i], float(n_pos[i]))
    return out


def _batch_pearson(Y: np.ndarray, S: np.ndarray) -> np.ndarray:
    """Exact vectorized Pearson correlation for 1D or 2D Y and 2D (B, n) S."""
    S_c = S - S.mean(axis=1, keepdims=True)
    S_norm = np.linalg.norm(S_c, axis=1)
    if Y.ndim == 1:
        y_c = Y - Y.mean()
        y_norm = float(np.linalg.norm(y_c))
        if y_norm == 0.0:
            return np.full(S.shape[0], np.nan, dtype=np.float64)
        denom = y_norm * S_norm
        out = np.full(S.shape[0], np.nan, dtype=np.float64)
        ok = denom > 0
        out[ok] = (S_c[ok] @ y_c) / denom[ok]
        return out
    Y_c = Y - Y.mean(axis=1, keepdims=True)
    Y_norm = np.linalg.norm(Y_c, axis=1)
    denom = Y_norm * S_norm
    out = np.full(S.shape[0], np.nan, dtype=np.float64)
    ok = denom > 0
    out[ok] = np.sum(Y_c[ok] * S_c[ok], axis=1) / denom[ok]
    return out


def _batch_spearman(Y: np.ndarray, S: np.ndarray) -> np.ndarray:
    """Exact vectorized Spearman correlation (average ranks for ties) for 1D or 2D Y and (B, n) S."""
    RS = rankdata(S, axis=1)
    RY = rankdata(Y) if Y.ndim == 1 else rankdata(Y, axis=1)
    return _batch_pearson(RY, RS)


def _batch_metric(Y: np.ndarray, S: np.ndarray, metric_name: str) -> np.ndarray:
    if metric_name == "auroc":
        return _batch_auroc(Y, S)
    if metric_name == "auprc":
        return _batch_auprc(Y, S)
    if metric_name == "spearman":
        return _batch_spearman(Y, S)
    if metric_name == "pearson":
        return _batch_pearson(Y, S)
    if metric_name == "rmse":
        return np.sqrt(np.mean((Y - S) ** 2, axis=1))
    if metric_name == "mae":
        return np.mean(np.abs(Y - S), axis=1)
    raise ValueError(f"Unknown metric: {metric_name}")


def bootstrap_metric(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metric_name: str,
    n_boot: int = 2000,
    seed: int = 20261124,
) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    point = _metric_val(y_true, y_pred, metric_name)
    rng = np.random.default_rng(seed)
    n = len(y_true)
    vals_chunks = []
    batch_size = 500
    for start in range(0, n_boot, batch_size):
        bs = min(batch_size, n_boot - start)
        idx = rng.integers(0, n, size=(bs, n))
        v = _batch_metric(y_true[idx], y_pred[idx], metric_name)
        vals_chunks.append(v[np.isfinite(v)])
    vals = np.concatenate(vals_chunks)
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return {"point": float(point), "ci_low": float(lo), "ci_high": float(hi)}


def paired_comparison(
    y_true: np.ndarray,
    pred_a: np.ndarray,
    pred_b: np.ndarray,
    metric_name: str,
    n_boot: int = 2000,
    n_perm: int = 10000,
    seed: int = 20261124,
) -> dict[str, Any]:
    """Compare pred_a - pred_b with paired bootstrap 95% CI and two-sided paired permutation p-value."""
    y_true = np.asarray(y_true, dtype=np.float64)
    pred_a = np.asarray(pred_a, dtype=np.float64)
    pred_b = np.asarray(pred_b, dtype=np.float64)

    val_a = _metric_val(y_true, pred_a, metric_name)
    val_b = _metric_val(y_true, pred_b, metric_name)
    delta_obs = float(val_a - val_b)

    rng = np.random.default_rng(seed)
    n = len(y_true)
    batch_size = 500

    # Paired bootstrap CI for delta
    delta_chunks = []
    for start in range(0, n_boot, batch_size):
        bs = min(batch_size, n_boot - start)
        idx = rng.integers(0, n, size=(bs, n))
        yt = y_true[idx]
        da = _batch_metric(yt, pred_a[idx], metric_name)
        db = _batch_metric(yt, pred_b[idx], metric_name)
        ok = np.isfinite(da) & np.isfinite(db)
        delta_chunks.append(da[ok] - db[ok])
    boot_deltas = np.concatenate(delta_chunks)
    ci_low, ci_high = np.percentile(boot_deltas, [2.5, 97.5])

    # Two-sided paired permutation test
    # For rank metrics (auroc, auprc, spearman, pearson), z-score predictions before swapping
    # so swaps test rank-order differences rather than arbitrary offset/scale shifts.
    if metric_name in ("auroc", "auprc", "spearman", "pearson"):
        pa = _zscore(pred_a)
        pb = _zscore(pred_b)
    else:
        pa = pred_a
        pb = pred_b

    rng_p = np.random.default_rng(seed + 1)
    extreme = 0
    abs_obs = abs(delta_obs)

    if metric_name == "rmse":
        err_a2 = (y_true - pa) ** 2
        err_b2 = (y_true - pb) ** 2
        for start in range(0, n_perm, 1000):
            bs = min(1000, n_perm - start)
            swap = rng_p.random((bs, n)) < 0.5
            ea = np.where(swap, err_b2, err_a2)
            eb = np.where(swap, err_a2, err_b2)
            d = np.sqrt(ea.mean(axis=1)) - np.sqrt(eb.mean(axis=1))
            extreme += int(np.sum(np.abs(d) >= abs_obs - 1e-15))
    elif metric_name == "mae":
        err_a = np.abs(y_true - pa)
        err_b = np.abs(y_true - pb)
        for start in range(0, n_perm, 1000):
            bs = min(1000, n_perm - start)
            swap = rng_p.random((bs, n)) < 0.5
            ea = np.where(swap, err_b, err_a)
            eb = np.where(swap, err_a, err_b)
            d = ea.mean(axis=1) - eb.mean(axis=1)
            extreme += int(np.sum(np.abs(d) >= abs_obs - 1e-15))
    elif metric_name == "spearman":
        ry = rankdata(y_true)
        ry_c = ry - ry.mean()
        ry_norm = float(np.linalg.norm(ry_c))
        for start in range(0, n_perm, batch_size):
            bs = min(batch_size, n_perm - start)
            swap = rng_p.random((bs, n)) < 0.5
            sa = np.where(swap, pb, pa)
            sb = np.where(swap, pa, pb)
            ra = rankdata(sa, axis=1)
            ra -= ra.mean(axis=1, keepdims=True)
            rb = rankdata(sb, axis=1)
            rb -= rb.mean(axis=1, keepdims=True)
            na = np.linalg.norm(ra, axis=1)
            nb = np.linalg.norm(rb, axis=1)
            da = np.where(na > 0, (ra @ ry_c) / np.where(na > 0, ry_norm * na, 1.0), np.nan)
            db = np.where(nb > 0, (rb @ ry_c) / np.where(nb > 0, ry_norm * nb, 1.0), np.nan)
            d = da - db
            extreme += int(np.sum(np.isfinite(d) & (np.abs(d) >= abs_obs - 1e-15)))
    else:
        # Vectorized exact permutation for auroc, auprc, pearson
        for start in range(0, n_perm, batch_size):
            bs = min(batch_size, n_perm - start)
            swap = rng_p.random((bs, n)) < 0.5
            sa = np.where(swap, pb, pa)
            sb = np.where(swap, pa, pb)
            da = _batch_metric(y_true, sa, metric_name)
            db = _batch_metric(y_true, sb, metric_name)
            d = da - db
            extreme += int(np.sum(np.isfinite(d) & (np.abs(d) >= abs_obs - 1e-15)))

    p_perm = float((1 + extreme) / (1 + n_perm))
    return {
        "metric": metric_name,
        "val_a": float(val_a),
        "val_b": float(val_b),
        "delta": float(delta_obs),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "p_perm": p_perm,
    }


def evaluate_predictions_suite(
    y_true: np.ndarray,
    preds_dict: dict[str, np.ndarray],
    task: str,
    n_boot: int = 2000,
    seed: int = 20261124,
) -> dict[str, Any]:
    metrics_list = ["auroc", "auprc"] if task == "classification" else ["spearman", "rmse", "mae"]
    out = {}
    for model_name, pred in preds_dict.items():
        out[model_name] = {
            m: bootstrap_metric(y_true, pred, m, n_boot=n_boot, seed=seed) for m in metrics_list
        }
    return out
