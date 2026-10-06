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

        st.markdown("### ⏱️ Campaign Game Speed (Locked)")
        speed_choices = {
            "1 Day (Micro / Crisis)": 1,
            "1 Month (Tactical)": 30,
            "1 Year (Strategic)": 365
        }
        chosen_speed_label = st.selectbox("Time Increment Per Turn", list(speed_choices.keys()), index=2)

    st.divider()
    if st.button("🚀 INITIALIZE NATION", type="primary", use_container_width=True):
        game_obj = create_game(
            country_name, year, historical_mode, selected, government_config,
            economy, territory, ideology, technology, society, foreign_position,
            scenario, crisis, leader
        )
        game_obj["era"] = era_name
        game_obj["state"]["month"] = 1
        game_obj["state"]["day"] = 1
        game_obj["time_scale"] = chosen_speed_label
        game_obj["days_per_turn"] = speed_choices[chosen_speed_label]
        
        st.session_state.game = game_obj
        st.rerun()
    st.stop()


# ==========================================================
# ACTIVE GAME RUNTIME
# ==========================================================

game = st.session_state.game
state = game["state"]
metrics = state["metrics"]

# Compatibility fallbacks & safety normalization
if "month" not in state or not (1 <= state["month"] <= 12):
    state["month"] = 1
if "day" not in state or not (1 <= state["day"] <= 31):
    state["day"] = 1
if "time_scale" not in game:
    game["time_scale"] = "1 Year (Strategic)"
if "days_per_turn" not in game:
    game["days_per_turn"] = 365

days_per_turn = game["days_per_turn"]


# ==========================================================
# SIDEBAR COMMAND CENTER
# ==========================================================

with st.sidebar:
    st.markdown("### 🏛️ STATECRAFT")
    st.markdown(f"**{game['country_name']}**")
    st.caption(f"Era: {game.get('era', 'Unknown Era')}")
    
    current_date_str = f"📅 {state['day']} / {state['month']} / {state['year']}"
    st.markdown(f"**{current_date_str}**")
    st.write(f"🔄 **Turn:** {state['turn']}")
    
    st.divider()
    st.markdown("### 👑 Leader Profile")
    st.write(f"**Leader:** {game['leader']}")
    st.write(f"**Government:** {game['government']['name']}")
    st.info(f"⏱️ Speed: {game['time_scale']}")

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

current_date_display = f"{state['day']:02d}/{state['month']:02d}/{state['year']}"
st.markdown(f"""
<div class="sc-hero">
    <div class="sc-kicker">Strategic Command • Turn {state["turn"]} • Date: {current_date_display}</div>
    <div class="sc-title">🏛️ {game["country_name"]}</div>
    <div class="sc-subtitle">
        {game.get('era', '')} &nbsp;•&nbsp; {game["government"]["name"]} &nbsp;•&nbsp; Leader: {game['leader']}
    </div>
</div>
""", unsafe_allow_html=True)

# 1. Active Crisis Dilemma Prompt Banner (If Triggered)
active_dilemma = state.get("active_dilemma")
if active_dilemma:
    st.markdown(f"""
    <div class="sc-alert">
        <div style="font-weight: 800; font-size: 1.05rem; color: #f87171; font-family: 'Cinzel', serif;">⚡ CRITICAL DILEMMA: {active_dilemma["title"]}</div>
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

# Helper badge logic for metrics
def get_badge(label, val):
    if label == "Growth":
        return "badge-good" if val >= 0 else "badge-bad"
    if label == "Inflation":
        return "badge-good" if val < 4 else ("badge-warn" if val < 8 else "badge-bad")
    if label == "Unemployment":
        return "badge-good" if val < 6 else ("badge-warn" if val < 10 else "badge-bad")
    if label == "Debt / GDP":
        return "badge-good" if val < 50 else ("badge-warn" if val < 90 else "badge-bad")
    if label in ["Stability", "Approval", "Legitimacy"]:
        return "badge-good" if val >= 60 else ("badge-warn" if val >= 40 else "badge-bad")
    return "badge-good"

# 2. Key Metrics Overview Grid with Status Badges
growth_val = metrics['growth']
inf_val = metrics['inflation']
unemp_val = metrics['unemployment']
debt_val = metrics['debt']
stab_val = metrics['government_stability']
supp_val = metrics['public_support']
leg_val = metrics['legitimacy']

snapshot = [
    ("GDP", f"{metrics['gdp']:.1f}", "Total Output", "badge-good"),
    ("Growth", f"{growth_val:.1f}%", "Annual Rate", get_badge("Growth", growth_val)),
    ("Inflation", f"{inf_val:.1f}%", "Price Index", get_badge("Inflation", inf_val)),
    ("Unemployment", f"{unemp_val:.1f}%", "Jobless Rate", get_badge("Unemployment", unemp_val)),
    ("Debt / GDP", f"{debt_val:.1f}%", "National Debt", get_badge("Debt / GDP", debt_val)),
    ("Stability", f"{stab_val:.1f}", "Regime Stability", get_badge("Stability", stab_val)),
    ("Approval", f"{supp_val:.1f}", "Public Support", get_badge("Approval", supp_val)),
    ("Legitimacy", f"{leg_val:.1f}", "Mandate Level", get_badge("Legitimacy", leg_val)),
]

m_cols = st.columns(4)
for i, (label, value, caption, badge_cls) in enumerate(snapshot):
    with m_cols[i % 4]:
        st.markdown(f"""
        <div class="sc-card">
            <div class="sc-card-title">{label} <span class="sc-badge {badge_cls}">●</span></div>
            <div class="sc-value">{value}</div>
            <div class="sc-caption">{caption}</div>
        </div>
        """, unsafe_allow_html=True)

# 3. DYNAMIC ERA-BASED NEWS TICKER & WIRE (ROBUST CHECK)
current_era_name = game.get("era", "")

if "Antiquity" in current_era_name:
    ticker_title = "🏛️ Imperial Scroll & Royal Decrees"
elif "Middle Ages" in current_era_name or "Feudalism" in current_era_name:
    ticker_title = "📜 Chronicles & Monastic Broadsheets"
elif "Early Modern" in current_era_name or "Colonial" in current_era_name:
    ticker_title = "📰 Gazette & Merchant Dispatches"
elif "Industrial" in current_era_name:
    ticker_title = "⚡ National Telegraph Wire & Press"
elif "Crises" in current_era_name or "World Wars" in current_era_name:
    ticker_title = "📻 Emergency Broadcast & Wire Service"
elif "Cold War" in current_era_name or "Atomic" in current_era_name:
    ticker_title = "📡 State News Network & Telex"
else:
    ticker_title = "🌐 Global Digital News Feed"

st.markdown(f'<div class="sc-section-header">{ticker_title}</div>', unsafe_allow_html=True)
events_list = state.get("events", [])

st.markdown("""
<style>
.sc-ticker-container {
    background: linear-gradient(135deg, rgba(10, 15, 25, 0.95), rgba(15, 23, 42, 0.9));
    border: 1px solid rgba(214, 179, 106, 0.25);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.4);
}
.sc-ticker-item {
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(30, 41, 59, 0.6);
}
.sc-ticker-item:last-child {
    border-bottom: none;
}
.sc-ticker-date {
    color: #e2b764;
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
}
.sc-ticker-title {
    color: #f8fafc;
    font-weight: 700;
    font-size: 0.9rem;
    margin-top: 0.1rem;
}
.sc-ticker-desc {
    color: #94a3b8;
    font-size: 0.82rem;
    margin-top: 0.15rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="sc-ticker-container">', unsafe_allow_html=True)
if events_list:
    for ev in reversed(events_list[-4:]):
        st.markdown(f"""
        <div class="sc-ticker-item">
            <div class="sc-ticker-date">📅 YEAR {ev['year']} — BULLETIN</div>
            <div class="sc-ticker-title">{ev['title']}</div>
            <div class="sc-ticker-desc">{ev['description']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div style="color: #64748b; font-style: italic;">No bulletins recorded on the wire. The nation rests in peace.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("📜 View Full Historical Wire Archive"):
    if events_list:
        for ev in reversed(events_list):
            st.markdown(f"**[{ev['year']}] {ev['title']}**")
            st.write(ev["description"])
            st.divider()
    else:
        st.info("Archive is empty.")

# 4. Charts & Analytics Section
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

# 5. Executive Actions Bar
st.markdown('<div class="sc-section-header">🎯 Executive Policy Deck</div>', unsafe_allow_html=True)
act_col1, act_col2 = st.columns([3, 1], gap="medium")
with act_col1:
    policy_name = st.selectbox("Select State Policy", list(POLICIES.keys()), label_visibility="collapsed")
with act_col2:
    if st.button("⚡ EXECUTE POLICY", type="primary", use_container_width=True):
        apply_policy(game, policy_name)
        st.rerun()

# 6. Full Detailed Records Tabs
st.markdown('<div class="sc-section-header">📚 Detailed State Records</div>', unsafe_allow_html=True)
tabs = st.tabs([
    "🏛 Government",
    "📈 Economy",
    "👥 Society & Factions",
    "🗳️ Politics",
    "🗺️️ Regions",
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
        st.markdown(f"### Year {event['year']} — {event['title']}")
        st.write(event["description"])
        st.divider()

# 7. Turn Advancement Dock
st.markdown("<br>", unsafe_allow_html=True)
if state.get("active_dilemma") is not None:
    st.warning("⚠️ You must resolve the active crisis dilemma above before advancing history!")
else:
    if st.button(f"⏩ ADVANCE TIME ({game['time_scale']})", type="primary", use_container_width=True):
        if days_per_turn == 365:
            state["year"] += 1
        elif days_per_turn == 30:
            state["month"] += 1
            if state["month"] > 12:
                state["month"] = 1
                state["year"] += 1
        else:
            state["day"] += days_per_turn
            while state["day"] > 30:
                state["day"] -= 30
                state["month"] += 1
                if state["month"] > 12:
                    state["month"] = 1
                    state["year"] += 1

        advance_turn(game)
        st.rerun()
