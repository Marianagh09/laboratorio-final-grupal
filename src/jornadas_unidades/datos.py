"""Generador de instancias sintéticas para Plataforma Pulso (Caso 2)."""
import random

# (inicio_min, fin_min, pacientes_alto_riesgo)
Jornada = tuple[int, int, int]


def generar_solicitudes(n: int, semilla: int = 2026) -> list[Jornada]:
    """Genera n solicitudes de jornadas médicas con semilla reproducible.

    Los tiempos se expresan en minutos acumulados del mes [0, 43200],
    escalando el horizonte temporal con n para mantener una densidad de
    traslapes representativa de una subregión.

    Args:
        n: Cantidad de solicitudes a generar.
        semilla: Semilla fija para reproducibilidad de experimentos.

    Returns:
        Lista de n tuplas (inicio, fin, pacientes_alto_riesgo).
    """
    azar = random.Random(semilla)
    solicitudes: list[Jornada] = []
    horizonte = max(1440, 120 * n)
    for _ in range(n):
        inicio = azar.randrange(0, horizonte)
        duracion = azar.randint(60, 480)  # jornadas entre 1 h y 8 h
        fin = inicio + duracion
        pacientes = azar.randint(10, 80)
        solicitudes.append((inicio, fin, pacientes))
    return solicitudes
