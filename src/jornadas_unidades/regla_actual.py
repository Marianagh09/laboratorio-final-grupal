"""Regla actual del coordinador: Orden de llegada descartando traslapes."""

from datos import Jornada

def regla_actual(solicitudes: list[Jornada]) -> list[Jornada]:
    """Simula la lógica actual: toma las solicitudes tal como llegan.
    
    Args:
        solicitudes: Lista de tuplas (inicio, fin, pacientes) en orden de llegada.
        
    Returns:
        Lista de jornadas aceptadas.
    """
    if not solicitudes:
        return []
        
    seleccionadas = []
    ultimo_fin = -1 # Para asegurar que la primera siempre entre
    
    for solicitud in solicitudes:
        inicio, fin, _ = solicitud
        
        # Si la solicitud no choca con la última aceptada
        if inicio >= ultimo_fin:
            seleccionadas.append(solicitud)
            ultimo_fin = fin
            
    return seleccionadas