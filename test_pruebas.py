from abc import ABC, abstractmethod
from random import choice

C = 0
D = 1

bin_str = {
    0:"C",
    1:"D"
}

class Resultados_partida:

    def __init__(self):
        self.lista_dic = []

    def append(self, resultado_ronda, decision_a1, decision_a2):
        self.lista_dic.append({"tupla_payoff": resultado_ronda, "tupla_decisiones": (decision_a1, decision_a2)})

    @property
    def totales(self):
        total_a1 = sum([dic['tupla_payoff'][0] for dic in self.lista_dic])
        total_a2 = sum([dic['tupla_payoff'][1] for dic in self.lista_dic])

        return (total_a1, total_a2)

    def ganador(self):
        return bool(self.totales[1] >= self.totales[0])

    def __str__(self):
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

    def __init__(self):
        self.resultados_partida = Resultados_partida()
        self.local = None

    def lista_decisiones_agente(self):
        if self.local is None:
            return None
        elif self.local == True:
            return self.resultados_partida.lista_jugadas_a1
        else:
            return self.resultados_partida.lista_jugadas_a2

    def lista_decisiones_oponente(self):
        if self.local is None:
            return None
        elif self.local == True:
            return self.resultados_partida.lista_jugadas_a2
        else:
            return self.resultados_partida.lista_jugadas_a1


    @abstractmethod
    def generar_decision(self):
        pass

    def guardar_resultado_ronda(self, resultado, decision_a1, decision_a2):
        self.resultados_partida.append(resultado, decision_a1, decision_a2)

class Player(ABC):

    @abstractmethod
    def __init__(self, dilemma: Dilemma, name: str = ""):
        """
        Abstract class that represents a generic player

        Parameters:
            - name (str): the name of the strategy
            - dilemma (Dilemma): the dilemma that this player will play
        """

        self.name = name
        self.dilemma = dilemma

        self.history  = []  # This is the main variable of this class. It is
                            # intended to store all the history of actions
                            # performed by this player.
                            # Example: [C, C, D, D, D] <- So far, the
                            # interaction lasts five rounds. In the first one,
                            # this player cooperated. In the second, he also
                            # cooperated. In the third, he defected. Etc.


    @abstractmethod
    def strategy(self, opponent: Player) -> int:
        """
        Main call of the class. Gives the action for the following round of the
        interaction, based on the history

        Parameters:
            - opponent (Player): is another instance of Player.

        Results:
            - An integer representing Cooperation (C=0) or Defection (D=1)
        """
        pass


    def compute_scores(self, opponent: Player) -> tuple[float, float]:
        """
        Compute the scores for a given opponent

        Parameters:
            - opponent (Player): is another instance of Player.

        Results:
            - A tuple of two floats, where the first value is the current
            player's payoff, and the second value is the opponent's payoff.
        """
        raise NotImplementedError


    # Este método ya está implementado
    def clean_history(self):
        """Resets the history of the current player"""
        self.history = []

class Agente_random(Agente):
    def __init__(self):
        super().__init__()

    def generar_decision(self):
        return choice((C, D))

class Agente_colaborador(Agente):
    def __init__(self):
        super().__init__()

    def generar_decision(self):
        return C

class Agente_desertor(Agente):
    def __init__(self):
        super().__init__()

    def generar_decision(self):
        return D

class Agente_tit_for_tat(Agente):
    def __init__(self):
        super().__init__()

    def generar_decision(self):
        if len(self.resultados_partida) == 0:
            return C
        else:
            return self.resultados_partida.lista_jugadas_a2[-1]


class Enfrentamiento_iterado:
    def __init__(self, a1 : Agente, a2 : Agente, iteraciones = 10):
        self.iteraciones = iteraciones
        self.a1 = a1
        self.a2 = a2

        self.payoff_matrix = [[(2, 2), (-1, 3)],
                              [(3, -1), (0, 0)]]

        self.resultados_partida = Resultados_partida()

        a1.local = True
        a2.local = False

    def simular_ronda(self):
        decision_a1 = self.a1.generar_decision()
        decision_a2 = self.a2.generar_decision()

        resultado_ronda = self.payoff_matrix[decision_a1][decision_a2]

        self.resultados_partida.append(resultado_ronda, decision_a1, decision_a2)

        self.a1.guardar_resultado_ronda(resultado_ronda, decision_a1, decision_a2)
        self.a2.guardar_resultado_ronda(resultado_ronda, decision_a1, decision_a2)

    def simular_partida(self):
        for i in range(self.iteraciones):
            resultado_ronda = self.simular_ronda()

        return self.resultados_partida


a1 = Agente_random()
a2 = Agente_tit_for_tat()

enfrentamiento = Enfrentamiento_iterado(a1, a2, 100)

resultado = enfrentamiento.simular_partida()
print(resultado)