import random

INTERACTIVE_EVENTS = [
    {
        "id": "labor_strike",
        "title": "General Strike in the Industrial Sector",
        "condition": lambda m, s: s["groups"]["Workers"]["radicalism"] > 45 or m["protest_risk"] > 50,
        "description": "Workers have walked off the job across major manufacturing hubs, demanding higher wages and price controls.",
        "choices": [
            {
                "label": "Cater to Workers (Increase Subsidies & Concede)",
                "effects": {"public_support": +5, "deficit": +2.0, "fdi": -4},
                "group_impact": {"Workers": +15, "Business": -10},
                "text": "The government conceded to union demands. Factories reopened, but foreign investors are rattled."
            },
            {
                "label": "Send in Security Forces (Crackdown)",
                "effects": {"protest_risk": -15, "government_stability": +6, "legitimacy": -8},
                "group_impact": {"Workers": -15, "Youth": -10, "Elite": +5},
                "text": "Police cleared the streets by force. Order is restored, but democratic legitimacy has plummeted."
            },
            {
                "label": "Ignore Them (Maintain Course)",
                "effects": {"growth": -2.0, "protest_risk": +10},
                "group_impact": {"Workers": -10},
                "text": "The government ignored the protests. Production stalled completely for weeks, hurting economic growth."
            }
        ]
    },
    {
        "id": "capital_flight",
        "title": "Capital Flight & Investor Panic",
        "condition": lambda m, s: m["debt"] > 70 or m["currency_strength"] < 50,
        "description": "Foreign and domestic investors are rapidly pulling money out of the country due to growing fiscal instability.",
        "choices": [
            {
                "label": "Austerity Measures & Spending Cuts",
                "effects": {"debt": -4.0, "deficit": -2.5, "public_support": -6},
                "group_impact": {"Business": +5, "Workers": -10, "Middle Class": -6},
                "text": "Creditors are appeased by severe budget cuts, but ordinary citizens bear the heavy cost."
            },
            {
                "label": "Capital Controls & Seize Foreign Assets",
                "effects": {"fdi": -15, "reserves": +10, "international_tension": +10},
                "group_impact": {"Business": -20, "Elite": -15},
                "text": "The state locked down capital movement. Currency stabilized temporarily, but foreign investors fled."
            },
            {
                "label": "Print Money to Cover Shortfalls",
                "effects": {"inflation": +4.5, "growth": +1.0},
                "group_impact": {"Workers": -8, "Middle Class": -8},
                "text": "The central bank printed cash to plug holes. Short-term liquidity is solved, but inflation is spiraling."
            }
        ]
    },
    {
        "id": "border_ultimatum",
        "title": "Hostile Border Ultimatum",
        "condition": lambda m, s: s.get("rivals") and any(r["stance"] == "Hostile" and r["relation"] < -30 for r in s["rivals"]),
        "description": "A hostile neighboring power has issued an aggressive territorial ultimatum, threatening military action if demands are unmet.",
        "choices": [
            {
                "label": "Mobilize the Military & Defy Them",
                "effects": {"military_readiness": +8, "international_tension": +15, "debt": +2.0},
                "group_impact": {"Elite": +5, "Workers": -2},
                "text": "The nation mobilized its armed forces. Tension has reached a boiling point."
            },
            {
                "label": "Diplomatic Capitulation & Concessions",
                "effects": {"diplomacy": +5, "legitimacy": -6, "public_support": -4},
                "group_impact": {"Elite": -10, "Middle Class": -5},
                "text": "The government backed down diplomatically, preserving peace at a steep cost to national pride."
            },
            {
                "label": "Ignore the Ultimatum",
                "effects": {"international_tension": +8, "government_stability": -4},
                "text": "Ignoring the threat left the country in a tense limbo as border skirmishes flare up."
            }
        ]
    }
]


def generate_event(state):
    metrics = state["metrics"]
    candidates = []

    for event in INTERACTIVE_EVENTS:
        try:
            if event["condition"](metrics, state):
                candidates.append(event)
        except Exception:
            continue

    if not candidates:
        if random.random() < 0.25:
            # Fallback random dynamic event
            return {
                "id": "political_scandal",
                "title": "High-Level Political Scandal",
                "description": "A corruption scandal involving prominent ministers has broken out in the capital.",
                "choices": [
                    {
                        "label": "Launch Public Investigation",
                        "effects": {"legitimacy": +3, "government_stability": -3},
                        "text": "Transparency restored trust, though the ruling cabinet took a political blow."
                    },
                    {
                        "label": "Cover It Up & Suppress Media",
                        "effects": {"institutional_stability": -4, "legitimacy": -6},
                        "text": "The scandal was buried, but public cynicism toward state institutions grew."
                    }
                ]
            }
        return None

    return random.choice(candidates)


def resolve_dilemma(state, choice_index):
    dilemma = state["active_dilemma"]
    if not dilemma:
        return

    choice = dilemma["choices"][choice_index]
    metrics = state["metrics"]

    # Apply metric effects
    for key, val in choice.get("effects", {}).items():
        if key in metrics:
            metrics[key] += val

    # Apply group impact effects
    if "group_impact" in choice:
        for group_name, delta in choice["group_impact"].items():
            if group_name in state["groups"]:
                from .game import clamp
                state["groups"][group_name]["approval"] = clamp(
                    state["groups"][group_name]["approval"] + delta
                )

    # Record historical event
    state["events"].append({
        "year": state["year"],
        "title": dilemma["title"],
        "description": choice["text"],
        "effects": choice.get("effects", {})
    })

    # Clear active dilemma so turns can resume
    state["active_dilemma"] = None
