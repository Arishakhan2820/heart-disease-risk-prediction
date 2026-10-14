"""Safe loading, validation, and cleaning for the heart-disease dataset."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

LOGGER = logging.getLogger(__name__)
REQUIRED_COLUMNS = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
NUMERIC_COLUMNS = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CATEGORICAL_COLUMNS = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]


def load_raw_data(path: str | Path) -> pd.DataFrame:
    """Load a CSV and ensure it has the expected Cleveland dataset columns."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")
    try:
        frame = pd.read_csv(source)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise ValueError(f"Could not read CSV '{source}': {exc}") from exc
    frame.columns = frame.columns.str.strip().str.lower()
    missing = set(REQUIRED_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")
    return frame[REQUIRED_COLUMNS].copy()


def data_quality_report(frame: pd.DataFrame) -> dict[str, Any]:
    """Return transparent pre-cleaning diagnostics without changing records."""
    return {
        "shape": list(frame.shape),
        "dtypes": {column: str(dtype) for column, dtype in frame.dtypes.items()},
        "missing_values": frame.isna().sum().to_dict(),
        "duplicate_rows": int(frame.duplicated().sum()),
        "unique_values": frame.nunique().to_dict(),
    }


def clean_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Standardize target, coerce values, flag impossible values, and de-duplicate.

    Median/mode imputation belongs in the training pipeline so it is learned from
    training folds only; this function deliberately preserves missing values.
    """
    cleaned = frame.copy()
    for column in REQUIRED_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    cleaned["target"] = (cleaned["target"] > 0).astype("Int64")

    impossible = (
        ~cleaned["age"].between(18, 120)
        | ~cleaned["trestbps"].between(50, 300)
        | ~cleaned["chol"].between(50, 1000)
        | ~cleaned["thalach"].between(40, 250)
        | ~cleaned["oldpeak"].between(0, 15)
    )
    # Preserve implausible-but-present values for transparent review; do not silently
    # discard potentially legitimate clinical records. Training reports their count.
    LOGGER.warning("Detected %d records with implausible values; retained for review.", int(impossible.sum()))

    duplicates = int(cleaned.duplicated().sum())
    if duplicates:
        LOGGER.info("Removing %d exact duplicate records after inspection.", duplicates)
        cleaned = cleaned.drop_duplicates().copy()
    return cleaned.reset_index(drop=True)


def prepare_dataset(raw_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Clean raw data and persist a reproducible processed CSV plus diagnostics."""
    raw = load_raw_data(raw_path)
    report = data_quality_report(raw)
    cleaned = clean_data(raw)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(destination, index=False)
    report["cleaned_shape"] = list(cleaned.shape)
    report["rows_removed"] = len(raw) - len(cleaned)
    report["duplicate_policy"] = "Exact full-row duplicates were inspected by all-column equality and removed; raw data is retained unchanged."
    return report
