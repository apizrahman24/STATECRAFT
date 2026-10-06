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
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="STATECRAFT",
    page_icon="🏛️",
    layout="wide"
)

# ==========================================================
# VISUAL THEME — STATECRAFT COMMAND UI
# ==========================================================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(214,179,106,.08), transparent 28%),
        linear-gradient(180deg, #0b1017 0%, #0d131c 100%);
}
[data-testid="stSidebar"] {
    background: #0a0f15;
    border-right: 1px solid #263444;
}
.block-container {
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}
.sc-hero {
    padding: 1.35rem 1.5rem;
    border: 1px solid #263444;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(17,25,35,.98), rgba(20,30,42,.92));
    margin-bottom: 1rem;
    box-shadow: 0 12px 30px rgba(0,0,0,.18);
}
.sc-kicker {
    color: #d6b36a;
    text-transform: uppercase;
    font-size: .72rem;
    letter-spacing: .16em;
    font-weight: 700;
}
.sc-title { font-size: 2rem; font-weight: 800; line-height: 1.05; }
.sc-subtitle { color: #8f9dad; margin-top: .35rem; font-size: .92rem; }
.sc-card {
    background: linear-gradient(180deg, rgba(17,25,35,.98), rgba(14,21,29,.98));
    border: 1px solid #263444;
    border-radius: 14px;
    padding: 1rem 1.05rem;
    min-height: 105px;
}
.sc-card-title {
    color: #8f9dad;
    font-size: .73rem;
    text-transform: uppercase;
    letter-spacing: .10em;
    font-weight: 700;
}
.sc-value { font-size: 1.45rem; font-weight: 800; margin-top: .28rem; }
.sc-caption { color: #8f9dad; font-size: .78rem; margin-top: .2rem; }
.sc-section {
    margin-top: 1.15rem;
    margin-bottom: .55rem;
    font-size: 1rem;
    font-weight: 750;
}
.sc-panel {
    border: 1px solid #263444;
    border-radius: 14px;
    background: rgba(17,25,35,.9);
    padding: 1rem 1.1rem;
}
.sc-alert {
    border-left: 4px solid #e56b6f;
    background: linear-gradient(90deg, rgba(229,107,111,.12), rgba(17,25,35,.85));
    border-radius: 12px;
    padding: .9rem 1rem;
    margin-bottom: .65rem;
}
.sc-alert-title { font-weight: 800; font-size: .95rem; }
.sc-alert-body { color: #8f9dad; font-size: .82rem; margin-top: .22rem; }
.sc-news { border-bottom: 1px solid #263444; padding: .7rem 0; }
.sc-news:last-child { border-bottom: 0; }
.sc-news-year { color: #d6b36a; font-size: .72rem; font-weight: 700; letter-spacing: .08em; }
.sc-news-title { font-weight: 700; margin-top: .15rem; }
.sc-news-body { color: #8f9dad; font-size: .8rem; margin-top: .15rem; }
div[data-testid="stMetric"] {
    background: rgba(17,25,35,.92);
    border: 1px solid #263444;
    padding: .85rem 1rem;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab-list"] { gap: .25rem; border-bottom: 1px solid #263444; }
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #caa85f, #e0bd74);
    color: #10151c;
    border: none;
    font-weight: 800;
}
.stButton > button { border-radius: 9px; }
@media (max-width: 900px) {
    .sc-title { font-size: 1.55rem; }
    .block-container { padding-left: .8rem; padding-right: .8rem; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION
# ==========================================================

if "game" not in st.session_state:
    st.session_state.game = None


# ==========================================================
# COUNTRY CREATION
# ==========================================================

if st.session_state.game is None:
    st.title("🏛️ STATECRAFT")
    st.subheader(
        "Build a country. Shape its institutions. "
        "Survive its history."
    )
    st.divider()

    st.header("🌍 1. Historical Era")
    era_name = st.selectbox("Historical Era", list(ERA_DATA.keys()))
    era = ERA_DATA[era_name]

    st.header("📅 2. Starting Period")
    period_name = st.selectbox("Starting Period", list(era["periods"].keys()))
    period_start, period_end = era["periods"][period_name]

    st.header("🗓️️ 3. Starting Year")
    year_mode = st.radio("Starting year", ["Early", "Middle", "Late", "Custom"], horizontal=True)
    if year_mode == "Early":
        year = period_start
    elif year_mode == "Middle":
        year = (period_start + period_end) // 2
    elif year_mode == "Late":
        year = period_end
    else:
        year = st.slider("Exact Year", period_start, period_end, period_start)

    st.info(f"Starting year: **{year}**")

    st.header("📜 4. Historical Mode")
    historical_mode = st.radio("Historical plausibility", ["Strict Historical", "Historically Plausible", "Alternate History"], horizontal=True)

    st.header("🏛️ 5. Government")
    def government_availability(government):
        gid = government["id"]
        if year <= 300:
            common = ["absolute_monarchy", "aristocratic_republic", "oligarchy", "city_state", "tribal_kingdom", "tribal_confederation", "theocracy", "military_government"]
        elif year <= 1500:
            common = ["absolute_monarchy", "aristocratic_republic", "oligarchy", "tribal_kingdom", "tribal_confederation", "theocracy", "military_government", "confederation", "collegial"]
        elif year <= 1800:
            common = ["absolute_monarchy", "constitutional_monarchy", "aristocratic_republic", "oligarchy", "theocracy", "military_government", "confederation", "colonial", "personalist"]
        elif year <= 1900:
            common = ["absolute_monarchy", "constitutional_monarchy", "parliamentary_republic", "presidential_republic", "aristocratic_republic", "military_government", "colonial", "confederation", "personalist"]
        else:
            common = ["constitutional_monarchy", "parliamentary_republic", "presidential_republic", "semi_presidential", "military_government", "one_party", "personalist", "technocracy", "theocracy", "direct_democracy", "revolutionary", "colonial", "hybrid"]
        return "🟢 Common" if gid in common else "🟡 Unusual"

    available = []
    for government in GOVERNMENTS:
        status = government_availability(government)
        if historical_mode == "Strict Historical" and status == "🟡 Unusual":
            continue
        available.append(government)

    selected = st.selectbox(
        "Government Type",
        available,
        format_func=lambda g: f"{g['name']} {government_availability(g)}"
    )
    st.info(selected["description"])

    st.subheader("⚙️️ Government Configuration")
    government_config = {}
    for setting, options in selected["configuration"].items():
        government_config[setting] = st.selectbox(setting, options)

    st.header("🌎 6. Country")
    country_name = st.text_input("Country Name", "Republic of Novara")
    leader = st.text_input("Leader", selected["leader"])

    col1, col2 = st.columns(2)
    with col1:
        economy = st.selectbox("Economic System", era["economies"])
        territory = st.selectbox("Territorial Structure", era["territories"])
        ideology = st.selectbox("Political Philosophy", era["ideologies"])
    with col2:
        technology = st.selectbox("Technology", era["technology"])
        society = st.selectbox("Social Structure", era["societies"])
        foreign_position = st.selectbox("International Position", era["foreign_positions"])

    st.header("⚠️ 7. Starting Conditions")
    scenario = st.selectbox("Starting Scenario", era["scenarios"])
    crisis = st.selectbox("Initial Crisis", era["crises"])

    st.divider()
    if st.button("🚀 CREATE COUNTRY", type="primary", use_container_width=True):
        st.session_state.game = create_game(
            country_name, year, historical_mode, selected, government_config,
            economy, territory, ideology, technology, society, foreign_position,
            scenario, crisis, leader
        )
        st.rerun()
    st.stop()


# ==========================================================
# ACTIVE GAME
# ==========================================================

game = st.session_state.game
state = game["state"]
metrics = state["metrics"]


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.title("🏛️ STATECRAFT")
    st.write(f"### {game['country_name']}")
    st.write(f"Year: **{state['year']}**")
    st.write(f"Turn: **{state['turn']}**")
    st.divider()
    st.write(f"**Government:** {game['government']['name']}")
    st.write(f"**Territory:** {game['territory']}")
    st.write(f"**Leader:** {game['leader']}")
    st.divider()

    if st.button("🔄 New Country"):
        st.session_state.game = None
        st.rerun()

    save_data = json.dumps(game, indent=4)
    st.download_button(
        "💾 Save Game",
        save_data,
        file_name="statecraft_save.json",
        mime="application/json"
    )


# ==========================================================
# NATIONAL COMMAND DASHBOARD
# ==========================================================

st.markdown(f"""
<div class="sc-hero">
    <div class="sc-kicker">National Command Dashboard • Turn {state["turn"]}</div>
    <div class="sc-title">🏛️ {game["country_name"]}</div>
    <div class="sc-subtitle">
        {game["era"]} • {game["period"]} • {state["year"]}
        &nbsp;|&nbsp; {game["government"]["name"]}
        &nbsp;|&nbsp; {game["territory"]}
        &nbsp;|&nbsp; {game["leader"]}
    </div>
</div>
""", unsafe_allow_html=True)

# Active Crisis / Interactive Dilemma Prompt Block
active_dilemma = state.get("active_dilemma")
if active_dilemma:
    st.markdown(f"""
    <div class="sc-alert" style="border-left-color: #f39c12; background: linear-gradient(90deg, rgba(243,156,18,.15), rgba(17,25,35,.9));">
        <div class="sc-alert-title" style="color: #f39c12;">⚡ ACTIVE CRISIS DILEMMA: {active_dilemma["title"]}</div>
        <div class="sc-alert-body" style="font-size: .9rem; margin-top: .4rem;">{active_dilemma["description"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("**Choose your administration's response:**")
    for idx, choice in enumerate(active_dilemma["choices"]):
        if st.button(f"👉 {choice['label']}", key=f"dilemma_choice_{idx}", use_container_width=True):
            resolve_dilemma(state, idx)
            st.rerun()
    st.divider()

# National snapshot
snapshot = [
    ("GDP", f"{metrics['gdp']:.1f}", "Economic size"),
    ("Growth", f"{metrics['growth']:.1f}%", "Annual growth"),
    ("Inflation", f"{metrics['inflation']:.1f}%", "Price pressure"),
    ("Unemployment", f"{metrics['unemployment']:.1f}%", "Labour market"),
    ("Debt", f"{metrics['debt']:.1f}%", "Debt / GDP"),
    ("Stability", f"{metrics['government_stability']:.1f}", "Government stability"),
    ("Approval", f"{metrics['public_support']:.1f}", "Public support"),
    ("Legitimacy", f"{metrics['legitimacy']:.1f}", "Political legitimacy"),
]
cols = st.columns(8)
for col, (label, value, caption) in zip(cols, snapshot):
    with col:
        st.markdown(f"""
        <div class="sc-card">
            <div class="sc-card-title">{label}</div>
            <div class="sc-value">{value}</div>
            <div class="sc-caption">{caption}</div>
        </div>
        """, unsafe_allow_html=True)

# Situation + political health
st.markdown('<div class="sc-section">⚠️ National Situation & Factions</div>', unsafe_allow_html=True)
left, right = st.columns([1.35, 1], gap="large")

with left:
    situations = state.get("situations", [])
    if situations:
        for situation in reversed(situations[-3:]):
            st.markdown(f"""
            <div class="sc-alert">
                <div class="sc-alert-title">🔴 {situation}</div>
                <div class="sc-alert-body">
                    Active pressure point affecting national stability.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No major active national crises.")

with right:
    st.markdown('<div class="sc-panel"><div class="sc-card-title">Political Health</div>', unsafe_allow_html=True)
    pc1, pc2 = st.columns(2)
    pc1.metric("Government Stability", f"{metrics['government_stability']:.1f}")
    pc2.metric("Legitimacy", f"{metrics['legitimacy']:.1f}")
    pc1.metric("Protest Risk", f"{metrics['protest_risk']:.1f}")
    pc2.metric("Election Risk", f"{metrics['election_risk']:.1f}")
    st.markdown("</div>", unsafe_allow_html=True)

# Performance charts
st.markdown('<div class="sc-section">📊 National Performance</div>', unsafe_allow_html=True)
history = pd.DataFrame(state["history"])
if not history.empty:
    chart_col1, chart_col2 = st.columns(2, gap="large")
    with chart_col1:
        chart = px.line(history, x="year", y=["gdp", "debt"], markers=True, title="Economy & Fiscal Position")
        chart.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=45, b=10), legend_title_text="")
        st.plotly_chart(chart, use_container_width=True)
    with chart_col2:
        chart2 = px.line(history, x="year", y=["inflation", "unemployment"], markers=True, title="Inflation & Unemployment")
        chart2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=45, b=10), legend_title_text="")
        st.plotly_chart(chart2, use_container_width=True)

# Four strategic panels including Rivals
st.markdown('<div class="sc-section">🌍 State Overview & Geopolitics</div>', unsafe_allow_html=True)
ov1, ov2, ov3, ov4 = st.columns(4)

with ov1:
    st.markdown('<div class="sc-panel"><b>💰 Economy</b>', unsafe_allow_html=True)
    st.write(f"**Interest rate:** {metrics['interest_rate']:.1f}%")
    st.write(f"**Currency strength:** {metrics['currency_strength']:.1f}")
    st.write(f"**FDI:** {metrics['fdi']:.1f}")
    st.write(f"**Reserves:** {metrics['reserves']:.1f}")
    st.markdown("</div>", unsafe_allow_html=True)

with ov2:
    st.markdown('<div class="sc-panel"><b>👥 Factions</b>', unsafe_allow_html=True)
    groups = state.get("groups", {})
    if groups:
        for gname, gdata in list(groups.items())[:3]:
            st.write(f"**{gname}:** App {gdata['approval']:.0f} | Rad {gdata['radicalism']:.0f}")
    st.markdown("</div>", unsafe_allow_html=True)

with ov3:
    st.markdown('<div class="sc-panel"><b>⚔️ Rival Powers</b>', unsafe_allow_html=True)
    rivals = state.get("rivals", [])
    if rivals:
        for r in rivals:
            st.write(f"**{r['name']}**")
            st.write(f"Rel: {r['relation']} | Stance: {r['stance']}")
    else:
        st.write("No major regional rivals.")
    st.markdown("</div>", unsafe_allow_html=True)

with ov4:
    st.markdown('<div class="sc-panel"><b>🌐 Foreign Affairs</b>', unsafe_allow_html=True)
    st.write(f"**Diplomacy:** {metrics['diplomacy']:.1f}")
    st.write(f"**Trade openness:** {metrics['trade_openness']:.1f}")
    st.write(f"**Military readiness:** {metrics['military_readiness']:.1f}")
    st.write(f"**International tension:** {metrics['international_tension']:.1f}")
    st.markdown("</div>", unsafe_allow_html=True)

# Executive Decisions
st.markdown('<div class="sc-section">🎯 Executive Decisions</div>', unsafe_allow_html=True)
action_col1, action_col2 = st.columns([2, 1])
with action_col1:
    policy_name = st.selectbox("Choose a policy", list(POLICIES.keys()), key="dashboard_policy")
with action_col2:
    st.write("")
    st.write("")
    if st.button("⚡ IMPLEMENT POLICY", type="primary", use_container_width=True):
        apply_policy(game, policy_name)
        st.rerun()

# Detailed records tabs
st.markdown('<div class="sc-section">📚 Detailed State Records</div>', unsafe_allow_html=True)
tabs = st.tabs([
    "🏛️️ Government",
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
    for key, value in game["government_config"].items():
        st.write(f"**{key}:** {value}")

with tabs[1]:
    st.header("📈 Economy")
    st.write(f"**Economic System:** {game['economy']}")

with tabs[2]:
    st.header("👥 Factional Social Groups")
    groups_df = pd.DataFrame(state["groups"]).T
    st.dataframe(groups_df.round(1), use_container_width=True)

with tabs[3]:
    st.header("🗳️ Political System")
    parties_df = pd.DataFrame(state["parties"]).T
    st.dataframe(parties_df.round(1), use_container_width=True)

with tabs[4]:
    st.header("🗺️ Regional Politics")
    regions_df = pd.DataFrame(state["regions"]).T
    st.dataframe(regions_df.round(1), use_container_width=True)

with tabs[5]:
    st.header("🌍 Foreign Affairs & Rival Nations")
    rivals_df = pd.DataFrame(state.get("rivals", []))
    if not rivals_df.empty:
        st.dataframe(rivals_df, use_container_width=True, hide_index=True)

with tabs[6]:
    st.header("⚠️ Current Situations")
    for situation in reversed(state["situations"]):
        st.warning(situation)

with tabs[7]:
    st.header("📜 Historical Record")
    for event in reversed(state["events"]):
        st.markdown(f"### {event['year']} — {event['title']}")
        st.write(event["description"])

# End turn
st.divider()
st.markdown('<div class="sc-section">⏳ Continue History</div>', unsafe_allow_html=True)
if state.get("active_dilemma") is not None:
    st.warning("⚠️ You must resolve the active crisis dilemma above before advancing history to the next turn!")
else:
    if st.button("⏩ END TURN — ADVANCE HISTORY", type="primary", use_container_width=True):
        advance_turn(game)
        st.rerun()
