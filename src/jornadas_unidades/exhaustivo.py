"""Búsqueda exhaustiva para la programación de jornadas (Plataforma Pulso)."""
from itertools import product
from datos import Jornada


def exhaustivo(solicitudes: list[Jornada]) -> list[Jornada]:
    """Elige el máximo número de jornadas compatibles probando todos los subconjuntos.

    Ordena previamente por hora de fin para validar cada subconjunto
    comparando únicamente con la última jornada aceptada.

    Args:
        solicitudes: Lista de tuplas (inicio, fin, pacientes).

    Returns:
        Subconjunto compatible de tamaño máximo.
    """
    n = len(solicitudes)
    ordenadas = sorted(solicitudes, key=lambda x: x[1])
    mejor_combinacion: list[Jornada] = []

    for mascara in product([0, 1], repeat=n):
        combinacion_actual: list[Jornada] = []
        es_valida = True
        for i in range(n):
            if mascara[i] == 1:
                if combinacion_actual:
                    ultimo_fin = combinacion_actual[-1][1]
                    if ordenadas[i][0] < ultimo_fin:
                        es_valida = False
                        break
                combinacion_actual.append(ordenadas[i])

        if es_valida and len(combinacion_actual) > len(mejor_combinacion):
            mejor_combinacion = combinacion_actual

    return mejor_combinacion
