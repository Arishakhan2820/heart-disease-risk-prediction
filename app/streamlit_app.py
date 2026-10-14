"""Streamlit entry point for the Home and Screening pages."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="Heart Risk | Educational Screening",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon=":material/home:",
    url_path="",
    default=True,
)
screening_page = st.Page(
    "pages/screening.py",
    title="Screening",
    icon=":material/monitor_heart:",
    url_path="screening",
)
about_page = st.Page(
    "pages/about.py",
    title="About",
    icon=":material/info:",
    url_path="about",
)

current_page = st.navigation([home_page, about_page, screening_page], position="hidden")
current_page.run()