"""Estrategia Voraz: Terminación más temprana."""

from datos import Jornada

def ordenar_por_fin(solicitudes: list[Jornada]) -> list[Jornada]:
    """Ordena las solicitudes por hora de fin (el segundo elemento)."""
    # Usamos sorted con una función lambda que toma el fin (indice 1)
    return sorted(solicitudes, key=lambda x: x[1])

def estrategia_voraz(solicitudes: list[Jornada]) -> list[Jornada]:
    """Selecciona el máximo número de jornadas sin cruces usando la regla voraz.
    
    Args:
        solicitudes: Lista de tuplas (inicio, fin, pacientes).
        
    Returns:
        Lista de las jornadas seleccionadas.
    """
    if not solicitudes:
        return []
        
    # 1. Ordenar por hora de fin
    solicitudes_ordenadas = ordenar_por_fin(solicitudes)
    
    seleccionadas = []
    
    # 2. Tomar la primera (la que termina más temprano)
    primera = solicitudes_ordenadas[0]
    seleccionadas.append(primera)
    ultimo_fin = primera[1]
    
    # 3. Recorrer el resto
    for i in range(1, len(solicitudes_ordenadas)):
        actual = solicitudes_ordenadas[i]
        inicio_actual = actual[0]
        
        # Si la jornada actual empieza cuando o después de que terminó la última
        if inicio_actual >= ultimo_fin:
            seleccionadas.append(actual)
            ultimo_fin = actual[1]
            
    return seleccionadas