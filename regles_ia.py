# regles.py

import random
import sys
import math
import time # ⬅️ Essential per a random.seed

# 🛑 CORRECCIÓ VITAL: Inicialització de la llavor de random
# Això prevé problemes de bloqueig amb simulacions ràpides.
random.seed(time.time())

# --- VARIABLES GLOBALS ---

# L'estat global del joc (ha de ser definit abans de les funcions)
ESTAT_JOC = {} # S'omple amb inicialitzar_joc()
SILENT_MODE = False 

# --- 1. FUNCIONS D'INICIALITZACIÓ I ESTAT ---

def inicialitzar_joc():
    """Reinicialitza l'ESTAT_JOC a la configuració inicial per a la simulació."""
    global ESTAT_JOC
    # Aquesta és la definició que faltava o estava mal anomenada!
    ESTAT_JOC = {
        # Variables de Seguiment
        "torn_actual": 1,
        "cicle_actual": 1, 

        # Recursos
        "efectiu": 3, 
        "deute_tokens": 0, 

        # Capacitat Operativa
        "brokers": 1,
        "punts_accio_disponibles": 1, 

        # Actius d'Inversió
        "accions": {"A": 0, "B": 0}, # ✅ Netejar a enters (0)
        
        # Estratègies (Cartes de Desenvolupament)
        "estrategies": [],
    }
    global SILENT_MODE
    SILENT_MODE = False


# Aquesta funció va ser movil a 'utilitats.py', però aquí la deixem si la necessites aïllada
def obtenir_cicle_actual():
    """Determina en quin cicle es troba el joc."""
    torn = ESTAT_JOC["torn_actual"]
    if torn <= 4:
        return 1
    elif torn <= 7:
        return 2
    else:
        return 3

# --- 2. FUNCIONS D'AVALUACIÓ D'ACCIONS (amb la correcció de tipus) ---

# S'hi inclou la correcció de tipus (convertir a int de forma robusta)

def avaluar_ticker_b(quantitat_accions):
    """Calcula el guany/pèrdua total per a les accions Ticker B (Volàtil)."""
    
    # 🛑 CORRECCIÓ ROBUSTA DE TIPUS
    try:
        accions_enter = int(float(quantitat_accions))
    except (ValueError, TypeError):
        accions_enter = 0 
        
    guany_total = 0
    guany_per_tiratge = {
        1: -2, 2: -1, 3: 0, 
        4: 1, 5: 2, 6: 4
    }
    
    for _ in range(accions_enter):
        tiratge = random.randint(1, 6)
        guany = guany_per_tiratge.get(tiratge, 0)
        guany_total += guany

    return guany_total

# La funció avaluar_ticker_a() és similar

# --- 3. FASES DEL JOC ---

def fase_de_mercat():
    """Executa la fase de Mercat (Càlcul de guany/pèrdua i pagament de CO)."""
    global ESTAT_JOC
    
    # 1. Càlcul de Guany/Pèrdua per Accions (similar a la funció de dalt)
    guany_ticker_a = 0 # avaluar_ticker_a(ESTAT_JOC["accions"]["A"])
    guany_ticker_b = avaluar_ticker_b(ESTAT_JOC["accions"]["B"])
    
    guany_total = guany_ticker_a + guany_ticker_b
    ESTAT_JOC["efectiu"] += guany_total

    # 2. Pagament de Costos Operatius (CO)
    cicle = obtenir_cicle_actual()
    # (El cost_operatiu_total depèn de variables que no estan aquí, p. ex., brokers * cost_base)
    cost_operatiu_total = ESTAT_JOC["brokers"] * 2 # Exemple: 2€ per broker
    
    if ESTAT_JOC["efectiu"] >= cost_operatiu_total:
        # Pagar CO
        ESTAT_JOC["efectiu"] -= cost_operatiu_total
        # ... (Missatges d'èxit)
        
    else:
        # Penalització per no poder pagar (Deute Proporcional)
        
        # 🛑 CORRECCIÓ DE CÀLCUL DE DEUTE (versió amb enters)
        deute_pendent = int(cost_operatiu_total) - int(ESTAT_JOC["efectiu"]) 
        
        # math.ceil(x / 3) és equivalent a (x + 2) // 3
        tokens_adquirits = (deute_pendent + 2) // 3 
        
        ESTAT_JOC["deute_tokens"] += tokens_adquirits
        ESTAT_JOC["efectiu"] = 0 
        # ... (Missatges de deute)
        

def finalitzar_torn():
    """Executa les fases de Tancament i prepara el següent torn."""
    global ESTAT_JOC
    
    # 1. Fase de Mercat (Càlculs i pagament de CO)
    fase_de_mercat()
    
    # 2. Preparació del nou torn
    if ESTAT_JOC["torn_actual"] < 9:
        ESTAT_JOC["torn_actual"] += 1
        ESTAT_JOC["punts_accio_disponibles"] = ESTAT_JOC["brokers"] * 1
        # ... (Altres preparacions, com la Fase de Desenvolupament)

# --- 4. CÀLCUL FINAL ---

def calcular_valor_net_final_silencios():
    """Calcula el Valor Net al final de la simulació."""
    
    vn_actius = ESTAT_JOC["efectiu"]
    
    # Penalització per deute: -3€ per token
    penalitzacio_deute = ESTAT_JOC["deute_tokens"] * 3 
    
    vn_final = vn_actius - penalitzacio_deute
    return vn_final