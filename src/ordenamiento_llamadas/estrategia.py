"""Estrategia optmizada (Merge Sort) para la operacion 2: Lista diarias de llamadas"""

from ordenamiento_llamadas.datos import Registro

def es_mayor_o_igual(r1: Registro, r2: Registro) -> bool:
    """Aplica la regla de negocio para la prioridad entre dos pacientes.
    
    Criterio 1: Mayor indice de riesgo va primero.
    Criterio 2(Desempate): A igual indice de riesgo, la fecha mas antigua va primero.
    
    Args:
        r1: Primer registro de paciente.
        r2: segunudo registro de paciente.
        
    Returns:    
        True si r1 tiene mayor prioridad que r2, False en caso contrario.
    """

    # r1[4] y r2[4] son los índices de riesgo
    if r1[4] != r2[4]:
        return r1[4] > r2[4]
    # r1[3] y r2[3] son las fechas en formato "YYYY-MM-DD HH:MM:SS" (string comparable)
    return r1[3] <= r2[3]

def ordenar_llamadas_optimo(
        registros: list[Registro]
) -> tuple[list[Registro], int]:
    """Ordena los registros usando Merge Sort e instrumenta comparaciones.
    
    Args:
        registros: Lista de registros de pacientes a ordenar.
        
    Returns:
        Una tupla con (lista_ordenada, total_comparaciones)
    """

    copia = list(registros)  

    def _merge_sort(arr: list[Registro]) -> tuple[list[Registro], int]:
        if len(arr) <= 1:
            return arr, 0

        medio = len(arr) // 2
        izquierda, comp_izq = _merge_sort(arr[:medio])
        derecha, comp_der = _merge_sort(arr[medio:])

        resultado: list[Registro] = []
        i = j = 0
        comp_mezcla = 0
        while i < len(izquierda) and j < len(derecha):
            comp_mezcla += 1
            if es_mayor_o_igual(izquierda[i], derecha[j]):
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])

        return resultado, comp_izq + comp_der + comp_mezcla
    return _merge_sort(copia)

if __name__ == "__main__":
    from src.ordenamiento_llamadas.datos import generar_registros

    datos_prueba = generar_registros(5, semilla=42)
    ordenados, comps= ordenar_llamadas_optimo(datos_prueba)
    print(f"Merge Sort completado. Comparaciones: {comps}")
    for r in ordenados:
        print(f" Riesgo: {r[4]} | Fecha: {r[3]} | Doc: {r[1]}")