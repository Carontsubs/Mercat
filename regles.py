# regles.py

import random
import sys
import math

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
    "punts_accio_disponibles": 1, # Es calcula: brokers * 2

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

# regles.py

# ... (resta del codi)

def fase_de_mercat():
    """Executada al final dels Torns 4, 7 i 9. Avaluació d'actius i Pagament de CO."""
    
    # 1. Càlcul de Dividends/Avaluació (inclou el guany base del Ticker A)
    guany_ticker_a_base = ESTAT_JOC["accions"]["A"] * 1
    guany_ticker_b = avaluar_ticker_b(ESTAT_JOC["accions"]["B"])
    
    # --- Aplicació d'Estratègies: GUANY ---
    bonus_a = 0
    if "Fons Diversificat" in ESTAT_JOC["estrategies"]:
        bonus_a = ESTAT_JOC["accions"]["A"] * 1
        print(f"📈 Estratègia 'Fons Diversificat' activa: +{bonus_a} € (bonus Ticker A)")

    guany_total = guany_ticker_a_base + bonus_a + guany_ticker_b
    ESTAT_JOC["efectiu"] += guany_total

    print(f"\n--- Resultats de l'Avaluació ---")
    
    # LÍNIA CORREGIDA per al desglossament:
    if bonus_a > 0:
        print(f"| Guany Ticker A: {guany_ticker_a_base} € (Base) + {bonus_a} € (Diversificat) = +{guany_ticker_a_base + bonus_a} €")
    else:
        print(f"| Guany Ticker A: +{guany_ticker_a_base} €") # Versió simple si no hi ha bonus
    print(f"| Guany Ticker B: {guany_ticker_b} €")
    print(f"| Efectiu abans de CO: {ESTAT_JOC['efectiu']} €")
    
    # 2. Pagament de Costos Operatius (CO)
    # Costos definitius: 8 € al Cicle I, 4 € al Cicle II i III (per Broker)
    cost_base = 0
    cicle = obtenir_cicle_actual()
    
    if cicle == 1:
        cost_base = 8 # CO nou
    else:
        cost_base = 4
        
    # --- Aplicació d'Estratègies: COST ---
    reduccio_co = 0
    if "Algoritme Alta Freqüència" in ESTAT_JOC["estrategies"]:
        reduccio_co = ESTAT_JOC["brokers"] * 1 # Redueix 1 € per Broker
        print(f"⬇️ Estratègia 'Algoritme Alta Freqüència' activa: CO reduït en {reduccio_co} €")

    cost_operatiu_total = (cost_base * ESTAT_JOC["brokers"]) - reduccio_co

    if ESTAT_JOC["efectiu"] >= cost_operatiu_total:
        ESTAT_JOC["efectiu"] -= cost_operatiu_total
        print(f"✅ CO pagat ({cost_operatiu_total} €). Efectiu restant: {ESTAT_JOC['efectiu']} €")
    else:
        # Penalització per no poder pagar (LÒGICA MODIFICADA)
        deute_pendent = cost_operatiu_total - ESTAT_JOC["efectiu"] # Quantitat que falta
        
        # 1. Càlcul de tokens adquirits
        # math.ceil(deute_pendent / 3)
        tokens_adquirits = int(math.ceil(deute_pendent / 3)) 
        
        # 2. Aplicació al total
        ESTAT_JOC["deute_tokens"] += tokens_adquirits
        
        # 3. Reinici d'efectiu
        ESTAT_JOC["efectiu"] = 0 # L'efectiu es reinicia a zero
        
        # Missatges
        nou_deute_total = ESTAT_JOC["deute_tokens"] 
        print(f"❌ NO S'HA POGUT PAGAR CO! ({cost_operatiu_total} €). Deute pendent: {deute_pendent} €")
        print(f"   Tokens de Deute adquirits: {tokens_adquirits}")
        print(f"   Tokens de Deute actuals: {nou_deute_total} (Penalització VN: -{nou_deute_total*3} €)") # <-- Missatge més clar

def finalitzar_torn():
    """Gestiona el final de cada torn."""
    
    if ESTAT_JOC["torn_actual"] in [4, 7, 9]:
        print("\n--- INICI FASE DE MERCAT (COLLITA) ---")
        fase_de_mercat()

    if ESTAT_JOC["torn_actual"] < 9:
        # Avançar al següent torn
        ESTAT_JOC["torn_actual"] += 1
        # Reiniciar AP al total de Brokers * 2
        ESTAT_JOC["punts_accio_disponibles"] = ESTAT_JOC["brokers"] * 1
    else:
        # Fi del joc
        calcular_valor_net_final()
        sys.exit() # Cal afegir 'import sys' aquí si el vols tancar

# regles.py - Funció calcular_valor_net_final() CORREGIDA

def calcular_valor_net_final():
    """Calcula la puntuació final (VN)."""
    
    # 1. Valoració dels Actius (Accions)
    # Valoració simple: 1 € per acció A i B
    vn_accions = ESTAT_JOC["accions"]["A"] * 1 + ESTAT_JOC["accions"]["B"] * 1
    
    # 2. Penalització per Deute
    tokens_deute = ESTAT_JOC["deute_tokens"]
    penalitzacio_deute = tokens_deute * 3 # 3 € per cada token
    
    # 3. Suma final
    # VN = Efectiu + Valor Accions - Penalització Deute
    vn_final = ESTAT_JOC["efectiu"] + vn_accions - penalitzacio_deute
    
    # --- Mostrar Detall Final ---
    print("\n--- DETALL DE LA PUNTUACIÓ FINAL (VN) ---")
    print(f"| Efectiu final: {ESTAT_JOC['efectiu']} €")
    print(f"| Valor d'Accions: {vn_accions} €")
    print(f"| Penalització Deute ({tokens_deute} tokens): -{penalitzacio_deute} €")
    print("-" * 43)
    
    print(f"| JOC FINALITZAT! VALOR NET (VN) FINAL: {vn_final} € |")
    print("=============================================\n")
    
