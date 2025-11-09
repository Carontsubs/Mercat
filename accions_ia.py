# accions_ia.py

import regles_ia as regles # Per accedir a l'ESTAT_JOC, les regles i SILENT_MODE
import random 

# --- CONFIGURACIÓ DE CARTES (Útil centralitzar-ho) ---

CARTES_DESENVOLUPAMENT = {
    "1": {"nom": "Analista Junior", "cost": 4, "efecte": "+1 Broker"},
    "2": {"nom": "Algoritme Alta Freqüència", "cost": 3, "efecte": "CO -1€/Broker/Cicle"},
    "3": {"nom": "Fons Diversificat", "cost": 2, "efecte": "+1 VN per Ticker A"}
}


# --- Funcions d'Acció Base ---

def usar_ap(cost):
    """Funció helper per comprovar AP i reduir-los."""
    if regles.ESTAT_JOC["punts_accio_disponibles"] >= cost:
        regles.ESTAT_JOC["punts_accio_disponibles"] -= cost
        return True
    else:
        # En mode silenciós, evitem el print d'error d'AP
        if not regles.SILENT_MODE:
            print("❌ No hi ha prou Punts d'Acció (AP) per aquesta acció.")
        return False

# 1. Ingrés Bàsic (Cost: 1 AP)
def ingresar_basic():
    """1 AP guanya 2 € en efectiu."""
    if usar_ap(1):
        guany = 2
        regles.ESTAT_JOC["efectiu"] += guany
        regles.ESTAT_JOC["comptador_ingres_basic"] += 1
        if not regles.SILENT_MODE:
            print(f"💰 Acció realitzada: Ingrés Bàsic. Guanyes {guany} €.")
        return True
    return False

# 2. Ticker A (Cost: 1 AP)
def comprar_accions_a(): # Nom canviat per consistència (comprar_ticker_a -> comprar_accions_a)
    """1 AP compra 1 Acció Ticker A (Baix Risc)."""
    if usar_ap(1):
        regles.ESTAT_JOC["accions"]["A"] += 1
        if not regles.SILENT_MODE:
            print("📈 Acció realitzada: Compra 1 Acció Ticker A. (+1 al teu Actiu)")
        return True
    return False

# 3. Ticker B (Cost: 1 AP)
def comprar_accions_b(): # Nom canviat per consistència (comprar_ticker_b -> comprar_accions_b)
    """1 AP compra 1 Acció Ticker B (Volàtil)."""
    if usar_ap(1):
        regles.ESTAT_JOC["accions"]["B"] += 1
        if not regles.SILENT_MODE:
            print("💥 Acció realitzada: Compra 1 Acció Ticker B. (+1 al teu Actiu, Risc Elevat)")
        return True
    return False

# 4. Préstec Ràpid (Cost: 1 AP)
def prestec_rapid():
    """1 AP guanya 5 € i obtens 2 Deute tokens. (El teu codi ho tenia a 1 AP)"""
    # NOTE: Segons el teu codi, aquesta acció consumeix 1 AP.
    if usar_ap(1):
        guany_immediat = 5
        regles.ESTAT_JOC["efectiu"] += guany_immediat
        regles.ESTAT_JOC["deute_tokens"] += 2
        if not regles.SILENT_MODE:
            print(f"💸 Acció realitzada: Préstec Ràpid. Guanyes {guany_immediat} € i obtens 2 de Deute.")
        return True
    return False
    
# 5. Contractar Broker (Falta al teu codi inicial, afegim una simulada)
def contractar_broker():
    """1 AP guanya 1 Broker per millorar els AP (però el cost d'efectiu va a Desenvolupament)."""
    if usar_ap(1):
        # Aquesta acció no té un efecte directe aquí, però gasta AP.
        if not regles.SILENT_MODE:
            print("👤 Acció realitzada: Contractació de Broker (simulada).")
        return True
    return False

# 6. Desenvolupament (Cost: 2 AP, tria automàtica en simulació)

# accions_ia.py (Funció comprar_desenvolupament amb lògica d'IA)

def comprar_desenvolupament():
    """
    Consumeix 1 AP per comprar una Carta d'Estratègia amb tria AUTOMÀTICA estratègica:
    1. Prioritza 'Fons Diversificat' si Accions A >= 3.
    2. Altrament, Prioritza 'Analista Junior'.
    """
    
    # 🛑 NOTA: Aquesta funció ha de consumir 1 AP si l'acció es realitza amb èxit.
    
    # Variables d'estat
    efectiu = regles.ESTAT_JOC["efectiu"]
    accions_a = regles.ESTAT_JOC["accions"]["A"]
    brokers = regles.ESTAT_JOC["brokers"]
    fons_count = regles.ESTAT_JOC["estrategies"].count("Fons Diversificat")
    # 🛑 PAS CLAU: Definició de variables de les cartes i comptes
    analista_junior = CARTES_DESENVOLUPAMENT["1"]
    algoritme = CARTES_DESENVOLUPAMENT["2"]
    fons_diversificat = CARTES_DESENVOLUPAMENT["3"]
    
    # Recompte de cartes actuals:
    algoritme_count = regles.ESTAT_JOC["estrategies"].count(algoritme["nom"])
    analista_count = regles.ESTAT_JOC["estrategies"].count(analista_junior["nom"])
    fons_count = regles.ESTAT_JOC["estrategies"].count(fons_diversificat["nom"])

    # 1. Comprovar si hi ha alguna carta disponible i pagable (assumint CARTES_DESENVOLUPAMENT existeix)
    cartes_pagables = [
         c for c in CARTES_DESENVOLUPAMENT.values() 
         if efectiu >= c['cost']
    ]

    if not cartes_pagables:
        # No hi ha cartes pagables, l'acció falla i no consumeix AP
        return False

    
    carta_tria = None
# 🛑 NOU: Límits Segons l'Estratègia V79
    MAX_JUN = 2 # Només 1 Junior en tota la partida
    MAX_FONS = 1 # Només 1 Fons Diversificat en tota la partida
    MAX_ALG = 0 # 🛑 L'estratègia no permet Algoritme

    carta_tria = None

    # 1. 🥇 PRIORITAT MÀXIMA: ANALISTA JUNIOR (Si no en tenim cap)
    if analista_count < MAX_JUN and efectiu >= analista_junior["cost"]:
        carta_tria = analista_junior
            
    # 2. 🥈 PRIORITAT ALTA: FONS DIVERSIFICAT (Si no en tenim cap)
    elif fons_count < MAX_FONS and efectiu >= fons_diversificat["cost"]:
        # No cal la condició accions_a >= 5 perquè l'estratègia obliga a comprar-lo
        carta_tria = fons_diversificat
                
    # 3. 🥉 PRIORITAT MITJANA: Altres (Algoritme) - BLOQUEJADES
    # Aquesta secció s'elimina o es bloqueja amb MAX_ALG=0
    if carta_tria:
        # Consumir AP (Ho has de gestionar amb la funció 'usar_ap')
        if not usar_ap(1):
            return False # Falla si no hi ha AP, tot i que la lògica de l'IA ja ho hauria d'haver filtrat
            
        # 1. Aplicar Cost
        regles.ESTAT_JOC["efectiu"] -= carta_tria['cost']
        
        # 2. Afegir a Estratègies (per al comptador final)
        regles.ESTAT_JOC["estrategies"].append(carta_tria['nom'])
        
        # 3. Aplicar Efecte (Només l'Analista Junior augmenta el Broker)
        if carta_tria['nom'] == "Analista Junior":
             regles.ESTAT_JOC["brokers"] += 1
        
        # 4. Retornar èxit (Crucial per al Tallafoc d'AP a simulador_ia.py)
        return True # Retorna True per indicar èxit
            
    return False # Retorna Fals si no s'ha pogut triar ni executar cap carta