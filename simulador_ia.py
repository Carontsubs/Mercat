import regles_ia as regles
import random
import time
from collections import Counter
import accions_ia as accions

# --- ESTRATÈGIA D'IA BASE (ALEATÒRIA) ---

def accio_ia_base():
    
    if regles.ESTAT_JOC["punts_accio_disponibles"] <= 0:
        return 

    # 🛑 Aquesta llista ha d'utilitzar els noms de les funcions reals a accions.py
    # La IA BASE només tria accions que existeixen i consumeixen AP.
    accions_possibles = [
        accions.comprar_accions_a, 
        accions.comprar_accions_b,
        accions.prestec_rapid,
        accions.comprar_desenvolupament,
        accions.ingresar_basic # Afegim l'acció d'Ingrés Bàsic
        # NOTE: Si contractar_broker és només un efecte de carta, l'eliminem d'aquí.
    ]

    # Trieu i executeu una funció d'acció aleatòria
    funcio_escollida = random.choice(accions_possibles)
    
    # 💥 EXECUCIÓ 💥
    # Com que cada funció gestiona el seu propi consum d'AP internament,
    # el bucle es trencarà quan s'esgotin els AP.
    funcio_escollida() 
    
    return

# --- BUCLE DE SIMULACIÓ ---

def simular_prova_base():
    """Executa una simulació completa del joc usant l'IA base."""
    
    regles.inicialitzar_joc()
    regles.SILENT_MODE = True # Desactivem els prints per a la velocitat de simulació

    while regles.ESTAT_JOC["torn_actual"] <= 9:
        # FASE D'ACCIÓ
        # L'IA fa accions fins que s'acaben els AP
        while regles.ESTAT_JOC["punts_accio_disponibles"] > 0:
            accio_ia_base()
            
        # FASE DE TANCAMENT DE TORN
        regles.finalitzar_torn()
        
    # El joc ha finalitzat (després del Torn 9 i la Fase de Mercat)
    vn = regles.calcular_valor_net_final_silencios()
    return vn

# --- EXECUCIÓ I RESULTATS ---

def executar_prova_base(num_simulacions=1000):
    """Executa múltiples simulacions i calcula el VN mitjà."""
    
    print(f"Iniciant {num_simulacions} simulacions (Mode Silenciós)...")
    
    resultats_vn = []
    temps_inici = time.time()

    for i in range(num_simulacions):
        vn = simular_prova_base()
        resultats_vn.append(vn)

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
    print("-" * 35)

# --- INICI DEL PROGRAMA ---
if __name__ == "__main__":
    # Executa la prova amb un nombre raonable de simulacions
    executar_prova_base(num_simulacions=50)