"""Reproducible teaching exercises. This program does not diagnose or design a vaccine."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score, brier_score_loss, confusion_matrix,
    roc_auc_score, roc_curve,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 20261024
THRESHOLD = 0.5
C_GRID = [0.01, 0.1, 1.0, 10.0]


def divide(a: float, b: float) -> float:
    return float(a / b) if b else float("nan")


def json_safe(value):
    """Represent undefined metrics as null, never zero or nonstandard JSON NaN."""
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def wilson_interval(successes, trials, z=1.959963984540054):
    """95% binomial score interval; remains informative at zero observed errors."""
    if trials == 0:
        return {"lower": None, "upper": None, "numerator": int(successes), "denominator": 0}
    p = successes / trials
    denom = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denom
    half = z * np.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denom
    return {"lower": float(max(0, center - half)), "upper": float(min(1, center + half)),
            "numerator": int(successes), "denominator": int(trials)}


def proportion_intervals(m):
    tp, fn, tn, fp = (m[k] for k in ["true_positives", "false_negatives", "true_negatives", "false_positives"])
    pairs = {"sensitivity": (tp, tp + fn), "specificity": (tn, tn + fp),
             "positive_predictive_value": (tp, tp + fp),
             "negative_predictive_value": (tn, tn + fn), "accuracy": (tp + tn, m["n"])}
    return {"method": "95% Wilson binomial score intervals",
            "interpretation": "Internal holdout sampling uncertainty only; no training or population-shift uncertainty.",
            "intervals": {k: wilson_interval(*v) for k, v in pairs.items()}}


def metrics(y: np.ndarray, p: np.ndarray, threshold: float = THRESHOLD) -> dict:
    """Class 1 means malignant. The threshold is fixed before holdout evaluation."""
    pred = (p >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "n": int(len(y)), "true_negatives": int(tn), "false_positives": int(fp),
        "false_negatives": int(fn), "true_positives": int(tp),
        "sensitivity": divide(tp, tp + fn), "specificity": divide(tn, tn + fp),
        "positive_predictive_value": divide(tp, tp + fp),
        "negative_predictive_value": divide(tn, tn + fn),
        "accuracy": float(np.mean(pred == y)),
        "roc_auc": float(roc_auc_score(y, p)),
        "average_precision": float(average_precision_score(y, p)),
        "brier_score": float(brier_score_loss(y, p)),
    }


def expected_screening_counts(prevalence, sensitivity, specificity, n=100_000):
    """Hypothetical expected counts, not measurements or WDBC-derived estimates."""
    for x in (prevalence, sensitivity, specificity):
        if not 0 <= x <= 1:
            raise ValueError("Probabilities must lie between zero and one")
    if n <= 0:
        raise ValueError("Population size must be positive")
    tp = n * prevalence * sensitivity
    fn = n * prevalence * (1 - sensitivity)
    fp = n * (1 - prevalence) * (1 - specificity)
    tn = n * (1 - prevalence) * specificity
    return dict(prevalence=prevalence, sensitivity=sensitivity, specificity=specificity,
                n=n, tp=tp, fn=fn, fp=fp, tn=tn,
                ppv=divide(tp, tp + fp), npv=divide(tn, tn + fn))


def bootstrap_intervals(y, p, repeats, rng):
    """Ordinary case bootstrap conditional on this fitted model and fixed split."""
    keys = ["roc_auc", "average_precision", "brier_score"]
    draws = {k: [] for k in keys}
    skipped = 0
    for _ in range(repeats):
        idx = rng.integers(0, len(y), size=len(y))
        if len(np.unique(y[idx])) < 2:
            skipped += 1
            continue
        sample = metrics(y[idx], p[idx])
        for k in keys:
            if np.isfinite(sample[k]):
                draws[k].append(sample[k])
    return {
        "method": "ordinary heldout case percentile bootstrap",
        "confidence_level": 0.95, "requested_replicates": repeats,
        "skipped_single_class_replicates": skipped,
        "interpretation": "Conditional test-sample uncertainty; excludes full training uncertainty and external validity.",
        "intervals": {k: {"lower": float(np.quantile(v, .025)),
                           "upper": float(np.quantile(v, .975)),
                           "valid_replicates": len(v)} for k, v in draws.items()},
    }


def diagnostic_exercise(out, repeats):
    ds = load_breast_cancer()
    X = np.asarray(ds.data)
    y = (np.asarray(ds.target) == 0).astype(int)
    idx = np.arange(len(y))
    train, test = train_test_split(idx, test_size=.25, random_state=SEED, stratify=y)
    assert not set(train) & set(test)
    pipeline = Pipeline([
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=10_000, solver="lbfgs", random_state=SEED)),
    ])
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED + 1)
    search = GridSearchCV(pipeline, {"model__C": C_GRID}, scoring="roc_auc", cv=folds,
                          n_jobs=1, refit=True, return_train_score=False)
    search.fit(X[train], y[train])
    p = search.predict_proba(X[test])[:, 1]
    dummy = DummyClassifier(strategy="prior").fit(X[train], y[train])
    p_dummy = dummy.predict_proba(X[test])[:, 1]
    result = {
        "dataset": "Wisconsin Diagnostic Breast Cancer bundled with scikit-learn",
        "dataset_doi": "10.24432/C5DW2B", "seed": SEED,
        "n_cases": len(y), "n_features": X.shape[1],
        "malignant_cases": int(y.sum()), "benign_cases": int((1-y).sum()),
        "training_cases": len(train), "test_cases": len(test),
        "positive_class": "malignant (recoded from sklearn target 0)",
        "threshold": THRESHOLD, "selection": "five-fold training-only grid search by ROC AUC",
        "C_grid": C_GRID, "best_C": float(search.best_params_["model__C"]),
        "training_cv_best_mean_auc": float(search.best_score_),
        "model": metrics(y[test], p), "dummy_prior_baseline": metrics(y[test], p_dummy),
        "proportion_intervals": proportion_intervals(metrics(y[test], p)),
        "bootstrap": bootstrap_intervals(y[test], p, repeats, np.random.default_rng(SEED + 2)),
        "data_sha256": hashlib.sha256(X.tobytes() + y.tobytes()).hexdigest(),
        "limitations": [
            "Selected breast-mass FNA nuclear measurements; not mammograms or population screening.",
            "The loader omits original identifiers; this is a stratified row/case split, not independently verified patient grouping.",
            "No stage labels: early-stage sensitivity cannot be assessed.",
            "No demographic columns: demographic subgroup fairness cannot be assessed.",
            "Internal evaluation only; no external clinical validation or mortality endpoint.",
            "Brier score measures probabilistic accuracy; it is not a pure calibration statistic.",
            "No generative model, vaccine candidate, or clinically deployable diagnostic tool is produced.",
        ],
    }
    pd.DataFrame({"row_index": idx, "split": np.where(np.isin(idx, test), "test", "train")}).to_csv(out / "split_indices.csv", index=False)
    pd.DataFrame({"row_index": test, "malignant": y[test], "probability_malignant": p,
                  "prediction": (p >= THRESHOLD).astype(int), "dummy_probability": p_dummy}).to_csv(out / "heldout_predictions.csv", index=False)
    pd.DataFrame(search.cv_results_).to_csv(out / "training_cv_results.csv", index=False)
    edges = np.linspace(0, 1, 6)
    bins = np.minimum(np.digitize(p, edges[1:-1], right=False), 4)
    reliability = []
    for b in range(5):
        mask = bins == b
        reliability.append({"bin": b + 1, "lower": edges[b], "upper": edges[b+1],
                            "n": int(mask.sum()),
                            "mean_prediction": float(p[mask].mean()) if mask.any() else None,
                            "observed_fraction": float(y[test][mask].mean()) if mask.any() else None})
    rel = pd.DataFrame(reliability)
    rel.to_csv(out / "reliability_bins.csv", index=False)
    model = search.best_estimator_
    parameters = {"features": list(ds.feature_names),
                  "scaler_mean": model.named_steps["scale"].mean_.tolist(),
                  "scaler_scale": model.named_steps["scale"].scale_.tolist(),
                  "coefficients": model.named_steps["model"].coef_[0].tolist(),
                  "intercept": float(model.named_steps["model"].intercept_[0])}
    (out / "fitted_parameters.json").write_text(json.dumps(parameters, indent=2) + "\n")
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.8))
    fpr, tpr, _ = roc_curve(y[test], p)
    axes[0].plot(fpr, tpr, color="black", label=f"Holdout AUC {result['model']['roc_auc']:.3f}")
    axes[0].plot([0, 1], [0, 1], linestyle="--", color="gray")
    axes[0].set(xlabel="False positive rate", ylabel="True positive rate", title="Diagnostic case classification")
    axes[0].legend(frameon=False)
    axes[1].plot([0, 1], [0, 1], linestyle="--", color="gray")
    occupied = rel.dropna()
    axes[1].plot(occupied.mean_prediction, occupied.observed_fraction, "o-", color="black")
    for row in occupied.itertuples():
        axes[1].annotate(f"n={row.n}", (row.mean_prediction, row.observed_fraction), xytext=(4, -12), textcoords="offset points", fontsize=8)
    axes[1].set(xlabel="Mean predicted probability", ylabel="Observed malignant fraction",
                title="Descriptive reliability with bin counts", xlim=(-.05, 1.05), ylim=(-.05, 1.05))
    fig.tight_layout()
    fig.savefig(out / "diagnostic_evaluation.png", dpi=180)
    plt.close(fig)
    return result


def prevalence_exercise(out):
    rows = [expected_screening_counts(prev, .90, .95) for prev in [.001, .005, .01, .05, .10]]
    pd.DataFrame(rows).to_csv(out / "hypothetical_prevalence.csv", index=False)
    return {"assumptions": "Hypothetical fixed sensitivity 0.90, specificity 0.95, N=100000; not derived from WDBC or a clinical trial.",
            "scenarios": rows}


def prioritization_exercise(out):
    """Artificial unitless features; no peptides, patients, learned models, or assays."""
    rng = np.random.default_rng(SEED + 3)
    feature_names = ["expression_support", "presentation_support", "clonality_support"]
    records = pd.DataFrame(rng.uniform(.15, .95, (12, 3)), columns=feature_names)
    records.insert(0, "candidate_id", [f"fictional_{i:02d}" for i in range(1, 13)])
    features = records[feature_names].to_numpy()
    weights = rng.dirichlet(np.ones(3), size=2_000)
    scores = features @ weights.T
    winners = scores.argmax(axis=0)
    rank = 1 + np.argsort(np.argsort(-scores, axis=0), axis=0)
    records["equal_weight_score"] = features.mean(axis=1)
    records["fraction_ranked_first"] = np.bincount(winners, minlength=len(records)) / len(weights)
    records["median_rank"] = np.median(rank, axis=1)
    records["best_rank"] = rank.min(axis=1)
    records["worst_rank"] = rank.max(axis=1)
    records.sort_values("equal_weight_score", ascending=False).to_csv(out / "fictional_priority_sensitivity.csv", index=False)
    pd.DataFrame(weights, columns=feature_names).to_csv(out / "fictional_weights.csv", index=False)
    return {"kind": "Unvalidated heuristic sensitivity analysis using fictional unitless features",
            "n_fictional_candidates": len(records), "n_weight_draws": len(weights),
            "distinct_first_ranked_candidates": int(np.count_nonzero(np.bincount(winners, minlength=len(records)))),
            "candidates": records.to_dict(orient="records"),
            "limitations": "No biological sequences, patient-specific vaccine design, generative AI training, immunogenicity prediction, normal-tissue safety test, or biological validation. Weight frequencies are not probabilities of efficacy."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "results")
    parser.add_argument("--bootstrap", type=int, default=2_000)
    args = parser.parse_args()
    if args.bootstrap < 100:
        parser.error("Use at least 100 bootstrap replicates")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    version = {name: importlib.metadata.version(name) for name in ["numpy", "scipy", "pandas", "scikit-learn", "matplotlib"]}
    result = {"purpose": "Education and reproducibility, not clinical use", "python": platform.python_version(),
              "versions": version, "diagnostic": diagnostic_exercise(args.output_dir, args.bootstrap),
              "prevalence": prevalence_exercise(args.output_dir),
              "prioritization": prioritization_exercise(args.output_dir)}
    (args.output_dir / "analysis.json").write_text(json.dumps(json_safe(result), indent=2, allow_nan=False) + "\n")
    print(json.dumps({"model": result["diagnostic"]["model"],
                      "hypothetical_prevalence_0.005": result["prevalence"]["scenarios"][1],
                      "distinct_first_ranked_candidates": result["prioritization"]["distinct_first_ranked_candidates"],
                      "output_dir": str(args.output_dir.resolve())}, indent=2))


if __name__ == "__main__":
    main()
