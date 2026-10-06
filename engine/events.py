import random

# ==========================================================
# ADVANCED ERA-SPECIFIC ARCHIVE (LONG NARRATIVE DISPATCHES)
# ==========================================================

COMPLEX_ERA_POOLS = {
    # ------------------------------------------------------
    # 1. ANTIQUITY (3000 BCE – 500 CE)
    # ------------------------------------------------------
    "Antiquity (3000 BCE – 500 CE)": {
        "events": [
            {
                "id": "anc_floods",
                "title": "Imperial Decree: Bumper Harvest along the Sacred River",
                "desc": "Favorable seasonal flooding has inundated the central river basins with thick, mineral-rich silt. Local agrarian overseers report record-breaking grain yields across all crown provinces. Granaries are overflowing, stabilizing food prices and bolstering the state's strategic food reserves for upcoming campaigns.",
                "conditions": {},
                "effect": {"gdp": 6.0, "public_support": 5.0, "reserves": 5.0}
            },
            {
                "id": "anc_debt_crisis",
                "title": "Socio-Economic Unrest: Agrarian Debt Bondage Crisis",
                "desc": "Compounding dry seasons and exorbitant interest rates levied by patrician landowners have forced thousands of tenant farmers into permanent debt bondage. Dispossessed peasants have abandoned their ancestral plots to gather in squalid camps outside the capital walls, threatening widespread bread riots and radicalization.",
                "conditions": {"metrics.public_support": ("<", 50.0)},
                "effect": {"public_support": -7.0, "government_stability": -5.0, "groups.Working Class.radicalization": 15}
            },
            {
                "id": "anc_barbarian_raid",
                "title": "Frontier Dispatch: Nomadic Horsemen Cross Border Marches",
                "desc": "Swarms of nomadic horse-archers have broken through our frontier garrison watchtowers along the northern marches. Peripheral granaries have been torched, herds plundered, and trade caravans butchered. Border commanders urgently demand military reinforcements to restore order.",
                "conditions": {"metrics.military_readiness": ("<", 55.0)},
                "effect": {"gdp": -5.0, "military_readiness": 4.0, "regions.Periphery.unrest": 20}
            }
        ],
        "dilemmas": [
            {
                "id": "anc_dil_granary",
                "title": "The Great Granary Famine & The Sacred Cattle",
                "description": "Two consecutive years of brutal drought have emptied provincial reserves. The High Priesthood asserts that the gods are enraged by moral decline and demands the immediate sacrifice of thousands of prize cattle. Meanwhile, provincial governors warn that starving urban mobs are preparing to breach royal granaries by force.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Heed the Priesthood: Conduct grand ritual sacrifices across all major temples",
                        "effects": {"metrics.legitimacy": 8.0, "metrics.public_support": -5.0, "metrics.gdp": -4.0, "groups.Elites.approval": 10},
                        "follow_up": None
                    },
                    {
                        "label": "Open the State Granaries: Distribute emergency bread rations free to the populace",
                        "effects": {"metrics.public_support": 10.0, "metrics.reserves": -8.0, "groups.Working Class.approval": 15},
                        "follow_up": "anc_dil_granary_corrupt"
                    },
                    {
                        "label": "Military Requisition: Seize all remaining grain strictly to keep frontier legions fed",
                        "effects": {"metrics.military_readiness": 8.0, "metrics.public_support": -12.0, "regions.Periphery.unrest": 25},
                        "follow_up": "anc_dil_peasant_revolt"
                    }
                ]
            }
        ]
    },

    # ------------------------------------------------------
    # 2. INDUSTRIAL REVOLUTION & EMPIRE (1789 – 1914)
    # ------------------------------------------------------
    "Industrial Revolution & Empire (1789 – 1914)": {
        "events": [
            {
                "id": "ind_strike",
                "title": "Special Dispatch: General Coal Miners Strike Paralyzes Industry",
                "desc": "Organized labor syndicates across major coal basins have downed tools following a collapse in safety standards and wage cuts. Steam locomotives sit idle at railyards, factory blast furnaces are cooling, and municipal gas lighting in major cities is failing as reserves dwindle rapidly.",
                "conditions": {"groups.Working Class.radicalization": (">", 25)},
                "effect": {"gdp": -7.0, "inflation": 4.0, "government_stability": -6.0}
            },
            {
                "id": "ind_rail_boom",
                "title": "Economic Gazette: Opening of the Trans-Continental Trunk Line",
                "desc": "With the placement of the golden spike, heavy iron rails now connect deep-water Atlantic ports directly to inland mining networks and agrarian plains. Shipping costs have plummeted by 40%, sparking intense domestic manufacturing activity and foreign investment.",
                "conditions": {"metrics.gdp": (">", 70.0)},
                "effect": {"gdp": 8.0, "trade_openness": 6.0, "groups.Middle Class.wealth_share": 5}
            }
        ],
        "dilemmas": [
            {
                "id": "ind_dil_luddite",
                "title": "The Machine Sabotage & Automated Weaving Riots",
                "description": "Secret societies of skilled artisans whose livelihoods have been destroyed by automated steam looms have launched organized night attacks across industrial districts. Factories are burned, overseers ambushed, and industrial machinery smashed with heavy hammers.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Pass Frame Breaking Act: Deploy infantry regiments and hang ringleaders",
                        "effects": {"metrics.government_stability": 7.0, "metrics.public_support": -9.0, "groups.Working Class.radicalization": 20},
                        "follow_up": "ind_dil_labor_martyrs"
                    },
                    {
                        "label": "Establish Labor Arbitration & Safety Limits: Legalize trade unions and regulate hours",
                        "effects": {"metrics.public_support": 8.0, "metrics.gdp": -3.0, "groups.Elites.approval": -15, "groups.Working Class.approval": 20},
                        "follow_up": None
                    }
                ]
            }
        ]
    },

    # ------------------------------------------------------
    # 3. MODERN & INFORMATION ERA (1991 – PRESENT)
    # ------------------------------------------------------
    "Modern & Information Era (1991 – Present)": {
        "events": [
            {
                "id": "mod_cyber_attack",
                "title": "Cybersecurity Alert: State-Sponsored Ransomware Paralyzes Grid",
                "desc": "A sophisticated zero-day cyber attack linked to hostile foreign intelligence agencies has encrypted primary supervisory control servers. Regional power grids, water treatment distribution centers, and hospital emergency networks across three provinces are operating on emergency generators.",
                "conditions": {"metrics.international_tension": (">", 35.0)},
                "effect": {"gdp": -6.0, "government_stability": -5.0, "metrics.military_readiness": -4.0}
            }
        ],
        "dilemmas": [
            {
                "id": "mod_dil_tech_monopoly",
                "title": "Big Tech Data Sovereignty & Antitrust Standoff",
                "description": "Multinational tech monopolies controlling national communications infrastructure threaten to pull cloud operations and digital payments out of the state if bipartisan privacy regulations and antitrust breakups are signed into law.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Enforce Strict Antitrust Breakups: Mandate algorithmic audits and data ownership",
                        "effects": {"metrics.legitimacy": 8.0, "metrics.public_support": 7.0, "metrics.fdi": -10.0, "metrics.gdp": -4.0},
                        "follow_up": None
                    },
                    {
                        "label": "Grant Full Exemption: Partner with tech monopolies for military AI surveillance contracts",
                        "effects": {"metrics.fdi": 10.0, "metrics.gdp": 6.0, "metrics.public_support": -8.0, "groups.Elites.wealth_share": 10},
                        "follow_up": "mod_dil_deepfake_crisis"
                    }
                ]
            }
        ]
    }
}

# Dynamic Follow-Up Chained Dilemmas Database
CHAINED_FOLLOW_UPS = {
    "anc_dil_granary_corrupt": {
        "title": "Corrupt Granary Official Embezzlement",
        "description": "Audit inspectors reveal that the emergency grain distribution program was hijacked by corrupt provincial magistrates, who resold state food stocks on the black market at extortionate prices while citizens starved.",
        "choices": [
            {
                "label": "Public Execution: Execute corrupt magistrates and confiscate their estates",
                "effects": {"metrics.legitimacy": 6.0, "metrics.government_stability": 4.0, "groups.Elites.approval": -10}
            },
            {
                "label": "Privatize Distribution: Sell granary concessions directly to wealthy merchant houses",
                "effects": {"metrics.reserves": 5.0, "metrics.public_support": -6.0, "groups.Middle Class.wealth_share": 5}
            }
        ]
    },
    "anc_dil_peasant_revolt": {
        "title": "The Northern Peasant Insurrection",
        "description": "Enraged by military grain requisitions, peripheral peasant militias armed with scythes have ambushed army supply columns and seized control of provincial fortresses.",
        "choices": [
            {
                "label": "Send the Legions: Iron-fisted suppression and destruction of rebellious villages",
                "effects": {"metrics.government_stability": 5.0, "regions.Periphery.stability": -20, "metrics.public_support": -10.0}
            },
            {
                "label": "Issue Royal Pardons: Return seized grain and reduce provincial tax burdens",
                "effects": {"metrics.public_support": 8.0, "metrics.military_readiness": -8.0, "regions.Periphery.unrest": -15}
            }
        ]
    },
    "ind_dil_labor_martyrs": {
        "title": "The Factory Riots Martyr Trial",
        "description": "Public hangings of union leaders have backfired severely. Executed organizers have been elevated as political martyrs, triggering sympathy strikes across transit, docks, and steel mills nationwide.",
        "choices": [
            {
                "label": "Declare State of Siege: Ban all public assemblies and suspend habeas corpus",
                "effects": {"metrics.government_stability": -8.0, "metrics.public_support": -15.0, "groups.Working Class.radicalization": 30}
            },
            {
                "label": "Capitulate to Demands: Grant an 8-hour workday and fund worker pensions",
                "effects": {"metrics.public_support": 12.0, "metrics.gdp": -4.0, "groups.Working Class.radicalization": -20}
            }
        ]
    },
    "mod_dil_deepfake_crisis": {
        "title": "AI Deepfake Political Scandal",
        "description": "Unregulated Big Tech AI algorithms have generated hyper-realistic synthetic audio depicting top state ministers accepting foreign bribes, sparking public outrage.",
        "choices": [
            {
                "label": "Shut Down Social Media Networks nationwide during investigation",
                "effects": {"metrics.government_stability": -5.0, "metrics.legitimacy": -8.0, "metrics.public_support": -10.0}
            },
            {
                "label": "Pass Digital Verification Laws and Subsidize Independent Fact-Checking",
                "effects": {"metrics.reserves": -5.0, "metrics.legitimacy": 5.0, "metrics.public_support": 4.0}
            }
        ]
    }
}


# ==========================================================
# PROCEDURAL HIGH-VARIETY RANDOM EVENT GENERATOR
# ==========================================================

PROCEDURAL_TEMPLATES = {
    "subjects": [
        "High-ranking naval admirals", "Prominent merchant syndicates", "Radical university student leagues",
        "Discontented agrarian guilds", "Foreign diplomatic attachés", "Regional mining magnates",
        "Dissident clergy members", "Provincial paramilitary groups"
    ],
    "actions": [
        "have launched a coordinated campaign demanding sweeping institutional reform",
        "are caught in an international financial embezzlement scandal",
        "have orchestrated widespread strikes across critical infrastructure nodes",
        "were discovered running a clandestine intelligence network",
        "have issued an ultimatum concerning regional taxation rights",
        "uncovered rich natural resource deposits in peripheral territories"
    ],
    "impacts": [
        "causing significant panic on national credit exchanges and volatile currency drops.",
        "forcing government ministers into emergency closed-door cabinet sessions.",
        "leading to clashes with local law enforcement and civil disruptions.",
        "boosting state revenue projections while triggering environmental protests.",
        "sparking intense international media scrutiny and foreign diplomatic friction."
    ]
}

def generate_procedural_event(state):
    """
    Generates a unique, randomized event with dynamic stat consequences.
    """
    subj = random.choice(PROCEDURAL_TEMPLATES["subjects"])
    act = random.choice(PROCEDURAL_TEMPLATES["actions"])
    imp = random.choice(PROCEDURAL_TEMPLATES["impacts"])
    
    title = f"Special Report: {subj} Incident"
    description = f"Official dispatches confirm that {subj.lower()} {act}, {imp}"
    
    # Random stat mutations
    possible_stats = ["gdp", "public_support", "government_stability", "legitimacy", "reserves", "inflation"]
    chosen_stat = random.choice(possible_stats)
    delta = random.choice([-5.0, -4.0, -3.0, 3.0, 4.0, 5.0])
    
    return {
        "title": title,
        "desc": description,
        "effect": {chosen_stat: delta}
    }


# ==========================================================
# STATE EVALUATION & MUTATION ENGINE
# ==========================================================

def evaluate_condition(state, path_str, operator, target_val):
    keys = path_str.split(".")
    curr = state
    try:
        for k in keys:
            curr = curr[k]
        
        if operator == "<":
            return float(curr) < float(target_val)
        elif operator == ">":
            return float(curr) > float(target_val)
        elif operator == "==":
            return curr == target_val
    except (KeyError, TypeError, ValueError):
        return False
    return False


def apply_nested_effect(state, path_str, delta):
    keys = path_str.split(".")
    curr = state
    for k in keys[:-1]:
        if k not in curr:
            return
        curr = curr[k]
    
    target_key = keys[-1]
    if target_key in curr:
        curr[target_key] += delta


def get_era_pool(era_name):
    if era_name in COMPLEX_ERA_POOLS:
        return COMPLEX_ERA_POOLS[era_name]
    
    for key in COMPLEX_ERA_POOLS:
        if "Ancient" in era_name or "Antiquity" in era_name:
            return COMPLEX_ERA_POOLS["Antiquity (3000 BCE – 500 CE)"]
        elif "Industrial" in era_name:
            return COMPLEX_ERA_POOLS["Industrial Revolution & Empire (1789 – 1914)"]
        elif "Modern" in era_name or "Information" in era_name:
            return COMPLEX_ERA_POOLS["Modern & Information Era (1991 – Present)"]
            
    return COMPLEX_ERA_POOLS["Modern & Information Era (1991 – Present)"]


def trigger_era_event(state, game):
    # 1. Check for queued chained dilemma
    if not state.get("active_dilemma") and state.get("queued_dilemma"):
        follow_up_id = state.pop("queued_dilemma")
        if follow_up_id in CHAINED_FOLLOW_UPS:
            state["active_dilemma"] = CHAINED_FOLLOW_UPS[follow_up_id]
            return

    era_name = game.get("era", "")
    pool = get_era_pool(era_name)
    
    # 2. Trigger Dilemma (45% probability per turn)
    if not state.get("active_dilemma") and random.random() < 0.45 and pool["dilemmas"]:
        valid_dilemmas = []
        for d in pool["dilemmas"]:
            conditions = d.get("conditions", {})
            met = all(evaluate_condition(state, path, op, val) for path, (op, val) in conditions.items())
            if met:
                valid_dilemmas.append(d)
                
        if valid_dilemmas:
            state["active_dilemma"] = random.choice(valid_dilemmas)

    # 3. Trigger Era Event OR Dynamic Procedural Event
    selected_event = None
    if pool["events"] and random.random() < 0.60:
        valid_events = []
        for e in pool["events"]:
            conditions = e.get("conditions", {})
            met = all(evaluate_condition(state, path, op, val) for path, (op, val) in conditions.items())
            if met:
                valid_events.append(e)
        if valid_events:
            selected_event = random.choice(valid_events)

    # Fallback to procedural generator for unlimited randomness
    if not selected_event:
        selected_event = generate_procedural_event(state)

    # Apply event
    state["events"].append({
        "year": state["year"],
        "title": selected_event["title"],
        "description": selected_event["desc"]
    })
    
    for key_path, delta in selected_event["effect"].items():
        if "." in key_path:
            apply_nested_effect(state, key_path, delta)
        elif key_path in state["metrics"]:
            state["metrics"][key_path] += delta


def resolve_dilemma(state, choice_idx):
    dilemma = state.get("active_dilemma")
    if not dilemma:
        return
    
    if choice_idx < 0 or choice_idx >= len(dilemma["choices"]):
        choice_idx = 0
        
    choice = dilemma["choices"][choice_idx]
    
    for path_str, delta in choice["effects"].items():
        if "." in path_str:
            apply_nested_effect(state, path_str, delta)
        elif path_str in state["metrics"]:
            state["metrics"][path_str] += delta
            
    if choice.get("follow_up"):
        state["queued_dilemma"] = choice["follow_up"]
        
    state["events"].append({
        "year": state["year"],
        "title": f"Executive Decree: {dilemma['title']}",
        "description": f"Enacted Order: '{choice['label']}'."
    })
    
    state["active_dilemma"] = None
