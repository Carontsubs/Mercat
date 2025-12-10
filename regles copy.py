# utilitats.py

def obtenir_cicle_actual(estat_joc):
    """Determina en quin cicle es troba el joc."""
    torn = estat_joc["torn_actual"]
    if torn <= 4:
        return 1
    elif torn <= 7:
        return 2
    else:
        return 3