import random
import sys
import regles
import accions

def bloqueig_mercat():
    """Simula l'acció bloquejada per l'Automa a l'inici del torn."""
    # Llista d'opcions que poden ser bloquejades
    opcions_bloqueig = [
        "Ingrés Bàsic", "Ticker A", "Ticker B", "Préstec Ràpid"
    ]
    
    # L'acció "Desenvolupament" (cost 2 AP) només està disponible a partir del Torn 5
    if regles.ESTAT_JOC["torn_actual"] >= 5:
        opcions_bloqueig.append("Desenvolupament")

    if not opcions_bloqueig:
        return None
    
    return random.choice(opcions_bloqueig)


def obtenir_opcions_disponibles():
    """Retorna un diccionari de totes les opcions i la seva lògica."""
    opcions = {
        "1": {"nom": "Ingrés Bàsic", "cost": 1, "func": accions.ingres_basic},
        "2": {"nom": "Ticker A", "cost": 1, "func": accions.comprar_ticker_a},
        "3": {"nom": "Ticker B", "cost": 1, "func": accions.comprar_ticker_b},
        "4": {"nom": "Préstec Ràpid", "cost": 1, "func": accions.prestec_rapid}
    }
    
    # S'obre "Desenvolupament" al Torn 5
    if regles.ESTAT_JOC["torn_actual"] >= 5:
        opcions["5"] = {"nom": "Desenvolupament", "cost": 2, "func": accions.comprar_desenvolupament}
    
    return opcions


def mostrar_estat_i_opcions(accio_bloquejada):
    """Mostra l'estat actual del joc i les opcions per al jugador."""
    estat = regles.ESTAT_JOC
    
    # --- Mostrar Estat ---
    print("\n" + "="*70)
    print(f"| 📊 ESTAT ACTUAL | TORN: {estat['torn_actual']} / CICLE: {regles.obtenir_cicle_actual()} | AP: {estat['punts_accio_disponibles']} |")
    print("-" * 70)
    print(f"| 👨‍💼 BROKERS: {estat['brokers']} | 💰 EFECTIU: {estat['efectiu']} € | DEUTES: {estat['deute_tokens']} (PENALITZACIÓ: -{estat['deute_tokens']*3} VN) |")
    print(f"| 📈 ACCIONS: Ticker A: {estat['accions']['A']}, Ticker B: {estat['accions']['B']}")
    print(f"| 🛠️ ESTRATÈGIES: {', '.join(estat['estrategies']) if estat['estrategies'] else 'Cap'}")
    print("=" * 70)
    
    # --- Mostrar Acció Bloquejada ---
    if accio_bloquejada:
        print(f"🛑 EL MERCAT BLOQUEJA: **{accio_bloquejada}**")
        
    # --- Mostrar Opcions d'Acció ---
    print("\n--- ACCIONS DISPONIBLES (SELECCIONA EL NÚMERO) ---")
    opcions = obtenir_opcions_disponibles()
    
    for clau, detalls in opcions.items():
        bloquejada = " [BLOQUEJADA 🛑]" if detalls["nom"] == accio_bloquejada else ""
        ap_disponibles = f" (Cost: {detalls['cost']} AP)"
        
        # Només mostra l'opció si el jugador té prou AP
        if detalls["cost"] <= estat["punts_accio_disponibles"]:
            print(f"{clau}: {detalls['nom']}{ap_disponibles}{bloquejada}")


def bucle_principal():
    """El bucle principal que gestiona la progressió del joc i la interacció."""
    print("--- INICI DEL JOC: Mercat Limit Solitari (9 Torns, Risc Agrícola) ---")
    
    # Bucle del joc (9 torns)
    while regles.ESTAT_JOC["torn_actual"] <= 9:
        
        accio_bloquejada = bloqueig_mercat()
        
        # Bucle d'Accions (Mentre li quedin AP)
        while regles.ESTAT_JOC["punts_accio_disponibles"] > 0:
            mostrar_estat_i_opcions(accio_bloquejada)
            opcions = obtenir_opcions_disponibles()
            
            # --- Entrada de l'Usuari ---
            eleccio = input(f"\nSelecciona acció (1-{len(opcions)}), 's' per Estat, o 'f' per finalitzar el torn: ").lower()
            
            if eleccio == 'f':
                break
            
            if eleccio == 's':
                continue
                
            detalls_accio = opcions.get(eleccio)
            
            if detalls_accio:
                # 1. Comprovació de Bloqueig
                if detalls_accio["nom"] == accio_bloquejada:
                    print(f"🛑 Error: L'acció '{detalls_accio['nom']}' està bloquejada pel Mercat aquest torn.")
                    continue
                
                # 2. Comprovació d'AP (ja filtrada a 'mostrar_estat_i_opcions', però important)
                if detalls_accio["cost"] > regles.ESTAT_JOC["punts_accio_disponibles"]:
                    print("❌ Error: No tens suficients Punts d'Acció (AP).")
                    continue
                
                # 3. Executar l'Acció
                detalls_accio["func"]()
            else:
                print("❌ Opció no vàlida. Intenta de nou.")

        # 4. Finalitzar Torn i Collita (Lògica a regles.py)
        regles.finalitzar_torn()
        
    # 5. Fi del joc: Ja gestionat a regles.finalitzar_torn (que crida calcular_valor_net_final)

if __name__ == "__main__":
    bucle_principal()