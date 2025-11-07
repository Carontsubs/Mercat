import regles_ia as regles
import random
import time
from collections import Counter
import accions_ia as accions

# --- ESTRATÈGIA D'IA BASE (ALEATÒRIA) ---

# simulador_ia.py (Funció accio_ia_base - Corregida)

def accio_ia_base():
    """Tria accions a l'atzar, filtrant per AP disponible (1 AP) i utilitzant strings."""
    
    ap_disponibles = regles.ESTAT_JOC["punts_accio_disponibles"]

    if ap_disponibles <= 0:
        return 

    # 1. Llista de NOMS (strings) i Costos d'AP.
    accions_costos = [
        ("comprar_accions_a", 1), 
        ("comprar_accions_b", 1),
        ("prestec_rapid", 1),
        ("ingresar_basic", 1),
        ("comprar_desenvolupament", 1) # Aquesta falla si AP=1
    ]

    # 🛑 FILTRE CLAU: Només tria accions que pot pagar amb AP.
    accions_possibles_filtrades = [
        name for name, cost in accions_costos if cost <= ap_disponibles
    ]

    if not accions_possibles_filtrades:
        # Aquesta condició no hauria de passar si AP > 0 i hem filtrat correctament, però ens protegeix.
        return

    # 2. Tria Aleatòria (ara accio_escollida és una STRING)
    accio_escollida = random.choice(accions_possibles_filtrades)
    
    # 3. EXECUCIÓ (El bloc if/elif ara funciona perquè compara strings)
    
    if accio_escollida == "comprar_accions_a":
        accions.comprar_accions_a()
    elif accio_escollida == "comprar_accions_b":
        accions.comprar_accions_b()
    elif accio_escollida == "prestec_rapid":
        accions.prestec_rapid()
    elif accio_escollida == "ingresar_basic":
        accions.ingresar_basic()
    elif accio_escollida == "comprar_desenvolupament":
        # Crida a l'acció
        accions.comprar_desenvolupament() 
    
    # La reducció d'AP ja es gestiona dins de cada funció cridada.
    return
# simulador_ia.py (Nova funció IA Supervivència)

def accio_ia_supervivencia():
    """Tria accions basades en la supervivència financera i el llindar de compra del Broker."""
    
    ap_disponibles = regles.ESTAT_JOC["punts_accio_disponibles"]
    efectiu = regles.ESTAT_JOC["efectiu"]
    torn = regles.obtenir_cicle_actual()
    deute = regles.ESTAT_JOC["deute_tokens"]
    te_fons_diversificat = "Fons Diversificat" in regles.ESTAT_JOC["estrategies"]
    
    if ap_disponibles <= 0:
        return 

    # --- Lògica de Decisió ---
    
    # 1. Prioritat Màxima: Comprar el Broker només si el podem mantenir.
    # Cost Broker: 4€
    # Cost de Manteniment (CO): 2€/Broker. Necessitem, com a mínim, un buffer de 6€ (4€ compra + 2€ marge).
    
    if torn > 1 and efectiu >= 3 and ap_disponibles >= 1: # ⬅️ LLINDAR DE 6€ CLAU!
        accio_escollida = "comprar_desenvolupament"
        
    # 2. Prioritat de Supervivència: Generar Fons.
    elif efectiu == 0:
        if torn > 1 and deute < 2:
            # Prioritzem el Préstec Ràpid (5€ immediats) per arribar al llindar de 6€ ràpidament.
            accio_escollida = "prestec_rapid"           
        else:
            accio_escollida = "ingresar_basic"
        
    # 3. Resta: Jugar a l'atzar (Accions de risc/recompensa)
# 3. RESTA: INVERTIR
    else:
        if te_fons_diversificat:
            # 🛑 NOU: Si ja té el Fons Diversificat, maximitza el VN acumulant 'A'
            accio_escollida = "comprar_accions_a"
        else:
            # Mantenir l'agressivitat fins a obtenir el Fons Diversificat (com ara)
            accions_alt_risc = ["comprar_accions_b", "comprar_accions_b", "comprar_accions_a"] 
            accio_escollida = random.choice(accions_alt_risc)   
# 🛑 REGISTRE DE L'ACCIÓ: L'afegim just abans de l'execució
    regles.ESTAT_JOC["accions_executades"].append(accio_escollida) 
    
    # 💥 EXECUCIÓ 💥
    accio_exitosa = False # Variable per monitoritzar si l'AP s'ha consumit

    if accio_escollida == "comprar_accions_a":
        accio_exitosa = accions.comprar_accions_a()
    elif accio_escollida == "comprar_accions_b":
        accio_exitosa = accions.comprar_accions_b()
    elif accio_escollida == "prestec_rapid":
        accio_exitosa = accions.prestec_rapid()
    elif accio_escollida == "ingresar_basic":
        accio_exitosa = accions.ingresar_basic()
    elif accio_escollida == "comprar_desenvolupament":
        resultat = accions.comprar_desenvolupament() # Aquesta funció retorna la carta (True) o False/None
        if resultat:
             accio_exitosa = True
        
    # 🛑 TALLAFOC CONTRA EL BLOQUEIG: Forcem el consum d'AP a zero si falla
    if not accio_exitosa and regles.ESTAT_JOC["punts_accio_disponibles"] > 0:
        # Si l'acció no ha tingut èxit (i no ha consumit AP), forcem la fi del torn.
        regles.ESTAT_JOC["punts_accio_disponibles"] = 0 
        
    return
# --- BUCLE DE SIMULACIÓ ---

def simular_prova_base():
    """Executa una simulació completa del joc usant l'IA base."""
    
    regles.inicialitzar_joc()
    regles.SILENT_MODE = True # Desactivem els prints per a la velocitat de simulació

    # 🛑 SOLUCIÓ CLAU: Creació/Reinicialització de les llistes per al comptatge
    # Aquesta línia evita l'AttributeError si la clau no existeix.
    regles.ESTAT_JOC["accions_executades"] = [] 
    regles.ESTAT_JOC["estrategies"] = []

    while regles.ESTAT_JOC["torn_actual"] <= 9:
        # FASE D'ACCIÓ
        # L'IA fa accions fins que s'acaben els AP
        while regles.ESTAT_JOC["punts_accio_disponibles"] > 0:
            # accio_ia_base()
            accio_ia_supervivencia()
            
        # FASE DE TANCAMENT DE TORN
        regles.finalitzar_torn()
        
    # El joc ha finalitzat (després del Torn 9 i la Fase de Mercat)
    vn = regles.calcular_valor_net_final_silencios()
    return vn

# --- EXECUCIÓ I RESULTATS ---

def executar_prova_base(num_simulacions=1000):
    """Executa múltiples simulacions i calcula el VN mitjà."""
    
    print(f"Iniciant {num_simulacions} simulacions (Mode Silenciós)...")
    
    # 🛑 NOU: Comptadors d'Accions i Desenvolupament
    comptador_accions_totals = Counter()
    comptador_desenvolupament = Counter()

    resultats_vn = []
    temps_inici = time.time()

    for i in range(num_simulacions):
        vn = simular_prova_base()
        resultats_vn.append(vn)
        # 🛑 NOU: Acumular les estadístiques de desenvolupament
        # Aquesta informació ja es troba a ESTAT_JOC["estrategies"]
        comptador_desenvolupament.update(regles.ESTAT_JOC["estrategies"])
        comptador_accions_totals.update(regles.ESTAT_JOC["accions_executades"]) 

    temps_final = time.time()
    
    # Càlcul d'Estadístiques
    vn_mitja = sum(resultats_vn) / len(resultats_vn)
    vn_maxim = max(resultats_vn)
    vn_minim = min(resultats_vn)
    
    # Càlcul de Freqüència (Opcional)
    counts = Counter(resultats_vn)
    vn_mes_comu = counts.most_common(1)[0][0]

    print("\n--- Resultats de la Simulació ---")
    print(f"Simulacions realitzades: {num_simulacions}")
    print(f"Temps total d'execució: {temps_final - temps_inici:.2f} segons")
    print(f"Valor Net (VN) Mitjà: {vn_mitja:.2f} €")
    print(f"VN Màxim Assolit: {vn_maxim} €")
    print(f"VN Mínim Assolit: {vn_minim} €")
    print(f"VN Més Comú (Moda): {vn_mes_comu} €")
    # 🛑 NOU BLOC: Impressió de la Freqüència d'Accions Base
    print("\n--- Freqüència d'Accions Base ---")
    if comptador_accions_totals:
        total_accions = sum(comptador_accions_totals.values())
        for nom, count in comptador_accions_totals.most_common():
            # Calculem el percentatge d'ús de cada acció
            percentatge = (count / total_accions) * 100
            print(f"- {nom}: {count} vegades ({percentatge:.1f}%)")
    else:
        print("- No s'han registrat accions base.")
    print("\n--- Estadístiques de Desenvolupament ---")
    if comptador_desenvolupament:
        # Si s'ha comprat alguna carta, mostrem el recompte per a cadascuna.
        for nom, count in comptador_desenvolupament.most_common():
            print(f"- {nom}: {count} vegades")
    else:
        # 🛑 CANVI CLAU: Si el comptador és buit, mostrem 0 vegades.
        print("- Cartes comprades: 0 vegades")    
    
    print("-" * 35)

# --- INICI DEL PROGRAMA ---
if __name__ == "__main__":
    # Executa la prova amb un nombre raonable de simulacions
    executar_prova_base(num_simulacions=100)