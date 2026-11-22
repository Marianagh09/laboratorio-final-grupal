"""Pruebas de la operacion 2: lista diaria de llamadas.

Aqui probamos que los dos algoritmos de ordenamiento (el Merge Sort
que hizo el companero y el Insertion Sort viejo) devuelvan lo mismo
y respeten la regla de negocio: primero el riesgo mas alto, y si
empatan, primero la fecha mas antigua.

Se corre con:  python -m ordenamiento_llamadas.pruebas
"""

from ordenamiento_llamadas.datos import Registro, generar_registros
from ordenamiento_llamadas.estrategia import (
    es_mayor_o_igual,
    ordenar_llamadas_optimo,
)
from ordenamiento_llamadas.regla_actual import ordenar_llamadas_actual


# funcion chiquita para no repetir tanto la tupla del registro
def _reg(doc, riesgo, fecha):
    return ("CC", doc, 1, fecha, riesgo, "Medellin")


def _solo_riesgo_y_doc(lista):
    # esto es solo para que los assert se lean mas facil
    return [(r[4], r[1]) for r in lista]


# ---------- casos limite ----------

def prueba_lista_vacia():
    # una lista vacia deberia devolver vacio y no contar comparaciones
    for algo in (ordenar_llamadas_optimo, ordenar_llamadas_actual):
        res, comps = algo([])
        assert res == [], f"{algo.__name__} fallo con lista vacia"
        assert comps == 0, f"{algo.__name__} conto comparaciones en lista vacia"


def prueba_un_elemento():
    # con un solo elemento no hay nada que ordenar
    r = _reg(1, 50, "2026-11-10 10:00:00")
    for algo in (ordenar_llamadas_optimo, ordenar_llamadas_actual):
        res, comps = algo([r])
        assert res == [r]
        assert comps == 0


def prueba_dos_elementos_ordenados():
    # si ya vienen ordenados el insertion solo compara 1 vez
    a = _reg(1, 90, "2026-11-10 10:00:00")
    b = _reg(2, 40, "2026-11-11 10:00:00")
    res, comps = ordenar_llamadas_actual([a, b])
    assert res == [a, b]
    assert comps == 1


# ---------- la regla de negocio ----------

def prueba_desempate_antiguedad():
    # a igual riesgo, la fecha mas vieja va primero
    reciente = _reg(1, 85, "2026-11-12 08:00:00")
    antiguo = _reg(2, 85, "2026-11-05 14:00:00")
    for algo in (ordenar_llamadas_optimo, ordenar_llamadas_actual):
        res, _ = algo([reciente, antiguo])
        assert _solo_riesgo_y_doc(res) == [(85, 2), (85, 1)], (
            f"{algo.__name__} no respeto el desempate por fecha"
        )


def prueba_riesgo_predomina_sobre_fecha():
    # el riesgo manda aunque la fecha sea mas reciente
    viejo_bajo = _reg(1, 30, "2026-10-01 00:00:00")
    nuevo_alto = _reg(2, 99, "2026-11-15 00:00:00")
    for algo in (ordenar_llamadas_optimo, ordenar_llamadas_actual):
        res, _ = algo([viejo_bajo, nuevo_alto])
        assert _solo_riesgo_y_doc(res) == [(99, 2), (30, 1)]


def prueba_empate_total_no_importa_orden():
    # si empatan en riesgo Y en fecha, no hay que cambiarlos de lugar
    r1 = _reg(1, 70, "2026-11-01 00:00:00")
    r2 = _reg(2, 70, "2026-11-01 00:00:00")
    r3 = _reg(3, 70, "2026-11-01 00:00:00")
    for algo in (ordenar_llamadas_optimo, ordenar_llamadas_actual):
        res, _ = algo([r1, r2, r3])
        assert [r[1] for r in res] == [1, 2, 3]


# ---------- el ejemplo del README ----------

def prueba_ejemplo_manual_readme():
    # estos son los R1..R4 del ejemplo que hicimos a mano
    # el resultado esperado era [R2, R3, R1, R4]
    r1 = _reg(101, 85, "2026-11-10 10:00:00")
    r2 = _reg(102, 95, "2026-11-12 08:00:00")
    r3 = _reg(103, 85, "2026-11-05 14:00:00")
    r4 = _reg(104, 60, "2026-11-15 09:00:00")
    esperado = [102, 103, 101, 104]
    for algo in (ordenar_llamadas_optimo, ordenar_llamadas_actual):
        res, _ = algo([r1, r2, r3, r4])
        assert [r[1] for r in res] == esperado, (
            f"{algo.__name__} no dio el mismo resultado del README"
        )


# ---------- validacion cruzada entre los dos algoritmos ----------

def prueba_coincidencia_con_datos_sinteticos():
    # si los dos algoritmos dan lo mismo con varias semillas,
    # es buena senal de que el Merge Sort esta bien hecho
    for semilla in (1, 7, 42, 2026):
        datos = generar_registros(500, semilla=semilla)
        a, _ = ordenar_llamadas_optimo(datos)
        b, _ = ordenar_llamadas_actual(datos)
        assert a == b, f"no coinciden con semilla {semilla}"


def prueba_invariante_riesgo_no_creciente():
    # despues de ordenar, el riesgo nunca deberia subir
    datos = generar_registros(300, semilla=2026)
    for algo in (ordenar_llamadas_optimo, ordenar_llamadas_actual):
        res, _ = algo(datos)
        riesgos = [r[4] for r in res]
        assert all(
            riesgos[i] >= riesgos[i + 1] for i in range(len(riesgos) - 1)
        ), f"{algo.__name__} dejo riesgos desordenados"


def prueba_misma_cantidad_de_registros():
    # ordenar no deberia perder ni duplicar registros
    datos = generar_registros(200, semilla=7)
    for algo in (ordenar_llamadas_optimo, ordenar_llamadas_actual):
        res, _ = algo(datos)
        assert len(res) == len(datos)
        assert sorted(r[1] for r in res) == sorted(r[1] for r in datos)


# ---------- la funcion de comparacion ----------

def prueba_es_mayor_o_igual():
    # revisamos la regla directo en la funcion de comparacion
    assert es_mayor_o_igual(
        _reg(1, 90, "2026-11-01 00:00:00"),
        _reg(2, 50, "2026-10-01 00:00:00"),
    ) is True
    assert es_mayor_o_igual(
        _reg(1, 50, "2026-11-01 00:00:00"),
        _reg(2, 90, "2026-10-01 00:00:00"),
    ) is False
    # empate: gana la fecha mas vieja
    assert es_mayor_o_igual(
        _reg(1, 70, "2026-10-01 00:00:00"),
        _reg(2, 70, "2026-11-01 00:00:00"),
    ) is True
    assert es_mayor_o_igual(
        _reg(1, 70, "2026-11-01 00:00:00"),
        _reg(2, 70, "2026-10-01 00:00:00"),
    ) is False


def ejecutar_todas():
    pruebas = [
        prueba_lista_vacia,
        prueba_un_elemento,
        prueba_dos_elementos_ordenados,
        prueba_desempate_antiguedad,
        prueba_riesgo_predomina_sobre_fecha,
        prueba_empate_total_es_estable,
        prueba_ejemplo_manual_readme,
        prueba_coincidencia_con_datos_sinteticos,
        prueba_invariante_riesgo_no_creciente,
        prueba_misma_cantidad_de_registros,
        prueba_es_mayor_o_igual,
    ]
    print(f"Corriendo {len(pruebas)} pruebas...\n")
    for p in pruebas:
        p()
        print(f"  [OK] {p.__name__}")
    print(f"\nListo, las {len(pruebas)} pruebas pasaron bien.")


if __name__ == "__main__":
    ejecutar_todas()