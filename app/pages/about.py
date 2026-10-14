"""Project background, methodology, and limitations."""
from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui import apply_theme, render_nav

apply_theme()
render_nav("about")

st.markdown(
    """<section class="screening-intro">
<span class="section-kicker">ABOUT THE PROJECT</span>
<h1>Making a machine-learning workflow easier to understand</h1>
<p>This project demonstrates how a historical heart-disease dataset can be prepared, evaluated, and connected to an explainable prediction interface. It is a portfolio and learning exercise, not a clinical product.</p>
</section>
<div class="steps-grid">
<article class="info-card"><span class="card-index">01 · DATA</span><h3>Historical records</h3><p>The bundled Cleveland-style dataset contains coded demographic, symptom, exercise, and test-result fields. Its size and provenance limit how broadly its results can be applied.</p></article>
<article class="info-card"><span class="card-index">02 · MODELING</span><h3>Comparable pipelines</h3><p>Preprocessing is kept inside each model pipeline. Logistic Regression, Random Forest, and XGBoost are compared with stratified cross-validation.</p></article>
<article class="info-card"><span class="card-index">03 · EXPLANATION</span><h3>Understand model behavior</h3><p>Evaluation metrics and feature explanations help inspect model behavior. They show associations learned from this dataset, not causes or medical reasoning.</p></article>
</div>
<section class="section-heading">
<span class="section-kicker">HOW TO READ AN ESTIMATE</span>
<h2>A probability is not a diagnosis</h2>
<p>The screening output is the model's estimated probability for the dataset's positive class. It is not an individual's confirmed likelihood of disease, and it does not provide a care plan.</p>
</section>
<div class="note-band"><span class="note-mark">LIMITATIONS</span><p>The dataset is small, historical, and not representative of every population. The model has not been clinically validated or prospectively tested. Errors, bias, missing context, and distribution changes can all affect its output.</p></div>
<section class="support-grid">
<article class="support-item"><span class="support-tag">DATA FIELDS</span><h3>What the pipeline uses</h3><p>Inputs include age, coded sex and chest-pain type, blood pressure, cholesterol, fasting blood sugar, ECG result, maximum heart rate, exercise-induced angina, ST depression, slope, vessel count, and thalassemia code.</p></article>
<article class="support-item"><span class="support-tag">PRIVACY & SAFETY</span><h3>Use sample values only</h3><p>Do not enter identifying information or real patient records. For health concerns, consult a qualified clinician. Review the repository's security guidance before deployment.</p></article>
</section>""",
    unsafe_allow_html=True,
)

start_column, _ = st.columns([1.2, 4])
with start_column:
    if st.button("Open screening", key="about_open_screening", type="primary", use_container_width=True):
        st.switch_page("pages/screening.py")