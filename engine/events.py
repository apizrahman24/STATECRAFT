import random

# ==========================================================
# ADVANCED STATE-MUTATING EVENT & DILEMMA ARCHIVE
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
                "desc": "Favorable seasonal flooding has inundated the central river basins with mineral-rich silt. Local agrarian overseers report record grain yields. Granaries are overflowing, stabilizing food prices and bolstering state food reserves for upcoming military campaigns.",
                "conditions": {},
                "effect": {"gdp": 6.0, "public_support": 5.0, "reserves": 5.0}
            },
            {
                "id": "anc_debt_crisis",
                "title": "Socio-Economic Unrest: Agrarian Debt Bondage Crisis",
                "desc": "Compounding dry seasons and exorbitant interest rates levied by patrician landowners have forced thousands of tenant farmers into permanent debt slavery. Dispossessed peasants gather outside the capital walls, threatening bread riots and radicalization.",
                "conditions": {"metrics.public_support": ("<", 50.0)},
                "effect": {"public_support": -7.0, "government_stability": -5.0, "groups.Working Class.radicalization": 15}
            },
            {
                "id": "anc_barbarian_raid",
                "title": "Frontier Dispatch: Nomadic Horsemen Cross Border Marches",
                "desc": "Swarms of nomadic horse-archers have broken through frontier watchtowers along the northern marches. Peripheral granaries have been torched, herds plundered, and trade caravans butchered.",
                "conditions": {"metrics.military_readiness": ("<", 55.0)},
                "effect": {"gdp": -5.0, "military_readiness": 4.0, "regions.Periphery.unrest": 20}
            }
        ],
        "dilemmas": [
            {
                "id": "anc_dil_granary",
                "title": "The Great Granary Famine & The Sacred Cattle",
                "description": "Two consecutive years of drought have emptied provincial grain reserves. The High Priesthood asserts that the gods demand the immediate sacrifice of thousands of prize cattle, while provincial governors warn that starving mobs are preparing to breach royal granaries by force.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Heed the Priesthood: Conduct grand ritual sacrifices across all major temples",
                        "effects": {"metrics.legitimacy": 8.0, "metrics.public_support": -5.0, "metrics.gdp": -4.0, "groups.Elites.approval": 10},
                        "follow_up": None
                    },
                    {
                        "label": "Open the Granaries: Distribute emergency bread rations free to the masses",
                        "effects": {"metrics.public_support": 10.0, "metrics.reserves": -8.0, "groups.Working Class.approval": 15},
                        "follow_up": "anc_dil_granary_corrupt"
                    },
                    {
                        "label": "Military Requisition: Seize all remaining grain strictly to feed frontier legions",
                        "effects": {"metrics.military_readiness": 8.0, "metrics.public_support": -12.0, "regions.Periphery.unrest": 25},
                        "follow_up": "anc_dil_peasant_revolt"
                    }
                ]
            },
            {
                "id": "anc_dil_slave_rebellion",
                "title": "The Gladiatorial & Agrarian Slave Uprising",
                "description": "A charismatic escaped gladiator has rallied thousands of runaway agricultural slaves, defeated a provincial garrison, and seized control of the southern silver mines.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Crush the Revolt Ruthlessly: Crucify captured rebels along the royal highway",
                        "effects": {"metrics.government_stability": 8.0, "metrics.public_support": -8.0, "groups.Elites.approval": 15, "groups.Working Class.radicalization": 20},
                        "follow_up": "anc_dil_crucifixion_outrage"
                    },
                    {
                        "label": "Offer Manumission & Land Grants: Incorporate former slaves into auxiliary legions",
                        "effects": {"metrics.military_readiness": 6.0, "metrics.legitimacy": -8.0, "groups.Elites.approval": -20, "groups.Working Class.approval": 15},
                        "follow_up": None
                    }
                ]
            },
            {
                "id": "anc_dil_temple_tax",
                "title": "The High Priest's Autonomy Mandate",
                "description": "The High Priest demands that all temple estates, sacred gold vaults, and clerical lands be granted permanent immunity from royal tax collectors and military requisitions.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Grant Full Sacred Immunity: Cede clerical tax autonomy to secure divine blessing",
                        "effects": {"metrics.legitimacy": 10.0, "metrics.reserves": -6.0, "metrics.government_stability": -4.0},
                        "follow_up": None
                    },
                    {
                        "label": "Storm the Holy Vaults: Requisition temple gold for state defensive infrastructure",
                        "effects": {"metrics.reserves": 12.0, "metrics.legitimacy": -12.0, "metrics.public_support": -8.0, "groups.Elites.approval": -10},
                        "follow_up": "anc_dil_priest_excommunication"
                    }
                ]
            }
        ]
    },

    # ------------------------------------------------------
    # 2. MIDDLE AGES & FEUDALISM (500 – 1500 CE)
    # ------------------------------------------------------
    "Middle Ages & Feudalism (500 – 1500 CE)": {
        "events": [
            {
                "id": "mid_baron_war",
                "title": "Feudal Crisis: Baronial Feud Escalates in Peripheral Duchies",
                "desc": "Two powerful Dukes have mobilized private armies of knights over disputed fiefdoms, burning peasant hamlets and disrupting overland trade routes.",
                "conditions": {},
                "effect": {"government_stability": -6.0, "gdp": -4.0, "legitimacy": -3.0}
            },
            {
                "id": "mid_plague",
                "title": "Pandemic Alert: Black Pestilence Strikes Port Hubs",
                "desc": "A contagious pestilence spread by maritime galleys is ravaging coastal markets. Labor shortages are severe, stopping harvest collection.",
                "conditions": {"metrics.public_support": ("<", 60.0)},
                "effect": {"gdp": -8.0, "unemployment": 4.0, "public_support": -6.0}
            }
        ],
        "dilemmas": [
            {
                "id": "mid_dil_papal_interdict",
                "title": "The Crown vs. Church Investiture Crisis",
                "description": "The Holy See has issued a Papal Bull forbidding the King from appointing local Bishops. If the monarch refuses to yield royal investiture rights, the Pope threatens excommunication and a Kingdom-wide Interdict.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Submit to Rome: Surrender bishopric appointments to the Holy See",
                        "effects": {"metrics.legitimacy": 9.0, "metrics.government_stability": -5.0, "groups.Elites.approval": -10},
                        "follow_up": None
                    },
                    {
                        "label": "Defy the Papacy: Ban papal legates and confiscate ecclesiastical court fees",
                        "effects": {"metrics.reserves": 8.0, "metrics.legitimacy": -10.0, "metrics.public_support": -8.0},
                        "follow_up": "mid_dil_crusader_rebellion"
                    }
                ]
            },
            {
                "id": "mid_dil_guild_charter",
                "title": "The Free City Merchant Charter Request",
                "description": "The wealthy Weaver and Armorer Guilds offer a vast treasury loan in exchange for a Royal Charter granting their city self-governance, independent courts, and exemption from feudal labor duties.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Grant the Free City Charter: Empower self-governing urban merchant republics",
                        "effects": {"metrics.gdp": 9.0, "metrics.reserves": 8.0, "groups.Elites.approval": -15, "groups.Middle Class.approval": 20},
                        "follow_up": "mid_dil_feudal_lord_backlash"
                    },
                    {
                        "label": "Protect Feudal Privileges: Reaffirm the local Duke's hereditary feudal domain",
                        "effects": {"metrics.government_stability": 6.0, "metrics.legitimacy": 4.0, "metrics.gdp": -4.0, "groups.Middle Class.approval": -15},
                        "follow_up": None
                    }
                ]
            },
            {
                "id": "mid_dil_heresy_outbreak",
                "title": "The Dualist Radical Heresy in the South",
                "description": "A charismatic itinerant preacher has converted three southern provinces to an anti-feudal religious doctrine that rejects royal taxation, noble marriage, and feudal oaths.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Launch an Internal Crusade: Authorize inquisitors and knightly orders to purge heresy",
                        "effects": {"metrics.legitimacy": 8.0, "regions.Periphery.stability": -25, "metrics.public_support": -8.0},
                        "follow_up": "mid_dil_heretic_martyrs"
                    },
                    {
                        "label": "Grant Toleration Charter: Protect southern religious customs in exchange for tribute",
                        "effects": {"metrics.reserves": 6.0, "metrics.legitimacy": -12.0, "groups.Elites.approval": -15},
                        "follow_up": None
                    }
                ]
            }
        ]
    },

    # ------------------------------------------------------
    # 3. EARLY MODERN & COLONIAL ERA (1500 – 1789)
    # ------------------------------------------------------
    "Early Modern & Colonial Era (1500 – 1789)": {
        "events": [
            {
                "id": "ear_treasure_fleet",
                "title": "Maritime Dispatch: Overseas Gold & Silver Fleet Arrives",
                "desc": "Galleons laden with bullion from colonial mines have docked safely, pouring treasure into royal vaults but stoking domestic price inflation.",
                "conditions": {},
                "effect": {"reserves": 10.0, "inflation": 4.5, "gdp": 3.0}
            },
            {
                "id": "ear_printing_subversion",
                "title": "Intellectual Crisis: Printing Press Pamphlet Wars",
                "desc": "Underground print shops circulate radical pamphlets questioning the divine right of kings and exposing royal court expenditures.",
                "conditions": {},
                "effect": {"legitimacy": -6.0, "government_stability": -4.0, "public_support": 3.0}
            }
        ],
        "dilemmas": [
            {
                "id": "ear_dil_privateers",
                "title": "The Imperial Monopoly & Caribbean Privateer Crisis",
                "description": "Rival empire privateers are decimating state colonial shipping. The chartered state trading company demands naval escorts, while independent merchants demand an end to monopoly charters.",
                "choices": [
                    {
                        "label": "Deploy the High Seas Armada: Fund massive naval escorts for state convoys",
                        "effects": {"metrics.military_readiness": 8.0, "metrics.reserves": -7.0, "metrics.international_tension": 6.0, "metrics.gdp": 5.0},
                        "follow_up": None
                    },
                    {
                        "label": "Abolish Company Monopolies: Open colonial trade lanes to all private free traders",
                        "effects": {"metrics.trade_openness": 10.0, "metrics.gdp": 7.0, "groups.Elites.wealth_share": -10, "groups.Middle Class.wealth_share": 10},
                        "follow_up": "ear_dil_monopoly_lawsuit"
                    },
                    {
                        "label": "Commission State Privateers: License pirate captains to raid enemy commerce in return",
                        "effects": {"metrics.reserves": 6.0, "metrics.international_tension": 8.0, "metrics.legitimacy": -5.0},
                        "follow_up": "ear_dil_pirate_mutiny"
                    }
                ]
            },
            {
                "id": "ear_dil_court_extravagance",
                "title": "Royal Palace Construction vs. Peasant Bread Taxes",
                "description": "The royal court is constructing a sprawling palace complex to showcase royal grandeur, funded by an unpopular salt and flour tax levied on agrarian provinces.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Complete the Grand Palace: Display absolute monarchical magnificence",
                        "effects": {"metrics.legitimacy": 8.0, "metrics.public_support": -10.0, "metrics.debt": 6.0, "groups.Elites.approval": 12},
                        "follow_up": "ear_dil_palace_jacquerie"
                    },
                    {
                        "label": "Halt Construction & Repeal Salt Taxes: Redirect funds to grain reserves",
                        "effects": {"metrics.public_support": 9.0, "metrics.legitimacy": -4.0, "metrics.debt": -3.0, "groups.Elites.approval": -10},
                        "follow_up": None
                    }
                ]
            }
        ]
    },

    # ------------------------------------------------------
    # 4. INDUSTRIAL REVOLUTION & EMPIRE (1789 – 1914)
    # ------------------------------------------------------
    "Industrial Revolution & Empire (1789 – 1914)": {
        "events": [
            {
                "id": "ind_strike",
                "title": "Special Dispatch: General Coal Miners Strike Paralyzes Industry",
                "desc": "Organized labor syndicates across major coal basins have downed tools following wage cuts. Steam locomotives sit idle at railyards and factory blast furnaces are cooling.",
                "conditions": {"groups.Working Class.radicalization": (">", 25)},
                "effect": {"gdp": -7.0, "inflation": 4.0, "government_stability": -6.0}
            },
            {
                "id": "ind_rail_boom",
                "title": "Economic Gazette: Opening of the Trans-Continental Trunk Line",
                "desc": "Iron rails now connect deep-water Atlantic ports directly to inland mining networks and agrarian plains, slashing freight transit costs by 40%.",
                "conditions": {"metrics.gdp": (">", 70.0)},
                "effect": {"gdp": 8.0, "trade_openness": 6.0, "groups.Middle Class.wealth_share": 5}
            }
        ],
        "dilemmas": [
            {
                "id": "ind_dil_luddite",
                "title": "The Machine Sabotage & Automated Weaving Riots",
                "description": "Secret societies of skilled artisans whose livelihoods have been destroyed by automated steam looms have launched night attacks across industrial districts, destroying mechanized looms with hammers.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Pass Frame Breaking Act: Deploy infantry regiments and execute ringleaders",
                        "effects": {"metrics.government_stability": 7.0, "metrics.public_support": -9.0, "groups.Working Class.radicalization": 20},
                        "follow_up": "ind_dil_labor_martyrs"
                    },
                    {
                        "label": "Establish Labor Arbitration Courts: Legalize trade unions and regulate working hours",
                        "effects": {"metrics.public_support": 8.0, "metrics.gdp": -3.0, "groups.Elites.approval": -15, "groups.Working Class.approval": 20},
                        "follow_up": None
                    }
                ]
            },
            {
                "id": "ind_dil_corn_laws",
                "title": "The Grain Protection Tariff Standoff",
                "description": "Industrial factory owners demand the immediate repeal of tariffs on foreign grain to lower worker food costs, while aristocratic landowners warn cheap imports will ruin domestic agriculture.",
                "choices": [
                    {
                        "label": "Abolish Grain Tariffs: Embrace unilateral global free trade",
                        "effects": {"metrics.gdp": 8.0, "metrics.inflation": -3.5, "metrics.trade_openness": 9.0, "groups.Elites.approval": -20},
                        "follow_up": "ind_dil_rural_landed_rebellion"
                    },
                    {
                        "label": "Maintain High Protectionist Tariffs: Protect agrarian noble estates",
                        "effects": {"metrics.legitimacy": 6.0, "metrics.gdp": -4.0, "metrics.inflation": 3.0, "groups.Working Class.approval": -12},
                        "follow_up": None
                    }
                ]
            },
            {
                "id": "ind_dil_child_labor",
                "title": "The Factory Acts & Child Labor Inquiry",
                "description": "A Parliamentary commission exposes appalling conditions where children as young as seven work 16-hour shifts in coal mines and textile mills.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Pass Comprehensive Factory Acts: Mandate compulsory schooling and ban under-13 labor",
                        "effects": {"metrics.public_support": 9.0, "metrics.gdp": -3.0, "groups.Elites.approval": -10, "groups.Working Class.approval": 15},
                        "follow_up": "ind_dil_factory_owner_lockout"
                    },
                    {
                        "label": "Reject State Regulation: Protect free contract rights and industrial output",
                        "effects": {"metrics.gdp": 4.0, "metrics.public_support": -8.0, "groups.Working Class.radicalization": 15},
                        "follow_up": None
                    }
                ]
            }
        ]
    },

    # ------------------------------------------------------
    # 5. THE AGE OF CRISES & WORLD WARS (1914 – 1945)
    # ------------------------------------------------------
    "The Age of Crises & World Wars (1914 – 1945)": {
        "events": [
            {
                "id": "ww_war_economy",
                "title": "War Cabinet Decree: Total Industrial Re-Tooling",
                "desc": "Automotive and locomotive assembly lines have been requisitioned for tank and artillery shell manufacturing to supply frontline armies.",
                "conditions": {},
                "effect": {"military_readiness": 9.0, "gdp": 3.0, "debt": 6.0, "inflation": 3.0}
            },
            {
                "id": "ww_hyperinflation",
                "title": "Economic Collapse: Uncontrolled Paper Currency Printing",
                "desc": "Uncontrolled printing of unbacked paper currency to finance war expenditures has triggered hyperinflation. Savings are wiped out.",
                "conditions": {"metrics.debt": (">", 80.0)},
                "effect": {"inflation": 9.0, "public_support": -9.0, "government_stability": -7.0}
            }
        ],
        "dilemmas": [
            {
                "id": "ww_dil_conscription",
                "title": "Frontline Manpower Crisis vs. Munitions Output",
                "description": "High frontline casualties require immediate military reinforcement. Generals demand drafting half a million industrial factory workers, while arms manufacturers warn shell production will plummet.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Enforce Factory Conscription: Prioritize military manpower for immediate offensives",
                        "effects": {"metrics.military_readiness": 12.0, "metrics.gdp": -8.0, "metrics.public_support": -7.0},
                        "follow_up": "ww_dil_munitions_shortage"
                    },
                    {
                        "label": "Protect Industrial Conscription Exemptions: Mobilize civilian women into heavy war factories",
                        "effects": {"metrics.gdp": 5.0, "metrics.public_support": 5.0, "metrics.government_stability": -3.0, "groups.Working Class.approval": 10},
                        "follow_up": None
                    }
                ]
            },
            {
                "id": "ww_dil_dissent_censorship",
                "title": "Anti-War General Strike & Subversive Propaganda",
                "description": "Radical anti-war pacifist leagues and socialist unions are printing underground newspapers urging soldiers to mutiny and factory workers to sabotage munitions.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Institute Emergency Sedition Acts: Suspend habeas corpus, ban anti-war unions, and imprison editors",
                        "effects": {"metrics.government_stability": 8.0, "metrics.public_support": -10.0, "metrics.legitimacy": -6.0},
                        "follow_up": "ww_dil_prison_strike"
                    },
                    {
                        "label": "Permit Peace Assemblies: Offer political concessions and open negotiations",
                        "effects": {"metrics.public_support": 8.0, "metrics.military_readiness": -10.0, "metrics.government_stability": -6.0},
                        "follow_up": None
                    }
                ]
            }
        ]
    },

    # ------------------------------------------------------
    # 6. COLD WAR & ATOMIC AGE (1945 – 1991)
    # ------------------------------------------------------
    "Cold War & Atomic Age (1945 – 1991)": {
        "events": [
            {
                "id": "cw_nuke_test",
                "title": "Strategic Dispatch: Successful Thermonuclear Test",
                "desc": "The nation has successfully detonated a hydrogen warhead at an island proving ground, confirming second-strike nuclear deterrence capability.",
                "conditions": {},
                "effect": {"military_readiness": 9.0, "international_tension": 8.0, "legitimacy": 6.0}
            },
            {
                "id": "cw_space_launch",
                "title": "Scientific Triumph: Satellite Placed into Orbit",
                "desc": "National space agency scientists have successfully launched an orbital satellite, proving long-range missile and technological parity.",
                "conditions": {},
                "effect": {"legitimacy": 8.0, "fdi": 4.0, "gdp": 3.0}
            }
        ],
        "dilemmas": [
            {
                "id": "cw_dil_missile_crisis",
                "title": "The Border Ballistic Missile Standoff",
                "description": "Hostile rival superpower intelligence reveals nuclear ballistic missile silos are under construction in a neighboring border state. Military chiefs demand a naval blockade and pre-emptive surgical airstrikes.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Enforce Military Naval Quarantine: Threaten nuclear retaliatory war if missiles are not dismantled",
                        "effects": {"metrics.international_tension": 15.0, "metrics.military_readiness": 10.0, "metrics.government_stability": 5.0, "metrics.gdp": -4.0},
                        "follow_up": "cw_dil_blockade_incident"
                    },
                    {
                        "label": "Initiate Secret Backchannel Diplomacy: Offer trade concessions and missile reductions in exchange for withdrawal",
                        "effects": {"metrics.diplomacy": 10.0, "metrics.international_tension": -10.0, "metrics.military_readiness": -5.0, "metrics.legitimacy": -4.0},
                        "follow_up": None
                    }
                ]
            },
            {
                "id": "cw_dil_red_scare",
                "title": "Ideological Subversion & Domestic Spy Rings",
                "description": "Counter-intelligence agencies report that enemy spies have embedded sleeper cells inside university faculties, nuclear research facilities, and state broadcasting networks.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Establish Domestic Surveillance Committees: Blacklist suspects and mandate loyalty oaths",
                        "effects": {"metrics.government_stability": 7.0, "metrics.public_support": -8.0, "metrics.legitimacy": -5.0, "groups.Middle Class.approval": -10},
                        "follow_up": "cw_dil_academic_exodus"
                    },
                    {
                        "label": "Uphold Civil Liberties: Require transparent judicial search warrants for all wiretaps",
                        "effects": {"metrics.public_support": 8.0, "metrics.legitimacy": 7.0, "metrics.government_stability": -5.0, "metrics.military_readiness": -4.0},
                        "follow_up": None
                    }
                ]
            }
        ]
    },

    # ------------------------------------------------------
    # 7. MODERN & INFORMATION ERA (1991 – PRESENT)
    # ------------------------------------------------------
    "Modern & Information Era (1991 – Present)": {
        "events": [
            {
                "id": "mod_cyber_attack",
                "title": "Cybersecurity Alert: State-Sponsored Ransomware Paralyzes Grid",
                "desc": "A zero-day ransomware cyber attack linked to foreign intelligence has encrypted supervisory control servers. Regional power grids and hospital networks operate on emergency generators.",
                "conditions": {"metrics.international_tension": (">", 35.0)},
                "effect": {"gdp": -6.0, "government_stability": -5.0, "metrics.military_readiness": -4.0}
            },
            {
                "id": "mod_ai_unicorn",
                "title": "Tech Boom: AI Venture Capital Windfall",
                "desc": "Domestic artificial intelligence research firms attract billions in foreign investment, boosting software exports and tech employment.",
                "conditions": {},
                "effect": {"gdp": 7.0, "fdi": 9.0, "unemployment": -2.0}
            }
        ],
        "dilemmas": [
            {
                "id": "mod_dil_tech_monopoly",
                "title": "Big Tech Data Sovereignty & Antitrust Standoff",
                "description": "Multinational tech monopolies controlling national communications threaten to pull cloud infrastructure and digital payment systems out of the country if privacy regulations and antitrust breakups are passed.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Enforce Strict Antitrust Breakups: Mandate open data ownership and algorithm audits",
                        "effects": {"metrics.legitimacy": 8.0, "metrics.public_support": 7.0, "metrics.fdi": -10.0, "metrics.gdp": -4.0},
                        "follow_up": None
                    },
                    {
                        "label": "Grant Full Regulatory Exemption: Partner with tech giants for military AI contract development",
                        "effects": {"metrics.fdi": 10.0, "metrics.gdp": 6.0, "metrics.public_support": -8.0, "groups.Elites.wealth_share": 10},
                        "follow_up": "mod_dil_deepfake_crisis"
                    }
                ]
            },
            {
                "id": "mod_dil_housing_crisis",
                "title": "Institutional Speculation & Housing Affordability Crisis",
                "description": "Foreign private equity funds have bought up residential housing inventory in major urban centers, driving home purchase prices up 200% and causing a severe crisis for young workers.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Ban Corporate Residential Buying: Impose steep vacancy taxes and rent caps",
                        "effects": {"metrics.public_support": 10.0, "metrics.fdi": -9.0, "metrics.gdp": -3.0, "groups.Middle Class.approval": 15},
                        "follow_up": "mod_dil_capital_flight"
                    },
                    {
                        "label": "Deregulate Suburban Zoning: Allow private developers to build dense high-rise towers",
                        "effects": {"metrics.gdp": 6.0, "metrics.unemployment": -2.0, "metrics.public_support": -4.0, "metrics.inflation": 3.0},
                        "follow_up": None
                    }
                ]
            },
            {
                "id": "mod_dil_crypto_sovereignty",
                "title": "De-Dollarization & Decoupled Crypto Capital Flight",
                "description": "Citizens and corporations are transferring domestic fiat currency reserves into decentralized, un-traceable cryptocurrencies to evade wealth taxes and capital controls.",
                "conditions": {},
                "choices": [
                    {
                        "label": "Outlaw Crypto Transactions: Ban crypto mining, ban exchanges, and launch Central Bank Digital Currency (CBDC)",
                        "effects": {"metrics.government_stability": 6.0, "metrics.reserves": 5.0, "metrics.public_support": -7.0, "groups.Middle Class.approval": -10},
                        "follow_up": "mod_dil_cbdc_surveillance_protest"
                    },
                    {
                        "label": "Adopt Crypto into National Treasury: Legalize digital assets and offer tax haven status",
                        "effects": {"metrics.fdi": 12.0, "metrics.gdp": 5.0, "metrics.inflation": 4.0, "metrics.legitimacy": -5.0},
                        "follow_up": None
                    }
                ]
            }
        ]
    }
}


# ==========================================================
# CASCADING FOLLOW-UP DILEMMAS (STAGE 2 & 3 BRANCHES)
# ==========================================================

CHAINED_FOLLOW_UPS = {
    # Antiquity Cascades
    "anc_dil_granary_corrupt": {
        "title": "Corrupt Granary Official Embezzlement",
        "description": "Audits reveal that the emergency grain distribution program was hijacked by corrupt magistrates, who resold state food on the black market while citizens starved.",
        "choices": [
            {
                "label": "Public Executions: Execute corrupt magistrates and seize their estates",
                "effects": {"metrics.legitimacy": 6.0, "metrics.government_stability": 4.0, "groups.Elites.approval": -10}
            },
            {
                "label": "Privatize Distribution: Sell granary concessions to merchant houses",
                "effects": {"metrics.reserves": 6.0, "metrics.public_support": -6.0, "groups.Middle Class.wealth_share": 5}
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
    "anc_dil_crucifixion_outrage": {
        "title": "Appian Way Insurrection Backlash",
        "description": "Mass executions of gladiatorial rebels have turned them into martyrs. Sympathetic agrarian uprisings erupt across neighboring client states.",
        "choices": [
            {
                "label": "Declare Martial Dictatorship: Suspend civilian tribunals",
                "effects": {"metrics.government_stability": 6.0, "metrics.legitimacy": -8.0, "groups.Elites.approval": -10}
            },
            {
                "label": "Pass Slave Treatment Ordinances: Limit master abuse rights",
                "effects": {"metrics.public_support": 6.0, "groups.Elites.approval": -15, "groups.Working Class.approval": 10}
            }
        ]
    },
    "anc_dil_priest_excommunication": {
        "title": "The High Priest's Anathema Decree",
        "description": "Having seized temple vaults, the High Priest has proclaimed the King's lineage cursed by the gods, causing army desertions.",
        "choices": [
            {
                "label": "Banish the High Priesthood: Install a loyal army chaplain as Pontiff",
                "effects": {"metrics.legitimacy": -12.0, "metrics.government_stability": 6.0, "groups.Elites.approval": -15}
            },
            {
                "label": "Repent publicly: Walk barefoot to the temple and return half the gold",
                "effects": {"metrics.legitimacy": 10.0, "metrics.reserves": -6.0, "metrics.public_support": 5.0}
            }
        ]
    },

    # Feudal Cascades
    "mid_dil_crusader_rebellion": {
        "title": "The Papal Holy Crusade for the Throne",
        "description": "Following excommunication, the Pope has authorized a neighboring Duke to launch a holy crusade to dethrone the King.",
        "choices": [
            {
                "label": "Rally Peasant Levies: Appeal to national sentiment against foreign interference",
                "effects": {"metrics.military_readiness": 8.0, "metrics.public_support": 7.0, "metrics.reserves": -6.0}
            },
            {
                "label": "Buy Papal Absolution: Pay an immense indemnity to Rome",
                "effects": {"metrics.reserves": -12.0, "metrics.legitimacy": 8.0, "metrics.government_stability": 4.0}
            }
        ]
    },
    "mid_dil_feudal_lord_backlash": {
        "title": "The Barons' Feudal Boycott",
        "description": "Outraged by free city charters, feudal lords withhold military knightly levies and stop forwarding provincial tax revenues.",
        "choices": [
            {
                "label": "Create Mercenary Standing Regiments: Hire professional pike-and-shot companies",
                "effects": {"metrics.military_readiness": 10.0, "metrics.reserves": -8.0, "groups.Elites.approval": -15}
            },
            {
                "label": "Restrict City Charters: Re-impose feudal transit taxes on urban merchants",
                "effects": {"metrics.gdp": -5.0, "groups.Elites.approval": 10, "groups.Middle Class.approval": -15}
            }
        ]
    },
    "mid_dil_heretic_martyrs": {
        "title": "Inquisitorial Overreach & Southern Massacres",
        "description": "Bloodthirsty inquisitors have torched southern market towns, forcing moderate nobles into an open regional war of independence.",
        "choices": [
            {
                "label": "Recall the Inquisitors: Restrain church courts and pay reparations",
                "effects": {"regions.Periphery.stability": 15, "metrics.legitimacy": -8.0, "metrics.reserves": -5.0}
            },
            {
                "label": "Raze Rebellious Castles: Annex southern fiefdoms directly to the Crown",
                "effects": {"metrics.government_stability": 7.0, "regions.Periphery.unrest": 30, "metrics.public_support": -10.0}
            }
        ]
    },

    # Early Modern Cascades
    "ear_dil_monopoly_lawsuit": {
        "title": "Merchant Admiralty Court Litigation",
        "description": "Displaced royal monopoly barons sue the Crown in High Chancery, freezing colonial shipping lines during trial.",
        "choices": [
            {
                "label": "Pack the Courts: Replace recalcitrant judges with loyalist magistrates",
                "effects": {"metrics.government_stability": 5.0, "metrics.legitimacy": -8.0, "metrics.gdp": 4.0}
            },
            {
                "label": "Buy Out Monopoly Stock: Compensate royal barons with state treasury bonds",
                "effects": {"metrics.debt": 6.0, "metrics.gdp": 5.0, "groups.Elites.approval": 10}
            }
        ]
    },
    "ear_dil_pirate_mutiny": {
        "title": "Privateer Republic of Tortuga",
        "description": "Licensed state privateers have renounced their letters of marque, turned full pirate, and established a buccaneer republic.",
        "choices": [
            {
                "label": "Send the Royal Navy to Bombard the Pirate Port",
                "effects": {"metrics.military_readiness": 6.0, "metrics.reserves": -5.0, "metrics.international_tension": -4.0}
            },
            {
                "label": "Appoint Pirate Captains as Colonial Governors: Grant royal pardons in exchange for gold cuts",
                "effects": {"metrics.reserves": 8.0, "metrics.legitimacy": -10.0, "metrics.trade_openness": 5.0}
            }
        ]
    },
    "ear_dil_palace_jacquerie": {
        "title": "The Palace Salt Tax Uprising",
        "description": "Enraged peasant bands armed with scythes have torched provincial tax offices and are marching on the royal palace.",
        "choices": [
            {
                "label": "Order the Royal Dragoon Guards to Charge the Crowds",
                "effects": {"metrics.government_stability": 6.0, "metrics.public_support": -15.0, "groups.Working Class.radicalization": 25}
            },
            {
                "label": "Concede Salt Tax Abolition: Suspend palace construction permanently",
                "effects": {"metrics.public_support": 10.0, "metrics.legitimacy": -6.0, "metrics.debt": -4.0}
            }
        ]
    },

    # Industrial Cascades
    "ind_dil_labor_martyrs": {
        "title": "The Factory Riots Martyr Trial",
        "description": "Public executions of union leaders backfired. Executed organizers are now political martyrs, triggering nationwide sympathy strikes.",
        "choices": [
            {
                "label": "Declare State of Siege: Ban public assemblies and suspend habeas corpus",
                "effects": {"metrics.government_stability": -8.0, "metrics.public_support": -15.0, "groups.Working Class.radicalization": 30}
            },
            {
                "label": "Capitulate to Demands: Grant an 8-hour workday and fund worker pensions",
                "effects": {"metrics.public_support": 12.0, "metrics.gdp": -4.0, "groups.Working Class.radicalization": -20}
            }
        ]
    },
    "ind_dil_rural_landed_rebellion": {
        "title": "Landed Aristocracy Constitutional Walkout",
        "description": "Furious over grain tariff abolition, rural landowning MPs resign from parliament, triggering a constitutional deadlock.",
        "choices": [
            {
                "label": "Create New Peerages: Dilute the House of Lords with industrialist appointments",
                "effects": {"metrics.government_stability": 6.0, "metrics.legitimacy": -7.0, "groups.Middle Class.approval": 15}
            },
            {
                "label": "Subsidize Farm Mechanization: Grant state loans to modern agricultural estates",
                "effects": {"metrics.reserves": -6.0, "metrics.gdp": 4.0, "groups.Elites.approval": 10}
            }
        ]
    },
    "ind_dil_factory_owner_lockout": {
        "title": "Industrialist Capital Strike & Factory Lockouts",
        "description": "Factory owners lock out 200,000 workers to protest child labor laws, demanding the repeal of safety inspectorships.",
        "choices": [
            {
                "label": "Nationalize Recalcitrant Mills: Run factories under state military administration",
                "effects": {"metrics.government_stability": -6.0, "metrics.gdp": -5.0, "groups.Working Class.approval": 20, "groups.Elites.approval": -25}
            },
            {
                "label": "Water Down Inspectorship Fines: Grant exceptions for family textile businesses",
                "effects": {"metrics.gdp": 3.0, "metrics.public_support": -6.0, "groups.Working Class.approval": -10}
            }
        ]
    },

    # World War Cascades
    "ww_dil_munitions_shortage": {
        "title": "Frontline Shell Scarcity Crisis",
        "description": "Drafting factory workers caused artillery shell production to drop 60%. Guns on the front line are out of ammo.",
        "choices": [
            {
                "label": "Import Munitions at Exorbitant Rates from Neutral Nations",
                "effects": {"metrics.debt": 10.0, "metrics.reserves": -8.0, "metrics.military_readiness": 6.0}
            },
            {
                "label": "Order Full Civilian War Rationing: Re-assign all non-essential workers to shell factories",
                "effects": {"metrics.public_support": -10.0, "metrics.military_readiness": 8.0, "metrics.government_stability": -4.0}
            }
        ]
    },
    "ww_dil_prison_strike": {
        "title": "Industrial Labor Prison Mutiny",
        "description": "Imprisoned union leaders launch a hunger strike inside state penitentiaries. Mass demonstrations paralyze the capital.",
        "choices": [
            {
                "label": "Force-Feed Strike Leaders & Deploy Anti-Riot Cavalry",
                "effects": {"metrics.government_stability": -6.0, "metrics.public_support": -12.0, "groups.Working Class.radicalization": 25}
            },
            {
                "label": "Grant General Amnesty for Political Prisoners",
                "effects": {"metrics.public_support": 10.0, "metrics.government_stability": 4.0, "metrics.legitimacy": 5.0}
            }
        ]
    },

    # Cold War Cascades
    "cw_dil_blockade_incident": {
        "title": "High Seas Cargo Interception Standoff",
        "description": "A state destroyer has boarded a rival superpower freighter carrying missile telemetry hardware. Rival fleets power up weapons systems.",
        "choices": [
            {
                "label": "Seize the Cargo: Stand firm at nuclear brinkmanship",
                "effects": {"metrics.international_tension": 20.0, "metrics.military_readiness": 12.0, "metrics.public_support": 5.0}
            },
            {
                "label": "Escort the Freighter Out of Territorial Waters: Defuse crisis safely",
                "effects": {"metrics.international_tension": -12.0, "metrics.military_readiness": -6.0, "metrics.legitimacy": -6.0}
            }
        ]
    },
    "cw_dil_academic_exodus": {
        "title": "Scientific & Intellectual Brain Drain",
        "description": "In response to domestic loyalty blacklists, top nuclear physicists and tech researchers are fleeing to neutral foreign nations.",
        "choices": [
            {
                "label": "Erect Iron Exit Visas: Restrict scientist foreign travel completely",
                "effects": {"metrics.government_stability": 5.0, "metrics.legitimacy": -10.0, "metrics.fdi": -8.0}
            },
            {
                "label": "Abolish Loyalty Commissions: Offer competitive state research grants",
                "effects": {"metrics.reserves": -6.0, "metrics.public_support": 8.0, "metrics.legitimacy": 6.0}
            }
        ]
    },

    # Modern Cascades
    "mod_dil_deepfake_crisis": {
        "title": "AI Deepfake Political Scandal",
        "description": "Unregulated Big Tech AI algorithms generate hyper-realistic synthetic audio depicting ministers taking bribes, sparking mass protests.",
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
    },
    "mod_dil_capital_flight": {
        "title": "Foreign Investor Capital Flight & Currency Run",
        "description": "Banning corporate home purchases caused private equity funds to dump sovereign bonds, collapsing the national currency.",
        "choices": [
            {
                "label": "Raise Central Bank Interest Rates to 18%",
                "effects": {"metrics.inflation": -5.0, "metrics.gdp": -4.0, "metrics.unemployment": 3.0}
            },
            {
                "label": "Impose Emergency Outward Capital Controls: Ban foreign currency transfers",
                "effects": {"metrics.fdi": -15.0, "metrics.reserves": 6.0, "metrics.government_stability": -4.0}
            }
        ]
    },
    "mod_dil_cbdc_surveillance_protest": {
        "title": "Central Bank Digital Currency Privacy Riots",
        "description": "Citizens take to the streets against CBDCs, fearing government tracking of individual purchases and programable spending limits.",
        "choices": [
            {
                "label": "Mandate Cashless Payment Terminals Nationwide by Decree",
                "effects": {"metrics.government_stability": 4.0, "metrics.public_support": -12.0, "metrics.legitimacy": -8.0}
            },
            {
                "label": "Guarantee Privacy Anonymity Protections for Cash & Small CBDC Transactions",
                "effects": {"metrics.public_support": 9.0, "metrics.legitimacy": 6.0, "metrics.reserves": -3.0}
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
        elif "Middle Ages" in era_name or "Feudalism" in era_name:
            return COMPLEX_ERA_POOLS["Middle Ages & Feudalism (500 – 1500 CE)"]
        elif "Early Modern" in era_name or "Colonial" in era_name:
            return COMPLEX_ERA_POOLS["Early Modern & Colonial Era (1500 – 1789)"]
        elif "Industrial" in era_name:
            return COMPLEX_ERA_POOLS["Industrial Revolution & Empire (1789 – 1914)"]
        elif "Crises" in era_name or "World Wars" in era_name:
            return COMPLEX_ERA_POOLS["The Age of Crises & World Wars (1914 – 1945)"]
        elif "Cold War" in era_name or "Atomic" in era_name:
            return COMPLEX_ERA_POOLS["Cold War & Atomic Age (1945 – 1991)"]
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
    
    # 2. Trigger Dilemma (50% probability per turn)
    if not state.get("active_dilemma") and random.random() < 0.50 and pool["dilemmas"]:
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

    # Fallback to procedural generator
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
