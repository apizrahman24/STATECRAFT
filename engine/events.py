import random


EVENTS = [

    {
        "name": "Cost-of-Living Crisis",

        "condition": lambda m:
            m["inflation"] > 6,

        "description":
            "Rapid price increases are creating widespread public frustration.",

        "effects": {
            "public_support": -4,
            "protest_risk": +6
        }
    },

    {
        "name": "Business Confidence Shock",

        "condition": lambda m:
            m["debt"] > 75,

        "description":
            "Investors are becoming increasingly concerned about government finances.",

        "effects": {
            "fdi": -5,
            "currency_strength": -3,
            "public_support": -1
        }
    },

    {
        "name": "Mass Demonstrations",

        "condition": lambda m:
            m["protest_risk"] > 65,

        "description":
            "Large demonstrations have appeared in major cities.",

        "effects": {
            "government_stability": -6,
            "legitimacy": -3
        }
    },

    {
        "name": "Economic Boom",

        "condition": lambda m:
            m["growth"] > 5,

        "description":
            "Strong economic performance has boosted confidence in the government.",

        "effects": {
            "public_support": +4,
            "government_stability": +3
        }
    },

    {
        "name": "Political Scandal",

        "condition": lambda m:
            random.random() < 0.05,

        "description":
            "A political scandal is damaging public confidence.",

        "effects": {
            "legitimacy": -5,
            "public_support": -4
        }
    },

    {
        "name": "Unexpected Foreign Crisis",

        "condition": lambda m:
            random.random() < 0.04,

        "description":
            "A sudden international development has increased pressure on the government.",

        "effects": {
            "international_tension": +8,
            "military_readiness": -2
        }
    }
]


def generate_event(state):

    metrics = state["metrics"]

    candidates = []

    for event in EVENTS:

        try:

            if event["condition"](metrics):

                candidates.append(event)

        except Exception:

            continue

    if not candidates:

        return None

    if random.random() > 0.35:

        return None

    event = random.choice(
        candidates
    )

    for key, value in event[
        "effects"
    ].items():

        if key in metrics:

            metrics[key] += value

    return {

        "year": state["year"],

        "title": event["name"],

        "description":
            event["description"],

        "effects":
            event["effects"]
    }
