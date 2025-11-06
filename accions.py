# accions.py

import regles # Per accedir a l'ESTAT_JOC i les regles
import random # Per a la funció de Bloqueig del Mercat (si cal)

# --- Funcions d'Acció Base ---

def usar_ap(cost):
    """Funció helper per comprovar AP i reduir-los."""
    if regles.ESTAT_JOC["punts_accio_disponibles"] >= cost:
        regles.ESTAT_JOC["punts_accio_disponibles"] -= cost
        return True
    else:
        print("❌ No hi ha prou Punts d'Acció (AP) per aquesta acció.")
        return False

# 1. Ingrés Bàsic (Cost: 1 AP)
def ingres_basic():
    """1 AP guanya 2 € en efectiu."""
    if usar_ap(1):
        guany = 2
        regles.ESTAT_JOC["efectiu"] += guany
        print(f"💰 Acció realitzada: Ingrés Bàsic. Guanyes {guany} €.")
    else:
        return # Fallada

# 2. Ticker A (Cost: 1 AP)
def comprar_ticker_a():
    """1 AP compra 1 Acció Ticker A (Baix Risc)."""
    if usar_ap(1):
        regles.ESTAT_JOC["accions"]["A"] += 1
        print("📈 Acció realitzada: Compra 1 Acció Ticker A. (+1 al teu Actiu)")
    else:
        return

# 3. Ticker B (Cost: 1 AP)
def comprar_ticker_b():
    """1 AP compra 1 Acció Ticker B (Volàtil)."""
    if usar_ap(1):
        regles.ESTAT_JOC["accions"]["B"] += 1
        print("💥 Acció realitzada: Compra 1 Acció Ticker B. (+1 al teu Actiu, Risc Elevat)")
    else:
        return

# 4. Préstec Ràpid (Cost: 1 AP)
def prestec_rapid():
    """1 AP guanya 5 € i obtens 1 Deute (-3 VN)."""
    if usar_ap(1):
        guany_immediat = 5
        regles.ESTAT_JOC["efectiu"] += guany_immediat
        regles.ESTAT_JOC["deute_tokens"] += 1
        print(f"💸 Acció realitzada: Préstec Ràpid. Guanyes {guany_immediat} € i obtens 1 Deute.")
    else:
        return

# 5. Desenvolupament (Cost: 2 AP)
def comprar_desenvolupament():
    """2 AP compra una Carta d'Estratègia."""
    
    # Comprovació de Fase (disponible només a partir del Torn 5)
    if regles.ESTAT_JOC["torn_actual"] < 5:
        print("🛑 L'acció de Desenvolupament no està disponible fins al Torn 5.")
        return

    # Comprovació d'AP
    if usar_ap(2):
        
        # Opcions de cartes (amb els seus costos definits)
        cartes = {
            "1": {"nom": "Analista Junior", "cost": 4, "efecte": "+1 Broker"},
            "2": {"nom": "Algoritme Alta Freqüència", "cost": 3, "efecte": "CO -1€/Broker/Cicle"}, # CO 12€/3€
            "3": {"nom": "Fons Diversificat", "cost": 2, "efecte": "+1 VN per Ticker A"}
        }

        print("\n--- Compra de Carta d'Estratègia ---")
        for clau, c in cartes.items():
            print(f"{clau}: {c['nom']} (Cost: {c['cost']} €) - Efecte: {c['efecte']}")

        while True:
            
            eleccio = input("Selecciona carta (1-3) o 's' per sortir: ").lower() # AFEGIT 's'
            
            if eleccio == 's': # NOVA CONDICIÓ DE SORTIDA
                print("❌ Surt de la compra d'Estratègies.")
                regles.ESTAT_JOC["punts_accio_disponibles"] += 2 # Retorna els AP gastats
                return # Tanca la funció i evita el bloqueig
            
            carta_tria = cartes.get(eleccio)
            if carta_tria:
                cost_carta = carta_tria['cost']
                if regles.ESTAT_JOC["efectiu"] >= cost_carta:
                    regles.ESTAT_JOC["efectiu"] -= cost_carta
                    regles.ESTAT_JOC["estrategies"].append(carta_tria['nom'])
                    
                    # Aplicació immediata de l'efecte del Broker
                    if carta_tria['nom'] == "Analista Junior":
                         regles.ESTAT_JOC["brokers"] += 1
                         print(f"🥳 Has contractat un nou Broker! Ara tens {regles.ESTAT_JOC['brokers']} Brokers.")

                    print(f"✅ Has comprat: {carta_tria['nom']}. (-{cost_carta} €)")
                    break
                else:
                    print(f"❌ No tens {cost_carta} € per comprar aquesta carta.")
            else:
                print("Opció no vàlida.")
    else:
        return