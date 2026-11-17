"""Pruebas unitarias y de validación para la operación jornadas_unidades."""
import random
import sys
from pathlib import Path

# Asegura resolución de imports tanto desde raíz como desde src/jornadas_unidades
RUTA_MODULO = str(Path(__file__).resolve().parent)
if RUTA_MODULO not in sys.path:
    sys.path.insert(0, RUTA_MODULO)

from datos import Jornada, generar_solicitudes
from estrategia import estrategia_voraz
from exhaustivo import exhaustivo
from regla_actual import regla_actual


def hay_cruce(jornadas: list[Jornada]) -> bool:
    """Verifica si existe algún traslape entre las jornadas seleccionadas.

    Dos jornadas [inicio_a, fin_a) y [inicio_b, fin_b) no se cruzan si
    una empieza cuando o después de que la otra termina.

    Args:
        jornadas: Lista de jornadas a validar.

    Returns:
        True si hay al menos un cruce; False en caso contrario.
    """
    n = len(jornadas)
    for i in range(n):
        for j in range(i + 1, n):
            if jornadas[i][0] < jornadas[j][1] and jornadas[j][0] < jornadas[i][1]:
                return True
    return False


def ejecutar_pruebas() -> None:
    """Ejecuta toda la batería de aserciones exigida para el Laboratorio 4."""
    # 1. Casos límite: lista vacía y una sola solicitud
    assert estrategia_voraz([]) == []
    assert exhaustivo([]) == []
    assert regla_actual([]) == []

    una: list[Jornada] = [(480, 600, 25)]
    assert estrategia_voraz(una) == una
    assert exhaustivo(una) == una
    assert regla_actual(una) == una

    # 2. Caso límite: todas las solicitudes se cruzan entre sí (solo cabe 1)
    todas_cruzadas: list[Jornada] = [(500, 900, 30), (520, 850, 20), (540, 800, 40)]
    res_cruzadas = estrategia_voraz(todas_cruzadas)
    assert len(res_cruzadas) == 1
    assert not hay_cruce(res_cruzadas)

    # 3. Caso límite: ninguna se cruza (se tocan en los extremos, caben todas)
    en_cadena: list[Jornada] = [(480, 600, 15), (600, 720, 20), (720, 840, 25)]
    res_cadena = estrategia_voraz(en_cadena)
    assert len(res_cadena) == 3
    assert not hay_cruce(res_cadena)

    # 4. Contraejemplo documentado en el README.md (S1, S2, S3, S4)
    # S1: 09:00-17:00 (540-1020), S2: 08:00-10:00 (480-600),
    # S3: 10:00-12:00 (600-720), S4: 12:00-14:00 (720-840)
    contraejemplo: list[Jornada] = [
        (540, 1020, 40),
        (480, 600, 25),
        (600, 720, 30),
        (720, 840, 35),
    ]
    res_actual = regla_actual(contraejemplo)
    res_optimo = estrategia_voraz(contraejemplo)
    assert len(res_actual) == 1, f"Se esperaba 1 jornada en regla actual, dio {len(res_actual)}"
    assert len(res_optimo) == 3, f"Se esperaban 3 jornadas óptimas, dio {len(res_optimo)}"
    assert not hay_cruce(res_optimo)

    # 5. Validación en 25 instancias aleatorias pequeñas frente a exhaustivo
    azar = random.Random(2026)
    for caso in range(25):
        n = azar.randint(1, 10)
        instancia = generar_solicitudes(n, semilla=1000 + caso)
        sol_voraz = estrategia_voraz(instancia)
        sol_exh = exhaustivo(instancia)
        assert not hay_cruce(sol_voraz), f"Cruce detectado en instancia {caso}"
        assert len(sol_voraz) == len(sol_exh), (
            f"Discrepancia en caso {caso}: voraz={len(sol_voraz)}, exh={len(sol_exh)}"
        )

    print("OK: Todas las pruebas unitarias, casos limite, contraejemplo y 25 instancias pasaron.")


if __name__ == "__main__":
    ejecutar_pruebas()
