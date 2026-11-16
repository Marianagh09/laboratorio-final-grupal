"""Medición experimental y generación de gráficas para jornadas_unidades."""
import sys
import time
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt

RUTA_MODULO = str(Path(__file__).resolve().parent)
if RUTA_MODULO not in sys.path:
    sys.path.insert(0, RUTA_MODULO)

from datos import Jornada, generar_solicitudes
from estrategia import estrategia_voraz
from exhaustivo import exhaustivo
from regla_actual import regla_actual


class Contador:
    """Acumula operaciones elementales (comparaciones/evaluaciones)."""

    def __init__(self) -> None:
        """Inicializa el contador en cero."""
        self.total = 0


def _merge_sort_contando(
    solicitudes: list[Jornada], contador: Contador
) -> list[Jornada]:
    """Ordena jornadas por hora de fin con merge sort contando comparaciones.

    Args:
        solicitudes: Lista de jornadas a ordenar.
        contador: Contador de comparaciones elementales.

    Returns:
        Lista ordenada por hora de fin.
    """
    if len(solicitudes) <= 1:
        return solicitudes
    mitad = len(solicitudes) // 2
    izq = _merge_sort_contando(solicitudes[:mitad], contador)
    der = _merge_sort_contando(solicitudes[mitad:], contador)
    mezcla: list[Jornada] = []
    i = j = 0
    while i < len(izq) and j < len(der):
        contador.total += 1
        if izq[i][1] <= der[j][1]:
            mezcla.append(izq[i])
            i += 1
        else:
            mezcla.append(der[j])
            j += 1
    mezcla.extend(izq[i:])
    mezcla.extend(der[j:])
    return mezcla


def contar_operaciones_voraz(solicitudes: list[Jornada]) -> int:
    """Cuenta las comparaciones realizadas por la estrategia voraz.

    Args:
        solicitudes: Lista de jornadas candidatas.

    Returns:
        Total de comparaciones elementales en ordenamiento y selección.
    """
    if not solicitudes:
        return 0
    contador = Contador()
    ordenadas = _merge_sort_contando(solicitudes, contador)
    ultimo_fin = ordenadas[0][1]
    for i in range(1, len(ordenadas)):
        contador.total += 1
        if ordenadas[i][0] >= ultimo_fin:
            ultimo_fin = ordenadas[i][1]
    return contador.total


def contar_operaciones_exhaustivo(solicitudes: list[Jornada]) -> int:
    """Cuenta las evaluaciones de subconjuntos y cruces del enfoque exhaustivo.

    Args:
        solicitudes: Lista de jornadas candidatas.

    Returns:
        Total de operaciones elementales exploradas.
    """
    n = len(solicitudes)
    operaciones = 0
    for mascara in product([0, 1], repeat=n):
        operaciones += 1
        elegidas = [solicitudes[i] for i in range(n) if mascara[i] == 1]
        for a in range(len(elegidas)):
            for b in range(a + 1, len(elegidas)):
                operaciones += 1
                if elegidas[a][0] < elegidas[b][1] and elegidas[b][0] < elegidas[a][1]:
                    break
    return operaciones


def contar_operaciones_actual(solicitudes: list[Jornada]) -> int:
    """Cuenta las comparaciones realizadas por la regla actual del coordinador.

    Args:
        solicitudes: Lista de jornadas candidatas.

    Returns:
        Total de comparaciones realizadas.
    """
    if not solicitudes:
        return 0
    operaciones = 0
    ultimo_fin = -1
    for inicio, fin, _ in solicitudes:
        operaciones += 1
        if inicio >= ultimo_fin:
            ultimo_fin = fin
    return operaciones


def medir_tiempo_medio(
    funcion, solicitudes: list[Jornada], repeticiones: int = 5
) -> float:
    """Mide el tiempo promedio de ejecución en milisegundos.

    Args:
        funcion: Algoritmo a cronometrar.
        solicitudes: Datos de entrada pregenerados.
        repeticiones: Número de ejecuciones para promediar ruido.

    Returns:
        Tiempo medio de ejecución en milisegundos.
    """
    acumulado = 0.0
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(solicitudes)
        acumulado += time.perf_counter() - inicio
    return (acumulado / repeticiones) * 1000.0


def ejecutar_experimentos() -> None:
    """Corre las mediciones, imprime tablas y genera las gráficas PNG."""
    Path("graficas/jornadas_unidades").mkdir(parents=True, exist_ok=True)

    # Parte A: Tamaños donde el enfoque exhaustivo logra ejecutarse (incluye duplos: 6->12, 8->16)
    tamanos_pequenos = [4, 6, 8, 10, 12, 14, 16]
    tiempos_voraz_p: list[float] = []
    tiempos_exh_p: list[float] = []
    tiempos_act_p: list[float] = []
    ops_voraz_p: list[int] = []
    ops_exh_p: list[int] = []
    ops_act_p: list[int] = []

    print("=== EXPERIMENTO 1: COMPARACION CON ENFOQUE EXHAUSTIVO ===")
    print(f"{'N':>4} | {'Voraz (ms)':>11} | {'Exh (ms)':>11} | {'Actual (ms)':>11} | {'Ops Voraz':>10} | {'Ops Exh':>10}")
    for n in tamanos_pequenos:
        datos = generar_solicitudes(n, semilla=2026 + n)
        # Verificación cruzada en el experimento
        assert len(estrategia_voraz(datos)) == len(exhaustivo(datos))

        tv = medir_tiempo_medio(estrategia_voraz, datos, repeticiones=10)
        te = medir_tiempo_medio(exhaustivo, datos, repeticiones=3)
        ta = medir_tiempo_medio(regla_actual, datos, repeticiones=10)

        ov = contar_operaciones_voraz(datos)
        oe = contar_operaciones_exhaustivo(datos)
        oa = contar_operaciones_actual(datos)

        tiempos_voraz_p.append(tv)
        tiempos_exh_p.append(te)
        tiempos_act_p.append(ta)
        ops_voraz_p.append(ov)
        ops_exh_p.append(oe)
        ops_act_p.append(oa)

        print(f"{n:>4} | {tv:>11.4f} | {te:>11.4f} | {ta:>11.4f} | {ov:>10,} | {oe:>10,}")

    # Parte B: Escalabilidad de la estrategia voraz hasta tamaños grandes (duplicando N)
    tamanos_grandes = [100, 1000, 2000, 4000, 8000, 16000, 32000, 64000]
    tiempos_voraz_g: list[float] = []
    ops_voraz_g: list[int] = []

    print("\n=== EXPERIMENTO 2: ESCALABILIDAD ESTRATEGIA VORAZ (DUPLICANDO N) ===")
    print(f"{'N':>7} | {'Voraz (ms)':>11} | {'Ops Voraz':>11}")
    for n in tamanos_grandes:
        datos = generar_solicitudes(n, semilla=5000 + n)
        tv = medir_tiempo_medio(estrategia_voraz, datos, repeticiones=10)
        ov = contar_operaciones_voraz(datos)
        tiempos_voraz_g.append(tv)
        ops_voraz_g.append(ov)
        print(f"{n:>7,} | {tv:>11.4f} | {ov:>11,}")

    # Gráfica 1: tiempo_vs_n.png (dos paneles: comparación exhaustiva + escalabilidad voraz)
    fig, ejes = plt.subplots(1, 2, figsize=(12, 4.8))
    ejes[0].plot(tamanos_pequenos, tiempos_exh_p, "o-", color="tab:red", label="Exhaustivo: Θ(n²·2ⁿ)")
    ejes[0].plot(tamanos_pequenos, tiempos_voraz_p, "s-", color="tab:blue", label="Estrategia Voraz: Θ(n log n)")
    ejes[0].plot(tamanos_pequenos, tiempos_act_p, "^--", color="tab:gray", label="Regla Actual: Θ(n)")
    ejes[0].set_yscale("log")
    ejes[0].set_title("Comparación directa (escala logarítmica)")
    ejes[0].set_xlabel("Número de solicitudes (N)")
    ejes[0].set_ylabel("Tiempo medio (ms)")
    ejes[0].grid(True, alpha=0.3)
    ejes[0].legend()

    ejes[1].plot(tamanos_grandes, tiempos_voraz_g, "s-", color="tab:blue", label="Estrategia Voraz: Θ(n log n)")
    ejes[1].set_title("Escalabilidad Estrategia Voraz hasta N = 64.000")
    ejes[1].set_xlabel("Número de solicitudes (N)")
    ejes[1].set_ylabel("Tiempo medio (ms)")
    ejes[1].grid(True, alpha=0.3)
    ejes[1].legend()

    fig.suptitle("Plataforma Pulso: Tiempo de ejecución frente al número de solicitudes")
    fig.tight_layout()
    fig.savefig("graficas/jornadas_unidades/tiempo_vs_n.png", dpi=150)
    plt.close(fig)

    # Gráfica 2: operaciones_vs_n.png
    fig2, ejes2 = plt.subplots(1, 2, figsize=(12, 4.8))
    ejes2[0].plot(tamanos_pequenos, ops_exh_p, "o-", color="tab:red", label="Exhaustivo: Θ(n²·2ⁿ)")
    ejes2[0].plot(tamanos_pequenos, ops_voraz_p, "s-", color="tab:green", label="Estrategia Voraz: Θ(n log n)")
    ejes2[0].plot(tamanos_pequenos, ops_act_p, "^--", color="tab:gray", label="Regla Actual: Θ(n)")
    ejes2[0].set_yscale("log")
    ejes2[0].set_title("Operaciones elementales (escala logarítmica)")
    ejes2[0].set_xlabel("Número de solicitudes (N)")
    ejes2[0].set_ylabel("Operaciones contadas")
    ejes2[0].grid(True, alpha=0.3)
    ejes2[0].legend()

    ejes2[1].plot(tamanos_grandes, ops_voraz_g, "s-", color="tab:green", label="Estrategia Voraz: Θ(n log n)")
    ejes2[1].set_title("Operaciones Estrategia Voraz hasta N = 64.000")
    ejes2[1].set_xlabel("Número de solicitudes (N)")
    ejes2[1].set_ylabel("Comparaciones contadas")
    ejes2[1].grid(True, alpha=0.3)
    ejes2[1].legend()

    fig2.suptitle("Plataforma Pulso: Operaciones elementales frente al número de solicitudes")
    fig2.tight_layout()
    fig2.savefig("graficas/jornadas_unidades/operaciones_vs_n.png", dpi=150)
    plt.close(fig2)

    print("\nGraficas generadas correctamente en graficas/jornadas_unidades/")


if __name__ == "__main__":
    ejecutar_experimentos()
