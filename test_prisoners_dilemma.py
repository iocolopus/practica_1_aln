# test_prisoners_dilemma.py

from prisoners_dilemma import (
    Dilema,
    Resultados_partida,
    Cooperator,
    Defector,
    Tft,
    Agente_random,
    Detective,
    Grudger,
    Partida,
    Torneo,
    Poblacion,
    Torneo_evolutivo
)

def test_Dilema():
    print("Testing Dilema class...")
    dilema = Dilema(cc=2, cd=-1, dc=3, dd=0)
    expected_payoff_matrix = [
        [(2, 2), (-1, 3)],
        [(3, -1), (0, 0)]
    ]
    assert dilema.payoff_matrix == expected_payoff_matrix, "Payoff matrix is incorrect"

    assert dilema.evaluate_result(0, 0) == (2, 2), "Incorrect payoff for (0, 0)"
    assert dilema.evaluate_result(0, 1) == (-1, 3), "Incorrect payoff for (0, 1)"
    assert dilema.evaluate_result(1, 0) == (3, -1), "Incorrect payoff for (1, 0)"
    assert dilema.evaluate_result(1, 1) == (0, 0), "Incorrect payoff for (1, 1)"
    print("Dilema class passed all tests.\n")

def test_Resultados_partida():
    print("Testing Resultados_partida class...")
    resultados = Resultados_partida()
    resultados.append((2, 2), 0, 0)
    resultados.append((-1, 3), 0, 1)

    assert resultados.totales == (1, 5), "Totals are incorrect"
    assert resultados.lista_jugadas_a1 == [0, 0], "lista_jugadas_a1 is incorrect"
    assert resultados.lista_jugadas_a2 == [0, 1], "lista_jugadas_a2 is incorrect"
    assert len(resultados) == 2, "Length of resultados is incorrect"
    print("Resultados_partida class passed all tests.\n")

def test_Agentes():
    print("Testing Agente subclasses...")
    dilema = Dilema(2, -1, 3, 0)

    # Test Cooperator
    cooperator = Cooperator(dilema)
    decision = cooperator.generar_decision()
    assert decision == 0, "Cooperator should always cooperate"

    # Test Defector
    defector = Defector(dilema)
    decision = defector.generar_decision()
    assert decision == 1, "Defector should always defect"

    # Test Tit-for-Tat
    tft = Tft(dilema)
    decision = tft.generar_decision()
    assert decision == 0, "Tft should cooperate on first move"
    tft.resultados_partida.append((3, -1), 1, 0)  # Opponent cooperated last
    decision = tft.generar_decision()
    assert decision == 0, "Tft should cooperate after opponent cooperated"
    tft.resultados_partida.append((0, 0), 1, 1)  # Opponent defected last
    decision = tft.generar_decision()
    assert decision == 1, "Tft should defect after opponent defected"

    # Test Random Agent
    agente_random = Agente_random(dilema)
    decision = agente_random.generar_decision()
    assert decision in [0, 1], "Agente_random should return 0 or 1"

    # Test Detective
    detective = Detective(dilema)
    decisions = [detective.generar_decision() for _ in range(4)]
    expected_decisions = [0, 1, 0, 0]
    assert decisions == expected_decisions, "Detective initial moves are incorrect"
    detective.resultados_partida.lista_jugadas_a2.extend([0, 0, 0, 0])
    decision = detective.generar_decision()
    assert decision == 1, "Detective should switch to Defector after opponent always cooperates"

    # Test Grudger
    grudger = Grudger(dilema)
    decision = grudger.generar_decision()
    assert decision == 0, "Grudger should cooperate initially"
    grudger.resultados_partida.lista_jugadas_a2.append(1)  # Opponent defected
    decision = grudger.generar_decision()
    assert decision == 1, "Grudger should defect after being betrayed"

    print("Agente subclasses passed all tests.\n")

def test_Partida():
    print("Testing Partida class...")
    dilema = Dilema(2, -1, 3, 0)
    agente_1 = Cooperator(dilema)
    agente_2 = Defector(dilema)
    partida = Partida(dilema, agente_1, agente_2, n_rondas=5)
    partida.simular_partida()

    total_a1, total_a2 = partida.resultados_partida.totales
    expected_total_a1 = 5 * (-1)
    expected_total_a2 = 5 * 3
    assert total_a1 == expected_total_a1, "Total for agente_1 is incorrect"
    assert total_a2 == expected_total_a2, "Total for agente_2 is incorrect"
    print("Partida class passed all tests.\n")

def test_Torneo():
    print("Testing Torneo class...")
    dilema = Dilema(2, -1, 3, 0)
    jugadores = [Cooperator(dilema), Defector(dilema)]
    torneo = Torneo(jugadores, n_rondas=5, repeticiones=1)
    torneo.simular_torneo()
    torneo.ordenar_ranking()

    rankings = torneo.ranking
    defector = next((player for player in rankings if player.nombre == 'Defector'), None)
    cooperator = next((player for player in rankings if player.nombre == 'Cooperator'), None)
    assert rankings[defector] > rankings[cooperator], "Defector should have a higher score than Cooperator"
    print("Torneo class passed all tests.\n")

def test_Poblacion():
    print("Testing Poblacion class...")
    dilema = Dilema(2, -1, 3, 0)
    jugadores = [Cooperator(dilema), Defector(dilema)]
    poblacion_inicial = [10, 10]
    poblacion = Poblacion(jugadores, poblacion_inicial)

    contador = poblacion.contador
    assert contador['Cooperator'] == 10, "Initial count for Cooperator is incorrect"
    assert contador['Defector'] == 10, "Initial count for Defector is incorrect"

    # Test eliminar_n_peores and reproducir_n_mejores
    for jugador in poblacion.dic_poblacion:
        poblacion.dic_poblacion[jugador] = 1  # Set scores
    poblacion.gestionar_evolucion(5)
    contador = poblacion.contador
    assert sum(contador.values()) == 20, "Total population should remain the same"
    print("Poblacion class passed all tests.\n")

def test_Torneo_evolutivo():
    print("Testing Torneo_evolutivo class...")
    dilema = Dilema(2, -1, 3, 0)
    jugadores = (
        Cooperator(dilema),
        Defector(dilema),
        Tft(dilema),
        Grudger(dilema),
        Agente_random(dilema),
        Detective(dilema)
    )
    torneo_evolutivo = Torneo_evolutivo(
        jugadores=jugadores,
        n_rondas=5,
        generaciones=10,
        reprodctividad=0.1,
        polacion_inicial=60
    )
    torneo_evolutivo.simular()
    final_counts = torneo_evolutivo.poblacion.contador
    total_population = sum(final_counts.values())
    assert total_population == 60, "Total population should remain constant"
    print("Torneo_evolutivo class passed all tests.\n")

def main():
    test_Dilema()
    test_Resultados_partida()
    test_Agentes()
    test_Partida()
    test_Torneo()
    test_Poblacion()
    test_Torneo_evolutivo()
    print("All tests passed successfully.")

if __name__ == "__main__":
    main()
