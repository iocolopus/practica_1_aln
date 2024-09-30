from abc import ABC, abstractmethod
from random import random
import matplotlib.pyplot as plt
import copy
import math
from random import randrange

class Dilema:
    """
    Representa un dilema del tipo dilema del prisionero iterado, donde las decisiones de los jugadores 
    generan diferentes recompensas.

    Atributos:
        cc (float): Recompensa cuando ambos jugadores cooperan.
        cd (float): Recompensa cuando el jugador 1 coopera y el jugador 2 traiciona.
        dc (float): Recompensa cuando el jugador 1 traiciona y el jugador 2 coopera.
        dd (float): Recompensa cuando ambos jugadores traicionan.
    """
    def __init__(self, cc: float, cd: float, dc: float, dd: float):
        """
        Inicializa un dilema con los pagos correspondientes a las diferentes combinaciones de decisiones.
        """
        self.cc = cc
        self.cd = cd
        self.dc = dc
        self.dd = dd

    @property
    def payoff_matrix(self) -> list[list[tuple[int, int]]]:
        """
        Devuelve la matriz de pagos del dilema para las decisiones de ambos jugadores.
        
        Devuelve:
            list[list[tuple[int, int]]]: Matriz de pagos, donde cada posición contiene una tupla con los pagos
            correspondientes a las decisiones de ambos jugadores.
        """
        return [[(self.cc, self.cc), (self.cd, self.dc)],
                [(self.dc, self.cd), (self.dd, self.dd)]]

    def evaluate_result(self, a_1: int, a_2: int) -> tuple[float, float]:
        """
        Evalúa el resultado de una ronda dada las decisiones de ambos jugadores.
        
        Parámetros:
            a_1 (int): Decisión del jugador 1 (0 para cooperar, 1 para traicionar).
            a_2 (int): Decisión del jugador 2 (0 para cooperar, 1 para traicionar).
        
        Devuelve:
            tuple[float, float]: Recompensas de ambos jugadores según sus decisiones.
        """
        return self.payoff_matrix[a_1][a_2]


class Resultados_partida:
    """
    Almacena los resultados de una partida entre dos agentes a lo largo de varias rondas.

    Atributos:
        lista_dic (list): Lista de diccionarios que contiene los resultados de cada ronda y las decisiones de ambos jugadores.
    """

    def __init__(self):
        """
        Inicializa una nueva instancia vacía de Resultados_partida.
        """
        self.lista_dic = []

    def append(self, resultado_ronda: tuple[float, float], decision_a1:int, decision_a2:int):
        """
        Añade el resultado de una ronda a la lista de resultados de la partida.
        
        Parámetros:
            resultado_ronda (tuple[float, float]): La recompensa obtenida por ambos jugadores en la ronda.
            decision_a1 (int): Decisión del jugador 1.
            decision_a2 (int): Decisión del jugador 2.
        """
        self.lista_dic.append({"tupla_payoff": resultado_ronda, "tupla_decisiones": (decision_a1, decision_a2)})

    @property
    def totales(self):
        """
        Calcula el total acumulado de recompensas para ambos jugadores.

        Devuelve:
            tuple[float, float]: Total acumulado de recompensas de ambos jugadores.
        """
        total_a1 = sum([dic['tupla_payoff'][0] for dic in self.lista_dic])
        total_a2 = sum([dic['tupla_payoff'][1] for dic in self.lista_dic])

        return (total_a1, total_a2)

    @property
    def lista_jugadas_a1(self):
        """
        Devuelve la lista de decisiones realizadas por el jugador 1.

        Devuelve:
            list[int]: Lista de decisiones del jugador 1 en cada ronda.
        """
        return [dic['tupla_decisiones'][0] for dic in self.lista_dic]


    @property
    def lista_jugadas_a2(self):
        """
        Devuelve la lista de decisiones realizadas por el jugador 2.

        Devuelve:
            list[int]: Lista de decisiones del jugador 2 en cada ronda.
        """
        return [dic['tupla_decisiones'][1] for dic in self.lista_dic]


    def __str__(self):
        """
        Devuelve una representación en cadena de texto de los resultados de la partida, mostrando 
        las recompensas obtenidas por ambos jugadores en cada ronda.

        Devuelve:
            str: Representación de los resultados de la partida.
        """
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
        """
        Devuelve la cantidad de rondas jugadas en la partida.

        Devuelve:
            int: Número de rondas jugadas.
        """
        return len(self.lista_dic)



class Agente(ABC):
    """
    Clase abstracta que representa un agente en el dilema del prisionero.

    Atributos:
        nombre (str): Nombre del agente.
        dilema (Dilema): Instancia del dilema que el agente juega.
        resultados_partida (Resultados_partida): Resultados de la partida jugada por el agente.
    """
    def __init__(self, dilema : Dilema):
        """
        Inicializa un agente con una instancia de un dilema.
        """
        self.nombre = self.__class__.__name__
        self.dilema = dilema
        self.resultados_partida = Resultados_partida()

    @abstractmethod
    def generar_decision(self):
        """
        Método abstracto que genera la decisión del agente (0 para cooperar, 1 para traicionar).
        """
        pass

    def resetear_resultado(self):
        """
        Resetea los resultados de la partida del agente.
        """
        self.resultados_partida = Resultados_partida()

    """ 
    Sub-clases de la clase Agente:

        Cooperator: Siempre coopera.
        Defector: Siempre traiciona.
        Tft (Tit-for-Tat): Empieza cooperando y luego imita la última decisión del otro jugador.
        Agente_random: Genera una decisión aleatoria (1 o 0).
        Detective: Sigue un patrón de decisiones predefinido y luego usa TFT o Defector.
        Grudger: Coopera hasta que el otro jugador traiciona, luego siempre traiciona.
    """

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
    
class Detective(Agente):
    
    def __init__(self, dilema: Dilema):
        super().__init__(dilema)
        self.defector = Defector(dilema)
        self.tft = Tft(dilema)

    def generar_decision(self):
        if len(self.resultados_partida.lista_dic) == 0:
            return 0
        elif len(self.resultados_partida.lista_dic) == 1:
            return 1
        elif len(self.resultados_partida.lista_dic) == 2:
            return 0
        elif len(self.resultados_partida.lista_dic) == 3:
            return 0
        
        else:
            if self.resultados_partida.lista_jugadas_a2[-1] == 0:
                return self.defector.generar_decision()
            
            if self.resultados_partida.lista_jugadas_a2[-1] == 1:
                return self.tft.generar_decision()
            
class Grudger(Agente):

    def __init__(self, dilema: Dilema):
        super().__init__(dilema)
        self.por_defecto = 0

    def generar_decision(self):
        if len(self.resultados_partida.lista_dic) == 0:
            return 0
        if self.resultados_partida.lista_jugadas_a2[-1] == 1:
            self.por_defecto = 1

        return self.por_defecto

class Partida:
    """
    Representa una partida entre dos agentes en el dilema del prisionero.

    Atributos:
        dilema (Dilema): Instancia del dilema jugado.
        agente_1 (Agente): Primer agente que participa en la partida.
        agente_2 (Agente): Segundo agente que participa en la partida.
        n_rondas (int): Número de rondas de la partida.
        probabilidad_de_finalizar (float): Probabilidad de que la partida finalice después de cada ronda.
        error (float): Probabilidad de que una decisión sea invertida debido a un error.
        resultados_partida (Resultados_partida): Resultados acumulados de la partida.
    """

    def __init__(self, dilema : Dilema, agente_1 : Agente, agente_2 : Agente, n_rondas = 10, probabilidad_de_finalizar = 0, error = 0.0):
        """
        Inicializa una partida entre dos agentes en el dilema del prisionero.
        """
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
        """
        Simula una partida entre los dos agentes durante el número de rondas especificado.
        """
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
    """
    Representa un torneo entre múltiples agentes en el dilema del prisionero.

    Atributos:
        jugadores (list[Agente]): Lista de agentes que participan en el torneo.
        n_rondas (int): Número de rondas por partida.
        probabilidad_de_finalizar (float): Probabilidad de que una partida termine antes de completar todas las rondas.
        error (float): Probabilidad de error en las decisiones de los agentes.
        repeticiones (int): Número de repeticiones de cada partida.
        dilema (Dilema): Instancia del dilema usado en el torneo.
        ranking (dict): Ranking de los agentes basado en sus puntuaciones.
    """
    def __init__(self, jugadores : list[Agente], n_rondas, probabilidad_de_finalizar = 0, error = 0.0, repeticiones = 2, dilema = Dilema(2, -1, 3, 0)):
        """
        Inicializa un torneo entre los agentes dados.
        """
        def generar_enfrentamientos():
            """
            Genera los enfrentamientos entre los agentes del torneo.

            Cada agente jugará contra todos los demás una vez.

            Retorna:
            list[tuple[Agente, Agente]]: Lista de tuplas, donde cada tupla representa un enfrentamiento entre dos agentes.
            """
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

    

    def simular_torneo(self):
        """
        Simula el torneo donde todos los jugadores juegan entre sí y acumulan puntos.
        """
        for repeticion in range(self.repeticiones):
            for agente_1, agente_2 in self.enfrentamientos:
                partida = Partida(self.dilema, agente_1, agente_2, self.n_rondas, self.probabilidad_de_finalizar, self.error)

                partida.simular_partida()

                self.ranking[agente_1] += partida.resultados_partida.totales[0]
                self.ranking[agente_2] += partida.resultados_partida.totales[1]

                agente_1.resetear_resultado()
                agente_2.resetear_resultado()


    def ordenar_ranking(self):
        """
        Ordena el ranking de los jugadores según sus puntuaciones.
        """
        self.ranking = dict(sorted(self.ranking.items(), key=lambda tup: tup[1], reverse=True))

    def dibujar_ranking(self):
        """
        Dibuja un gráfico de barras con el ranking de los jugadores.
        """
        self.ordenar_ranking()

        lista_nombres = list(map(lambda agente: agente.nombre, self.ranking.keys()))
        lista_valores = list(self.ranking.values())

        plt.bar(lista_nombres, lista_valores)
        plt.show()

class Poblacion:
    """
    Representa una población de agentes que participan en un torneo evolutivo de dilemas del prisionero.

    Atributos:
        jugadores (list[Agente]): Lista de agentes que forman parte de la población.
        dic_poblacion (dict): Diccionario que contiene los agentes y sus puntuaciones dentro de la población.
        historial_contadores (list): Historial de las puntuaciones acumuladas para cada jugador a lo largo de las generaciones.
    """
    def __init__(self, jugadores, poblacion_inicial):
        """
        Inicializa una nueva instancia de población con los jugadores y sus respectivas cantidades iniciales.
        """
        self.jugadores = jugadores
        self.dic_poblacion = {copy.deepcopy(player): 0.0 for player, cantidad in zip(jugadores, poblacion_inicial) for _ in range(cantidad)}
        self.historial_contadores = [[] for _ in jugadores]

    @property
    def lista_poblacion(self):
        """
        Devuelve la lista de agentes que actualmente forman parte de la población.

        Retorna:
            list: Lista de agentes en la población.
        """
        return list(self.dic_poblacion.keys())

    def ordenar_dic_poblacion(self):
        """
        Ordena el diccionario de la población basado en las puntuaciones de los agentes de forma descendente.
        """
        self.dic_poblacion = dict(sorted(self.dic_poblacion.items(), key=lambda tup: tup[1], reverse=True))

    def eliminar_n_peores(self, n):
        """
        Elimina a los 'n' agentes con las puntuaciones más bajas de la población.
        
        Parámetros:
            n (int): Número de agentes a eliminar.
        """
        for i in range(n):
            self.dic_poblacion.popitem()

    def reproducir_n_mejores(self, n):
        """
        Duplica los 'n' agentes con las puntuaciones más altas de la población.
        
        Parámetros:
            n (int): Número de agentes a duplicar.
        """
        items_poblacion = list(self.dic_poblacion.items())
        for i in range(n):
            items_poblacion.append(copy.deepcopy(items_poblacion[i]))

        self.dic_poblacion = dict(items_poblacion)

    def gestionar_evolucion(self, repr_int):
        """
        Gestiona la evolución de la población eliminando a los peores agentes y reproduciendo a los mejores.
        
        Parámetros:
            repr_int (int): Número de agentes a eliminar y reproducir.
        """
        #Mejorar la gestion de los casos de empate
        self.ordenar_dic_poblacion()
        self.eliminar_n_peores(repr_int)
        self.reproducir_n_mejores(repr_int)


    def actualizar_historial_contadores(self):
        """
        Actualiza el historial de las puntuaciones de los jugadores en cada generación.
        """
        for i, puntuacion in enumerate(self.contador.values()):
            self.historial_contadores[i].append(puntuacion)

    @property
    def contador(self):
        """
        Es un contador que muestra cuántas veces aparece cada tipo de jugador en la población.

        Devuelve:
            dict: Diccionario con los nombres de los jugadores como claves y sus frecuencias en la población como valores.
        """
        contador = {jugador.nombre:0 for jugador in self.jugadores}

        for jugador in self.lista_poblacion:
                contador[jugador.nombre] += 1

        return contador

class Torneo_evolutivo:
    """
    Representa un torneo evolutivo en el que diferentes agentes compiten entre sí en múltiples generaciones.

    Atributos:
        jugadores (tuple[Agente]): Tupla de agentes que participan en el torneo evolutivo.
        n_rondas (int): Número de rondas por partida.
        error (float): Probabilidad de error en las decisiones de los agentes, es decir, cambiar cooperar por desertar y viceversa.
        probabilidad_de_finalizar (float): Probabilidad de que una partida termine antes de completar todas las rondas.
        repeticiones (int): Número de veces que se repite cada enfrentamiento.
        generaciones (int): Número total de generaciones en el torneo.
        reproductividad (float): Proporción de agentes que se reproducen en cada generación.
        poblacion_inicial (tuple[int] | int): Tamaño o distribución inicial de la población.
        dilema (Dilema): Instancia del dilema que se usa en cada partida del torneo.
        poblacion (Poblacion): Instancia de la población que evoluciona durante el torneo.
        repr_int (int): Número de agentes que se eliminarán y se reproducirán en cada generación.
    """
    def __init__(self, jugadores: tuple[Agente, ...],
                       n_rondas: int = 100,
                       error: float = 0.0,
                       probabilidad_de_finalizar: float = 0.0,
                       repeticiones: int = 2,
                       generaciones: int = 100,
                       reprodctividad: float = 0.05,
                       polacion_inicial: tuple[int, ...] | int = 100,
                       dilema = Dilema(2, -1, 3, 0)):

        """
        Inicializa un torneo evolutivo con los parámetros especificados.
        """
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
        """
        Simula el torneo evolutivo a lo largo de todas las generaciones.

        Parámetros:
            imprimir (bool): Si es True, imprime el estado de la población en cada generación.
        """
        for generacion in range(self.generaciones):
            torneo_iterado = Torneo(self.poblacion.lista_poblacion, self.n_rondas, self.probabilidad_de_finalizar,self.error, self.repeticiones, self.dilema)
            torneo_iterado.simular_torneo()

            self.poblacion.dic_poblacion = torneo_iterado.ranking

            if imprimir:
                print(f"Generacion {generacion}: Poblacion: {self.poblacion.contador}")

            self.poblacion.actualizar_historial_contadores()

            self.poblacion.gestionar_evolucion(self.repr_int)


    def dibujar_resultados(self):
        """
        Dibuja un gráfico con los resultados.
        """
        plt.stackplot([i+1 for i in range(self.generaciones)], self.poblacion.historial_contadores)
        plt.legend([jugador.nombre for jugador in self.jugaodores])
        plt.xlabel('Generaciones')
        plt.ylabel('Poblaciones')
        plt.show()
