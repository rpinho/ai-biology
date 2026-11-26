"""Execute the sealed TDC ADMET empirical benchmark of SynFactor CP16 (SEALED.md)."""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from chemistry_utils import (
    brics_one_cut,
    featurize_smiles,
    generate_cartesian_pairs,
    make_random_split,
    make_scaffold_split,
    standardize_dataset,
)
from models import (
    fit_additive_id_ridge,
    fit_lgbm_teacher,
    fit_synthon_neural,
    predict_lgbm_scores,
)
from stats_utils import (
    bootstrap_metric,
    evaluate_predictions_suite,
    paired_comparison,
    valid_stratum,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
SEEDS = (42, 43, 44)


def verify_data_manifest() -> dict[str, Any]:
    manifest = json.loads((DATA_DIR / "manifest.json").read_text())
    for key, info in manifest.items():
        path = DATA_DIR / info["filename"]
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset file: {path}")
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        if h != info["sha256"]:
            raise ValueError(f"SHA-256 mismatch for {path}: got {h}, expected {info['sha256']}")
    return manifest


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40.0, 40.0)))


def _build_synthon_table(
    df_list: list[pd.DataFrame],
) -> tuple[np.ndarray, dict[str, int], list[np.ndarray]]:
    """Build unique capped-synthon embedding table and [N, 3] tuple index arrays."""
    unique_synthons = sorted(
        set().union(*(set(d["capped_0"]).union(set(d["capped_1"])) for d in df_list if len(d) > 0))
    )
    smi_to_idx = {s: i for i, s in enumerate(unique_synthons)}
    emb = featurize_smiles(unique_synthons)
    tuple_arrays = []
    for d in df_list:
        if len(d) == 0:
            tuple_arrays.append(np.zeros((0, 3), dtype=np.int64))
            continue
        arr = np.full((len(d), 3), -1, dtype=np.int64)
        arr[:, 0] = [smi_to_idx[s] for s in d["capped_0"]]
        arr[:, 1] = [smi_to_idx[s] for s in d["capped_1"]]
        tuple_arrays.append(arr)
    return emb, smi_to_idx, tuple_arrays


def _train_3seed_neural(
    arch: str,
    x_emb: np.ndarray,
    tuples_tr: np.ndarray,
    y_tr: np.ndarray,
    tuples_va: np.ndarray,
    y_va: np.ndarray,
    tuples_te: np.ndarray,
    loss_mode: str,
    task: str,
) -> tuple[np.ndarray, list[np.ndarray], list[dict[str, Any]]]:
    """Train 3 seeds (42, 43, 44); return ensemble mean prediction, per-seed list, and logs."""
    seed_preds = []
    logs = []
    for seed in SEEDS:
        raw, info = fit_synthon_neural(
            arch=arch,
            x_emb=x_emb,
            tuples_tr=tuples_tr,
            y_tr=y_tr,
            tuples_va=tuples_va,
            y_va=y_va,
            tuples_eval=tuples_te,
            loss_mode=loss_mode,
            seed=seed,
        )
        # Convert logits to probabilities for classification ensemble averaging if BCE
        if task == "classification" and loss_mode == "bce":
            pred = _sigmoid(raw)
        else:
            pred = raw
        seed_preds.append(pred)
        logs.append({"seed": seed, **info})
    ens = np.mean(np.stack(seed_preds, axis=0), axis=0)
    return ens, seed_preds, logs


def run_endpoint_split(
    key: str,
    task: str,
    clean_df: pd.DataFrame,
    decomp_df: pd.DataFrame,
    X_clean_full: np.ndarray,
    X_decomp_full: np.ndarray,
    split_name: str,
) -> dict[str, Any]:
    t0 = time.perf_counter()

    # 1. Compute split on decomposable molecules
    if split_name == "scaffold":
        split = make_scaffold_split(decomp_df["smiles"].to_numpy())
        split_all = make_scaffold_split(clean_df["smiles"].to_numpy())
    elif split_name == "random":
        split = make_random_split(
            decomp_df["smiles"].to_numpy(), decomp_df["Y"].to_numpy(), task=task, seed=42
        )
        split_all = make_random_split(
            clean_df["smiles"].to_numpy(), clean_df["Y"].to_numpy(), task=task, seed=42
        )
    else:
        raise ValueError(f"Unknown split_name: {split_name}")

    tr_mask = split == "train"
    va_mask = split == "validation"
    te_mask = split == "test"

    y_all = decomp_df["Y"].to_numpy(dtype=np.float64)
    y_tr, y_va, y_te = y_all[tr_mask], y_all[va_mask], y_all[te_mask]

    # Audit coverage selection bias: FullMol-LGBM on all N_clean molecules
    y_clean = clean_df["Y"].to_numpy(dtype=np.float64)
    lgbm_clean = fit_lgbm_teacher(
        X_clean_full[split_all == "train"],
        y_clean[split_all == "train"],
        X_clean_full[split_all == "validation"],
        y_clean[split_all == "validation"],
        task=task,
        seed=42,
    )
    clean_eval_pred, _ = predict_lgbm_scores(lgbm_clean, X_clean_full[split_all == "test"], task)
    clean_primary = "auroc" if task == "classification" else "spearman"
    clean_audit = {
        "n_clean_test": int(np.sum(split_all == "test")),
        clean_primary: bootstrap_metric(
            y_clean[split_all == "test"], clean_eval_pred, clean_primary
        ),
    }

    # 2. Synthon overlap statistics on decomposable test split
    tr_df = decomp_df.iloc[np.flatnonzero(tr_mask)].reset_index(drop=True)
    te_df = decomp_df.iloc[np.flatnonzero(te_mask)].reset_index(drop=True)

    train_slot0 = set(tr_df["capped_0"])
    train_slot1 = set(tr_df["capped_1"])
    train_any_slot = train_slot0.union(train_slot1)

    s0_seen = np.array([s in train_slot0 for s in te_df["capped_0"]], dtype=bool)
    s1_seen = np.array([s in train_slot1 for s in te_df["capped_1"]], dtype=bool)
    both_seen = s0_seen & s1_seen
    one_seen = s0_seen ^ s1_seen
    neither_seen = (~s0_seen) & (~s1_seen)
    unseen_any = ~both_seen

    any0_seen = np.array([s in train_any_slot for s in te_df["capped_0"]], dtype=bool)
    any1_seen = np.array([s in train_any_slot for s in te_df["capped_1"]], dtype=bool)
    both_seen_any_slot = any0_seen & any1_seen

    overlap_stats = {
        "n_train": int(tr_mask.sum()),
        "n_val": int(va_mask.sum()),
        "n_test": int(te_mask.sum()),
        "unique_train_slot0": int(len(train_slot0)),
        "unique_train_slot1": int(len(train_slot1)),
        "both_seen_n": int(both_seen.sum()),
        "both_seen_pct": float(100.0 * both_seen.mean()),
        "one_seen_n": int(one_seen.sum()),
        "one_seen_pct": float(100.0 * one_seen.mean()),
        "neither_seen_n": int(neither_seen.sum()),
        "neither_seen_pct": float(100.0 * neither_seen.mean()),
        "unseen_any_n": int(unseen_any.sum()),
        "unseen_any_pct": float(100.0 * unseen_any.mean()),
        "both_seen_any_slot_n": int(both_seen_any_slot.sum()),
        "both_seen_any_slot_pct": float(100.0 * both_seen_any_slot.mean()),
    }

    # 3. Model 1: FullMol-LGBM teacher/baseline on decomposable molecules
    print(f"    [{key}/{split_name}] fitting FullMol-LGBM teacher ({time.perf_counter()-t0:.1f}s)...", flush=True)
    teacher = fit_lgbm_teacher(
        X_decomp_full[tr_mask], y_tr, X_decomp_full[va_mask], y_va, task=task, seed=42
    )
    teacher_eval_all, teacher_distill_all = predict_lgbm_scores(teacher, X_decomp_full, task)
    teacher_eval_te = teacher_eval_all[te_mask]
    teacher_distill_tr = teacher_distill_all[tr_mask]
    teacher_distill_va = teacher_distill_all[va_mask]
    teacher_distill_te = teacher_distill_all[te_mask]

    # 4. Synthetic train-only BRICS Cartesian pairs for distillation (strictly leak-free)
    forbidden = set(decomp_df["smiles"]).union(set(clean_df["smiles"]))
    max_cart = min(20000, 5 * int(tr_mask.sum()))
    cart_df = generate_cartesian_pairs(tr_df, forbidden_smiles=forbidden, max_pairs=max_cart, seed=42)
    print(
        f"    [{key}/{split_name}] Cartesian pairs={len(cart_df)} ({time.perf_counter()-t0:.1f}s)",
        flush=True,
    )
    if len(cart_df) > 0:
        X_cart_full = featurize_smiles(cart_df["smiles"].tolist())
        _, cart_teacher_distill = predict_lgbm_scores(teacher, X_cart_full, task)
    else:
        cart_teacher_distill = np.zeros((0,), dtype=np.float64)

    # 5. Build shared capped-synthon embedding table across decomp_df + cart_df
    x_syn_emb, _, [tuples_decomp, tuples_cart] = _build_synthon_table([decomp_df, cart_df])
    tuples_tr = tuples_decomp[tr_mask]
    tuples_va = tuples_decomp[va_mask]
    tuples_te = tuples_decomp[te_mask]

    tuples_tr_cart = np.concatenate([tuples_tr, tuples_cart], axis=0)
    y_tr_cart_distill = np.concatenate([teacher_distill_tr, cart_teacher_distill], axis=0)

    # 6. Model 2b: Exact synfactor/experiments/compare.py Ridge ID Additive control
    add_id_direct_all, add_id_direct_info = fit_additive_id_ridge(y_all, tuples_decomp, split)
    add_id_distill_all, add_id_distill_info = fit_additive_id_ridge(
        teacher_distill_all, tuples_decomp, split
    )

    # 7. Train Neural models (3 seeds each)
    direct_loss = "bce" if task == "classification" else "huber"

    print(f"    [{key}/{split_name}] training neural Direct models ({time.perf_counter()-t0:.1f}s)...", flush=True)
    add_direct_ens, add_direct_seeds, add_direct_logs = _train_3seed_neural(
        "additive", x_syn_emb, tuples_tr, y_tr, tuples_va, y_va, tuples_te, direct_loss, task
    )
    cp16_direct_ens, cp16_direct_seeds, cp16_direct_logs = _train_3seed_neural(
        "cp16", x_syn_emb, tuples_tr, y_tr, tuples_va, y_va, tuples_te, direct_loss, task
    )

    # Distillation on train split only (Huber on continuous teacher targets; val MSE on teacher val predictions)
    print(f"    [{key}/{split_name}] training neural Distilled-Train models ({time.perf_counter()-t0:.1f}s)...", flush=True)
    add_dist_tr_ens, add_dist_tr_seeds, add_dist_tr_logs = _train_3seed_neural(
        "additive",
        x_syn_emb,
        tuples_tr,
        teacher_distill_tr,
        tuples_va,
        teacher_distill_va,
        tuples_te,
        "huber",
        task,
    )
    cp16_dist_tr_ens, cp16_dist_tr_seeds, cp16_dist_tr_logs = _train_3seed_neural(
        "cp16",
        x_syn_emb,
        tuples_tr,
        teacher_distill_tr,
        tuples_va,
        teacher_distill_va,
        tuples_te,
        "huber",
        task,
    )

    # Distillation on train + synthetic train-only Cartesian pairs
    print(f"    [{key}/{split_name}] training neural Distilled-Cartesian models ({len(tuples_tr_cart)} rows, {time.perf_counter()-t0:.1f}s)...", flush=True)
    add_dist_cart_ens, add_dist_cart_seeds, add_dist_cart_logs = _train_3seed_neural(
        "additive",
        x_syn_emb,
        tuples_tr_cart,
        y_tr_cart_distill,
        tuples_va,
        teacher_distill_va,
        tuples_te,
        "huber",
        task,
    )
    cp16_dist_cart_ens, cp16_dist_cart_seeds, cp16_dist_cart_logs = _train_3seed_neural(
        "cp16",
        x_syn_emb,
        tuples_tr_cart,
        y_tr_cart_distill,
        tuples_va,
        teacher_distill_va,
        tuples_te,
        "huber",
        task,
    )
    print(f"    [{key}/{split_name}] evaluating metrics & paired tests ({time.perf_counter()-t0:.1f}s)...", flush=True)

    # Convert distilled logit scores to probabilities for classification (monotonic, preserves AUROC/Spearman)
    def _to_eval(arr: np.ndarray) -> np.ndarray:
        return _sigmoid(arr) if task == "classification" else arr

    preds_test_eval = {
        "FullMol-LGBM": teacher_eval_te,
        "Additive-ID-Direct": add_id_direct_all[te_mask],
        "Additive-ID-Distilled": _to_eval(add_id_distill_all[te_mask]),
        "Additive-Direct": add_direct_ens,
        "CP16-Direct": cp16_direct_ens,
        "Additive-Distilled-Train": _to_eval(add_dist_tr_ens),
        "CP16-Distilled-Train": _to_eval(cp16_dist_tr_ens),
        "Additive-Distilled-Cartesian": _to_eval(add_dist_cart_ens),
        "CP16-Distilled-Cartesian": _to_eval(cp16_dist_cart_ens),
    }

    preds_test_raw_distill = {
        "Additive-ID-Distilled": add_id_distill_all[te_mask],
        "Additive-Distilled-Train": add_dist_tr_ens,
        "CP16-Distilled-Train": cp16_dist_tr_ens,
        "Additive-Distilled-Cartesian": add_dist_cart_ens,
        "CP16-Distilled-Cartesian": cp16_dist_cart_ens,
    }

    # Per-seed summary for neural models (mean +/- sd across seeds 42, 43, 44)
    primary_metric = "auroc" if task == "classification" else "spearman"
    per_seed_map = {
        "Additive-Direct": add_direct_seeds,
        "CP16-Direct": cp16_direct_seeds,
        "Additive-Distilled-Train": [_to_eval(p) for p in add_dist_tr_seeds],
        "CP16-Distilled-Train": [_to_eval(p) for p in cp16_dist_tr_seeds],
        "Additive-Distilled-Cartesian": [_to_eval(p) for p in add_dist_cart_seeds],
        "CP16-Distilled-Cartesian": [_to_eval(p) for p in cp16_dist_cart_seeds],
    }
    from stats_utils import _metric_val

    per_seed_stats = {}
    for mname, slist in per_seed_map.items():
        vals = [_metric_val(y_te, p, primary_metric) for p in slist]
        entry = {
            f"{primary_metric}_seeds": [float(v) for v in vals],
            f"{primary_metric}_mean": float(np.mean(vals)),
            f"{primary_metric}_sd": float(np.std(vals, ddof=1)),
        }
        if task == "regression":
            rmses = [_metric_val(y_te, p, "rmse") for p in slist]
            entry["rmse_seeds"] = [float(v) for v in rmses]
            entry["rmse_mean"] = float(np.mean(rmses))
            entry["rmse_sd"] = float(np.std(rmses, ddof=1))
        per_seed_stats[mname] = entry

    # 8. Evaluate experimental metrics across strata (all, both_seen, unseen_any)
    strata_masks = {
        "all": np.ones(len(y_te), dtype=bool),
        "both_seen": both_seen,
        "unseen_any": unseen_any,
    }
    exp_metrics: dict[str, Any] = {}
    teacher_fidelity: dict[str, Any] = {}
    paired_tests: dict[str, Any] = {}

    for sname, smask in strata_masks.items():
        n_s = int(smask.sum())
        if not valid_stratum(y_te[smask], task):
            exp_metrics[sname] = {"n": n_s, "status": f"N/A (n={n_s})"}
            teacher_fidelity[sname] = {"n": n_s, "status": f"N/A (n={n_s})"}
            paired_tests[sname] = {"n": n_s, "status": f"N/A (n={n_s})"}
            continue

        yt_s = y_te[smask]
        sub_preds = {k: v[smask] for k, v in preds_test_eval.items()}
        exp_metrics[sname] = {
            "n": n_s,
            "models": evaluate_predictions_suite(yt_s, sub_preds, task=task),
        }

        # Teacher fidelity (student vs FullMol-LGBM continuous teacher target)
        tf_dict = {}
        t_ref = teacher_distill_te[smask]
        for mname, raw_p in preds_test_raw_distill.items():
            tf_dict[mname] = {
                "spearman": bootstrap_metric(t_ref, raw_p[smask], "spearman"),
                "pearson": bootstrap_metric(t_ref, raw_p[smask], "pearson"),
                "rmse": bootstrap_metric(t_ref, raw_p[smask], "rmse"),
            }
        teacher_fidelity[sname] = {"n": n_s, "models": tf_dict}

        # Paired tests
        cmp_metrics = ["auroc", "auprc"] if task == "classification" else ["spearman", "rmse", "mae"]
        pt = {}
        pairs_exp = [
            ("CP16-Direct_vs_Additive-Direct", "CP16-Direct", "Additive-Direct"),
            (
                "CP16-Distilled-Train_vs_Additive-Distilled-Train",
                "CP16-Distilled-Train",
                "Additive-Distilled-Train",
            ),
            (
                "CP16-Distilled-Cartesian_vs_Additive-Distilled-Cartesian",
                "CP16-Distilled-Cartesian",
                "Additive-Distilled-Cartesian",
            ),
            (
                "CP16-Distilled-Cartesian_vs_CP16-Direct",
                "CP16-Distilled-Cartesian",
                "CP16-Direct",
            ),
            (
                "CP16-Distilled-Cartesian_vs_FullMol-LGBM",
                "CP16-Distilled-Cartesian",
                "FullMol-LGBM",
            ),
            (
                "CP16-Direct_vs_FullMol-LGBM",
                "CP16-Direct",
                "FullMol-LGBM",
            ),
            (
                "CP16-Direct_vs_Additive-ID-Direct",
                "CP16-Direct",
                "Additive-ID-Direct",
            ),
        ]
        for label, ma, mb in pairs_exp:
            pt[label] = {
                m: paired_comparison(yt_s, sub_preds[ma], sub_preds[mb], m) for m in cmp_metrics
            }
        # Teacher fidelity paired comparison (CP16 vs Additive on teacher scores)
        pt["teacher_fidelity_CP16-Distilled-Cartesian_vs_Additive-Distilled-Cartesian"] = {
            "spearman": paired_comparison(
                t_ref,
                preds_test_raw_distill["CP16-Distilled-Cartesian"][smask],
                preds_test_raw_distill["Additive-Distilled-Cartesian"][smask],
                "spearman",
            ),
            "rmse": paired_comparison(
                t_ref,
                preds_test_raw_distill["CP16-Distilled-Cartesian"][smask],
                preds_test_raw_distill["Additive-Distilled-Cartesian"][smask],
                "rmse",
            ),
        }
        pt["teacher_fidelity_CP16-Distilled-Train_vs_Additive-Distilled-Train"] = {
            "spearman": paired_comparison(
                t_ref,
                preds_test_raw_distill["CP16-Distilled-Train"][smask],
                preds_test_raw_distill["Additive-Distilled-Train"][smask],
                "spearman",
            ),
        }
        paired_tests[sname] = {"n": n_s, "comparisons": pt}

    # Save test predictions CSV for independent referee verification
    pred_df = te_df[["smiles", "Y", "btype_0", "capped_0", "btype_1", "capped_1"]].copy()
    pred_df["both_seen"] = both_seen
    pred_df["one_seen"] = one_seen
    pred_df["neither_seen"] = neither_seen
    pred_df["teacher_distill_target"] = teacher_distill_te
    for mname, arr in preds_test_eval.items():
        pred_df[f"pred_{mname}"] = arr
    for mname, arr in preds_test_raw_distill.items():
        pred_df[f"raw_{mname}"] = arr
    out_csv = RESULTS_DIR / f"test_preds_{key}_{split_name}.csv"
    pred_df.to_csv(out_csv, index=False)

    elapsed = time.perf_counter() - t0
    return {
        "endpoint": key,
        "split": split_name,
        "task": task,
        "elapsed_seconds": float(elapsed),
        "clean_fullmol_audit": clean_audit,
        "overlap": overlap_stats,
        "cartesian_synthetic_pairs": int(len(cart_df)),
        "lgbm_best_iteration": int(teacher.best_iteration_),
        "additive_id_direct_info": add_id_direct_info,
        "additive_id_distill_info": add_id_distill_info,
        "training_logs": {
            "Additive-Direct": add_direct_logs,
            "CP16-Direct": cp16_direct_logs,
            "Additive-Distilled-Train": add_dist_tr_logs,
            "CP16-Distilled-Train": cp16_dist_tr_logs,
            "Additive-Distilled-Cartesian": add_dist_cart_logs,
            "CP16-Distilled-Cartesian": cp16_dist_cart_logs,
        },
        "per_seed_stats": per_seed_stats,
        "experimental_metrics": exp_metrics,
        "teacher_fidelity": teacher_fidelity,
        "paired_tests": paired_tests,
        "predictions_csv": str(out_csv.relative_to(ROOT)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--endpoints",
        nargs="+",
        default=["herg", "lipophilicity_astrazeneca", "solubility_aqsoldb", "cyp3a4_veith"],
    )
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest = verify_data_manifest()

    overall_start = time.perf_counter()
    summary: dict[str, Any] = {
        "synfactor_commit": "1eaee90610d1a54654c0ec22544154676df4f8fa",
        "sealed_protocol_commit": "ee30be763e5c800ddc5c47a62ecc1700231c7599",
        "endpoints": {},
    }

    for key in args.endpoints:
        info = manifest[key]
        task = info["task"]
        print(f"\n=== Endpoint: {info['tdc_name']} ({key}, {task}) ===", flush=True)
        raw_df = pd.read_csv(DATA_DIR / info["filename"], sep="\t")
        clean_df, std_stats = standardize_dataset(raw_df, task=task)

        # BRICS 1-cut decomposition
        decomp_records = []
        for idx, row in clean_df.iterrows():
            cut = brics_one_cut(row["smiles"])
            if cut is not None:
                decomp_records.append({"clean_idx": idx, "smiles": row["smiles"], "Y": row["Y"], **cut})
        decomp_df = pd.DataFrame(decomp_records)
        coverage_stats = {
            **std_stats,
            "n_decomp": int(len(decomp_df)),
            "n_nondecomp": int(len(clean_df) - len(decomp_df)),
            "coverage_pct": float(100.0 * len(decomp_df) / len(clean_df)),
        }
        print(
            f"  Standardized: {std_stats['n_clean']} / {std_stats['n_raw']} | "
            f"BRICS 1-cut coverage: {coverage_stats['n_decomp']} / {coverage_stats['n_clean']} "
            f"({coverage_stats['coverage_pct']:.2f}%)",
            flush=True,
        )

        # Featurize all clean molecules once
        X_clean_full = featurize_smiles(clean_df["smiles"].tolist())
        X_decomp_full = X_clean_full[decomp_df["clean_idx"].to_numpy(dtype=np.int64)]

        ep_result: dict[str, Any] = {
            "tdc_name": info["tdc_name"],
            "task": task,
            "data_sha256": info["sha256"],
            "coverage": coverage_stats,
            "splits": {},
        }

        for split_name in ("scaffold", "random"):
            print(f"  Running split={split_name} ...", flush=True)
            res = run_endpoint_split(
                key=key,
                task=task,
                clean_df=clean_df,
                decomp_df=decomp_df,
                X_clean_full=X_clean_full,
                X_decomp_full=X_decomp_full,
                split_name=split_name,
            )
            ep_result["splits"][split_name] = res
            # Per-split checkpoint flush
            (RESULTS_DIR / f"result_{key}.json").write_text(json.dumps(ep_result, indent=2) + "\n")
            all_m = res["experimental_metrics"]["all"]["models"]
            pm = "auroc" if task == "classification" else "spearman"
            print(
                f"    [{split_name}] {res['elapsed_seconds']:.1f}s | "
                f"both_seen={res['overlap']['both_seen_pct']:.1f}% | "
                f"cart={res['cartesian_synthetic_pairs']} | "
                f"FullMol={all_m['FullMol-LGBM'][pm]['point']:.4f} | "
                f"AddDir={all_m['Additive-Direct'][pm]['point']:.4f} | "
                f"CP16Dir={all_m['CP16-Direct'][pm]['point']:.4f} | "
                f"AddCart={all_m['Additive-Distilled-Cartesian'][pm]['point']:.4f} | "
                f"CP16Cart={all_m['CP16-Distilled-Cartesian'][pm]['point']:.4f}",
                flush=True,
            )

        summary["endpoints"][key] = ep_result

    # Peak RSS in MB (macOS ru_maxrss is in bytes)
    peak_rss_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
    summary["total_elapsed_seconds"] = float(time.perf_counter() - overall_start)
    summary["peak_rss_mb"] = float(peak_rss_mb)
    (RESULTS_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"\nALL DONE in {summary['total_elapsed_seconds']:.1f}s | Peak RSS: {peak_rss_mb:.1f} MB",
        flush=True,
    )


if __name__ == "__main__":
    main()
