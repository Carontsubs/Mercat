import regles
import random
import time
from collections import Counter

# --- ESTRATÈGIA D'IA BASE (ALEATÒRIA) ---

def accio_ia_base():
    """L'IA executa una acció aleatòria basada en els AP disponibles."""
    
    punts_accio = regles.ESTAT_JOC["punts_accio_disponibles"]
    
    if punts_accio <= 0:
        return # No es pot fer res

    # Opcions d'acció amb el seu cost d'AP. 
    # Notem que comprar accions i desenvolupament pot costar 1 o 2 AP.
    # Assumim aquí que totes les accions costen 1 AP per simplicitat en la prova base.
    
    accions_possibles = [
        "comprar_accions_a", 
        "comprar_accions_b",
        "contractar_broker",
        # Inclou altres accions que costin 1 AP, com ara comprar desenvolupament (si costa 1 AP).
        "prestec_rapid" # Aquesta acció no gasta AP, però és una acció vàlida.
    ]

    # L'IA només tria una acció si té AP.
    if regles.ESTAT_JOC["punts_accio_disponibles"] > 0:
        # Trieu una acció aleatòria entre les que costen 1 AP o no costen AP
        accio_escollida = random.choice(accions_possibles)
        
        # NOTE: Aquí normalment cridaríem a la funció corresponent del mòdul accions.py
        # Per simplificar la prova base, simulem el cost d'AP.
        
        if accio_escollida == "prestec_rapid":
            # La funció prestec_rapid() no gasta AP però guanya diners i genera deute.
            # Hauries de cridar: accions.prestec_rapid()
            pass # Implementació simplificada
        else:
            # Per a la prova base, només gastem 1 AP per simular la compra/contractació.
            # En el teu codi real, caldria la lògica de accions.py
            regles.ESTAT_JOC["punts_accio_disponibles"] -= 1

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