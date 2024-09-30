from dpi import *
import matplotlib.pyplot as plt
from dpi import Agente_random

"""En este fichero se proponen algunas pruebas para comprobar el funcionamiento de las clases implementadas en la libreria dpi."""


def main():
    # Definir el dilema
    dilema = Dilema(cc=2, cd=-1, dc=3, dd=0)
    
    # Crear agentes
    agentes = [
        Cooperator(dilema),
        Defector(dilema),
        Tft(dilema),
        Agente_random(dilema),
        Detective(dilema),
    ]
    
    # Simular una partida entre dos agentes
    print("Simulando una partida entre Tft y Random...")
    partida = Partida(dilema, Tft(dilema), Agente_random(dilema), n_rondas=10)
    partida.simular_partida()
    print(partida.resultados_partida)
    
    # Simular un torneo entre todos los agentes
    print("\nSimulando un torneo entre todos los agentes...")
    torneo = Torneo(agentes, n_rondas=10, repeticiones=5)
    torneo.simular_torneo()
    torneo.ordenar_ranking()
    print("Ranking del torneo:")
    for agente, puntuacion in torneo.ranking.items():
        print(f"{agente.nombre}: {puntuacion}")
    
    # Dibujar el ranking del torneo
    torneo.dibujar_ranking()
    
    # Simular un torneo evolutivo
    print("\nSimulando un torneo evolutivo...")
    torneo_evolutivo = Torneo_evolutivo(
        jugadores=tuple(agentes),
        n_rondas=10,
        generaciones=15,
        reprodctividad=0.1,
        polacion_inicial=60
    )
    torneo_evolutivo.simular()
    torneo_evolutivo.dibujar_resultados()


if __name__ == "__main__":
    main()
