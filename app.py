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
    page_icon="🏛️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(214,179,106,.06), transparent 30%),
        linear-gradient(180deg, #090d12 0%, #0e1520 100%);
}
[data-testid="stSidebar"] {
    background: #070a0f;
    border-right: 1px solid #1e293b;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
.sc-hero {
    padding: 1.5rem 1.8rem;
    border: 1px solid #1e293b;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85));
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}
.sc-kicker {
    color: #e2b764;
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    font-weight: 700;
}
.sc-title { font-size: 2.1rem; font-weight: 800; line-height: 1.1; color: #f8fafc; }
.sc-subtitle { color: #94a3b8; margin-top: 0.4rem; font-size: 0.95rem; }

.sc-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.5rem;
}
.sc-card-title {
    color: #94a3b8;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
}
.sc-value { font-size: 1.4rem; font-weight: 800; margin-top: 0.2rem; color: #f1f5f9; }
.sc-caption { color: #64748b; font-size: 0.75rem; margin-top: 0.1rem; }

.sc-section-header {
    font-size: 1.1rem;
    font-weight: 750;
    color: #e2e8f0;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 0.3rem;
}
.sc-alert {
    border-left: 4px solid #ef4444;
    background: linear-gradient(90deg, rgba(239,68,68,0.1), rgba(15,23,42,0.9));
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.75rem;
}
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; border-bottom: 1px solid #1e293b; }
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #d97706, #b45309);
    color: #ffffff;
    border: none;
    font-weight: 700;
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
    st.title("🏛 STATECRAFT")
    st.subheader("Build a country. Shape its institutions. Survive its history.")
    st.divider()

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("### 🌍 Epoch & Government")
        era_name = st.selectbox("Historical Era", list(ERA_DATA.keys()))
        era = ERA_DATA[era_name]

        period_name = st.selectbox("Starting Period", list(era["periods"].keys()))
        period_start, period_end = era["periods"][period_name]

        year_mode = st.radio("Starting Year Focus", ["Early", "Middle", "Late", "Custom"], horizontal=True)
        if year_mode == "Early":
            year = period_start
        elif year_mode == "Middle":
            year = (period_start + period_end) // 2
        elif year_mode == "Late":
            year = period_end
        else:
            year = st.slider("Exact Year", period_start, period_end, period_start)

        historical_mode = st.radio("Plausibility Mode", ["Strict Historical", "Historically Plausible", "Alternate History"], horizontal=True)
        
        selected = st.selectbox("Government Type", GOVERNMENTS, format_func=lambda g: g['name'])
        st.caption(selected["description"])

        government_config = {}
        for setting, options in selected["configuration"].items():
            government_config[setting] = st.selectbox(setting, options)

    with col2:
        st.markdown("### ⚙️ Identity & Conditions")
        country_name = st.text_input("Country Name", "Republic of Novara")
        leader = st.text_input("Leader Name", selected["leader"])

        economy = st.selectbox("Economic System", era["economies"])
        territory = st.selectbox("Territorial Structure", era["territories"])
        ideology = st.selectbox("Political Philosophy", era["ideologies"])
        technology = st.selectbox("Technology Level", era["technology"])
        society = st.selectbox("Social Structure", era["societies"])
        foreign_position = st.selectbox("Foreign Policy Stance", era["foreign_positions"])

        scenario = st.selectbox("Starting Scenario", era["scenarios"])
        crisis = st.selectbox("Initial Crisis", era["crises"])

    st.divider()
    if st.button("🚀 INITIALIZE NATION", type="primary", use_container_width=True):
        st.session_state.game = create_game(
            country_name, year, historical_mode, selected, government_config,
            economy, territory, ideology, technology, society, foreign_position,
            scenario, crisis, leader
        )
        st.rerun()
    st.stop()


# ==========================================================
# ACTIVE GAME RUNTIME
# ==========================================================

game = st.session_state.game
state = game["state"]
metrics = state["metrics"]


# ==========================================================
# SIDEBAR COMMAND CENTER
# ==========================================================

with st.sidebar:
    st.title("🏛️ STATECRAFT")
    st.markdown(f"### {game['country_name']}")
    st.caption(f"Era: {game['era']}")
    st.write(f"📅 **Year:** {state['year']} &nbsp;|&nbsp; 🔄 **Turn:** {state['turn']}")
    st.divider()
    st.write(f"**Government:** {game['government']['name']}")
    st.write(f"**Leader:** {game['leader']}")
    st.divider()

    if st.button("🔄 Abandon / New Country", use_container_width=True):
        st.session_state.game = None
        st.rerun()

    save_data = json.dumps(game, indent=4)
    st.download_button(
        "💾 Export Save File",
        save_data,
        file_name="statecraft_save.json",
        mime="application/json",
        use_container_width=True
    )


# ==========================================================
# MAIN DASHBOARD VIEW
# ==========================================================

st.markdown(f"""
<div class="sc-hero">
    <div class="sc-kicker">Strategic Command • Turn {state["turn"]}</div>
    <div class="sc-title">🏛️ {game["country_name"]}</div>
    <div class="sc-subtitle">
        {game["era"]} ({state["year"]}) &nbsp;•&nbsp; {game["government"]["name"]} &nbsp;•&nbsp; {game["territory"]}
    </div>
</div>
""", unsafe_allow_html=True)

# 1. Active Crisis Dilemma Prompt Banner (If Triggered)
active_dilemma = state.get("active_dilemma")
if active_dilemma:
    st.markdown(f"""
    <div class="sc-alert">
        <div style="font-weight: 800; font-size: 1.05rem; color: #f87171;">⚡ CRITICAL DILEMMA: {active_dilemma["title"]}</div>
        <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 0.3rem;">{active_dilemma["description"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Choose Executive Response:")
    d_cols = st.columns(len(active_dilemma["choices"]))
    for idx, (col, choice) in enumerate(zip(d_cols, active_dilemma["choices"])):
        with col:
            if st.button(f"👉 {choice['label']}", key=f"dilemma_btn_{idx}", use_container_width=True):
                resolve_dilemma(state, idx)
                st.rerun()
    st.divider()

# 2. Key Metrics Overview Grid
snapshot = [
    ("GDP", f"{metrics['gdp']:.1f}", "Total Output"),
    ("Growth", f"{metrics['growth']:.1f}%", "Annual Rate"),
    ("Inflation", f"{metrics['inflation']:.1f}%", "Price Index"),
    ("Unemployment", f"{metrics['unemployment']:.1f}%", "Jobless Rate"),
    ("Debt / GDP", f"{metrics['debt']:.1f}%", "National Debt"),
    ("Stability", f"{metrics['government_stability']:.1f}", "Regime Stability"),
    ("Approval", f"{metrics['public_support']:.1f}", "Public Support"),
    ("Legitimacy", f"{metrics['legitimacy']:.1f}", "Mandate Level"),
]

m_cols = st.columns(4)
for i, (label, value, caption) in enumerate(snapshot):
    with m_cols[i % 4]:
        st.markdown(f"""
        <div class="sc-card">
            <div class="sc-card-title">{label}</div>
            <div class="sc-value">{value}</div>
            <div class="sc-caption">{caption}</div>
        </div>
        """, unsafe_allow_html=True)

# 3. Charts & Analytics Section
st.markdown('<div class="sc-section-header">📈 Macroeconomic Trends</div>', unsafe_allow_html=True)
history = pd.DataFrame(state["history"])
if not history.empty:
    ch1, ch2 = st.columns(2, gap="large")
    with ch1:
        fig_econ = px.line(history, x="year", y=["gdp", "debt"], markers=True, title="GDP vs. National Debt")
        fig_econ.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=40, b=10), legend_title_text="")
        st.plotly_chart(fig_econ, use_container_width=True)
    with ch2:
        fig_inf = px.line(history, x="year", y=["inflation", "unemployment"], markers=True, title="Inflation vs. Unemployment")
        fig_inf.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=40, b=10), legend_title_text="")
        st.plotly_chart(fig_inf, use_container_width=True)

# 4. Executive Actions Bar
st.markdown('<div class="sc-section-header">🎯 Executive Policy Deck</div>', unsafe_allow_html=True)
act_col1, act_col2 = st.columns([3, 1], gap="medium")
with act_col1:
    policy_name = st.selectbox("Select State Policy", list(POLICIES.keys()), label_visibility="collapsed")
with act_col2:
    if st.button("⚡ EXECUTE POLICY", type="primary", use_container_width=True):
        apply_policy(game, policy_name)
        st.rerun()

# 5. Full Detailed Records Tabs (Restored!)
st.markdown('<div class="sc-section-header">📚 Detailed State Records</div>', unsafe_allow_html=True)
tabs = st.tabs([
    "🏛 Government",
    "📈 Economy",
    "👥 Society & Factions",
    "🗳️ Politics",
    "🗺️ Regions",
    "🌍 Foreign & Rivals",
    "⚠️ Situations",
    "📜 History"
])

with tabs[0]:
    st.header(game["government"]["name"])
    st.write(game["government"]["description"])
    st.divider()
    for key, value in game["government_config"].items():
        st.write(f"**{key}:** {value}")

with tabs[1]:
    st.header("📈 Economic Parameters")
    st.write(f"**Economic System:** {game['economy']}")
    st.write(f"**Interest Rate:** {metrics['interest_rate']:.1f}%")
    st.write(f"**Currency Strength:** {metrics['currency_strength']:.1f}")
    st.write(f"**Foreign Direct Investment (FDI):** {metrics['fdi']:.1f}")
    st.write(f"**Reserves:** {metrics['reserves']:.1f}")

with tabs[2]:
    st.header("👥 Factional Social Groups")
    st.caption("Track group approvals, wealth shares, and radicalization metrics.")
    groups_df = pd.DataFrame(state["groups"]).T
    st.dataframe(groups_df.round(1), use_container_width=True)

with tabs[3]:
    st.header("🗳️ Political System & Parties")
    parties_df = pd.DataFrame(state["parties"]).T
    st.dataframe(parties_df.round(1), use_container_width=True)

with tabs[4]:
    st.header("🗺️ Regional Politics & Unrest")
    regions_df = pd.DataFrame(state["regions"]).T
    st.dataframe(regions_df.round(1), use_container_width=True)

with tabs[5]:
    st.header("🌍 Foreign Affairs & Rival Nations")
    st.write(f"**Diplomacy:** {metrics['diplomacy']:.1f}")
    st.write(f"**Trade Openness:** {metrics['trade_openness']:.1f}")
    st.write(f"**Military Readiness:** {metrics['military_readiness']:.1f}")
    st.write(f"**International Tension:** {metrics['international_tension']:.1f}")
    st.divider()
    st.subheader("Neighboring Rivals")
    rivals_df = pd.DataFrame(state.get("rivals", []))
    if not rivals_df.empty:
        st.dataframe(rivals_df, use_container_width=True, hide_index=True)
    else:
        st.info("No active rival states.")

with tabs[6]:
    st.header("⚠️ Current Situations & Crises")
    situations = state.get("situations", [])
    if situations:
        for situation in reversed(situations):
            st.warning(situation)
    else:
        st.success("No active national crises.")

with tabs[7]:
    st.header("📜 Historical Log")
    for event in reversed(state["events"]):
        st.markdown(f"### {event['year']} — {event['title']}")
        st.write(event["description"])
        st.divider()

# 6. Turn Advancement Dock
st.markdown("<br>", unsafe_allow_html=True)
if state.get("active_dilemma") is not None:
    st.warning("⚠️ You must resolve the active crisis dilemma above before advancing history to the next turn!")
else:
    if st.button("⏩ END TURN — ADVANCE HISTORY", type="primary", use_container_width=True):
        advance_turn(game)
        st.rerun()
