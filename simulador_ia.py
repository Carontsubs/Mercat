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

# simulador_ia.py (Funció accio_ia_supervivencia - Estratègia V6)

import regles_ia as regles
import random
import accions_ia as accions

def accio_ia_supervivencia():
    """Tria accions basades en l'estratègia guanyadora: Supervivència, Control de CO i Maximització de VN."""
    
    # --- Inicialització d'Estat ---
    ap_disponibles = regles.ESTAT_JOC["punts_accio_disponibles"]
    efectiu = regles.ESTAT_JOC["efectiu"]
    # Utilitzem el CICLE per a la gestió de la fase de joc (Cicle 2 = Torn 5)
    cicle = regles.obtenir_cicle_actual() 
    deute = regles.ESTAT_JOC["deute_tokens"]
    # Clau per a la lògica de maximització de VN
    te_fons_diversificat = "Fons Diversificat" in regles.ESTAT_JOC["estrategies"]
    
    if ap_disponibles <= 0:
        return 

    # --- Lògica de Decisió Prioritzada ---
    
    # P1: SUPERVIVÈNCIA (GENERAR FONS DE FORMA SEGURA)
    # L'acció més barata d'inversió és 1€ (Accions A/B), necessitem fons per jugar.
# P1: SUPERVIVÈNCIA/GENERAR FONS (efectiu < 3€)
    if efectiu < 1: 
        
        # 🛑 PRIORITAT 1A: CICLE INICIAL (SUPERVIVÈNCIA SEGURA i coberta de CO)
        if cicle == 1:
            # Utilitzem Ingresar Bàsic per generar fons sense risc de deute ni pèrdua d'accions
            # accio_escollida = "ingresar_basic"
            accions_alt_risc = ["comprar_accions_b", "comprar_accions_a", "comprar_accions_a", "ingresar_basic"] 
            accio_escollida = random.choice(accions_alt_risc)

                
        # 🛑 PRIORITAT 1B: CICLE AVANÇAT (NOMÉS RISC/DEUTE SI CAL)
        elif cicle > 1:
            if deute < 2:
                # Si el joc avança, usem Préstec Ràpid per accelerar la inversió
                accio_escollida = "prestec_rapid"
            else:
                # Si el deute és alt, encara hem de fer servir Ingresar Basic com a últim recurs
                accions_alt_risc = ["comprar_accions_b", "comprar_accions_a", "comprar_accions_a"] 
                accio_escollida = random.choice(accions_alt_risc)
                # accio_escollida = "ingresar_basic"

                
    # P2: DESENVOLUPAMENT (A partir del Cicle 2, per comprar Fons Diversificat, Algoritme o Broker)
    # El llindar de 3€ permet pagar la majoria de cartes i la funció interna tria la millor.
    elif cicle > 1 and efectiu >= 2: 
        accio_escollida = "comprar_desenvolupament"
        
    # P3: MAXIMITZACIÓ DE VN / INVERSIÓ
    else:
        # Si tenim fons i no necessitem comprar desenvolupament, invertim.
        
        if te_fons_diversificat:
            # 🛑 CLAU DE LA VICTÒRIA: Prioritzem Accions A per obtenir +1€/Unitat (VN)
            accio_escollida = "comprar_accions_a"
        else:
            # Altrament, busquem fons ràpids per al desenvolupament amb el màxim potencial de guany (B).
            accions_alt_risc = ["comprar_accions_b", "comprar_accions_a", "comprar_accions_a"] 
            accio_escollida = random.choice(accions_alt_risc)

    # --- EXECUCIÓ I TALLAFOC ---

    # 🛑 REGISTRE DE L'ACCIÓ
    regles.ESTAT_JOC["accions_executades"].append(accio_escollida) 
    
    accio_exitosa = False 

    if accio_escollida == "comprar_accions_a":
        accio_exitosa = accions.comprar_accions_a()
    elif accio_escollida == "comprar_accions_b":
        accio_exitosa = accions.comprar_accions_b()
    elif accio_escollida == "prestec_rapid":
        accio_exitosa = accions.prestec_rapid()
    elif accio_escollida == "ingresar_basic":
        accio_exitosa = accions.ingresar_basic()
    elif accio_escollida == "comprar_desenvolupament":
        # La funció interna retorna True si l'acció ha tingut èxit (s'ha pogut comprar i pagar)
        accio_exitosa = accions.comprar_desenvolupament()
        
    # 🛑 TALLAFOC CONTRA EL BLOQUEIG: Forcem el consum d'AP a zero si l'acció falla
    if not accio_exitosa and regles.ESTAT_JOC["punts_accio_disponibles"] > 0:
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
    regles.ESTAT_JOC["comptador_ingres_basic"] = 0


    # while regles.ESTAT_JOC["torn_actual"] <= 9:
        # FASE D'ACCIÓ
        # L'IA fa accions fins que s'acaben els AP
    while regles.ESTAT_JOC["punts_accio_disponibles"] > 0:
        # accio_ia_base()
        accio_ia_supervivencia()
            
        # FASE DE TANCAMENT DE TORN
        joc_finalitzat = regles.finalitzar_torn() 
        
        if joc_finalitzat:
            break # ⬅️ Surt del bucle quan el joc ha acabat

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
    total_co_acumulat = 0 
    total_deute_tokens = 0

    resultats_vn = []
    temps_inici = time.time()

    for i in range(num_simulacions):
        vn = simular_prova_base()
        resultats_vn.append(vn)
        # 🛑 NOU: Acumular les estadístiques de desenvolupament
        # Aquesta informació ja es troba a ESTAT_JOC["estrategies"]
        comptador_desenvolupament.update(regles.ESTAT_JOC["estrategies"])
        comptador_accions_totals.update(regles.ESTAT_JOC["accions_executades"])
        total_co_acumulat += regles.ESTAT_JOC["registre_co_total"]
        total_deute_tokens += regles.ESTAT_JOC["registre_deute_adquirit"] 

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

    # 🛑 NOU BLOC: Resultats de CO
    co_mitja_per_simulacio = total_co_acumulat / num_simulacions
    deute_mitja_per_simulacio = total_deute_tokens / num_simulacions

    print("\n--- Estadístiques de Cost Operatiu (CO) ---")
    print(f"CO Acumulat Mitjà per Simulació: {co_mitja_per_simulacio:.2f} €")
    print(f"Tokens de Deute Adquirits Mitjà: {deute_mitja_per_simulacio:.2f}")
    
    print("-" * 35)

# --- INICI DEL PROGRAMA ---
if __name__ == "__main__":
    # Executa la prova amb un nombre raonable de simulacions
    executar_prova_base(num_simulacions=100)