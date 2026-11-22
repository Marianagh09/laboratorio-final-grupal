"""Mediciones de la operacion 2: lista diaria de llamadas.

Aqui medimos cuanto se demora el Merge Sort del companero contra el
Insertion Sort viejo, para varios tamanos de N, y sacamos las graficas
que pide el informe. La idea del metodo de medicion la sacamos de la
leccion "Programacion dinamica: decidir, verificar y medir" (usar
time.perf_counter, semilla fija y tamanos crecientes).

Se corre con:  python -m ordenamiento_llamadas.medicion
"""

import os
import time
import matplotlib
matplotlib.use("Agg")  # para que no abra ventana y solo guarde el png
import matplotlib.pyplot as plt

from ordenamiento_llamadas.datos import generar_registros
from ordenamiento_llamadas.estrategia import ordenar_llamadas_optimo
from ordenamiento_llamadas.regla_actual import ordenar_llamadas_actual


# tamanos que vamos a medir (ojala no meter mas de 6400 porque
# el insertion ya se demora bastante)
TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400]
SEMILLA = 42
RUTA_GRAFICAS = os.path.join("graficas", "ordenamiento_llamadas")


def _medir(algoritmo, datos):
    # medimos una sola vez con perf_counter
    # (revisar si vale la pena repetir 3 veces y quedarse con el mejor;
    #  por ahora con 1 corrida alcanza para ver la tendencia)
    t0 = time.perf_counter()
    _, comps = algoritmo(datos)
    dt = time.perf_counter() - t0
    return dt, comps


def ejecutar_benchmark():
    filas = []
    print(f"{'N':>7} | {'Merge(s)':>10} {'Merge(cmp)':>12} | "
          f"{'Insert(s)':>11} {'Insert(cmp)':>13}")
    print("-" * 70)
    for n in TAMANOS:
        datos = generar_registros(n, semilla=SEMILLA)

        tM, cM = _medir(ordenar_llamadas_optimo, datos)
        tI, cI = _medir(ordenar_llamadas_actual, datos)

        filas.append({"n": n, "tM": tM, "cM": cM, "tI": tI, "cI": cI})
        print(f"{n:>7} | {tM:>10.5f} {cM:>12,} | "
              f"{tI:>11.5f} {cI:>13,}")
    return filas


def _grafica(filas, campo_y, etiquetas, colores, titulo, ylabel, archivo):
    os.makedirs(RUTA_GRAFICAS, exist_ok=True)

    N = [f["n"] for f in filas]

    plt.figure(figsize=(9, 5.5))
    for campo, et, col in zip(campo_y, etiquetas, colores):
        plt.plot(N, [f[campo] for f in filas], "o-", label=et, color=col)

    plt.xlabel("N (numero de registros)")
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.legend()
    plt.grid(True, alpha=0.3)

    ruta = os.path.join(RUTA_GRAFICAS, archivo)
    plt.savefig(ruta, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  -> {ruta}")


def generar_graficas(filas):
    _grafica(
        filas,
        campo_y=["tM", "tI"],
        etiquetas=["Merge Sort", "Insertion Sort"],
        colores=["#2E86C1", "#C0392B"],
        titulo="Tiempo de ejecucion vs N (Operacion 2)",
        ylabel="Tiempo (s)",
        archivo="tiempo_vs_n.png",
    )
    _grafica(
        filas,
        campo_y=["cM", "cI"],
        etiquetas=["Merge Sort", "Insertion Sort"],
        colores=["#2E86C1", "#C0392B"],
        titulo="Numero de comparaciones vs N (Operacion 2)",
        ylabel="Comparaciones",
        archivo="operaciones_vs_n.png",
    )


def estimar_consumo(filas, potencia_w=200.0, n_real=1_450_000, dias_anio=365):
    """Estima cuanto se demoraria con N = 1.450.000 y cuanto consumiria.

    Supuestos que asumimos (van en el README):
        - Un equipo de escritorio del call center gasta mas o menos 200 W.
        - Se corre una vez al dia, todos los dias del ano.
        - Extrapolamos con el modelo de complejidad de cada algoritmo:
            Merge:     t crece como N * log N
            Insertion: t crece como N^2
    """
    ref = filas[-1]
    n_ref = ref["n"]
    tM_ref = ref["tM"]
    tI_ref = ref["tI"]

    # para no meter math.log2 a la brava, usamos el truco de bit_length
    tM_real = tM_ref * (n_real * n_real.bit_length()) / (
        n_ref * n_ref.bit_length()
    )
    tI_real = tI_ref * (n_real / n_ref) ** 2

    kw = potencia_w / 1000.0
    kWh_M = tM_real / 3600 * dias_anio * kw
    kWh_I = tI_real / 3600 * dias_anio * kw

    print(f"\nSi lo corrieramos con N = {n_real:,} registros "
          f"(suponiendo {potencia_w:.0f} W):")
    print(f"  Merge    : {tM_real:,.1f} s ({tM_real/60:.2f} min) "
          f"-> {kWh_M:.2f} kWh/anio")
    print(f"  Insertion: {tI_real:,.0f} s ({tI_real/3600:.1f} h) "
          f"-> {kWh_I:,.0f} kWh/anio")
    print(f"  Ahorro aprox: {kWh_I - kWh_M:,.0f} kWh/anio")

    return {
        "tM_real": tM_real,
        "tI_real": tI_real,
        "kWh_M": kWh_M,
        "kWh_I": kWh_I,
    }


def main():
    filas = ejecutar_benchmark()
    print("\nGenerando graficas...")
    generar_graficas(filas)
    estimar_consumo(filas)


if __name__ == "__main__":
    main()