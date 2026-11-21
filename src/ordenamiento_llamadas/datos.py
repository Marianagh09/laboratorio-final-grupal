"""Generador de datos para la operacion 2: Lista diarias de llamadas"""

from datetime import datetime, timedelta
import random   

# Tipo de dato para un registro de prueba de paciente: 
# (tipo\_documento, numero\_documento, id\_laboratorio, fecha\_resultado, indice\_riesgo, municipio) 

Registro = tuple[str, int, int, str, int, str]

def generar_registros(
        n: int,
        semilla: int = 42,
) -> list[Registro]:
    """Genera una lista sintetica de n registros de pacientes pendientes.
    
    args: 
        n: cantidad de registros de pruebas a generar
        semilla: semilla para el generador aleatorio (garantiza reproducibilidad)
    
    returns:
        Lista de tuplas de registros de pacientes con la estrcutura oficial.
    """

    random.seed(semilla)
    registros: list[Registro] = []

    tipos_doc = ["CC", "TI", "CE", "PA"]
    municipios = [
        "Medellin",
        "Bello",
        "Itagui",
        "Envigado",
        "Apartado",
        "Rionegro",
        "Caucasia",
        "Puerto Berrio",
        "Santa Fe de Antioquia"
    ]

    fecha_base = datetime(2026, 10, 1, 0, 0, 0)

    for _ in range(n):
        t_doc = random.choice(tipos_doc)
        n_doc = random.randint(1000000, 99999999)
        id_lab = random.randint(1, 100)

        #Generar una fecha dentro de los ultimos 30 dias para evaluar la antiguedad
        minutos_aleatorios = random.randint(0, 30 * 24 * 60)
        fecha_dt = fecha_base + timedelta(minutes=minutos_aleatorios)
        fecha_str = fecha_dt.strftime("%Y-%m-%d %H:%M:%S")

        riesgo = random.randint(0, 100)
        municipio = random.choice(municipios)

        registros.append((t_doc, n_doc, id_lab, fecha_str, riesgo, municipio))

    return registros

if __name__ == "__main__":
    muestra = generar_registros(3, semilla=42)
    print("Muestra de registros generados:")
    for registro in muestra:
        print(f" Doc: {registro[0]} - Num: {registro[1]} - Lab: {registro[2]} - Fecha: {registro[3]} - Riesgo: {registro[4]} - Municipio: {registro[5]}")