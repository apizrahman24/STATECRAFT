

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

    st.header(
        "🌍 1. Historical Era"
    )

    era_name = st.selectbox(

        "Historical Era",

        list(ERA_DATA.keys())
    )

    era = ERA_DATA[
        era_name
    ]

    st.header(
        "📅 2. Starting Period"
    )

    period_name = st.selectbox(

        "Starting Period",

        list(
            era["periods"].keys()
        )
    )

    period_start, period_end = (
        era["periods"][period_name]
    )

    st.header(
        "🗓️ 3. Starting Year"
    )

    year_mode = st.radio(

        "Starting year",

        [
            "Early",
            "Middle",
            "Late",
            "Custom"
        ],

        horizontal=True
    )

    if year_mode == "Early":

        year = period_start

    elif year_mode == "Middle":

        year = (
            period_start +
            period_end
        ) // 2

    elif year_mode == "Late":

        year = period_end

    else:

        year = st.slider(

            "Exact Year",

            period_start,

            period_end,

            period_start
        )

    st.info(
        f"Starting year: **{year}**"
    )

    st.header(
        "📜 4. Historical Mode"
    )

    historical_mode = st.radio(

        "Historical plausibility",

        [
            "Strict Historical",
            "Historically Plausible",
            "Alternate History"
        ],

        horizontal=True
    )

    # ======================================================
    # GOVERNMENTS
    # ======================================================

    st.header(
        "🏛️ 5. Government"
    )

    def government_availability(
        government
    ):

        gid = government["id"]

        if year <= 300:

            common = [

                "absolute_monarchy",
                "aristocratic_republic",
                "oligarchy",
                "city_state",
                "tribal_kingdom",
                "tribal_confederation",
                "theocracy",
                "military_government"
            ]

        elif year <= 1500:

            common = [

                "absolute_monarchy",
                "aristocratic_republic",
                "oligarchy",
                "tribal_kingdom",
                "tribal_confederation",
                "theocracy",
                "military_government",
                "confederation",
                "collegial"
            ]

        elif year <= 1800:

            common = [

                "absolute_monarchy",
                "constitutional_monarchy",
                "aristocratic_republic",
                "oligarchy",
                "theocracy",
                "military_government",
                "confederation",
                "colonial",
                "personalist"
            ]

        elif year <= 1900:

            common = [

                "absolute_monarchy",
                "constitutional_monarchy",
                "parliamentary_republic",
                "presidential_republic",
                "aristocratic_republic",
                "military_government",
                "colonial",
                "confederation",
                "personalist"
            ]

        else:

            common = [

                "constitutional_monarchy",
                "parliamentary_republic",
                "presidential_republic",
                "semi_presidential",
                "military_government",
                "one_party",
                "personalist",
                "technocracy",
                "theocracy",
                "direct_democracy",
                "revolutionary",
                "colonial",
                "hybrid"
            ]

        if gid in common:

            return "🟢 Common"

        return "🟡 Unusual"

    available = []

    for government in GOVERNMENTS:

        status = government_availability(
            government
        )

        if (

            historical_mode ==
            "Strict Historical"

            and

            status ==
            "🟡 Unusual"

        ):

            continue

        available.append(
            government
        )

    selected = st.selectbox(

        "Government Type",

        available,

        format_func=lambda g:
            (
                f"{g['name']} "
                f"{government_availability(g)}"
            )
    )

    st.info(
        selected["description"]
    )

    st.subheader(
        "⚙️ Government Configuration"
    )

    government_config = {}

    for setting, options in (
        selected["configuration"].items()
    ):

        government_config[
            setting
        ] = st.selectbox(

            setting,

            options
        )

    # ======================================================
    # COUNTRY
    # ======================================================

    st.header(
        "🌎 6. Country"
    )

    country_name = st.text_input(

        "Country Name",

        "Republic of Novara"
    )

    leader = st.text_input(

        "Leader",

        selected["leader"]
    )

    col1, col2 = st.columns(2)

    with col1:

        economy = st.selectbox(
            "Economic System",
            era["economies"]
        )

        territory = st.selectbox(
            "Territorial Structure",
            era["territories"]
        )

        ideology = st.selectbox(
            "Political Philosophy",
            era["ideologies"]
        )

    with col2:

        technology = st.selectbox(
            "Technology",
            era["technology"]
        )

        society = st.selectbox(
            "Social Structure",
            era["societies"]
        )

        foreign_position = st.selectbox(
            "International Position",
            era["foreign_positions"]
        )

    # ======================================================
    # STARTING CONDITIONS
    # ======================================================

    st.header(
        "⚠️ 7. Starting Conditions"
    )

    scenario = st.selectbox(
        "Starting Scenario",
        era["scenarios"]
    )

    crisis = st.selectbox(
        "Initial Crisis",
        era["crises"]
    )

    st.divider()

    if st.button(

        "🚀 CREATE COUNTRY",

        type="primary",

        use_container_width=True

    ):

        st.session_state.game = create_game(

            country_name,

            year,

            historical_mode,

            selected,

            government_config,

            economy,

            territory,

            ideology,

            technology,

            society,

            foreign_position,

            scenario,

            crisis,

            leader
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

    st.write(
        f"### {game['country_name']}"
    )

    st.write(
        f"Year: **{state['year']}**"
    )

    st.write(
        f"Turn: **{state['turn']}**"
    )

    st.divider()

    st.write(
        f"**Government:** "
        f"{game['government']['name']}"
    )

    st.write(
        f"**Territory:** "
        f"{game['territory']}"
    )

    st.write(
        f"**Leader:** "
        f"{game['leader']}"
    )

    st.divider()

    if st.button(
        "🔄 New Country"
    ):

        st.session_state.game = None

        st.rerun()

    save_data = json.dumps(
        game,
        indent=4
    )

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
st.markdown('<div class="sc-section">⚠️ National Situation</div>', unsafe_allow_html=True)
left, right = st.columns([1.35, 1], gap="large")

with left:
    situations = state.get("situations", [])
    if situations:
        for situation in reversed(situations[-3:]):
            st.markdown(f"""
            <div class="sc-alert">
                <div class="sc-alert-title">🔴 {situation}</div>
                <div class="sc-alert-body">
                    This situation is currently affecting the national environment.
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
        chart.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=10, r=10, t=45, b=10), legend_title_text="")
        st.plotly_chart(chart, use_container_width=True)

    with chart_col2:
        chart2 = px.line(history, x="year", y=["inflation", "unemployment"], markers=True,
                         title="Inflation & Unemployment")
        chart2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             margin=dict(l=10, r=10, t=45, b=10), legend_title_text="")
        st.plotly_chart(chart2, use_container_width=True)

# Four strategic panels
st.markdown('<div class="sc-section">🌍 State Overview</div>', unsafe_allow_html=True)
ov1, ov2, ov3, ov4 = st.columns(4)

with ov1:
    st.markdown('<div class="sc-panel"><b>💰 Economy</b>', unsafe_allow_html=True)
    st.write(f"**Interest rate:** {metrics['interest_rate']:.1f}%")
    st.write(f"**Currency strength:** {metrics['currency_strength']:.1f}")
    st.write(f"**FDI:** {metrics['fdi']:.1f}")
    st.write(f"**Reserves:** {metrics['reserves']:.1f}")
    st.markdown("</div>", unsafe_allow_html=True)

with ov2:
    st.markdown('<div class="sc-panel"><b>👥 Society</b>', unsafe_allow_html=True)
    st.write(f"**Public support:** {metrics['public_support']:.1f}")
    st.write(f"**Protest risk:** {metrics['protest_risk']:.1f}")
    groups_preview = state.get("groups", {})
    if groups_preview:
        def group_score(item):
            data = item[1]
            return data.get("approval", data.get("support", 0))
        strongest = max(groups_preview.items(), key=group_score)
        st.write(f"**Strongest group:** {strongest[0]}")
    st.markdown("</div>", unsafe_allow_html=True)

with ov3:
    st.markdown('<div class="sc-panel"><b>🏛️ Institutions</b>', unsafe_allow_html=True)
    institutions = state.get("institutions", {})
    if institutions:
        for key, value in list(institutions.items())[:5]:
            try:
                shown = f"{float(value):.1f}"
            except (TypeError, ValueError):
                shown = str(value)
            st.write(f"**{key.replace('_', ' ').title()}:** {shown}")
    else:
        st.write("Institutional data unavailable.")
    st.markdown("</div>", unsafe_allow_html=True)

with ov4:
    st.markdown('<div class="sc-panel"><b>🌐 Foreign Affairs</b>', unsafe_allow_html=True)
    st.write(f"**Diplomacy:** {metrics['diplomacy']:.1f}")
    st.write(f"**Trade openness:** {metrics['trade_openness']:.1f}")
    st.write(f"**Military readiness:** {metrics['military_readiness']:.1f}")
    st.write(f"**International tension:** {metrics['international_tension']:.1f}")
    st.markdown("</div>", unsafe_allow_html=True)

# Political landscape + news
st.markdown('<div class="sc-section">🗳️ Political Landscape</div>', unsafe_allow_html=True)
political_col, news_col = st.columns([1.4, 1], gap="large")

with political_col:
    parties_data = state.get("parties", {})
    if parties_data:
        party_df = pd.DataFrame(parties_data).T.reset_index().rename(columns={"index": "Party"})
        if "support" in party_df.columns:
            pchart = px.bar(party_df.sort_values("support"), x="support", y="Party",
                            orientation="h", title="Political Support")
            pchart.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                 plot_bgcolor="rgba(0,0,0,0)",
                                 margin=dict(l=10, r=10, t=45, b=10))
            st.plotly_chart(pchart, use_container_width=True)
        else:
            visible = [c for c in ["Party", "seats", "power", "loyalty"] if c in party_df.columns]
            st.dataframe(party_df[visible].round(1), use_container_width=True, hide_index=True)
    else:
        st.info("No detailed party data available.")

with news_col:
    st.markdown('<div class="sc-panel"><div class="sc-card-title">National News</div>', unsafe_allow_html=True)
    events = state.get("events", [])
    if events:
        for event in reversed(events[-5:]):
            st.markdown(f"""
            <div class="sc-news">
                <div class="sc-news-year">{event.get("year", state["year"])}</div>
                <div class="sc-news-title">{event.get("title", "National Event")}</div>
                <div class="sc-news-body">{event.get("description", "")}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("The historical record is just beginning.")
    st.markdown("</div>", unsafe_allow_html=True)

# Quick decisions
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

# Detailed records
st.markdown('<div class="sc-section">📚 Detailed State Records</div>', unsafe_allow_html=True)
tabs = st.tabs([
    "🏛️ Government",
    "📈 Economy",
    "👥 Society",
    "🗳️ Politics",
    "🗺️ Regions",
    "🌍 Foreign",
    "⚠️ Situations",
    "📜 History"
])


# ==========================================================
# GOVERNMENT
# ==========================================================

with tabs[0]:

    st.header(
        game["government"]["name"]
    )

    st.write(
        game["government"]["description"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Institutional Structure"
        )

        for key, value in (
            game[
                "government_config"
            ].items()
        ):

            st.write(
                f"**{key}:** {value}"
            )

    with col2:

        st.metric(
            "Legitimacy",
            f"{metrics['legitimacy']:.1f}"
        )

        st.metric(
            "Government Stability",
            f"{metrics['government_stability']:.1f}"
        )

        st.metric(
            "Institutional Stability",
            f"{metrics['institutional_stability']:.1f}"
        )

    st.subheader(
        "State Institutions"
    )

    institutions = pd.DataFrame(
        [
            {
                "Institution":
                    key.replace(
                        "_",
                        " "
                    ).title(),

                "Strength":
                    value
            }

            for key, value in
            state[
                "institutions"
            ].items()
        ]
    )

    st.dataframe(
        institutions.round(1),
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# ECONOMY
# ==========================================================

with tabs[1]:

    st.header(
        "📈 Economy"
    )

    st.write(
        f"**Economic System:** "
        f"{game['economy']}"
    )

    history = pd.DataFrame(
        state["history"]
    )

    chart = px.line(

        history,

        x="year",

        y=[
            "gdp",
            "debt"
        ],

        markers=True,

        title="Economic Development"
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    chart2 = px.line(

        history,

        x="year",

        y=[
            "inflation",
            "unemployment"
        ],

        markers=True,

        title="Inflation and Unemployment"
    )

    st.plotly_chart(
        chart2,
        use_container_width=True
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Interest Rate",
        f"{metrics['interest_rate']:.1f}%"
    )

    c2.metric(
        "Currency",
        f"{metrics['currency_strength']:.1f}"
    )

    c3.metric(
        "FDI",
        f"{metrics['fdi']:.1f}"
    )

    c4.metric(
        "Reserves",
        f"{metrics['reserves']:.1f}"
    )


# ==========================================================
# SOCIETY
# ==========================================================

with tabs[2]:

    st.header(
        "👥 Society"
    )

    groups = pd.DataFrame(
        state["groups"]
    ).T

    st.dataframe(
        groups.round(1),
        use_container_width=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Public Support",
        f"{metrics['public_support']:.1f}"
    )

    c2.metric(
        "Protest Risk",
        f"{metrics['protest_risk']:.1f}"
    )

    c3.metric(
        "Election Risk",
        f"{metrics['election_risk']:.1f}"
    )


# ==========================================================
# POLITICS
# ==========================================================

with tabs[3]:

    st.header(
        "🗳️ Political System"
    )

    st.subheader(
        "Parliament"
    )

    st.info(
        state.get(
            "parliament_status",
            "Initial Parliament"
        )
    )

    parties = pd.DataFrame(
        state["parties"]
    ).T

    st.dataframe(
        parties.round(1),
        use_container_width=True
    )

    st.subheader(
        "Political Leaders"
    )

    leaders = pd.DataFrame(
        state["leaders"]
    ).T

    st.dataframe(
        leaders,
        use_container_width=True
    )


# ==========================================================
# REGIONS
# ==========================================================

with tabs[4]:

    st.header(
        "🗺️ Regional Politics"
    )

    regions = pd.DataFrame(
        state["regions"]
    ).T

    st.dataframe(
        regions.round(1),
        use_container_width=True
    )


# ==========================================================
# FOREIGN
# ==========================================================

with tabs[5]:

    st.header(
        "🌍 Foreign Affairs"
    )

    st.write(
        f"**International Position:** "
        f"{game['foreign_position']}"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Diplomacy",
        f"{metrics['diplomacy']:.1f}"
    )

    c2.metric(
        "Military Readiness",
        f"{metrics['military_readiness']:.1f}"
    )

    c3.metric(
        "Trade Openness",
        f"{metrics['trade_openness']:.1f}"
    )

    c4.metric(
        "International Tension",
        f"{metrics['international_tension']:.1f}"
    )


# ==========================================================
# SITUATIONS
# ==========================================================

with tabs[6]:

    st.header(
        "⚠️ Current Situations"
    )

    for situation in reversed(
        state["situations"]
    ):

        st.warning(
            situation
        )

    st.subheader(
        "Pending Consequences"
    )

    if state["pending_effects"]:

        for effect in state[
            "pending_effects"
        ]:

            st.info(

                f"Effects arriving in "
                f"**{effect['turns']} turn(s)**: "
                f"{effect['effects']}"
            )

    else:

        st.success(
            "No major delayed effects."
        )


# ==========================================================
# HISTORY
# ==========================================================

with tabs[7]:

    st.header(
        "📜 Historical Record"
    )

    for event in reversed(
        state["events"]
    ):

        st.markdown(

            f"### {event['year']} — "
            f"{event['title']}"
        )

        st.write(
            event["description"]
        )


# ==========================================================
# END TURN
# ==========================================================

st.divider()

st.markdown('<div class="sc-section">⏳ Continue History</div>', unsafe_allow_html=True)

st.write(

    "End the current turn and allow the "
    "economic, political, social and "
    "international systems to evolve."
)

if st.button(
    "⏩ END TURN — ADVANCE HISTORY",
    type="primary",
    use_container_width=True
):

    advance_turn(
        game
    )

    st.rerun()
