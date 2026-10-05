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


# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(

    page_title="STATECRAFT",

    page_icon="🏛️",

    layout="wide"
)


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
# HEADER
# ==========================================================

st.title(
    f"🏛️ {game['country_name']}"
)

st.caption(

    f"{game['era']} • "
    f"{game['period']} • "
    f"{state['year']}"
)


# ==========================================================
# MAIN METRICS
# ==========================================================

columns = st.columns(6)

main_metrics = [

    ("GDP",
     metrics["gdp"],
     ""),

    ("Growth",
     metrics["growth"],
     "%"),

    ("Inflation",
     metrics["inflation"],
     "%"),

    ("Unemployment",
     metrics["unemployment"],
     "%"),

    ("Debt",
     metrics["debt"],
     "%"),

    ("Government Stability",
     metrics["government_stability"],
     "")
]

for column, data in zip(
    columns,
    main_metrics
):

    name, value, suffix = data

    column.metric(

        name,

        f"{value:.1f}{suffix}"
    )


# ==========================================================
# TABS
# ==========================================================

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
# GOVERNMENT DECISIONS
# ==========================================================

st.divider()

st.header(
    "🎯 Government Decisions"
)

policy_name = st.selectbox(

    "Choose a policy",

    list(
        POLICIES.keys()
    )
)

if st.button(

    "Implement Policy",

    type="primary",

    use_container_width=True
):

    apply_policy(

        game,

        policy_name
    )

    st.rerun()


# ==========================================================
# END TURN
# ==========================================================

st.divider()

st.subheader(
    "⏳ Continue History"
)

st.write(

    "End the current turn and allow the "
    "economic, political, social and "
    "international systems to evolve."
)

if st.button(

    "⏩ END TURN",

    use_container_width=True
):

    advance_turn(
        game
    )

    st.rerun()
