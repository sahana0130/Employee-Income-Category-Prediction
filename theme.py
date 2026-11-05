
from pathlib import Path
import streamlit as st

THEME_PATH = Path(__file__).resolve().parent / "style.css"


def apply_light_theme():
    if THEME_PATH.exists():
        css = THEME_PATH.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )


def apply_light_themefrom():
    return None