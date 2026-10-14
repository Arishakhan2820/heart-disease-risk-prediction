"""Train, tune, compare, explain, and serialize heart-risk screening models."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from src.data_loader import REQUIRED_COLUMNS, prepare_dataset
from src.evaluate_model import model_metrics, save_evaluation_plots, save_metrics
from src.explain_model import create_shap_artifacts
from src.preprocessing import build_preprocessor

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]


def candidates() -> dict[str, tuple[Pipeline, dict[str, list]]]:
    """Return compact, reproducible hyperparameter searches for required models."""
    return {
        "logistic_regression": (
            Pipeline([("preprocessor", build_preprocessor(scale_numeric=True)), ("model", LogisticRegression(class_weight="balanced", max_iter=3000, random_state=42))]),
            {"model__C": [0.05, 0.1, 0.5, 1, 2, 5]},
        ),
        "random_forest": (
            Pipeline([("preprocessor", build_preprocessor()), ("model", RandomForestClassifier(class_weight="balanced", random_state=42, n_jobs=-1))]),
            {"model__n_estimators": [200, 400], "model__max_depth": [3, 5, 8, None], "model__min_samples_leaf": [1, 2, 4], "model__max_features": ["sqrt", 0.7]},
        ),
        "xgboost": (
            Pipeline([("preprocessor", build_preprocessor()), ("model", XGBClassifier(objective="binary:logistic", eval_metric="logloss", random_state=42, n_jobs=-1, tree_method="hist"))]),
            {"model__n_estimators": [100, 200, 300], "model__max_depth": [2, 3, 4], "model__learning_rate": [0.03, 0.05, 0.1], "model__subsample": [0.7, 0.85, 1.0], "model__colsample_bytree": [0.7, 0.85, 1.0]},
        ),
    }


def main() -> None:
    """Run the complete reproducible training workflow from repository root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default=ROOT / "data/raw/heart.csv", type=Path)
    parser.add_argument("--processed", default=ROOT / "data/processed/clean_heart_disease.csv", type=Path)
    args = parser.parse_args()
    report = prepare_dataset(args.raw, args.processed)
    LOGGER.info("Cleaned dataset: %s; removed %d rows", report["cleaned_shape"], report["rows_removed"])
    data = pd.read_csv(args.processed)
    X, y = data.drop(columns="target"), data["target"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results: dict[str, dict] = {}
    fitted: dict[str, Pipeline] = {}
    for name, (pipeline, params) in candidates().items():
        search = RandomizedSearchCV(pipeline, params, n_iter=min(12, int(np.prod([len(v) for v in params.values()]))), scoring="roc_auc", cv=cv, n_jobs=-1, random_state=42, refit=True)
        search.fit(X_train, y_train)
        # Selection uses training-fold CV only; untouched test labels are not consulted here.
        results[name] = {"cv_roc_auc": round(float(search.best_score_), 4), "best_params": search.best_params_}
        fitted[name] = search.best_estimator_
        LOGGER.info("%s: CV ROC-AUC=%s", name, results[name]["cv_roc_auc"])
    best_name = max(results, key=lambda key: results[key]["cv_roc_auc"])
    best_pipeline = fitted[best_name]
    probabilities = best_pipeline.predict_proba(X_test)[:, 1]
    results[best_name]["final_test_metrics"] = model_metrics(y_test, probabilities)
    output_metrics = {"data_quality": report, "selection_rule": "Highest 5-fold CV ROC-AUC on training data; held-out test evaluated once only. Positive-class recall is reported because missed risk may be costly.", "best_model": best_name, "models": results}
    save_metrics(output_metrics, ROOT / "reports/metrics.json")
    save_evaluation_plots(y_test, probabilities, ROOT / "reports/figures")
    joblib.dump(best_pipeline, ROOT / "models/best_model.pkl")
    create_shap_artifacts(best_pipeline, X_test.reset_index(drop=True), ROOT / "reports/figures")
    LOGGER.info("Saved %s model, metrics, and evaluation artifacts.", best_name)


if __name__ == "__main__":
    main()
