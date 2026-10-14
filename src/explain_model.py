"""SHAP artifact generation for the fitted tree-based final pipeline."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.linear_model import LogisticRegression


NUMERIC_FEATURE_LABELS = {
    "age": "Age (years)",
    "trestbps": "Resting blood pressure (mm Hg)",
    "chol": "Serum cholesterol (mg/dL)",
    "thalach": "Maximum heart rate (bpm)",
    "oldpeak": "ST depression (oldpeak)",
}
CATEGORICAL_FEATURE_LABELS = {
    "sex": "Sex",
    "cp": "Chest pain type",
    "fbs": "Fasting blood sugar >120 mg/dL",
    "restecg": "Resting ECG result",
    "exang": "Exercise-induced angina",
    "slope": "ST slope",
    "ca": "Major vessels",
    "thal": "Thalassemia indicator",
}
CATEGORY_VALUES = {
    "sex": {"0": "Female", "1": "Male"},
    "fbs": {"0": "No", "1": "Yes"},
    "exang": {"0": "No", "1": "Yes"},
}


def create_local_explainer(pipeline: object, training_features: pd.DataFrame) -> shap.LinearExplainer:
    """Create a LogisticRegression explainer with a bounded training-only background."""
    steps = getattr(pipeline, "named_steps", {})
    preprocessor = steps.get("preprocessor")
    estimator = steps.get("model")
    if preprocessor is None or not isinstance(estimator, LogisticRegression):
        estimator_name = type(estimator).__name__ if estimator is not None else type(pipeline).__name__
        raise TypeError(f"Local SHAP supports the saved LogisticRegression pipeline, not {estimator_name}.")
    if training_features.empty:
        raise ValueError("Training data is empty; cannot create a SHAP background.")

    input_columns = list(preprocessor.feature_names_in_)
    background_rows = training_features.loc[:, input_columns].sample(
        n=min(40, len(training_features)),
        random_state=42,
    )
    transformed_background = preprocessor.transform(background_rows)
    feature_names = preprocessor.get_feature_names_out()
    if transformed_background.shape[1] != len(feature_names):
        raise ValueError("Transformed background and fitted feature names do not match.")
    return shap.LinearExplainer(
        estimator,
        transformed_background,
    )


def explain_local_prediction(
    pipeline: object,
    explainer: shap.LinearExplainer,
    patient_frame: pd.DataFrame,
    positive_class: int = 1,
) -> shap.Explanation:
    """Explain one ordered raw input and validate SHAP against its raw model score."""
    steps = getattr(pipeline, "named_steps", {})
    preprocessor = steps.get("preprocessor")
    estimator = steps.get("model")
    if preprocessor is None or not isinstance(estimator, LogisticRegression):
        raise TypeError("Local SHAP requires the saved LogisticRegression preprocessing pipeline.")

    classes = list(estimator.classes_)
    if len(classes) != 2 or positive_class not in classes:
        raise ValueError(f"Positive class {positive_class!r} is not supported by model classes {classes!r}.")
    positive_index = classes.index(positive_class)
    input_columns = list(preprocessor.feature_names_in_)
    ordered_patient = patient_frame.loc[:, input_columns]
    if len(ordered_patient) != 1:
        raise ValueError("A local explanation requires exactly one current input row.")

    transformed_patient = preprocessor.transform(ordered_patient)
    feature_names = list(preprocessor.get_feature_names_out())
    if transformed_patient.shape[1] != len(feature_names):
        raise ValueError("Transformed input and fitted feature names do not match.")

    raw_explanation = explainer(transformed_patient)
    raw_values = np.asarray(raw_explanation.values, dtype=float)
    feature_count = len(feature_names)
    class_count = len(classes)
    binary_margin = False

    if raw_values.shape == (1, feature_count):
        local_values = raw_values[0]
        binary_margin = True
    elif raw_values.shape == (feature_count, class_count):
        local_values = raw_values[:, positive_index]
    elif raw_values.shape == (1, feature_count, class_count):
        local_values = raw_values[0, :, positive_index]
    elif raw_values.shape == (1, class_count, feature_count):
        local_values = raw_values[0, positive_index, :]
    elif raw_values.shape == (class_count, 1, feature_count):
        local_values = raw_values[positive_index, 0, :]
    else:
        raise ValueError(f"Unexpected SHAP value shape {raw_values.shape!r} for {class_count} classes.")

    base_values = np.asarray(raw_explanation.base_values, dtype=float)
    if base_values.ndim == 0:
        base_value = float(base_values)
    elif base_values.shape == (1,):
        base_value = float(base_values[0])
    elif base_values.shape == (1, class_count):
        base_value = float(base_values[0, positive_index])
    elif base_values.shape == (class_count, 1):
        base_value = float(base_values[positive_index, 0])
    elif base_values.shape == (class_count,):
        base_value = float(base_values[positive_index])
    else:
        raise ValueError(f"Unexpected SHAP base-value shape {base_values.shape!r}.")

    if binary_margin and positive_index == 0:
        local_values = -local_values
        base_value = -base_value

    raw_score = float(np.asarray(estimator.decision_function(transformed_patient)).reshape(-1)[0])
    expected_score = raw_score if positive_index == 1 else -raw_score
    if not np.isclose(base_value + float(np.sum(local_values)), expected_score, atol=1e-5):
        raise ValueError("SHAP contributions do not add up to this prediction's positive-class log-odds.")

    transformed_row = np.asarray(transformed_patient, dtype=float)[0]
    patient_values = ordered_patient.iloc[0]
    display_names: list[str] = []
    display_values: list[float] = []
    for index, feature_name in enumerate(feature_names):
        if feature_name in NUMERIC_FEATURE_LABELS:
            display_names.append(NUMERIC_FEATURE_LABELS[feature_name])
            display_values.append(float(patient_values[feature_name]))
            continue

        raw_name, separator, category = feature_name.rpartition("_")
        if separator and raw_name in CATEGORICAL_FEATURE_LABELS:
            category_name = CATEGORY_VALUES.get(raw_name, {}).get(category, category)
            display_names.append(f"{CATEGORICAL_FEATURE_LABELS[raw_name]} = {category_name} ({category})")
            display_values.append(float(transformed_row[index]))
        else:
            display_names.append(feature_name)
            display_values.append(float(transformed_row[index]))

    return shap.Explanation(
        values=np.asarray(local_values, dtype=float),
        base_values=base_value,
        data=np.asarray(display_values, dtype=float),
        feature_names=display_names,
    )


def create_shap_artifacts(pipeline: object, samples: pd.DataFrame, output_dir: str | Path) -> None:
    """Save global bar, beeswarm, and two individual SHAP waterfall explanations."""
    directory = Path(output_dir); directory.mkdir(parents=True, exist_ok=True)
    preprocessor = pipeline.named_steps["preprocessor"]
    estimator = pipeline.named_steps["model"]
    transformed = pd.DataFrame(preprocessor.transform(samples), columns=preprocessor.get_feature_names_out())
    explainer = shap.Explainer(estimator, transformed)
    values = explainer(transformed)
    shap.plots.bar(values, max_display=15, show=False); plt.tight_layout(); plt.savefig(directory / "shap_global_importance.png", dpi=180, bbox_inches="tight"); plt.close()
    shap.plots.beeswarm(values, max_display=15, show=False); plt.tight_layout(); plt.savefig(directory / "shap_beeswarm.png", dpi=180, bbox_inches="tight"); plt.close()
    for index in range(min(2, len(transformed))):
        shap.plots.waterfall(values[index], max_display=12, show=False); plt.tight_layout(); plt.savefig(directory / f"shap_patient_{index + 1}.png", dpi=180, bbox_inches="tight"); plt.close()
