"""Generador de datos de solicitudes de jornadas de valoracion"""

import random

Jornada = tuple[int, int, int]

def generar_solicitudes(
        n: int, 
        semilla: int = 42,
        duracion_min: int = 120,
        duracion_max: int = 240,
        minutos_mes: int = 43200
) -> list[Jornada]:
    """Genera una lista de n solicitudes de jornadas de valoracion.
    
    Args:
        n: Cantidad de solicitudes de jornadas a generar para la subregio.
        semilla: Semilla para el generados que garantiza la reproducibilidad de los resultados.
        duracion_min: Duracion minima de la jornada en minutos.
        duracion_max: Duracion maxima de la jornada en minutos.
        minutos_mes: Cantidad de minutos en un mes.

    Returns:
        lista de tuplas (inicio, fin, paciente_alto_riesgo) en el orden en que llegaron las solicitudes.
        """

    random.seed(semilla)
    solicitudes: list[Jornada] = []

    for _ in range(n):
        inicio = random.randint(0, minutos_mes - duracion_max)
        duracion = random.randint(duracion_min, min(duracion_max, minutos_mes - inicio))
        fin = inicio + duracion
        pacientes = random.randint(10, 100)

        solicitudes.append((inicio, fin, pacientes))

    return solicitudes

if __name__ == "__main__":
    datos_prueba = generar_solicitudes(5, semilla=42)
    print("muestra de 5 solicitudes generadas (inicio min, fin min, pacientes):")
    for idx, sol in enumerate(datos_prueba, 1):
        print(f"Solicitud {idx}: Inicio: {sol[0]} min, Fin: {sol[1]} min, Pacientes: {sol[2]}")