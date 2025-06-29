def harmonize_party(party):

    if party in ["vas", "Vasemmistoliiton eduskuntaryhmä", "Left Alliance Parliamentary Group"]:
        party = "vas"

    elif party in ["kok", "Kansallisen kokoomuksen eduskuntaryhmä", "Parliamentary Group of the National Coalition Party"]:
        party = "kok"

    elif party in ["ps", "Perussuomalaisten eduskuntaryhmä", "The Finns Party Parliamentary Group"]:
        party = "ps"

    elif party in ["vihr", "Vihreä eduskuntaryhmä", "Green Parliamentary Group"]:
        party = "vihr"

    elif party in ["sd", "Sosialidemokraattinen eduskuntaryhmä", "Social Democratic Parliamentary Group"]:
        party = "sd"

    elif party in ["kd", "Kristillisdemokraattinen eduskuntaryhmä", "Christian Democratic Parliamentary Group"]:
        party = "kd"

    elif party in ["kesk", "Keskustan eduskuntaryhmä", "Centre Party Parliamentary Group"]:
        party = "kesk"

    elif party in ["r", "Ruotsalainen eduskuntaryhmä", "Swedish Parliamentary Group"]:
        party = "r"

    elif party in ["liik", "Liike Nyt -eduskuntaryhmä", "Liike Nyt-Movement's Parliamentary Group"]:
        party = "liik"

    elif party == "Eduskuntaryhmään kuulumaton":
        party = "-"

    else:
        party = party.lower()

    return party