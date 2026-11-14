"""Búsqueda exhaustiva para validar la estrategia voraz."""

from itertools import product
from datos import Jornada

def exhaustivo(solicitudes: list[Jornada]) -> list[Jornada]:
    """Prueba todas las combinaciones posibles para hallar el máximo de jornadas.
    
    Args:
        solicitudes: Lista de tuplas (inicio, fin, pacientes).
        
    Returns:
        Lista de las jornadas óptimas.
    """
    n = len(solicitudes)
    if n == 0:
        return []
        
    mejor_combinacion = []
    
    # Genera todas las combinaciones binarias (0 y 1) para n elementos
    # product([0, 1], repeat=n) devuelve tuplas como (0,0,1,0...)
    for interruptores in product([0, 1], repeat=n):
        combinacion_actual = []
        es_valida = True
        
        for i in range(n):
            if interruptores[i] == 1: # Si el interruptor está encendido, entra
                # Verificamos si choca con la última que metimos
                if combinacion_actual:
                    ultimo_fin = combinacion_actual[-1][1]
                    if solicitudes[i][0] < ultimo_fin:
                        es_valida = False
                        break # Choca, descartamos esta combinación
                combinacion_actual.append(solicitudes[i])
                
        if es_valida and len(combinacion_actual) > len(mejor_combinacion):
            mejor_combinacion = combinacion_actual
            
    return mejor_combinacion