# regles.py

import random
import sys

# ESTAT GLOBAL DEL JOC (Aquí resideixen totes les dades)
ESTAT_JOC = {
    # Variables de Seguiment
    "torn_actual": 1,
    "cicle_actual": 1,  # 1 (Torns 1-4), 2 (Torns 5-7), 3 (Torns 8-9)

    # Recursos
    "efectiu": 0,
    "deute_tokens": 0,  # Penalització: -3 VN per token al final

    # Capacitat Operativa (Brokers)
    "brokers": 1,
    "punts_accio_disponibles": 2, # Es calcula: brokers * 2

    # Actius d'Inversió
    "accions": {"A": 0, "B": 0},

    # Estratègies (Cartes de Desenvolupament)
    "estrategies": [],
}

# --- FUNCIONS DE CÀLCUL I AVALUACIÓ ---

def obtenir_cicle_actual():
    """Determina en quin cicle es troba el joc."""
    torn = ESTAT_JOC["torn_actual"]
    if torn <= 4:
        return 1
    elif torn <= 7:
        return 2
    else:
        return 3

def avaluar_ticker_b(quantitat_accions):
    """Calcula el guany/pèrdua total per a les accions Ticker B (Volàtil)."""
    guany_total = 0
    guany_per_tiratge = {
        1: -3,  # Pífia
        2: 0,   # Punt Mort
        3: 0,   # Punt Mort
        4: 3,   # Guany Moderat
        5: 5,   # Guany Fort
        6: 8    # Crític
    }
    
    for _ in range(quantitat_accions):
        tiratge = random.randint(1, 6)
        guany = guany_per_tiratge.get(tiratge, 0)
        guany_total += guany

    return guany_total

def fase_de_mercat():
    """Executada al final dels Torns 4, 7 i 9. Avaluació d'actius i Pagament de CO."""
    
    # 1. Càlcul de Dividends/Avaluació
    guany_ticker_a = ESTAT_JOC["accions"]["A"] * 1  # Ticker A: +1 € fix
    guany_ticker_b = avaluar_ticker_b(ESTAT_JOC["accions"]["B"])
    
    guany_total = guany_ticker_a + guany_ticker_b
    ESTAT_JOC["efectiu"] += guany_total

    print(f"\n--- Resultats de l'Avaluació ---")
    print(f"| Guany Ticker A: +{guany_ticker_a} €")
    print(f"| Guany Ticker B: {guany_ticker_b} €")
    print(f"| Efectiu abans de CO: {ESTAT_JOC['efectiu']} €")

    # 2. Pagament de Costos Operatius (CO)
    
    # Costos definitius: 12 € al Cicle I, 4 € al Cicle II i III (per Broker)
    cost_base = 0
    cicle = obtenir_cicle_actual()
    
    if cicle == 1:
        cost_base = 12
    else:
        cost_base = 4
    
    cost_operatiu_total = cost_base * ESTAT_JOC["brokers"]

    if ESTAT_JOC["efectiu"] >= cost_operatiu_total:
        ESTAT_JOC["efectiu"] -= cost_operatiu_total
        print(f"✅ CO pagat ({cost_operatiu_total} €). Efectiu restant: {ESTAT_JOC['efectiu']} €")
    else:
        # Penalització per no poder pagar
        ESTAT_JOC["deute_tokens"] += 1
        ESTAT_JOC["efectiu"] = 0 # L'efectiu es reinicia a zero
        print(f"❌ NO S'HA POGUT PAGAR CO! ({cost_operatiu_total} €). Deute adquirit. Nou Deute Total: {ESTAT_JOC['deute_tokens']}")
        
    # 3. Avançament del Cicle
    ESTAT_JOC["cicle_actual"] += 1

def finalitzar_torn():
    """Gestiona el final de cada torn."""
    
    if ESTAT_JOC["torn_actual"] in [4, 7, 9]:
        print("\n--- INICI FASE DE MERCAT (COLLITA) ---")
        fase_de_mercat()
        print("--- FINAL FASE DE MERCAT ---\n")

    if ESTAT_JOC["torn_actual"] < 9:
        # Avançar al següent torn
        ESTAT_JOC["torn_actual"] += 1
        # Reiniciar AP al total de Brokers * 2
        ESTAT_JOC["punts_accio_disponibles"] = ESTAT_JOC["brokers"] * 2
    else:
        # Fi del joc
        calcular_valor_net_final()
        sys.exit() # Cal afegir 'import sys' aquí si el vols tancar

def calcular_valor_net_final():
    """Calcula la puntuació final (VN)."""
    # Valoració simple dels actius: 1 € per acció
    vn_accions = ESTAT_JOC["accions"]["A"] * 1 + ESTAT_JOC["accions"]["B"] * 1
    penalitzacio_deute = ESTAT_JOC["deute_tokens"] * 3
    
    # La valoració final pot ser més complexa (p. ex., bonus per cartes),
    # però aquí utilitzem la base.
    vn_final = ESTAT_JOC["efectiu"] + vn_accions - penalitzacio_deute
    
    print("\n=============================================")
    print(f"| JOC FINALITZAT! VALOR NET (VN) FINAL: {vn_final} € |")
    print("=============================================\n")