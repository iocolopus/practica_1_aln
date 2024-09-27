from abc import ABC, abstractmethod
from random import random
import matplotlib.pyplot as plt

class Dilema:

    def __init__(self, cc: float, cd: float, dc: float, dd: float):
        self.cc = cc
        self.cd = cd
        self.dc = dc
        self.dd = dd

    @property
    def payoff_matrix(self) -> list[list[tuple[int, int]]]:
        return [
            [(self.cc, self.cc), (self.cd, self.dc)],
            [(self.dc, self.cd), (self.dd, self.dd)],
        ]

    def evaluate_result(self, a_1: int, a_2: int) -> tuple[float, float]:
        """
        Given two actions, returns the payoffs of the two players.

        Parameters:
            - a_1 (int): action of player 1 ('C' or 'D', i.e. '1' or '0')
            - a_2 (int): action of player 2 ('C' or 'D', i.e. '1' or '0')

        Returns:
            - tuple of two floats, being the first and second values the payoff
            for the first and second player, respectively.
        """
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

    @property
    def lista_jugadas_a1(self):
        return [dic['tupla_decisiones'][0] for dic in self.lista_dic]


    @property
    def lista_jugadas_a2(self):
        return [dic['tupla_decisiones'][1] for dic in self.lista_dic]



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

class Defecator(Agente):
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

class Torneo_evolutivo():
    pass


def main():
    dp = Dilema(2, -1, 3, 0)

    colaborador = Cooperator(dp)
    colaborador_2 = Cooperator(dp)
    defecador = Defecator(dp)
    tft1 = Tft(dp)
    tft2 = Tft(dp)

    lista_jugaores = [tft1, tft2, colaborador_2, defecador]

    #partida = Partida(dp, colaborador, defecador, probabilidad_de_finalizar = 0.01, error = 0.1)
    #partida.simular_partida()
    #print(partida.resultados_partida)

    te_torneo = Torneo(lista_jugaores, 10)
    te_torneo.simular_torneo()
    te_torneo.ordenar_ranking()
    print(te_torneo.ranking)
    te_torneo.dibujar_ranking()

    print()


if __name__ == "__main__":
    main()