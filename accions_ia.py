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
def comprar_desenvolupament():
    """2 AP compra una Carta d'Estratègia amb tria automàtica en simulació."""
    
    # Comprovació de Fase
    if regles.ESTAT_JOC["torn_actual"] < 5:
        if not regles.SILENT_MODE:
            print("🛑 L'acció de Desenvolupament no està disponible fins al Torn 5.")
        return False

    # Comprovació d'AP (COST FIXAT A 2 AP)
    if usar_ap(2): 
        
        # --- LÒGICA DE TRIA D'IA (SIMULACIÓ) ---
        
        # Filtrar cartes que l'IA pot pagar
        cartes_pagables = [
            c for c in CARTES_DESENVOLUPAMENT.values() 
            if regles.ESTAT_JOC["efectiu"] >= c['cost']
        ]

        if not cartes_pagables:
            # Si no pot pagar res, l'IA no compra.
            if not regles.SILENT_MODE:
                print("❌ No hi ha fons per comprar cap carta de Desenvolupament.")
            return False

        # Trieu una carta aleatòriament (Estratègia d'IA Base)
        carta_tria = random.choice(cartes_pagables)
        
        # 3. Execució de la compra
        cost_carta = carta_tria['cost']
        nom_carta = carta_tria['nom']
        
        regles.ESTAT_JOC["efectiu"] -= cost_carta
        regles.ESTAT_JOC["estrategies"].append(nom_carta)
        
        # Aplicació immediata de l'efecte del Broker
        if nom_carta == "Analista Junior":
            regles.ESTAT_JOC["brokers"] += 1
        
        if not regles.SILENT_MODE:
            print(f"✅ Has comprat: {nom_carta}. (-{cost_carta} €)")
        
        return True

    return False