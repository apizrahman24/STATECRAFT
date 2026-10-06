import copy
from engine.events import trigger_era_event

POLICIES = {
    "Austerity Measures": {
        "description": "Cut public spending to lower national debt, at the cost of public approval.",
        "effects": {"debt": -5.0, "public_support": -6.0, "government_stability": -2.0}
    },
    "Infrastructure Stimulus": {
        "description": "Fund large-scale public works to boost economic growth and employment.",
        "effects": {"gdp": 4.0, "unemployment": -1.5, "debt": 4.0, "inflation": 1.0}
    },
    "Military Buildup": {
        "description": "Increase defense spending to elevate military readiness and national power projection.",
        "effects": {"military_readiness": 8.0, "debt": 3.0, "international_tension": 2.0}
    },
    "Price Controls": {
        "description": "Legislate strict price ceilings on essential commodities to curb runaway inflation.",
        "effects": {"inflation": -3.5, "public_support": 3.0, "gdp": -1.0}
    }
}

def create_game(
    country_name, year, historical_mode, selected_gov, government_config,
    economy, territory, ideology, technology, society, foreign_position,
    scenario, crisis, leader
):
    return {
        "country_name": country_name,
        "leader": leader,
        "government": selected_gov,
        "government_config": government_config,
        "economy": economy,
        "territory": territory,
        "ideology": ideology,
        "technology": technology,
        "society": society,
        "foreign_position": foreign_position,
        "scenario": scenario,
        "crisis": crisis,
        "historical_mode": historical_mode,
        "state": {
            "turn": 1,
            "year": year,
            "month": 1,
            "day": 1,
            "metrics": {
                "gdp": 100.0,
                "growth": 2.5,
                "inflation": 2.4,
                "unemployment": 5.0,
                "debt": 45.0,
                "government_stability": 75.0,
                "public_support": 55.0,
                "legitimacy": 60.0,
                "interest_rate": 4.0,
                "currency_strength": 100.0,
                "fdi": 10.0,
                "reserves": 20.0,
                "diplomacy": 50.0,
                "trade_openness": 50.0,
                "military_readiness": 50.0,
                "international_tension": 20.0
            },
            "groups": {
                "Elites": {"approval": 70, "wealth_share": 40, "radicalization": 10},
                "Middle Class": {"approval": 60, "wealth_share": 35, "radicalization": 15},
                "Working Class": {"approval": 50, "wealth_share": 25, "radicalization": 25}
            },
            "parties": {
                "Ruling Party": {"seats": 55, "loyalty": 80},
                "Opposition": {"seats": 45, "loyalty": 40}
            },
            "regions": {
                "Capital Region": {"stability": 80, "unrest": 10, "wealth": 50},
                "Periphery": {"stability": 60, "unrest": 30, "wealth": 20}
            },
            "rivals": [
                {"name": "Neighboring Empire", "relation": "Neutral", "tension": 30}
            ],
            "situations": [crisis],
            "events": [
                {
                    "year": year,
                    "title": "Founding of the Nation",
                    "description": f"{country_name} has emerged onto the world stage under the rule of {leader}."
                }
            ],
            "history": [
                {
                    "year": year,
                    "gdp": 100.0,
                    "debt": 45.0,
                    "inflation": 2.4,
                    "unemployment": 5.0,
                    "stability": 75.0
                }
            ],
            "active_dilemma": None
        }
    }

def advance_turn(game):
    state = game["state"]
    metrics = state["metrics"]
    
    # Basic economic drift simulation
    growth_drift = (metrics["government_stability"] - 50) * 0.02
    metrics["growth"] = max(-15.0, min(15.0, 2.5 + growth_drift))
    metrics["gdp"] *= (1.0 + metrics["growth"] / 100.0)
    
    state["turn"] += 1
    
    # Save a historical snapshot
    state["history"].append({
        "year": state["year"],
        "gdp": metrics["gdp"],
        "debt": metrics["debt"],
        "inflation": metrics["inflation"],
        "unemployment": metrics["unemployment"],
        "stability": metrics["government_stability"]
    })
    
    # Trigger dynamic era-specific events & dilemmas
    trigger_era_event(state, game)

def apply_policy(game, policy_name):
    policy = POLICIES.get(policy_name)
    if not policy:
        return
    
    metrics = game["state"]["metrics"]
    for key, delta in policy["effects"].items():
        if key in metrics:
            metrics[key] += delta
            
    game["state"]["events"].append({
        "year": game["state"]["year"],
        "title": f"Policy Implemented: {policy_name}",
        "description": policy["description"]
    })
