"""Prediction interface used by Streamlit and other consumers."""
from __future__ import annotations

from typing import Any
import pandas as pd


def risk_category(probability: float) -> str:
    """Map probability to a transparent screening band."""
    return "Low" if probability < 0.30 else "Moderate" if probability < 0.65 else "High"


def predict_risk(pipeline: Any, patient: dict[str, float | int]) -> tuple[float, str]:
    """Return positive-class risk probability and display category."""
    frame = pd.DataFrame([patient])
    estimator = pipeline.named_steps.get("model", pipeline) if hasattr(pipeline, "named_steps") else pipeline
    classes = getattr(estimator, "classes_", None)
    if classes is None:
        raise ValueError("The predictor must expose classes_ to identify the positive class.")
    class_labels = list(classes)
    positive_indices = [index for index, label in enumerate(class_labels) if label == 1]
    if len(positive_indices) != 1:
        raise ValueError(f"The predictor does not contain exactly one positive class labeled 1: {class_labels!r}")

    probabilities = pipeline.predict_proba(frame)
    if probabilities.ndim != 2 or probabilities.shape[1] != len(class_labels):
        raise ValueError("predict_proba output columns do not match the predictor's classes_.")
    probability = float(probabilities[0, positive_indices[0]])
    return probability, risk_category(probability)
