import random


def create_parties(year):

    # Modern parties
    if year >= 1900:

        return {

            "National Conservative Party": {
                "ideology": "Conservative",
                "seats": 28,
                "popularity": 46,
                "loyalty": 70,
                "organization": 75,
                "radicalism": 15
            },

            "Liberal Party": {
                "ideology": "Liberal",
                "seats": 22,
                "popularity": 42,
                "loyalty": 65,
                "organization": 65,
                "radicalism": 10
            },

            "Labour Party": {
                "ideology": "Social Democratic",
                "seats": 18,
                "popularity": 40,
                "loyalty": 60,
                "organization": 70,
                "radicalism": 25
            },

            "Regional Alliance": {
                "ideology": "Regionalist",
                "seats": 12,
                "popularity": 38,
                "loyalty": 45,
                "organization": 60,
                "radicalism": 20
            },

            "Reform Movement": {
                "ideology": "Reformist",
                "seats": 10,
                "popularity": 35,
                "loyalty": 35,
                "organization": 45,
                "radicalism": 35
            }
        }

    # Pre-modern political elites
    return {

        "Royalists": {
            "ideology": "Traditionalist",
            "seats": 35,
            "popularity": 55,
            "loyalty": 75,
            "organization": 70,
            "radicalism": 10
        },

        "Nobility": {
            "ideology": "Aristocratic",
            "seats": 25,
            "popularity": 45,
            "loyalty": 55,
            "organization": 70,
            "radicalism": 15
        },

        "Merchants": {
            "ideology": "Commercial",
            "seats": 15,
            "popularity": 42,
            "loyalty": 50,
            "organization": 60,
            "radicalism": 10
        },

        "Reformers": {
            "ideology": "Reformist",
            "seats": 15,
            "popularity": 35,
            "loyalty": 40,
            "organization": 45,
            "radicalism": 35
        }
    }


def create_leaders(year):

    if year >= 1900:

        return {

            "Prime Minister": {
                "name": "Alexander Voss",
                "competence": 72,
                "popularity": 58,
                "ambition": 75,
                "loyalty": 70,
                "corruption": 15,
                "age": 52
            },

            "Opposition Leader": {
                "name": "Elena Maren",
                "competence": 79,
                "popularity": 51,
                "ambition": 90,
                "loyalty": 45,
                "corruption": 10,
                "age": 44
            },

            "Finance Minister": {
                "name": "Daniel Rook",
                "competence": 86,
                "popularity": 39,
                "ambition": 62,
                "loyalty": 75,
                "corruption": 8,
                "age": 57
            }
        }

    return {

        "Ruler": {
            "name": "King Adrian",
            "competence": 68,
            "popularity": 61,
            "ambition": 80,
            "loyalty": 75,
            "corruption": 12,
            "age": 38
        },

        "Chief Minister": {
            "name": "Marcus Vale",
            "competence": 76,
            "popularity": 48,
            "ambition": 72,
            "loyalty": 55,
            "corruption": 20,
            "age": 51
        }
    }


def create_regions():

    return {

        "Capital Region": {
            "population": 20,
            "economy": "Services",
            "wealth": 70,
            "development": 75,
            "unrest": 15,
            "government_support": 55
        },

        "Northern Province": {
            "population": 20,
            "economy": "Agriculture",
            "wealth": 40,
            "development": 45,
            "unrest": 20,
            "government_support": 50
        },

        "Industrial Belt": {
            "population": 25,
            "economy": "Industry",
            "wealth": 55,
            "development": 65,
            "unrest": 25,
            "government_support": 52
        },

        "Eastern Region": {
            "population": 20,
            "economy": "Resources",
            "wealth": 45,
            "development": 50,
            "unrest": 18,
            "government_support": 48
        },

        "Southern Province": {
            "population": 15,
            "economy": "Agriculture + Trade",
            "wealth": 50,
            "development": 55,
            "unrest": 16,
            "government_support": 53
        }
    }


def create_institutions():

    return {

        "state_capacity": 65,
        "bureaucratic_quality": 60,
        "rule_of_law": 65,
        "judicial_independence": 60,
        "press_freedom": 60,
        "civil_military_relations": 65,
        "tax_capacity": 60,
        "administrative_capacity": 65,
        "corruption": 25
    }


def total_seats(parties):

    return sum(
        party["seats"]
        for party in parties.values()
    )


def government_seats(parties):

    return max(
        party["seats"]
        for party in parties.values()
    )


def parliament_status(parties):

    total = total_seats(parties)

    largest = government_seats(parties)

    if largest > total / 2:

        return "Majority Government"

    if largest >= total * 0.4:

        return "Minority Government"

    return "Hung Parliament"


def simulate_party_politics(
    state,
    inflation,
    unemployment
):

    parties = state["parties"]

    for party in parties.values():

        # Economic pressure changes popularity

        if inflation > 5:

            if party["ideology"] in [
                "Social Democratic",
                "Reformist"
            ]:

                party["popularity"] += 0.5

            else:

                party["popularity"] -= 0.2

        if unemployment > 8:

            party["popularity"] -= 0.4

        party["popularity"] += random.uniform(
            -0.7,
            0.7
        )

        party["popularity"] = max(
            0,
            min(100, party["popularity"])
        )


def calculate_coalition_stability(state):

    parties = state["parties"]

    seats = sorted(
        [
            party["seats"]
            for party in parties.values()
        ],
        reverse=True
    )

    total = sum(seats)

    if not seats:

        return 0

    largest = seats[0]

    if largest > total / 2:

        return 80

    if len(seats) >= 2:

        coalition = seats[0] + seats[1]

        if coalition > total / 2:

            return 65

    return 35
