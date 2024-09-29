from dpi import *
import random

dp = Dilema(2, -1, 3, 0)

def generar_memoria_random(n):
    return [random.choice((0,1)) for _ in range(n)]

class Agente_memoria(Agente):
    def __init__(self, parametro_memoria: list, dilema: Dilema = dp):
        super().__init__(dilema)
        self.parametro_memoria = parametro_memoria

    def diccionario_decisiones(self):

        diccionario = {}

        for i in range(16):
            diccionario[f"{int(bin(i)[2:]):04d}"] = self.parametro_memoria[i]

        return diccionario

    def diccionario_decisiones_formateado(self):

        diccionario = {}

        for i in range(16):
            clave = f"{int(bin(i)[2:]):04d}"
            clave = clave.replace("0","C")
            clave = clave.replace("1","D")

            bin_to_str = {
                0:"C",
                1:"D"
            }

            valor = bin_to_str[self.parametro_memoria[i]]

            diccionario[clave] = valor

        return diccionario

    def __str__(self):
        return "".join(self.parametro_memoria)

    def __repr__(self):
        return str(self)

    def generar_decision(self):
        if len(self.resultados_partida) == 1:
            return 0
        elif rondas := len(self.resultados_partida) <= 3:
            prob_cooperar = (rondas - sum(self.resultados_partida.lista_jugadas_a2)) / rondas

            if random.random() < prob_cooperar:
                return 0
            else:
                return 1
        else:
            indice = int("".join([str(x) for x in self.resultados_partida.lista_jugadas_a2[-4:]]), 2)
            return self.parametro_memoria[indice]


class Poblacion:
    def __init__(self, poblacion_inicial):
        self.dic_poblacion = {Agente_memoria(generar_memoria_random(16), dp): 0.0 for _ in range(poblacion_inicial)}

    @property
    def lista_poblacion(self):
        return list(self.dic_poblacion.keys())

    def ordenar_dic_poblacion(self):
        self.dic_poblacion = dict(sorted(self.dic_poblacion.items(), key=lambda tup: tup[1], reverse=True))

    def eliminar_n_peores(self, n):
        for i in range(n):
            self.dic_poblacion.popitem()

    def reproducir_n_mejores(self, n, p_mutacion=0.2):
        def mutar_agente(agente: Agente_memoria):
            for i in range(len(agente.parametro_memoria)):
                if random.random() < p_mutacion:
                    agente.parametro_memoria[i] = int(not bool(agente.parametro_memoria[i]))

        agentes_poblacion = list(self.dic_poblacion.keys())
        mejores_poblacion = agentes_poblacion[:n]

        hijos = []

        for i in range(n):
            padre_a = random.choice(mejores_poblacion)
            padre_b = random.choice(mejores_poblacion)

            punto_corte = randrange(0, 16)

            parametros_hijo = padre_a.parametro_memoria[0:punto_corte] + padre_b.parametro_memoria[punto_corte:]

            hijos.append(Agente_memoria(parametros_hijo))

        for hijo in hijos:
            mutar_agente(hijo)
            self.dic_poblacion[hijo] = 0.0

    def gestionar_evolucion(self, repr_int):
        # Mejorar la gestion de los casos de empate
        self.eliminar_n_peores(repr_int)
        self.reproducir_n_mejores(repr_int)


class Evolucionar:

    def __init__(self, n_rondas: int = 100,
                 error: float = 0.0,
                 probabilidad_de_finalizar: float = 0.0,
                 generaciones: int = 100,
                 repeticiones: int = 1,
                 reprodctividad: float = 0.05,
                 poblacion_inicial: int = 100,
                 dilema=Dilema(2, -1, 3, 0)):

        self.n_rondas = n_rondas
        self.error = error
        self.probabilidad_de_finalizar = probabilidad_de_finalizar
        self.repeticiones = repeticiones
        self.generaciones = generaciones
        self.reproductividad = reprodctividad
        self.dilema = dilema
        self.poblacion_inicial = poblacion_inicial
        self.poblacion = Poblacion(self.poblacion_inicial)
        self.repr_int = int(self.poblacion_inicial * self.reproductividad)

    # Hay que gestionar los casos de empates
    def simular(self, imprimir=False):
        for generacion in range(self.generaciones):
            torneo_iterado = Torneo(self.poblacion.lista_poblacion, self.n_rondas, self.probabilidad_de_finalizar,
                                    self.error, self.repeticiones, self.dilema)
            torneo_iterado.simular_torneo()

            self.poblacion.dic_poblacion = torneo_iterado.ranking
            self.poblacion.ordenar_dic_poblacion()

            if imprimir:
                print(f"Generacion {generacion}: Poblacion: {self.poblacion.lista_poblacion[0].parametro_memoria}")
                # print(self.poblacion.dic_poblacion.values())

            self.poblacion.gestionar_evolucion(self.repr_int)

    def top_parametros(self, n):

        return [agente.parametro_memoria for agente in self.poblacion.lista_poblacion[:n]]


"""tupla_cero_uno = (0,1)
parametros_random = [random.choice(tuple(tupla_cero_uno)) for x in range(16)]
print(parametros_random)

agente_random = Agente_random(dp)
agente_binario = Agente_memoria(parametros_random, dilema=dp)

partida = Partida(dp, agente_binario, agente_random, n_rondas=30)
partida.simular_partida()
print(partida.resultados_partida)


print(agente_binario.diccionario_decisiones())"""

evolucionar = Evolucionar(generaciones=1000, poblacion_inicial=30, reprodctividad=0.2, n_rondas=15, error=0.01)
evolucionar.simular(imprimir=True)

agente_binario = Agente_memoria([0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1])
print(agente_binario.diccionario_decisiones_formateado())