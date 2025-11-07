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
    
    # 1. Comprovar si hi ha alguna carta disponible i pagable (assumint CARTES_DESENVOLUPAMENT existeix)
    cartes_pagables = [
         c for c in CARTES_DESENVOLUPAMENT.values() 
         if efectiu >= c['cost']
    ]

    if not cartes_pagables:
        # No hi ha cartes pagables, l'acció falla i no consumeix AP
        return False

    carta_tria = None
    
    # --- LÒGICA DE TRIA D'IA ESTRATÈGICA ---
    
    # 2. PRIORITAT 1: FONS DIVERSIFICAT (Si es compleix la condició de 3+ Accions A)
    fons_diversificat = next((c for c in cartes_pagables if c['nom'] == "Fons Diversificat"), None)
    
    if fons_diversificat and accions_a >= 4:
        carta_tria = fons_diversificat
    
    # 3. PRIORITAT 2: ANALISTA JUNIOR (Si no s'ha triat Fons Diversificat)
    if not carta_tria:
         analista_junior = next((c for c in cartes_pagables if c['nom'] == "Analista Junior"), None)
         if analista_junior and brokers < 3:
             carta_tria = analista_junior
             
    # 4. TRIA FINAL (Si encara no s'ha triat, pot triar l'Algoritme si és l'únic que queda)
    if not carta_tria:
        # Triar a l'atzar entre les pagables com a últim recurs.
        carta_tria = random.choice(cartes_pagables)

    # --- EXECUCIÓ DE LA COMPRA (Si s'ha triat una carta) ---
    
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