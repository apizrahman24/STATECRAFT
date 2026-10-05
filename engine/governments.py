GOVERNMENTS = [

    {
        "id": "absolute_monarchy",
        "name": "Absolute Monarchy",
        "description": "The monarch possesses dominant executive and constitutional authority.",
        "leader": "Monarch",

        "configuration": {

            "Power Base": [
                "Royal Family",
                "Military",
                "Aristocracy",
                "Religious Establishment",
                "Bureaucracy",
                "Business Elites"
            ],

            "Succession": [
                "Primogeniture",
                "Male Preference",
                "Male Only",
                "Elective Royal Succession",
                "Monarch Chooses Successor"
            ],

            "Administration": [
                "Centralized",
                "Provincial Governors",
                "Feudal / Local Autonomy",
                "Hybrid"
            ],

            "Military Control": [
                "Monarch Directly",
                "Royal Commander",
                "Military Aristocracy",
                "Mixed"
            ]
        }
    },

    {
        "id": "constitutional_monarchy",
        "name": "Constitutional Monarchy",
        "description": "A monarch remains head of state while constitutional institutions limit political authority.",
        "leader": "Prime Minister",

        "configuration": {

            "Monarch Power": [
                "Ceremonial",
                "Reserve Powers",
                "Significant Reserve Powers"
            ],

            "Government Formation": [
                "Parliamentary Majority",
                "Monarch Appoints",
                "Parliamentary Appointment"
            ],

            "Parliament": [
                "Unicameral",
                "Bicameral"
            ],

            "Succession": [
                "Primogeniture",
                "Male Preference",
                "Customary"
            ]
        }
    },

    {
        "id": "parliamentary_republic",
        "name": "Parliamentary Republic",
        "description": "Parliament determines the government and the Prime Minister leads the executive.",
        "leader": "Prime Minister",

        "configuration": {

            "Head of State": [
                "Ceremonial President",
                "Reserved-Powers President",
                "Elected President"
            ],

            "Parliament": [
                "Unicameral",
                "Bicameral"
            ],

            "Electoral System": [
                "Proportional Representation",
                "First Past the Post",
                "Mixed Member",
                "Ranked Choice"
            ],

            "Government Formation": [
                "Majority",
                "Coalition",
                "Minority Government"
            ]
        }
    },

    {
        "id": "presidential_republic",
        "name": "Presidential Republic",
        "description": "A directly elected president leads the executive separately from the legislature.",
        "leader": "President",

        "configuration": {

            "Presidential Power": [
                "Limited",
                "Moderate",
                "Strong"
            ],

            "Legislature": [
                "Unicameral",
                "Bicameral"
            ],

            "Term": [
                "4 Years",
                "5 Years",
                "6 Years"
            ],

            "Re-election": [
                "One Additional Term",
                "Unlimited",
                "No Immediate Re-election"
            ]
        }
    },

    {
        "id": "semi_presidential",
        "name": "Semi-Presidential Republic",
        "description": "Executive authority is divided between a president and prime minister.",
        "leader": "President / Prime Minister",

        "configuration": {

            "Presidential Power": [
                "Ceremonial",
                "Moderate",
                "Strong"
            ],

            "Presidential Powers": [
                "Foreign Affairs",
                "Defence",
                "Dissolve Parliament",
                "Emergency Powers",
                "Legislative Veto"
            ]
        }
    },

    {
        "id": "aristocratic_republic",
        "name": "Aristocratic Republic",
        "description": "Political authority is concentrated among aristocratic families or privileged elites.",
        "leader": "Chief Magistrate",

        "configuration": {

            "Political Class": [
                "Nobility",
                "Landowners",
                "Merchant Families",
                "Military Elite"
            ],

            "Legislature": [
                "Council",
                "Senate",
                "Assembly + Council"
            ],

            "Leadership": [
                "Elite Election",
                "Hereditary Offices",
                "Rotating Offices"
            ]
        }
    },

    {
        "id": "oligarchy",
        "name": "Oligarchic Republic",
        "description": "A small group of powerful families, merchants or elites controls the state.",
        "leader": "First Councillor",

        "configuration": {

            "Elite Base": [
                "Merchant",
                "Military",
                "Landowners",
                "Industrialists"
            ],

            "Decision Making": [
                "Council",
                "Elite Assembly",
                "Executive Committee"
            ]
        }
    },

    {
        "id": "city_state",
        "name": "City-State Republic",
        "description": "A compact state centered around a city and surrounding territory.",
        "leader": "Chief Magistrate",

        "configuration": {

            "Citizenship": [
                "Broad Citizen Body",
                "Property Owners",
                "Aristocratic Citizens"
            ],

            "Assembly": [
                "Citizen Assembly",
                "Council",
                "Assembly + Council"
            ],

            "Military": [
                "Citizen Militia",
                "Professional Guard",
                "Mixed"
            ]
        }
    },

    {
        "id": "tribal_kingdom",
        "name": "Tribal Kingdom",
        "description": "A hereditary ruler governs a network of tribes and local chiefs.",
        "leader": "High King",

        "configuration": {

            "Local Autonomy": [
                "High",
                "Moderate",
                "Low"
            ],

            "Succession": [
                "Hereditary",
                "Clan Election",
                "Warrior Elite"
            ]
        }
    },

    {
        "id": "tribal_confederation",
        "name": "Tribal Confederation",
        "description": "Autonomous tribes cooperate through a council or common leader.",
        "leader": "High Chief / Council",

        "configuration": {

            "Central Power": [
                "Very Weak",
                "Weak",
                "Moderate"
            ],

            "Leadership": [
                "Council",
                "Elected High Chief",
                "Rotating Chiefs"
            ]
        }
    },

    {
        "id": "theocracy",
        "name": "Theocracy",
        "description": "Religious authorities possess major political and constitutional authority.",
        "leader": "Supreme Religious Authority",

        "configuration": {

            "Religious Structure": [
                "Priesthood",
                "Council of Clerics",
                "Supreme Religious Leader"
            ],

            "Civil Authority": [
                "Subordinate",
                "Shared",
                "Independent"
            ],

            "Law": [
                "Religious Law Dominant",
                "Mixed Law",
                "Religious Constitutional Law"
            ]
        }
    },

    {
        "id": "military_government",
        "name": "Military Government / Junta",
        "description": "The armed forces directly control the government.",
        "leader": "Military Council Chairman",

        "configuration": {

            "Military Structure": [
                "Army Dominant",
                "Joint Command",
                "Rotating Leadership"
            ],

            "Civilian Role": [
                "Military Only",
                "Technocratic Ministers",
                "Limited Civilian Participation",
                "Transition Government"
            ]
        }
    },

    {
        "id": "one_party",
        "name": "One-Party State",
        "description": "A single political party monopolizes national political power.",
        "leader": "Party Leader",

        "configuration": {

            "Party Centralization": [
                "Moderate",
                "High",
                "Very High"
            ],

            "Economic Control": [
                "Command Economy",
                "State Capitalism",
                "Mixed Economy"
            ],

            "Internal Competition": [
                "None",
                "Factional",
                "Managed"
            ]
        }
    },

    {
        "id": "personalist",
        "name": "Personalist Government",
        "description": "Political institutions revolve around a dominant individual.",
        "leader": "Supreme Leader",

        "configuration": {

            "Leader Authority": [
                "High",
                "Very High",
                "Near Absolute"
            ],

            "Elite Structure": [
                "Patronage",
                "Security Apparatus",
                "Party + Patronage"
            ],

            "Succession": [
                "Family",
                "Chosen Successor",
                "Elite Decision",
                "Unclear"
            ]
        }
    },

    {
        "id": "technocracy",
        "name": "Technocratic Government",
        "description": "Experts and professional administrators dominate executive decision-making.",
        "leader": "Executive Council",

        "configuration": {

            "Expertise": [
                "Economic",
                "Engineering / Industrial",
                "Mixed Expert Council"
            ],

            "Public Role": [
                "Limited",
                "Consultative",
                "Strong Electoral Mandate"
            ]
        }
    },

    {
        "id": "collegial",
        "name": "Collegial / Council Government",
        "description": "Executive authority is shared among several council members.",
        "leader": "National Council",

        "configuration": {

            "Council Size": [
                "3",
                "5",
                "7",
                "11"
            ],

            "Decision Rule": [
                "Simple Majority",
                "Qualified Majority",
                "Consensus"
            ],

            "Rotation": [
                "None",
                "Annual",
                "Periodic"
            ]
        }
    },

    {
        "id": "confederation",
        "name": "Confederation",
        "description": "Member states retain substantial sovereignty while cooperating through a weak central government.",
        "leader": "Confederal Council",

        "configuration": {

            "Central Power": [
                "Very Weak",
                "Weak",
                "Moderate"
            ],

            "Member Veto": [
                "Full",
                "Limited",
                "None"
            ],

            "Common Policy": [
                "Trade Only",
                "Trade + Defence",
                "Broad Cooperation"
            ]
        }
    },

    {
        "id": "direct_democracy",
        "name": "Direct Democracy",
        "description": "Citizens exercise substantial direct political authority through referendums and initiatives.",
        "leader": "Elected Executive",

        "configuration": {

            "Referendum Frequency": [
                "Occasional",
                "Regular",
                "Frequent"
            ],

            "Initiative Threshold": [
                "Low",
                "Medium",
                "High"
            ],

            "Parliament Role": [
                "Strong",
                "Balanced",
                "Limited"
            ]
        }
    },

    {
        "id": "revolutionary",
        "name": "Revolutionary Government",
        "description": "A revolutionary movement controls the state during a major political transition.",
        "leader": "Revolutionary Council",

        "configuration": {

            "Revolutionary Base": [
                "Workers",
                "Military",
                "Nationalist Movement",
                "Popular Coalition"
            ],

            "Transition Goal": [
                "Republic",
                "Socialist State",
                "Constitutional Monarchy",
                "Unspecified"
            ]
        }
    },

    {
        "id": "colonial",
        "name": "Colonial Administration",
        "description": "Political authority is exercised by an external imperial power.",
        "leader": "Governor",

        "configuration": {

            "Local Participation": [
                "None",
                "Advisory Council",
                "Limited Assembly"
            ],

            "Economic Model": [
                "Extraction",
                "Plantation / Export",
                "Mixed Development"
            ]
        }
    },

    {
        "id": "hybrid",
        "name": "Custom / Hybrid Government",
        "description": "Create an unusual combination of political institutions.",
        "leader": "Head of State",

        "configuration": {

            "Executive": [
                "Monarch",
                "President",
                "Prime Minister",
                "Council",
                "Military Council"
            ],

            "Legislature": [
                "None",
                "Unicameral",
                "Bicameral",
                "Council"
            ],

            "Judiciary": [
                "Independent",
                "Executive Appointed",
                "Religious",
                "Mixed"
            ],

            "Military Control": [
                "Civilian",
                "Executive",
                "Legislature",
                "Military"
            ]
        }
    }
]


def get_government(government_id):

    for government in GOVERNMENTS:

        if government["id"] == government_id:
            return government

    return None
