import json
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
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    transition: border-color 0.2s ease;
}
.sc-card:hover {
    border-color: rgba(214,179,106,0.4);
}
.sc-card-title {
    color: #94a3b8;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
}
.sc-value { font-size: 1.45rem; font-weight: 800; margin-top: 0.2rem; color: #f1f5f9; }
.sc-caption { color: #64748b; font-size: 0.75rem; margin-top: 0.1rem; }

.sc-badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 6px;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-left: 0.4rem;
}
.badge-good { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.badge-warn { background: rgba(234, 179, 8, 0.15); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.3); }
.badge-bad  { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

.sc-section-header {
    font-family: 'Cinzel', serif;
    font-size: 1.2rem;
    font-weight: 750;
    color: #e2e8f0;
    margin-top: 1.8rem;
    margin-bottom: 0.85rem;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 0.35rem;
}
.sc-alert {
    border-left: 4px solid #ef4444;
    background: linear-gradient(90deg, rgba(239,68,68,0.12), rgba(15,23,42,0.9));
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(239,68,68,0.15);
}
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; border-bottom: 1px solid #1e293b; }
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #d97706, #b45309);
    color: #ffffff;
    border: none;
    font-weight: 700;
    font-family: 'Cinzel', serif;
    letter-spacing: 0.05em;
}
.stButton > button { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION
# ==========================================================

if "game" not in st.session_state:
    st.session_state.game = None


# ==========================================================
# COUNTRY CREATION WIZARD
# ==========================================================

if st.session_state.game is None:
    st
