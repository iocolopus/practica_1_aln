from abc import ABC, abstractmethod
from random import random, randint
import matplotlib.pyplot as plt
import math

class Dilema:
    def __init__(self, cc: float, cd: float, dc: float, dd: float):
        self.payoff_matrix = [[(cc, cc), (cd, dc)],
                              [(dc, cd), (dd, dd)]]

    def evaluate_result(self, a_1: int, a_2: int) -> tuple[float, float]:
        return self.payoff_matrix[a_1][a_2]


class Agente(ABC):
    def __init__(self, dilema: Dilema):
        self.nombre = self.__class__.__name__
        self.dilema = dilema

    @abstractmethod
    def generar_decision(self, historial_oponente):
        pass


class Cooperator(Agente):
    def generar_decision(self, historial_oponente):
        return 0  # Siempre coopera


class Defector(Agente):
    def generar_decision(self, historial_oponente):
        return 1  # Siempre defrauda


class Tft(Agente):
    def generar_decision(self, historial_oponente):
        if not historial_oponente:  # Primer movimiento
            return 0  # Coopera
        return historial_oponente[-1]  # Copia la última jugada del oponente


class Partida:
    def __init__(self, dilema: Dilema, agente_1: Agente, agente_2: Agente, n_rondas=10, probabilidad_de_finalizar=0, error=0.0):
        self.dilema = dilema
        self.agente_1 = agente_1
        self.agente_2 = agente_2
        self.n_rondas = n_rondas if probabilidad_de_finalizar == 0 else self.calcular_rondas(probabilidad_de_finalizar)
        self.error = error
        self.historial_a1 = []
        self.historial_a2 = []

    def calcular_rondas(self, probabilidad_de_finalizar):
        rondas = 1
        while random() > probabilidad_de_finalizar:
            rondas += 1
        return rondas

    def simular_partida(self):
        total_a1, total_a2 = 0, 0
        for _ in range(self.n_rondas):
            decision_a1 = self.agente_1.generar_decision(self.historial_a2)
            decision_a2 = self.agente_2.generar_decision(self.historial_a1)
            if random() < self.error:
                decision_a1 = 1 - decision_a1
            if random() < self.error:
                decision_a2 = 1 - decision_a2
            resultado_a1, resultado_a2 = self.dilema.evaluate_result(decision_a1, decision_a2)
            total_a1 += resultado_a1
            total_a2 += resultado_a2
            self.historial_a1.append(decision_a1)
            self.historial_a2.append(decision_a2)
        return total_a1, total_a2


class Torneo:
    def __init__(self, jugadores, n_rondas, probabilidad_de_finalizar=0, error=0.0, repeticiones=2, dilema=Dilema(2, -1, 3, 0)):
        self.jugadores = jugadores
        self.n_rondas = n_rondas
        self.probabilidad_de_finalizar = probabilidad_de_finalizar
        self.error = error
        self.repeticiones = repeticiones
        self.dilema = dilema
        self.resultados = {jugador: 0.0 for jugador in jugadores}

    def simular_torneo(self):
        for _ in range(self.repeticiones):
            for i in range(len(self.jugadores)):
                for j in range(i + 1, len(self.jugadores)):
                    partida = Partida(self.dilema, self.jugadores[i], self.jugadores[j], self.n_rondas, self.probabilidad_de_finalizar, self.error)
                    resultado_a1, resultado_a2 = partida.simular_partida()
                    self.resultados[self.jugadores[i]] += resultado_a1
                    self.resultados[self.jugadores[j]] += resultado_a2

    def ordenar_ranking(self):
        return sorted(self.resultados.items(), key=lambda x: x[1], reverse=True)


class Poblacion:
    def __init__(self, jugadores, poblacion_inicial):
        self.jugadores = jugadores
        self.poblacion = {jugador: poblacion_inicial[i] for i, jugador in enumerate(jugadores)}
        self.historial = {jugador: [] for jugador in jugadores}

    def gestionar_evolucion(self, mejores, peores):
        self.eliminar_n_peores(peores)
        self.reproducir_n_mejores(mejores)

    def eliminar_n_peores(self, n):
        peores = sorted(self.poblacion.items(), key=lambda x: x[1])[:n]
        for peor in peores:
            del self.poblacion[peor[0]]

    def reproducir_n_mejores(self, n):
        mejores = sorted(self.poblacion.items(), key=lambda x: x[1], reverse=True)[:n]
        for mejor in mejores:
            self.poblacion[mejor[0]] += 1

    def actualizar_historial(self):
        for jugador, cantidad in self.poblacion.items():
            self.historial[jugador].append(cantidad)


class TorneoEvolutivo:
    def __init__(self, jugadores, n_rondas=100, error=0.0, probabilidad_de_finalizar=0.0, repeticiones=2, generaciones=100, reproductividad=0.05, poblacion_inicial=100, dilema=Dilema(2, -1, 3, 0)):
        self.jugadores = jugadores
        self.n_rondas = n_rondas
        self.error = error
        self.probabilidad_de_finalizar = probabilidad_de_finalizar
        self.repeticiones = repeticiones
        self.generaciones = generaciones
        self.reproductividad = reproductividad
        self.dilema = dilema
        poblacion_inicial = [poblacion_inicial // len(jugadores)] * len(jugadores)
        self.poblacion = Poblacion(jugadores, poblacion_inicial)
        self.reprod_int = int(poblacion_inicial[0] * self.reproductividad)

    def simular(self, imprimir=False):
        for generacion in range(self.generaciones):
            torneo = Torneo(self.poblacion.poblacion.keys(), self.n_rondas, self.probabilidad_de_finalizar, self.error, self.repeticiones, self.dilema)
            torneo.simular_torneo()
            ranking = torneo.ordenar_ranking()
            self.poblacion.gestionar_evolucion(self.reprod_int, self.reprod_int)
            if imprimir:
                print(f"Generacion {generacion}: {ranking}")
            self.poblacion.actualizar_historial()

    def dibujar_resultados(self):
        generaciones = range(1, self.generaciones + 1)
        for jugador in self.jugadores:
            plt.plot(generaciones, self.poblacion.historial[jugador], label=jugador.nombre)
        plt.xlabel('Generaciones')
        plt.ylabel('Población')
        plt.legend()
        plt.show()