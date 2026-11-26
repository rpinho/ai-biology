"""Isolated LightGBM worker subprocess (avoids macOS ARM64 dual-libomp conflict with PyTorch).

Never imports torch. Uses the exact locked LightGBM hyperparameters from SEALED.md (n_jobs=4).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import lightgbm as lgb
import numpy as np


def _fit(args: argparse.Namespace) -> None:
    data = np.load(args.input_npz, allow_pickle=False)
    X_tr = data["X_tr"]
    y_tr = data["y_tr"]
    X_va = data["X_va"]
    y_va = data["y_va"]
    task = args.task
    seed = args.seed

    common = dict(
        n_estimators=2000,
        learning_rate=0.03,
        num_leaves=31,
        min_child_samples=20,
        subsample=0.8,
        subsample_freq=1,
        colsample_bytree=0.5,
        reg_lambda=1.0,
        random_state=seed,
        n_jobs=4,
        verbose=-1,
    )
    if task == "classification":
        model = lgb.LGBMClassifier(objective="binary", **common)
        model.fit(
            X_tr,
            y_tr.astype(int),
            eval_set=[(X_va, y_va.astype(int))],
            eval_metric="binary_logloss",
            callbacks=[lgb.early_stopping(50, verbose=False)],
        )
    else:
        model = lgb.LGBMRegressor(objective="regression", **common)
        model.fit(
            X_tr,
            y_tr.astype(np.float64),
            eval_set=[(X_va, y_va.astype(np.float64))],
            eval_metric="rmse",
            callbacks=[lgb.early_stopping(50, verbose=False)],
        )

    Path(args.model_txt).write_text(model.booster_.model_to_string())
    out: dict[str, np.ndarray] = {"best_iteration": np.array(int(model.best_iteration_), dtype=np.int64)}
    if "X_eval" in data:
        X_eval = data["X_eval"]
        if task == "classification":
            out["eval_score"] = model.predict_proba(X_eval)[:, 1].astype(np.float64)
            out["distill_target"] = model.predict(X_eval, raw_score=True).astype(np.float64)
        else:
            preds = model.predict(X_eval).astype(np.float64)
            out["eval_score"] = preds
            out["distill_target"] = preds
    np.savez(args.output_npz, **out)


def _predict(args: argparse.Namespace) -> None:
    data = np.load(args.input_npz, allow_pickle=False)
    X = data["X"]
    best_iter = int(data["best_iteration"])
    booster = lgb.Booster(model_file=args.model_txt)
    if args.task == "classification":
        probs = booster.predict(X, num_iteration=best_iter).astype(np.float64)
        logits = booster.predict(X, raw_score=True, num_iteration=best_iter).astype(np.float64)
        np.savez(args.output_npz, eval_score=probs, distill_target=logits)
    else:
        preds = booster.predict(X, num_iteration=best_iter).astype(np.float64)
        np.savez(args.output_npz, eval_score=preds, distill_target=preds)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", choices=["fit", "predict"], required=True)
    p.add_argument("--task", choices=["classification", "regression"], required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--input-npz", required=True)
    p.add_argument("--output-npz", required=True)
    p.add_argument("--model-txt", required=True)
    args = p.parse_args()
    if args.mode == "fit":
        _fit(args)
    else:
        _predict(args)


if __name__ == "__main__":
    main()
