"""Home page introducing the educational heart-risk screening."""
from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui import apply_theme, render_nav

apply_theme()
render_nav("home")

hero_copy, hero_heart = st.columns([1.15, .85], gap="large", vertical_alignment="center")
with hero_copy:
    st.markdown(
        """<span class="home-hero-marker"></span><div class="hero-copy">
<span class="hero-kicker">EDUCATIONAL · EXPLAINABLE MACHINE LEARNING</span>
<h1>Heart-health data, explored with care.</h1>
<p>A learning-focused machine-learning project that makes model estimates easier to explore, while keeping their limits clear.</p>
</div>""",
        unsafe_allow_html=True,
    )
    st.page_link("pages/about.py", label="Explore the project", icon=":material/arrow_forward:")
    st.markdown('<p class="hero-note">Educational project only; not a clinical diagnostic system.</p>', unsafe_allow_html=True)
with hero_heart:
    st.markdown(
        '<div class="heart-stage" aria-label="Animated anatomical heart illustration"><div class="heart-object" role="img" aria-label="Anatomical heart"><span>🫀</span></div><span class="heart-caption">Learning through explainable ML</span></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    """<section class="section-heading" id="project">
<span class="section-kicker">THE PROJECT</span>
<h2>Learning-first, transparent by design</h2>
<p>This portfolio project brings together data cleaning, model evaluation, and explainability in one educational experience. It demonstrates how a prediction pipeline works without presenting its output as medical advice.</p>
</section>
<section class="support-grid">
<article class="support-item"><span class="support-tag">DATA & METHODS</span><h3>A reproducible ML workflow</h3><p>Explore how historical data is prepared and how several classification approaches are compared using a consistent evaluation process.</p></article>
<article class="support-item"><span class="support-tag">RESPONSIBLE USE</span><h3>Context before conclusions</h3><p>This project is not clinically validated. Its estimate cannot represent a complete medical history and must not be used for diagnosis or treatment decisions.</p></article>
</section>""",
    unsafe_allow_html=True,
)