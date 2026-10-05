import random


def simulate_economy(state):

    m = state["metrics"]

    # ------------------------------------------------------
    # RANDOM ECONOMIC SHOCK
    # ------------------------------------------------------

    economic_noise = random.uniform(
        -0.35,
        0.35
    )

    m["growth"] += economic_noise

    # ------------------------------------------------------
    # INFLATION
    # ------------------------------------------------------

    inflation_pressure = (

        (m["growth"] * 0.05) +

        (m["deficit"] * 0.03) +

        random.uniform(-0.2, 0.2)
    )

    m["inflation"] += inflation_pressure

    # ------------------------------------------------------
    # UNEMPLOYMENT
    # ------------------------------------------------------

    m["unemployment"] -= (
        m["growth"] * 0.08
    )

    m["unemployment"] += random.uniform(
        -0.15,
        0.15
    )

    # ------------------------------------------------------
    # GDP
    # ------------------------------------------------------

    m["gdp"] += (
        m["gdp"] *
        m["growth"] /
        100
    )

    # ------------------------------------------------------
    # DEBT
    # ------------------------------------------------------

    m["debt"] += (
        m["deficit"] * 0.12
    )

    # ------------------------------------------------------
    # WAGES
    # ------------------------------------------------------

    real_wage_pressure = (

        m["inflation"] -
        m["growth"]
    )

    m["wages"] -= (
        real_wage_pressure *
        0.12
    )

    # ------------------------------------------------------
    # INVESTOR CONFIDENCE
    # ------------------------------------------------------

    if m["debt"] > 80:

        m["currency_strength"] -= 0.8

        m["interest_rate"] += 0.2

        m["fdi"] -= 1

    elif m["debt"] < 50:

        m["currency_strength"] += 0.2

        m["fdi"] += 0.5

    # ------------------------------------------------------
    # HIGH INFLATION
    # ------------------------------------------------------

    if m["inflation"] > 6:

        m["public_support"] -= 1.5

        m["protest_risk"] += 2

    # ------------------------------------------------------
    # HIGH UNEMPLOYMENT
    # ------------------------------------------------------

    if m["unemployment"] > 8:

        m["public_support"] -= 1.5

        m["protest_risk"] += 2

    # ------------------------------------------------------
    # CLAMP
    # ------------------------------------------------------

    m["inflation"] = max(
        0,
        m["inflation"]
    )

    m["unemployment"] = max(
        0,
        m["unemployment"]
    )

    m["growth"] = max(
        -15,
        min(15, m["growth"])
    )

    m["debt"] = max(
        0,
        m["debt"]
    )
