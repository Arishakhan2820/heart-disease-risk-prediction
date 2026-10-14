"""Evaluation helpers and consistently named report artifacts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_recall_curve, precision_score,
                             recall_score, roc_auc_score, roc_curve)


def model_metrics(y_true: Any, probabilities: np.ndarray, threshold: float = 0.5) -> dict[str, Any]:
    """Compute classification metrics, including risk-screening-relevant recall."""
    predictions = (probabilities >= threshold).astype(int)
    return {
        "accuracy": round(float(accuracy_score(y_true, predictions)), 4),
        "precision": round(float(precision_score(y_true, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_true, probabilities)), 4),
        "classification_report": classification_report(y_true, predictions, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, predictions).tolist(),
    }


def save_evaluation_plots(y_true: Any, probabilities: np.ndarray, output_dir: str | Path) -> None:
    """Save ROC, precision-recall, and confusion-matrix plots."""
    directory = Path(output_dir); directory.mkdir(parents=True, exist_ok=True)
    fpr, tpr, _ = roc_curve(y_true, probabilities)
    precision, recall, _ = precision_recall_curve(y_true, probabilities)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(fpr, tpr, label="Model"); axes[0].plot([0, 1], [0, 1], "--", color="gray")
    axes[0].set(title="ROC Curve", xlabel="False Positive Rate", ylabel="True Positive Rate"); axes[0].legend()
    axes[1].plot(recall, precision, label="Model", color="#C0392B")
    axes[1].set(title="Precision–Recall Curve", xlabel="Recall", ylabel="Precision"); axes[1].legend()
    fig.tight_layout(); fig.savefig(directory / "roc_and_pr_curve.png", dpi=180); plt.close(fig)


def save_metrics(metrics: dict[str, Any], destination: str | Path) -> None:
    """Write serializable metrics as formatted JSON."""
    with Path(destination).open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
