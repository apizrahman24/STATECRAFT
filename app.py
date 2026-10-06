import json
import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

from engine.eras import ERA_DATA
from engine.governments import GOVERNMENTS
from engine.game import (
    create_game,
    advance_turn,
    apply_policy,
    POLICIES
)
from engine.events import resolve_dilemma


# ==========================================================
# CONFIG & THEME
# ==========================================================

st.set_page_config(
    page_title="STATECRAFT",
    page_icon="🏛",
    layout="wide"
)

# Inject Google Fonts (Cinzel for Grand Strategy vibe, Inter for clean UI) & Custom Polish
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(214,179,106,.07), transparent 35%),
        linear-gradient(180deg, #070a0f 0%, #0c121d 100%);
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background: #05070a;
    border-right: 1px solid #1e293b;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
h1, h2, h3, .sc-title {
    font-family: 'Cinzel', serif !important;
}
.sc-hero {
    padding: 1.8rem 2rem;
    border: 1px solid rgba(214,179,106,0.2);
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(20,27,45,0.85));
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.sc-kicker {
    color: #e2b764;
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    font-weight: 700;
}
.sc-title { 
    font-size: 2.3rem; 
    font-weight: 900; 
    line-height: 1.1; 
    color: #f8fafc; 
    letter-spacing: 0.03em;
}
.sc-subtitle { color: #94a3b8; margin-top: 0.4rem; font-size: 0.95rem; }

.sc-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid #1e293b;
