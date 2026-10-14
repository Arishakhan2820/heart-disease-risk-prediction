"""Input form and prediction result for the educational screening."""
from __future__ import annotations

import logging
import sys
import time
from html import escape
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui import apply_theme, render_nav
from src.explain_model import create_local_explainer, explain_local_prediction
from src.predict import predict_risk

LOGGER = logging.getLogger(__name__)
PROCESSED_DATA_PATH = ROOT / "data/processed/clean_heart_disease.csv"

apply_theme()
render_nav("screening")

st.markdown(
    """<section class="screening-intro" id="screening-form">
<span class="section-kicker">SCREENING WORKSPACE · EDUCATIONAL USE ONLY</span>
<h1>Build a sample screening profile</h1>
<p>Enter values from the form below to see how the saved model responds. The result is a probability estimate from a limited historical dataset, not a medical evaluation.</p>
</section>
<div class="note-band"><span class="note-mark">BEFORE YOU BEGIN</span><p>Use sample or non-identifying values only. No names, IDs, contact details, or real patient records. If you have health concerns, speak with a qualified healthcare professional.</p></div>
<div class="section-heading"><h2>Health measurements</h2><p>Choose the values that match each field's dataset coding.</p></div>""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    path = ROOT / "models/best_model.pkl"
    if not path.is_file():
        raise FileNotFoundError("Approved model unavailable")
    return joblib.load(path)


@st.cache_resource
def load_local_shap_explainer():
    """Cache a small training-only background and its fitted-model explainer."""
    model = load_model()
    if not PROCESSED_DATA_PATH.is_file():
        raise FileNotFoundError("Processed training data is unavailable for SHAP explanations.")

    data = pd.read_csv(PROCESSED_DATA_PATH)
    features = data.drop(columns="target")
    target = data["target"].astype(int)
    training_features, _ = train_test_split(
        features,
        test_size=0.20,
        stratify=target,
        random_state=42,
    )
    return create_local_explainer(model, training_features)


with st.form("risk_form"):
    first, second = st.columns(2)
    with first:
        st.markdown('<div class="field-group"><span class="field-index">01</span>Personal profile</div>', unsafe_allow_html=True)
        age = st.number_input("Age (years)", 18, 120, 55)
        sex = st.selectbox("Sex", [0, 1], format_func=lambda value: "Female (0)" if value == 0 else "Male (1)")
        cp = st.selectbox("Chest pain type", [0, 1, 2, 3])
        trestbps = st.number_input("Resting blood pressure (mm Hg)", 50, 300, 130)
        chol = st.number_input("Serum cholesterol (mg/dL)", 50, 1000, 240)
        fbs = st.selectbox("Fasting blood sugar >120 mg/dL", [0, 1])
        restecg = st.selectbox("Resting ECG result", [0, 1, 2])
    with second:
        st.markdown('<div class="field-group"><span class="field-index">02</span>Clinical measures</div>', unsafe_allow_html=True)
        thalach = st.number_input("Maximum heart rate", 40, 250, 150)
        exang = st.selectbox("Exercise-induced angina", [0, 1])
        oldpeak = st.number_input("ST depression (oldpeak)", 0.0, 15.0, 1.0, 0.1)
        slope = st.selectbox("ST slope", [0, 1, 2])
        ca = st.selectbox("Major vessels", [0, 1, 2, 3, 4])
        thal = st.selectbox("Thalassemia indicator", [0, 1, 2, 3])
    submitted = st.form_submit_button("Predict educational risk")

if submitted:
    if time.monotonic() - st.session_state.get("last_prediction_at", 0) < 2:
        st.warning("Please wait two seconds before another prediction.")
    else:
        st.session_state.last_prediction_at = time.monotonic()
        st.session_state.pop("screening_prediction", None)
        try:
            model = load_model()
            input_values = {
                "age": age,
                "sex": sex,
                "cp": cp,
                "trestbps": trestbps,
                "chol": chol,
                "fbs": fbs,
                "restecg": restecg,
                "thalach": thalach,
                "exang": exang,
                "oldpeak": oldpeak,
                "slope": slope,
                "ca": ca,
                "thal": thal,
            }
            input_columns = list(model.named_steps["preprocessor"].feature_names_in_)
            patient = {column: input_values[column] for column in input_columns}
            probability, category = predict_risk(model, patient)
            st.session_state.screening_prediction = {
                "probability": probability,
                "category": category,
                "patient": patient,
            }
        except (FileNotFoundError, ValueError, TypeError):
            LOGGER.exception("Heart-risk prediction failed for the submitted input.")
            st.error("Prediction is unavailable. Contact the administrator.")
        except Exception:
            LOGGER.exception("Unexpected error while predicting heart-risk probability.")
            st.error("Prediction service is temporarily unavailable. Please try again later.")

prediction = st.session_state.get("screening_prediction")
if prediction is not None:
    probability = prediction["probability"]
    category = prediction["category"]
    patient_frame = pd.DataFrame([prediction["patient"]])

    st.markdown(
        f'<section class="result-panel"><span class="section-kicker">MODEL ESTIMATE</span>'
        f'<h2>{category} educational risk band</h2>'
        f'<p>Estimated positive-class probability: <strong>{probability:.1%}</strong></p>'
        f'<div role="progressbar" aria-label="Estimated positive-class probability" '
        f'aria-valuemin="0" aria-valuemax="100" aria-valuenow="{int(probability * 100)}" '
        f'style="height:9px;overflow:hidden;background:#f1e6e9;border-radius:99px">'
        f'<span style="display:block;width:{probability:.1%};height:100%;background:#781d39"></span></div>'
        '<p>Higher scores are not diagnoses. This result cannot assess your overall health or guide treatment.</p></section>',
        unsafe_allow_html=True,
    )
    st.caption("If you have health concerns, consult a qualified healthcare professional.")
    st.subheader("Why did the model make this prediction?")
    st.caption(
        "The displayed probability comes from the saved LogisticRegression pipeline. "
        "SHAP values decompose its raw decision score (log-odds); they are not probability percentages."
    )
    st.info(
        "These explanations describe the model's associations, not medical causes or treatment advice. "
        "This application is an educational demonstration, not a medical diagnosis."
    )

    try:
        local_explanation = explain_local_prediction(
            load_model(),
            load_local_shap_explainer(),
            patient_frame,
            positive_class=1,
        )
        shap_values = np.asarray(local_explanation.values, dtype=float)
        feature_names = list(local_explanation.feature_names)
        feature_values = np.asarray(local_explanation.data, dtype=float)
        top_indices = np.argsort(np.abs(shap_values))[::-1][:8]
        contribution_rows = []
        for index in top_indices:
            contribution = float(shap_values[index])
            if contribution > 1e-10:
                direction = "Increases log-odds"
            elif contribution < -1e-10:
                direction = "Decreases log-odds"
            else:
                direction = "No change"
            contribution_rows.append(
                {
                    "Feature": feature_names[index],
                    "Feature value": f"{feature_values[index]:g}",
                    "SHAP contribution (log-odds)": round(contribution, 4),
                    "Direction": direction,
                }
            )

        st.markdown("#### Local feature contributions")
        headers = ["Feature", "Feature value", "SHAP contribution (log-odds)", "Direction"]
        header_html = "".join(f"<th scope=\"col\">{escape(label)}</th>" for label in headers)
        row_html = "".join(
            "<tr>" + "".join(f"<td>{escape(str(row[label]))}</td>" for label in headers) + "</tr>"
            for row in contribution_rows
        )
        st.markdown(
            f'<div class="contribution-table-wrap"><table class="contribution-table">'
            f'<thead><tr>{header_html}</tr></thead><tbody>{row_html}</tbody></table></div>',
            unsafe_allow_html=True,
        )

        figure = plt.figure(figsize=(10, 7))
        try:
            import shap

            shap.plots.waterfall(local_explanation, max_display=12, show=False)
            figure = plt.gcf()
            st.pyplot(figure, use_container_width=True)
        finally:
            plt.close(figure)
    except Exception:
        LOGGER.exception("SHAP explanation generation failed for the current screening input.")
        st.warning(
            "The prediction is available, but a local SHAP explanation could not be generated for this input. "
            "Please try again later."
        )