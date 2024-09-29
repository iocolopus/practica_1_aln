from abc import ABC, abstractmethod
from random import random
import matplotlib.pyplot as plt
import copy
import math
from random import randrange

class Dilema:

    def __init__(self, cc: float, cd: float, dc: float, dd: float):
        self.cc = cc
        self.cd = cd
        self.dc = dc
        self.dd = dd

    @property
    def payoff_matrix(self) -> list[list[tuple[int, int]]]:
        return [[(self.cc, self.cc), (self.cd, self.dc)],
                [(self.dc, self.cd), (self.dd, self.dd)]]

    def evaluate_result(self, a_1: int, a_2: int) -> tuple[float, float]:
        return self.payoff_matrix[a_1][a_2]


class Resultados_partida:

    def __init__(self):
        self.lista_dic = []

    def append(self, resultado_ronda: tuple[float, float], decision_a1:int, decision_a2:int):
        self.lista_dic.append({"tupla_payoff": resultado_ronda, "tupla_decisiones": (decision_a1, decision_a2)})

    @property
    def totales(self):
        total_a1 = sum([dic['tupla_payoff'][0] for dic in self.lista_dic])
        total_a2 = sum([dic['tupla_payoff'][1] for dic in self.lista_dic])

        return (total_a1, total_a2)

    @property
    def lista_jugadas_a1(self):
        return [dic['tupla_decisiones'][0] for dic in self.lista_dic]


    @property
    def lista_jugadas_a2(self):
        return [dic['tupla_decisiones'][1] for dic in self.lista_dic]


    def __str__(self):
        bin_str = {
            0: "C",
            1: "D"
        }

        mi_string = ""

        for dic in self.lista_dic:
            mi_string += f"({dic['tupla_payoff'][0]}){bin_str[dic["tupla_decisiones"][0]]} | {bin_str[dic["tupla_decisiones"][1]]}({dic['tupla_payoff'][1]})\n"
        mi_string += f"Total: {self.totales[0]} | {self.totales[1]}\n"

        return mi_string

    def __len__(self):
        return len(self.lista_dic)



class Agente(ABC):
    def __init__(self, dilema : Dilema):
        self.nombre = self.__class__.__name__
        self.dilema = dilema
        self.resultados_partida = Resultados_partida()

    @abstractmethod
    def generar_decision(self):
        pass

    def resetear_resultado(self):
        self.resultados_partida = Resultados_partida()



class Cooperator(Agente):
    def __init__(self, dilema : Dilema):
        super().__init__(dilema)

    def generar_decision(self):
        return 0

class Defector(Agente):
    def __init__(self, dilema: Dilema):
        super().__init__(dilema)

    def generar_decision(self):
        return 1

class Tft(Agente):
    def __init__(self, dilema: Dilema):
        super().__init__(dilema)

    def generar_decision(self):
        if len(self.resultados_partida.lista_dic) == 0:
            return 0
        else:
            return self.resultados_partida.lista_jugadas_a2[-1]

class Agente_random(Agente):
    def __init__(self, dilema: Dilema):
        super().__init__(dilema)

    def generar_decision(self):
        return randrange(0,2)

class Partida:
    def __init__(self, dilema : Dilema, agente_1 : Agente, agente_2 : Agente, n_rondas = 10, probabilidad_de_finalizar = 0, error = 0.0):
        self.dilema = dilema
        self.agente_1 = agente_1
        self.agente_2 = agente_2
        self.probabilidad_de_finalizar = probabilidad_de_finalizar
        self.resultados_partida = Resultados_partida()
        self.error = error

        if probabilidad_de_finalizar != 0:
            assert 0 < probabilidad_de_finalizar <= 1, "La probabilidad de finalizar debe ser entre 0 y 1"

            i = 1

            terminado = False

            while not terminado:
                n_aleatorio = random()
                if n_aleatorio <= probabilidad_de_finalizar:
                    terminado = True
                i += 1

            self.n_rondas = i

        else:
            self.n_rondas = n_rondas


    def simular_partida(self):

        def ajustar_a_error(decision):
            n_aleatorio = random()
            if n_aleatorio < self.error:
                return int(not bool(decision))
            else:
                return decision

        for i in range(self.n_rondas):
            decision_a1 = ajustar_a_error(self.agente_1.generar_decision())
            decision_a2 = ajustar_a_error(self.agente_2.generar_decision())

            tupla_resultado_ronda = self.dilema.evaluate_result(decision_a1, decision_a2)

            self.resultados_partida.append(tupla_resultado_ronda, decision_a1, decision_a2)

            self.agente_1.resultados_partida.append(tupla_resultado_ronda, decision_a1, decision_a2)
            self.agente_2.resultados_partida.append(self.dilema.evaluate_result(decision_a2, decision_a1), decision_a2, decision_a1)

        self.agente_1.resetear_resultado()
        self.agente_2.resetear_resultado()

class Torneo():
    def __init__(self, jugadores : [Agente, ...], n_rondas, probabilidad_de_finalizar = 0, error = 0.0, repeticiones = 2, dilema = Dilema(2, -1, 3, 0)):
        def generar_enfrentamientos():

            lista_enfrentamientos = []

            for i in range(len(jugadores)):
                for j in range(i + 1, len(jugadores)):
                    lista_enfrentamientos.append((jugadores[i], jugadores[j]))

            return lista_enfrentamientos


        self.jugadores = jugadores
        self.n_rondas = n_rondas
        self.probabilidad_de_finalizar = probabilidad_de_finalizar
        self.error = error
        self.repeticiones = repeticiones
        self.enfrentamientos = generar_enfrentamientos()
        self.dilema = dilema
        self.ranking = {jugador: 0.0 for jugador in self.jugadores}  # initial vals

    #Modificar para poder hacer graficos bonitos

    def simular_torneo(self):
        for repeticion in range(self.repeticiones):
            for agente_1, agente_2 in self.enfrentamientos:
                partida = Partida(self.dilema, agente_1, agente_2, self.n_rondas, self.probabilidad_de_finalizar, self.error)

                partida.simular_partida()

                self.ranking[agente_1] += partida.resultados_partida.totales[0]
                self.ranking[agente_2] += partida.resultados_partida.totales[1]

                agente_1.resetear_resultado()
                agente_2.resetear_resultado()


    def ordenar_ranking(self):
        self.ranking = dict(sorted(self.ranking.items(), key=lambda tup: tup[1], reverse=True))

    def dibujar_ranking(self):
        self.ordenar_ranking()

        lista_nombres = list(map(lambda agente: agente.nombre, self.ranking.keys()))
        lista_valores = list(self.ranking.values())

        plt.bar(lista_nombres, lista_valores)
        plt.show()

class Poblacion:
    def __init__(self, jugadores, poblacion_inicial):
        self.jugadores = jugadores
        self.dic_poblacion = {copy.deepcopy(player): 0.0 for player, cantidad in zip(jugadores, poblacion_inicial) for _ in range(cantidad)}
        self.historial_contadores = [[] for _ in jugadores]

    @property
    def lista_poblacion(self):
        return list(self.dic_poblacion.keys())

    def ordenar_dic_poblacion(self):
        self.dic_poblacion = dict(sorted(self.dic_poblacion.items(), key=lambda tup: tup[1], reverse=True))

    def eliminar_n_peores(self, n):
        for i in range(n):
            self.dic_poblacion.popitem()

    def reproducir_n_mejores(self, n):
        items_poblacion = list(self.dic_poblacion.items())
        for i in range(n):
            items_poblacion.append(copy.deepcopy(items_poblacion[i]))

        self.dic_poblacion = dict(items_poblacion)

    def gestionar_evolucion(self, repr_int):
        #Mejorar la gestion de los casos de empate
        self.ordenar_dic_poblacion()
        self.eliminar_n_peores(repr_int)
        self.reproducir_n_mejores(repr_int)


    def actualizar_historial_contadores(self):
        for i, puntuacion in enumerate(self.contador.values()):
            self.historial_contadores[i].append(puntuacion)

    @property
    def contador(self):
        contador = {jugador.nombre:0 for jugador in self.jugadores}

        for jugador in self.lista_poblacion:
                contador[jugador.nombre] += 1

        return contador

class Torneo_evolutivo:

    def __init__(self, jugadores: tuple[Agente, ...],
                       n_rondas: int = 100,
                       error: float = 0.0,
                       probabilidad_de_finalizar: float = 0.0,
                       repeticiones: int = 2,
                       generaciones: int = 100,
                       reprodctividad: float = 0.05,
                       polacion_inicial: tuple[int, ...] | int = 100,
                       dilema = Dilema(2, -1, 3, 0)):


        self.jugaodores = jugadores
        self.n_rondas = n_rondas
        self.error = error
        self.probabilidad_de_finalizar = probabilidad_de_finalizar
        self.repeticiones = repeticiones
        self.generaciones = generaciones
        self.reproductividad = reprodctividad
        self.dilema = dilema

        if isinstance(polacion_inicial, int):
            self.poblacion_inicial = [math.floor(polacion_inicial
                                                 / len(self.jugaodores))
                                      for _ in range(len(self.jugaodores))]
        else:
            self.poblacion_inicial = polacion_inicial

        self.poblacion_total = sum(self.poblacion_inicial)
        self.repr_int = int(self.poblacion_total * self.reproductividad)



        self.poblacion = Poblacion(jugadores, self.poblacion_inicial)


    #Hayy que gestionar los casos de empates
    def simular(self, imprimir = False):
        for generacion in range(self.generaciones):
            torneo_iterado = Torneo(self.poblacion.lista_poblacion, self.n_rondas, self.probabilidad_de_finalizar,self.error, self.repeticiones, self.dilema)
            torneo_iterado.simular_torneo()

            self.poblacion.dic_poblacion = torneo_iterado.ranking

            if imprimir:
                print(f"Generacion {generacion}: Poblacion: {self.poblacion.contador}")

            self.poblacion.actualizar_historial_contadores()

            self.poblacion.gestionar_evolucion(self.repr_int)


    def dibujar_resultados(self):
        plt.stackplot([i+1 for i in range(self.generaciones)], self.poblacion.historial_contadores)
        plt.legend([jugador.nombre for jugador in self.jugaodores])
        plt.xlabel('Generaciones')
        plt.ylabel('Poblaciones')
        plt.show()
