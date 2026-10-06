import random

ERA_EVENT_POOLS = {
    "Ancient Era": {
        "events": [
            {"title": "Bumper Harvest along the River", "desc": "Favorable flooding has blessed our fields with unprecedented grain yields.", "effect": {"gdp": 5, "public_support": 4}},
            {"title": "Temple Desecration Rumors", "desc": "Priests claim the local gods are angered by lax sacrifices and moral decay.", "effect": {"government_stability": -3, "legitimacy": -4}},
            {"title": "Border Nomadic Raids", "desc": "Nomadic horsemen probe our border fortresses, testing the strength of our guards.", "effect": {"military_readiness": 2, "gdp": -2}}
        ],
        "dilemmas": [
            {
                "title": "The Great Granary Crisis",
                "description": "A severe drought threatens grain reserves. The high priests demand massive ritual offerings of cattle, while provincial governors warn of bread riots.",
                "choices": [
                    {"label": "Heed the Priests: Perform lavish ritual sacrifices", "effects": {"legitimacy": 6, "public_support": 2, "gdp": -4}},
                    {"label": "Distribute Grain to the Masses", "effects": {"public_support": 7, "government_stability": -2, "reserves": -5}},
                    {"label": "Consolidate supplies strictly for the border legions", "effects": {"military_readiness": 5, "public_support": -6}}
                ]
            },
            {
                "title": "Corvée Labor Dispute",
                "description": "Peasants drafted for the construction of the royal monument are threatening to desert before the harvest season begins.",
                "choices": [
                    {"label": "Send the guards to crush dissent and accelerate quotas", "effects": {"government_stability": 5, "public_support": -8, "legitimacy": -3}},
                    {"label": "Grant temporary leave for harvesting", "effects": {"public_support": 4, "gdp": 2, "legitimacy": -2}},
                    {"label": "Hire foreign bondmen to replace them at great expense", "effects": {"gdp": -6, "public_support": 3}}
                ]
            }
        ]
    },
    "Middle Ages & Feudalism (500 – 1500 CE)": {
        "events": [
            {"title": "Baron Rebellion Suppressed", "desc": "A rebellious lord has submitted to the crown after his keep was besieged.", "effect": {"government_stability": 4, "legitimacy": 5}},
            {"title": "Monastic Codex Completed", "desc": "Local scribes have finished copying ancient texts, boosting scholarly prestige.", "effect": {"legitimacy": 3}},
            {"title": "Guild Monopoly Dispute", "desc": "Merchants and craftsmen guilds are feuding over market rights and taxation.", "effect": {"inflation": 1, "gdp": -2}}
        ],
        "dilemmas": [
            {
                "title": "The Bishop's Tithe Conflict",
                "description": "The local Church hierarchy demands higher tithes and judicial autonomy from secular royal courts.",
                "choices": [
                    {"label": "Yield to the Church to secure divine sanction", "effects": {"legitimacy": 8, "public_support": -4, "government_stability": -2}},
                    {"label": "Assert royal supremacy and tax ecclesiastical lands", "effects": {"government_stability": 5, "legitimacy": -7, "reserves": 6}},
                    {"label": "Compromise via diplomatic council", "effects": {"public_support": 2, "legitimacy": 1}}
                ]
            }
        ]
    },
    "Industrial Revolution & Empire (1789 – 1914)": {
        "events": [
            {"title": "Railway Expansion Boom", "desc": "New locomotive networks connect distant manufacturing hubs to coastal ports.", "effect": {"gdp": 6, "inflation": 1}},
            {"title": "Factory Workers Strike", "desc": "Laborers in the textile sector demand a ten-hour workday and safer conditions.", "effect": {"public_support": -4, "government_stability": -3}},
            {"title": "Telegraph Breakthrough", "desc": "Instantaneous communication across major cities drastically improves bureaucratic efficiency.", "effect": {"legitimacy": 3, "gdp": 2}}
        ],
        "dilemmas": [
            {
                "title": "The Luddite Machine Riots",
                "description": "Desperate artisans whose livelihoods have been destroyed by automated factory looms are burning down textile mills.",
                "choices": [
                    {"label": "Deploy the military to protect industrial property ruthlessly", "effects": {"government_stability": 6, "public_support": -7, "gdp": 3}},
                    {"label": "Pass welfare relief and regulate mechanization limits", "effects": {"public_support": 6, "gdp": -4, "budget": -3}},
                    {"label": "Subsidize retraining programs for displaced artisans", "effects": {"gdp": -2, "public_support": 4, "reserves": -4}}
                ]
            }
        ]
    }
}

def trigger_era_event(state, game):
    era_name = game.get("era", "Ancient Era")
    # Fallback to Ancient Era if the exact text key isn't found
    pool = ERA_EVENT_POOLS.get(era_name, ERA_EVENT_POOLS["Ancient Era"])
    
    # 35% chance to trigger an active dilemma if one isn't already active
    if not state.get("active_dilemma") and random.random() < 0.35 and pool["dilemmas"]:
        dilemma = random.choice(pool["dilemmas"])
        state["active_dilemma"] = dilemma
    
    # Pull a standard flavor event
    event_template = random.choice(pool["events"])
    new_event = {
        "year": state["year"],
        "title": event_template["title"],
        "description": event_template["desc"]
    }
    
    state["events"].append(new_event)
    
    # Apply baseline effects safely
    metrics = state["metrics"]
    for k, v in event_template["effect"].items():
        if k in metrics:
            metrics[k] += v

def resolve_dilemma(state, choice_idx):
    dilemma = state.get("active_dilemma")
    if not dilemma:
        return
    
    choice = dilemma["choices"][choice_idx]
    metrics = state["metrics"]
    
    for k, v in choice["effects"].items():
        if k in metrics:
            metrics[k] += v
            
    # Record choice into historical events log
    state["events"].append({
        "year": state["year"],
        "title": f"Resolved: {dilemma['title']}",
        "description": f"Executive choice selected: '{choice['label']}'."
    })
    
    state["active_dilemma"] = None
