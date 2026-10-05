import random

from .eras import get_era
from .politics import (
    create_parties,
    create_leaders,
    create_regions,
    create_institutions,
    simulate_party_politics,
    calculate_coalition_stability,
    parliament_status
)
from .economy import simulate_economy
from .events import generate_event


def clamp(value, minimum=0, maximum=100):

    return max(
        minimum,
        min(maximum, value)
    )


def create_social_groups():

    return {

        "Workers": {
            "population": 20,
            "approval": 55,
            "wealth": 40,
            "radicalism": 20
        },

        "Farmers": {
            "population": 20,
            "approval": 55,
            "wealth": 40,
            "radicalism": 15
        },

        "Business": {
            "population": 12,
            "approval": 55,
            "wealth": 75,
            "radicalism": 10
        },

        "Middle Class": {
            "population": 18,
            "approval": 55,
            "wealth": 60,
            "radicalism": 15
        },

        "Elite": {
            "population": 5,
            "approval": 60,
            "wealth": 95,
            "radicalism": 10
        },

        "Youth": {
            "population": 15,
            "approval": 50,
            "wealth": 40,
            "radicalism": 25
        }
    }


def create_metrics():

    return {

        "gdp": 100,

        "growth": 2.5,

        "inflation": 2.4,

        "unemployment": 5,

        "debt": 45,

        "deficit": 3,

        "wages": 100,

        "interest_rate": 3,

        "currency_strength": 70,

        "trade_balance": 2,

        "fdi": 50,

        "reserves": 100,

        "legitimacy": 60,

        "public_support": 55,

        "government_stability": 65,

        "institutional_stability": 65,

        "protest_risk": 20,

        "election_risk": 20,

        "diplomacy": 55,

        "military_readiness": 50,

        "trade_openness": 50,

        "international_tension": 20
    }


def create_game(

    country_name,
    year,
    historical_mode,
    government,
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

):

    era, period = get_era(year)

    metrics = create_metrics()

    state = {

        "year": year,

        "turn": 1,

        "metrics": metrics,

        "groups": create_social_groups(),

        "parties": create_parties(year),

        "leaders": create_leaders(year),

        "regions": create_regions(),

        "institutions": create_institutions(),

        "situations": [
            scenario,
            crisis
        ],

        "events": [],

        "history": [],

        "pending_effects": []
    }

    # Government-specific starting conditions

    government_id = government["id"]

    if government_id == "absolute_monarchy":

        metrics["government_stability"] += 10

        metrics["institutional_stability"] -= 5

    elif government_id == "military_government":

        metrics["military_readiness"] += 15

        metrics["legitimacy"] -= 10

    elif government_id == "one_party":

        metrics["government_stability"] += 8

        metrics["institutional_stability"] += 3

    elif government_id == "personalist":

        metrics["government_stability"] += 5

        metrics["institutional_stability"] -= 8

    elif government_id == "parliamentary_republic":

        metrics["institutional_stability"] += 5

    elif government_id == "constitutional_monarchy":

        metrics["institutional_stability"] += 5

    # Initial historical record

    state["history"].append({

        "year": year,

        **metrics
    })

    return {

        "country_name": country_name,

        "leader": leader,

        "year": year,

        "era": era,

        "period": period,

        "historical_mode": historical_mode,

        "government": government,

        "government_config": government_config,

        "economy": economy,

        "territory": territory,

        "ideology": ideology,

        "technology": technology,

        "society": society,

        "foreign_position": foreign_position,

        "scenario": scenario,

        "crisis": crisis,

        "state": state
    }


# ==========================================================
# SOCIAL SYSTEM
# ==========================================================

def calculate_public_support(state):

    groups = state["groups"]

    total = sum(
        group["population"]
        for group in groups.values()
    )

    if total == 0:

        return 0

    return sum(

        group["population"] *
        group["approval"]

        for group in groups.values()

    ) / total


def simulate_society(state):

    m = state["metrics"]

    groups = state["groups"]

    inflation_pressure = max(
        0,
        m["inflation"] - 3
    )

    unemployment_pressure = max(
        0,
        m["unemployment"] - 6
    )

    for name, group in groups.items():

        group["approval"] -= (
            inflation_pressure * 0.15
        )

        group["approval"] -= (
            unemployment_pressure * 0.10
        )

        # Different groups react differently

        if name == "Business":

            if m["tax_burden"] if "tax_burden" in m else False:
                group["approval"] -= 0.2

        if name == "Workers":

            if m["inflation"] > 5:

                group["radicalism"] += 0.3

        if name == "Youth":

            if m["government_stability"] < 45:

                group["radicalism"] += 0.5

        group["approval"] += random.uniform(
            -0.5,
            0.5
        )

        group["approval"] = clamp(
            group["approval"]
        )

        group["radicalism"] = clamp(
            group["radicalism"]
        )


# ==========================================================
# POLITICAL SYSTEM
# ==========================================================

def simulate_politics(state):

    m = state["metrics"]

    parties = state["parties"]

    support = calculate_public_support(
        state
    )

    m["public_support"] = (

        support * 0.70 +

        m["public_support"] * 0.30
    )

    simulate_party_politics(

        state,

        m["inflation"],

        m["unemployment"]
    )

    coalition_stability = (
        calculate_coalition_stability(
            state
        )
    )

    m["government_stability"] = (

        m["legitimacy"] * 0.20 +

        m["public_support"] * 0.25 +

        coalition_stability * 0.20 +

        m["institutional_stability"] * 0.20 +

        state["institutions"][
            "state_capacity"
        ] * 0.15
    )

    if m["government_stability"] < 45:

        m["election_risk"] += 3

    if m["government_stability"] < 35:

        m["legitimacy"] -= 2

    # Parliament status

    state["parliament_status"] = (
        parliament_status(parties)
    )


# ==========================================================
# INSTITUTIONS
# ==========================================================

def simulate_institutions(state):

    institutions = state[
        "institutions"
    ]

    m = state["metrics"]

    # Weak institutions amplify crises

    if institutions["state_capacity"] < 40:

        m["government_stability"] -= 1

    if institutions["corruption"] > 60:

        institutions["tax_capacity"] -= 0.3

        m["fdi"] -= 0.3

    # Stable government slowly strengthens institutions

    if m["government_stability"] > 70:

        institutions[
            "administrative_capacity"
        ] += 0.2

        institutions[
            "bureaucratic_quality"
        ] += 0.2

    for key in institutions:

        institutions[key] = clamp(
            institutions[key]
        )


# ==========================================================
# REGIONS
# ==========================================================

def simulate_regions(state):

    regions = state["regions"]

    m = state["metrics"]

    for region in regions.values():

        if m["unemployment"] > 8:

            region["unrest"] += 0.4

        if m["inflation"] > 6:

            region["unrest"] += 0.3

        if m["growth"] > 4:

            region["government_support"] += 0.2

        region["unrest"] = clamp(
            region["unrest"]
        )

        region["government_support"] = clamp(
            region["government_support"]
        )


# ==========================================================
# FOREIGN AFFAIRS
# ==========================================================

def simulate_foreign_affairs(state):

    m = state["metrics"]

    m["international_tension"] += (
        random.uniform(-1, 1)
    )

    if m["international_tension"] > 70:

        m["military_readiness"] -= 0.5

        m["diplomacy"] -= 1


# ==========================================================
# DELAYED EFFECTS
# ==========================================================

def process_pending_effects(state):

    remaining = []

    metrics = state["metrics"]

    for effect in state[
        "pending_effects"
    ]:

        effect["turns"] -= 1

        if effect["turns"] <= 0:

            for key, value in effect[
                "effects"
            ].items():

                if key in metrics:

                    metrics[key] += value

        else:

            remaining.append(
                effect
            )

    state[
        "pending_effects"
    ] = remaining


# ==========================================================
# POLICIES
# ==========================================================

POLICIES = {

    "Economic Stimulus": {

        "immediate": {
            "growth": 0.8,
            "inflation": 0.4,
            "public_support": 3
        },

        "delayed": {

            "turns": 2,

            "effects": {
                "debt": 2,
                "deficit": 1
            }
        }
    },

    "Fiscal Austerity": {

        "immediate": {

            "growth": -0.5,

            "public_support": -4,

            "government_stability": -2
        },

        "delayed": {

            "turns": 2,

            "effects": {

                "debt": -3,

                "deficit": -2
            }
        }
    },

    "Tax Cuts": {

        "immediate": {

            "growth": 0.4,

            "public_support": 1
        },

        "delayed": {

            "turns": 1,

            "effects": {

                "debt": 1.5,

                "deficit": 1
            }
        }
    },

    "Raise Taxes": {

        "immediate": {

            "growth": -0.2,

            "public_support": -2
        },

        "delayed": {

            "turns": 1,

            "effects": {

                "debt": -1.5,

                "deficit": -1
            }
        }
    },

    "Expand Subsidies": {

        "immediate": {

            "inflation": 0.3,

            "public_support": 4,

            "protest_risk": -2
        },

        "delayed": {

            "turns": 2,

            "effects": {

                "debt": 2,

                "deficit": 1.5
            }
        }
    },

    "Price Controls": {

        "immediate": {

            "inflation": -0.7,

            "growth": -0.4,

            "public_support": 2
        },

        "delayed": {

            "turns": 2,

            "effects": {

                "business_confidence": -5
            }
        }
    },

    "Raise Interest Rates": {

        "immediate": {

            "inflation": -0.7,

            "growth": -0.5,

            "unemployment": 0.5,

            "currency_strength": 2
        }
    },

    "Lower Interest Rates": {

        "immediate": {

            "inflation": 0.6,

            "growth": 0.6,

            "unemployment": -0.4,

            "currency_strength": -2
        }
    },

    "Increase Military Spending": {

        "immediate": {

            "military_readiness": 5,

            "public_support": -1
        },

        "delayed": {

            "turns": 1,

            "effects": {

                "debt": 1.2,

                "deficit": 0.8
            }
        }
    },

    "Political Reform": {

        "immediate": {

            "legitimacy": 4,

            "institutional_stability": 2
        },

        "delayed": {

            "turns": 3,

            "effects": {

                "government_stability": 3
            }
        }
    },

    "Security Crackdown": {

        "immediate": {

            "protest_risk": -6,

            "legitimacy": -5,

            "government_stability": 4
        }
    },

    "Open Trade Negotiations": {

        "immediate": {

            "trade_openness": 5,

            "fdi": 5,

            "trade_balance": 1,

            "international_tension": -2
        }
    }
}


def apply_policy(
    game,
    policy_name
):

    state = game["state"]

    metrics = state[
        "metrics"
    ]

    policy = POLICIES[
        policy_name
    ]

    for key, value in policy[
        "immediate"
    ].items():

        if key in metrics:

            metrics[key] += value

    if "delayed" in policy:

        delayed = policy[
            "delayed"
        ]

        state[
            "pending_effects"
        ].append({

            "turns":
                delayed["turns"],

            "effects":
                delayed["effects"]
        })

    state["events"].append({

        "year":
            state["year"],

        "title":
            policy_name,

        "description":
            (
                f"The government implemented "
                f"{policy_name}. "
                "Some consequences will "
                "appear later."
            ),

        "effects":
            policy
    })


# ==========================================================
# TURN ENGINE
# ==========================================================

def advance_turn(game):

    state = game["state"]

    state["year"] += 1

    state["turn"] += 1

    process_pending_effects(
        state
    )

    simulate_economy(
        state
    )

    simulate_society(
        state
    )

    simulate_politics(
        state
    )

    simulate_institutions(
        state
    )

    simulate_regions(
        state
    )

    simulate_foreign_affairs(
        state
    )

    event = generate_event(
        state
    )

    if event:

        state["events"].append(
            event
        )

        state[
            "situations"
        ].append(
            event["title"]
        )

    m = state[
        "metrics"
    ]

    # Keep values sane

    for key in [

        "public_support",
        "legitimacy",
        "government_stability",
        "institutional_stability",
        "protest_risk",
        "election_risk",
        "diplomacy",
        "military_readiness",
        "trade_openness",
        "international_tension",
        "currency_strength"

    ]:

        m[key] = clamp(
            m[key]
        )

    state["history"].append({

        "year":
            state["year"],

        **m
    })

    state[
        "situations"
    ] = state[
        "situations"
    ][-10:]
