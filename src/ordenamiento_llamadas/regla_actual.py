"""Procedimiento actual heredado (Insertion Sort) para la operacion 2"""

from ordenamiento_llamadas.datos import Registro
from ordenamiento_llamadas.estrategia import es_mayor_o_igual

def ordenar_llamadas_actual(
        registros: list[Registro]
) -> tuple[list[Registro], int]:
    """Ordena los registros usando insertion Sort e instrumenta comparaciones
    
    Args: 
        registros: Lista de registros de pacientes a ordenar.
        
    Returns:
        Una tupla con (lista_ordenada, total_comparaciones)
    """

    arr = list(registros)  
    comparaciones = 0

    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1

        while j >= 0:
            comparaciones += 1
            if es_mayor_o_igual(clave, arr[j]):
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = clave
    
    return arr, comparaciones

if __name__ == "__main__":
    from src.ordenamiento_llamadas.datos import generar_registros

    datos_prueba = generar_registros(5, semilla=42)
    ordenados, comps= ordenar_llamadas_actual(datos_prueba)
    print(f"Insertion Sort actual completado. Comparaciones: {comps}")
    for r in ordenados:
        print(f" Riesgo: {r[4]} | Fecha: {r[3]} | Doc: {r[1]}")
