import random

class Estrategia_12695(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        super().__init__(dilemma, name)
        self.parametro_memoria = parametro_memoria = [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1]

    def strategy(self, opponent: Player) -> int:
        historial_oponente = opponent.history

        """Durante las 4 primeras rondas empieza cooperando y la probabilidad cooperar se basa en lo que haya cooperado el oponente, de modo que acepta cadenas de cooperacion si no hay error"""
        if len(historial_oponente) == 1:
            return 0
        elif rondas := len(historial_oponente) <= 3:
            prob_cooperar = (rondas - sum(historial_oponente)) / rondas

            if random.random() < prob_cooperar:
                return 0
            else:
                return 1
        else:
            indice = int("".join([str(x) for x in historial_oponente[-4:]]), 2)
            return self.parametro_memoria[indice]