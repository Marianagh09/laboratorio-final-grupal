# Proyecto Final — Análisis de Algoritmos: Plataforma Pulso

**Integrantes:**
* Mariana García
* Maria Fernanda Muñoz
* Diego Alejandro Quintero
* Roberto Echeverri

---

## Instrucciones de Reproducción del Proyecto

Con el repositorio clonado y ubicado en la raíz del proyecto (`laboratorio-final-grupal`), sigue estos pasos en tu terminal:

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```
   *(En CMD de Windows: `env\Scripts\activate.bat`)*

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar pruebas unitarias y mediciones de ambas operaciones:**
   ```bash
   python src/jornadas_unidades/pruebas.py
   python src/jornadas_unidades/medicion.py
   python src/ordenamiento_llamadas/pruebas.py
   python src/ordenamiento_llamadas/medicion.py
   ```

---

## Operación 3 — Jornadas de Unidades Móviles

### 1. Análisis del Problema

* **Entradas:**
  * Un conjunto de $N$ solicitudes de jornadas de valoración recibidas durante el mes en una subregión específica ($N$ varía entre $40$ y $120$ solicitudes por subregión al mes).
  * Cada solicitud $i$ viene representada por una tupla: $(\text{inicio}_i, \text{fin}_i, \text{pacientes}_i)$, donde $\text{inicio}_i$ y $\text{fin}_i$ se expresan en minutos acumulados del mes ($0 \le \text{inicio}_i < \text{fin}_i \le 43.200\text{ min}$) e incluye el tiempo de desplazamiento de la unidad. $\text{pacientes}_i$ indica el número de pacientes de alto riesgo en el municipio.
* **Salida:**
  * Un subconjunto óptimo de solicitudes aceptadas, ordenadas por hora de inicio, que se asignan a la unidad de movilidad sin generar solapamientos de tiempo.
* **Restricciones del negocio:**
  * **Sin traslapes:** La programación de la unidad móvil nunca puede tener $2$ jornadas que se crucen en el tiempo.
  * **Capacidad única:** Cada subregión dispone de exactamente una unidad móvil de valoración.

### 2. Supuestos Técnicos Adoptados

1. **Criterio de solapamiento en fronteras:** Si una jornada finaliza en el minuto $M$ ($\text{fin}_1 = M$) y otra jornada inicia exactamente en el mismo minuto $M$ ($\text{inicio}_2 = M$), no se considera cruce de horario, ya que el tiempo de desplazamiento e inspección previa está incluido en el cálculo del límite $M$.
2. **Criterio de optimización elegido:** El equipo selecciona la **Estrategia voraz de selección de actividades** (ordenando por menor hora de finalización) para maximizar la cantidad total de jornadas atendidas por la unidad móvil en la subregión.

### 3. Análisis Comparativo

#### Descripción del fallo de la regla actual
El procedimiento actual asigna las jornadas por orden de llegada de las solicitudes y rechaza automáticamente cualquier solicitud que se cruce con una previamente aceptada. Esta regla es ineficiente porque si una solicitud que llega temprano abarca un rango de tiempo excesivamente largo, bloquea múltiples jornadas más cortas que podrían haberse atendido en ese mismo intervalo.

#### Instancia del contraejemplo (cálculo a mano)
Considere la siguiente secuencia de $4$ solicitudes que llegan a la plataforma en el orden $S_1, S_2, S_3, S_4$:
* **Solicitud 1 ($S_1$):** Inicio = 09:00 (540 min), Fin = 17:00 (1020 min), Pacientes = 40.
* **Solicitud 2 ($S_2$):** Inicio = 08:00 (480 min), Fin = 10:00 (600 min), Pacientes = 25.
* **Solicitud 3 ($S_3$):** Inicio = 10:00 (600 min), Fin = 12:00 (720 min), Pacientes = 30.
* **Solicitud 4 ($S_4$):** Inicio = 12:00 (720 min), Fin = 14:00 (840 min), Pacientes = 35.

1. **Procesamiento con la regla actual (orden de llegada):**
   * Evalúa $S_1$ (09:00 - 17:00) $\rightarrow$ **Aceptada**.
   * Evalúa $S_2$ (08:00 - 10:00) $\rightarrow$ Se cruza con $S_1$ (09:00 - 17:00) $\rightarrow$ **Rechazada**.
   * Evalúa $S_3$ (10:00 - 12:00) $\rightarrow$ Se cruza con $S_1$ (09:00 - 17:00) $\rightarrow$ **Rechazada**.
   * Evalúa $S_4$ (12:00 - 14:00) $\rightarrow$ Se cruza con $S_1$ (09:00 - 17:00) $\rightarrow$ **Rechazada**.
   * **Resultado de la regla actual:** Atiende **1 sola jornada** ($S_1$).

2. **Procesamiento con la estrategia voraz óptima:**
   * Ordena las solicitudes por hora de finalización: $S_2$ (Fin: 10:00), $S_3$ (Fin: 12:00), $S_4$ (Fin: 14:00), $S_1$ (Fin: 17:00).
   * Selecciona $S_2$ (08:00 - 10:00) $\rightarrow$ **Aceptada**.
   * Selecciona $S_3$ (10:00 - 12:00) $\rightarrow$ No se cruza con $S_2$ $\rightarrow$ **Aceptada**.
   * Selecciona $S_4$ (12:00 - 14:00) $\rightarrow$ No se cruza con $S_3$ $\rightarrow$ **Aceptada**.
   * Evalúa $S_1$ (09:00 - 17:00) $\rightarrow$ Se cruza con las anteriores $\rightarrow$ **Rechazada**.
   * **Resultado de la solución óptima:** Atiende **3 jornadas** ($S_2, S_3, S_4$).

#### Cuantificación del impacto
* **Diferencia absoluta:** La regla actual deja de atender $2$ jornadas completas en la subregión.
* **Pérdida relativa:** El procedimiento del coordinador desperdicia un **66.6%** de la capacidad operativa de la unidad móvil en esta instancia.

#### Condición contraria
Para que la programación dinámica de intervalos ponderados fuera la estrategia adecuada en lugar de la estrategia voraz de selección de actividades, el objetivo del negocio tendría que cambiar de maximizar la cantidad de jornadas a maximizar el número total de pacientes de alto riesgo atendidos, donde cada jornada tiene un peso diferente ($\text{pacientes}_i$) y elegir la jornada de menor duración no garantiza acumular el mayor número de pacientes.

### 4. Evaluación del Desempeño (Operación 3)

#### 4.1 Complejidad teórica
* **Estrategia voraz (terminación más temprana):** $\Theta(n \log n)$ en tiempo (dominado por el ordenamiento por hora de finalización, seguido de una pasada lineal $\Theta(n)$) y $\Theta(n)$ en espacio auxiliar.
* **Enfoque exhaustivo (fuerza bruta):** $\Theta(n \cdot 2^n)$ en tiempo (evalúa los $2^n$ subconjuntos posibles y valida compatibilidad en hasta $n$ pasos) y $\Theta(n)$ en espacio.
* **Regla actual (orden de llegada):** $\Theta(n)$ en tiempo y $\Theta(n)$ en espacio, pero subóptima en calidad de solución.

#### 4.2 Verificación experimental y pruebas unitarias
La corrección funcional se validó mediante `pruebas.py` y `datos.py` (semilla fija `2026`), cubriendo:
* Casos límite: lista vacía, una sola solicitud, solicitudes totalmente traslapadas y jornadas encadenadas en los extremos ($s_i = f_{i-1}$).
* El contraejemplo calculado a mano ($S_1, S_2, S_3, S_4$), confirmando que la regla actual acepta $1$ jornada mientras la estrategia voraz obtiene las $3$ óptimas sin cruces.
* $25$ instancias aleatorias pequeñas donde `estrategia_voraz` iguala exactamente el número máximo de jornadas hallado por exhaustivo sin producir solapamientos.

#### 4.3 Resultados experimentales y contraste empírico
Las mediciones se realizaron en `medicion.py` cronometrando únicamente la ejecución algorítmica con `time.perf_counter()` (promediando $10$ repeticiones para la voraz y $3$ para la exhaustiva) y contando comparaciones elementales.

**Experimento A: Comparación directa frente al enfoque exhaustivo**

| $N$ (solicitudes) | Voraz (ms) | Exhaustivo (ms) | Regla Actual (ms) | Ops Voraz | Ops Exhaustivo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 4 | 0.0021 | 0.0136 | 0.0009 | 8 | 40 |
| 6 | 0.0022 | 0.0360 | 0.0007 | 14 | 232 |
| 8 | 0.0028 | 0.1745 | 0.0007 | 24 | 1,712 |
| 10 | 0.0018 | 0.5749 | 0.0009 | 30 | 8,216 |
| 12 | 0.0024 | 1.8519 | 0.0007 | 38 | 48,192 |
| 14 | 0.0027 | 7.4732 | 0.0011 | 51 | 258,432 |
| 16 | 0.0051 | 25.2141 | 0.0010 | 62 | 1,272,832 |

**Experimento B: Escalabilidad de la estrategia voraz al duplicar $N$**

| $N$ (solicitudes) | Voraz (ms) | Factor tiempo | Ops Voraz | Factor operaciones |
| :--- | :--- | :--- | :--- | :--- |
| 100 | 0.0137 | — | 635 | — |
| 1,000 | 0.1425 | — | 9,714 | — |
| 2,000 | 0.4084 | $2.87\times$ | 21,405 | $2.20\times$ |
| 4,000 | 1.1598 | $2.84\times$ | 46,879 | $2.19\times$ |
| 8,000 | 2.4323 | $2.10\times$ | 101,589 | $2.17\times$ |
| 16,000 | 6.0262 | $2.48\times$ | 219,316 | $2.16\times$ |
| 32,000 | 10.5287 | $1.75\times$ | 470,712 | $2.15\times$ |
| 64,000 | 28.7519 | $2.73\times$ | 1,004,920 | $2.13\times$ |

**Contraste teórico vs. empírico:**
* **Enfoque exhaustivo:** Al pasar de $N = 8$ ($0.1745\text{ ms}$, $1.712\text{ ops}$) a $N = 16$ ($25.2141\text{ ms}$, $1.272.832\text{ ops}$), el tiempo se multiplicó por $144.5\times$ (cercano al factor teórico $2 \cdot 2^8 = 512\times$ de $\Theta(n \cdot 2^n)$), confirmando el crecimiento exponencial.
* **Estrategia voraz:** Al duplicar $N$ (por ejemplo, de $8.000$ a $16.000$ y de $32.000$ a $64.000$), las operaciones elementales crecen por un factor estable de $2.13\times$ a $2.20\times$ ("un poco más del doble"), coincidiendo exactamente con la firma matemática $\frac{2n \log_2(2n)}{n \log_2 n} = 2\left(1 + \frac{1}{\log_2 n}\right)$ de $\Theta(n \log n)$.

#### 4.4 Extrapolación al volumen real y consumo energético (implicaciones ambientales)
* **Volumen real del caso:** $9$ subregiones, con entre $40$ y $120$ solicitudes mensuales cada una (peor caso: $N = 120$ por subregión), ejecutado en un servidor de $380\text{ W}$ ($0.38\text{ kW}$). Como referencia operativa, la programación mensual debe resolverse dentro de una ventana de planeación nocturna de $1\text{ hora}$ ($3.600\text{ s}$).
* **Estimación estrategia voraz:** Partiendo de la medición empírica para $N = 100$ ($0.0137\text{ ms}$) y escalando bajo $\Theta(n \log n)$ hasta $N = 120$, cada subregión toma $\approx 0.017\text{ ms}$. Para las $9$ subregiones en conjunto, el tiempo total mensual es de $0.15\text{ ms}$ ($0.00015\text{ s}$), cumpliendo ampliamente con la ventana operativa.
  * **Consumo energético:** $0.38\text{ kW} \times \frac{0.00015}{3600}\text{ h} \approx 1.58 \times 10^{-8}\text{ kWh/mes}$ ($1.90 \times 10^{-7}\text{ kWh/año}$).
* **Estimación regla actual:** Con complejidad $\Theta(n)$, para $N = 120$ en $9$ subregiones tarda $\approx 0.010\text{ ms}$ totales ($1.06 \times 10^{-8}\text{ kWh/mes}$ o $1.27 \times 10^{-7}\text{ kWh/año}$). La diferencia anual de consumo eléctrico frente a la estrategia voraz es despreciable ($\approx 6.3 \times 10^{-8}\text{ kWh/año}$), pero la estrategia voraz elimina el desperdicio operativo de unidades móviles subutilizadas.
* **Estimación enfoque exhaustivo:** Partiendo de $N = 16$ ($25.21\text{ ms}$) y proyectando bajo $\Theta(n \cdot 2^n)$ hasta $N = 120$, el factor de crecimiento es $\frac{120}{16} \cdot 2^{104} \approx 1.52 \times 10^{32}$. Una sola subregión tardaría $\approx 1.2 \times 10^{23}\text{ años}$, por lo que sencillamente no terminaría y es inviable para operación real.

---

## Operación 2 — Lista Diaria de Llamadas (1.450.000 Registros)

**Enlaces al código de la Operación 2:**
* Generador de datos sintéticos: `src/ordenamiento_llamadas/datos.py`
* Algoritmo optimizado Merge Sort: `src/ordenamiento_llamadas/estrategia.py`
* Procedimiento heredado Insertion Sort: `src/ordenamiento_llamadas/regla_actual.py`
* Pruebas unitarias: `src/ordenamiento_llamadas/pruebas.py`
* Benchmark y mediciones: `src/ordenamiento_llamadas/medicion.py`

### 1. Análisis del Problema (Operación 2)

* **Entradas:**
  * Un volumen masivo diario de $N = 1.450.000$ registros pendientes de gestión almacenados en la plataforma.
  * Cada registro es una tupla: $(\text{tipo\_doc}, \text{num\_doc}, \text{id\_lab}, \text{fecha\_resultado}, \text{indice\_riesgo}, \text{municipio})$, donde $\text{indice\_riesgo} \in [0, 100]$.
* **Salidas:**
  * La lista de exactamente $9.000$ pacientes seleccionados para ser contactados por el call center durante la jornada.
* **Restricciones del negocio:**
  * **Prioridad estricta por riesgo:** Ningún paciente con menor riesgo puede quedar ubicado por encima de uno con mayor riesgo que haya sido excluido.
  * **Criterio de desempate por antigüedad:** A igual índice de riesgo, se debe priorizar el resultado con la fecha más antigua.
  * **Ventana nocturna estricta:** Las Operaciones 1 y 2 deben completarse conjuntamente dentro de una ventana inflexible de $4\text{ horas}$ (01:00 a. m. a 05:00 a. m.).

### 2. Diseño de la Solución y Ejemplo Resuelto a Mano

#### Por qué el problema admite Merge Sort ($\Theta(N \log N)$)
El problema de generar la lista diaria exige un ordenamiento determinista por dos claves (riesgo descendente y fecha ascendente). Merge Sort es ideal porque:
1. Aplica el paradigma de Divide y Vencerás, garantizando una complejidad determinista $\Theta(N \log N)$ en el mejor, promedio y peor caso.
2. Es un algoritmo **estable**, lo que preserva el orden relativo temporal exacto de los registros sin alterar la antigüedad del paciente.

#### Ejemplo resuelto a mano (4 registros)
Considere los siguientes $4$ registros recibidos en la plataforma:
* **$R_1$:** Doc 101, Riesgo: 85, Fecha: `"2026-11-10 10:00"`
* **$R_2$:** Doc 102, Riesgo: 95, Fecha: `"2026-11-12 08:00"`
* **$R_3$:** Doc 103, Riesgo: 85, Fecha: `"2026-11-05 14:00"`
* **$R_4$:** Doc 104, Riesgo: 60, Fecha: `"2026-11-15 09:00"`

* **Paso 1 (División):** Se divide la lista en dos mitades de $2$ elementos: Izquierda: $[R_1, R_2]$, Derecha: $[R_3, R_4]$.
* **Paso 2 (Conquista y mezcla local):**
  * Mitad izquierda ordenada por riesgo: $[R_2\ (95),\ R_1\ (85)]$.
  * Mitad derecha ordenada por riesgo: $[R_3\ (85),\ R_4\ (60)]$.
* **Paso 3 (Mezcla final con desempate):**
  1. Compara $R_2\ (95)$ vs $R_3\ (85)$ $\rightarrow$ Elige $R_2$.
  2. Compara $R_1\ (85)$ vs $R_3\ (85)$ $\rightarrow$ Empate en riesgo. Evalúa fechas (`"2026-11-10"` vs `"2026-11-05"`). $R_3$ es más antiguo $\rightarrow$ Elige $R_3$.
  3. Compara $R_1\ (85)$ vs $R_4\ (60)$ $\rightarrow$ Elige $R_1$.
  4. Anexa el sobrante $R_4$.

* **Resultado final ordenado:** $[R_2, R_3, R_1, R_4]$.

### 3. Evaluación del Desempeño (Operación 2 — Integrante 2)

#### 3.1 Complejidad teórica

| Algoritmo | Mejor caso | Caso promedio | Peor caso | Espacio extra |
| :--- | :--- | :--- | :--- | :--- |
| Merge Sort (`estrategia.py`) | $\Theta(N \log N)$ | $\Theta(N \log N)$ | $\Theta(N \log N)$ | $\Theta(N)$ |
| Insertion Sort (`regla_actual.py`) | $\Theta(N)$ | $\Theta(N^2)$ | $\Theta(N^2)$ | $\Theta(1)$ |

El Merge Sort siempre se comporta igual (no tiene caso malo), mientras que el Insertion Sort se dispara cuando los datos vienen desordenados, que es justo lo que pasa con los $1.450.000$ registros reales.

#### 3.2 Verificación experimental y pruebas unitarias
La corrección funcional se validó mediante `pruebas.py`, cubriendo:
* Casos límite: lista vacía, un solo elemento, dos elementos ya ordenados.
* Regla del negocio: que el riesgo quede de mayor a menor y que a igual riesgo gane la fecha más vieja.
* Empates totales: si empatan en riesgo y fecha, se verifica que se conserven todos los registros (el orden entre idénticos no importa).
* El ejemplo del README ($R_1..R_4$): que ambos algoritmos den lo mismo que hicimos a mano.
* Validación cruzada: que los dos algoritmos coincidan con varias semillas (`1`, `7`, `42` y `2026`).
* Conservación: que no se pierdan ni dupliquen registros.

Salida en consola:
```text
Corriendo 11 pruebas...
  [OK] prueba_lista_vacia
  [OK] prueba_un_elemento
  [OK] prueba_dos_elementos_ordenados
  [OK] prueba_desempate_antiguedad
  [OK] prueba_riesgo_predomina_sobre_fecha
  [OK] prueba_empate_total_no_importa_orden
  [OK] prueba_ejemplo_manual_readme
  [OK] prueba_coincidencia_con_datos_sinteticos
  [OK] prueba_invariante_riesgo_no_creciente
  [OK] prueba_misma_cantidad_de_registros
  [OK] prueba_es_mayor_o_igual
Listo, las 11 pruebas pasaron bien.
```

#### 3.3 Resultados experimentales y contraste empírico
Las mediciones se realizaron en `medicion.py` cronometrando únicamente la ejecución algorítmica con `time.perf_counter()`, con semilla fija (`42`). Los tiempos son aproximados y dependen del equipo donde se corran, pero el número de comparaciones es determinista.

**Experimento A: Medición directa de tiempos y operaciones**

| $N$ | Merge Sort (s) | Merge (cmp) | Insertion Sort (s) | Insertion (cmp) |
| :--- | :--- | :--- | :--- | :--- |
| 100 | 0.00031 | 538 | 0.00044 | 2,769 |
| 200 | 0.00043 | 1,277 | 0.00188 | 11,042 |
| 400 | 0.00087 | 2,940 | 0.00677 | 41,388 |
| 800 | 0.00212 | 6,685 | 0.02625 | 155,822 |
| 1,600 | 0.00429 | 15,016 | 0.10290 | 632,359 |
| 3,200 | 0.00887 | 33,210 | 0.39316 | 2,553,655 |
| 6,400 | 0.02249 | 72,920 | 1.73321 | 10,267,844 |

**Contraste teórico vs. empírico:**
* **Merge Sort:** Al pasar de $N = 3.200$ a $N = 6.400$ el tiempo creció más o menos $2.5\times$ y las comparaciones $2.2\times$. La teoría dice que con $N \log N$ el factor debería ser cercano a $2.1$, así que coincide (la diferencia en tiempo es por el ruido del procesador).
* **Insertion Sort:** Al doble de $N$ el tiempo creció casi $4.4\times$ y las comparaciones casi $4\times$. Eso es exactamente lo que uno espera con $N^2$.
* A medida que $N$ crece la diferencia entre los dos se hace enorme: con $N = 100$ el Merge es solo $1.4$ veces más rápido, pero con $N = 6.400$ ya es como $77$ veces más rápido. Por eso el Insertion no sirve para el volumen real.

#### 3.4 Extrapolación al volumen real y consumo energético (Servidor de 380 W — 365 madrugadas)
Para evaluar la sostenibilidad energética del proceso nocturno se toma un servidor de $380\text{ W}$ ($0.38\text{ kW}$) operando en una proyección anual de $365$ madrugadas para $N = 1.450.000$ registros:
* **Merge Sort ($\Theta(N \log N)$):** Tomando la escala de tiempo de ejecución algorítmica ($\approx 8.2\text{ s}$ por madrugada, equivalente a $0.00228\text{ h}$):
  * Consumo por madrugada: $0.38\text{ kW} \times 0.00228\text{ h} \approx 0.000866\text{ kWh}$.
  * Consumo en $365$ madrugadas: $0.000866\text{ kWh} \times 365 \approx \mathbf{0.32\text{ kWh/año}}$.
* **Insertion Sort ($\Theta(N^2)$):** Con tiempo extrapolado de $\approx 88.967\text{ s}$ ($24.71\text{ h}$) por madrugada:
  * Consumo por madrugada: $0.38\text{ kW} \times 24.71\text{ h} \approx 9.39\text{ kWh}$.
  * Consumo en $365$ madrugadas: $9.39\text{ kWh} \times 365 \approx \mathbf{3.427,35\text{ kWh/año}}$.
* **Ahorro proyectado y viabilidad operativa:** El paso a Merge Sort ahorra aproximadamente $3.427,03\text{ kWh/año}$ ($3.427,35 - 0,32\text{ kWh/año}$, más del $99.99\%$ de reducción en tiempo de cómputo del servidor) y garantiza cumplir holgadamente con la ventana nocturna de $4\text{ horas}$ (01:00 a. m. a 05:00 a. m.).

---

## Parte 3 — Impacto Humano, Marco Normativo y Escenario de Crecimiento (Integrante 3)

### 1. Dimensión Humana y Social
* **Borrar por error a un paciente en la consolidación:** Puede retrasar la intervención oportuna de un caso de alto riesgo clínico, agravando su pronóstico o generando complicaciones evitables. El costo humano recae directamente en el paciente y su familia (riesgo de salud y desgaste emocional), mientras que el costo institucional/operativo recae en la Secretaría de Salud y el equipo gestor por reprocesos, auditorías y pérdida de confianza ciudadana.
* **Enviar a valoración a personas sanas por un laboratorio descalibrado:** Genera falsos positivos o alertas inexactas que saturan agendas médicas, movilizan recursos escasos sin necesidad y provocan ansiedad innecesaria en personas sanas. El costo social y de tiempo recae en los ciudadanos citados y en los pacientes reales que pierden cupos, y el costo económico/logístico recae en la entidad de salud y el laboratorio responsable.

### 2. Marco Normativo y Privacidad
* El tratamiento de datos de salud exige estricta observancia del habeas data médico, la confidencialidad y la protección de datos sensibles (principios de finalidad, acceso restringido, minimización y seguridad de la información).
* **Inmutabilidad y trazabilidad:** Los registros originales de laboratorio y consolidación no deben sobrescribirse ni eliminarse en caliente; las transformaciones, filtros o listas generadas deben quedar auditadas con trazabilidad (origen, marca de tiempo, criterio aplicado e identificador de ejecución) para garantizar integridad y verificación ante eventuales revisiones clínicas o legales.

### 3. Escenario de Crecimiento: Duplicación a $2.900.000$ Registros (Tamizaje de Hipertensión)
Al incorporar el tamizaje de hipertensión arterial y duplicar el volumen diario de $1.450.000$ a $2.900.000$ registros:
* **Merge Sort ($\Theta(N \log N)$):** Escala de forma controlada (apenas un poco más del doble de trabajo más el factor logarítmico adicional), manteniendo tiempos de segundos y asegurando el cumplimiento de la ventana nocturna de $4\text{ horas}$, aunque requiere prever memoria auxiliar suficiente para arreglos temporales.
* **Insertion Sort ($\Theta(N^2)$):** Al duplicar $N$, las operaciones se multiplican por $\approx 4\times$ (pasando de decenas de horas a varios días de cómputo), volviéndolo completamente inviable para la ventana nocturna y provocando un cuello de botella crítico en la operación.

---

## Parte 4 — Análisis Comparativo, Recomendación Técnica y Reproducción (Integrante 4)

### 1. Análisis Comparativo y Recomendación Técnica para la Secretaría de Salud
* **Síntesis comparativa:**
  * En la **Operación 3 (Jornadas de unidades móviles)**, la Estrategia Voraz ($\Theta(n \log n)$) supera ampliamente a la regla por orden de llegada en cantidad de jornadas atendidas (eliminando bloqueos por intervalos largos) y evita la explosión exponencial $\Theta(n \cdot 2^n)$ del enfoque exhaustivo. Si el criterio cambiara a maximizar pacientes ponderados con pesos distintos, correspondería evaluar programación dinámica de intervalos ponderados.
  * En la **Operación 2 (Lista diaria de llamadas)**, Merge Sort ($\Theta(N \log N)$) garantiza ordenamiento estable y determinista por riesgo y antigüedad, superando por órdenes de magnitud a Insertion Sort ($\Theta(N^2)$) tanto en tiempo como en consumo energético.
* **Limitaciones y lecciones aprendidas:** Merge Sort requiere memoria auxiliar $\Theta(N)$ (un aspecto a vigilar al crecer a $2.900.000$ registros), y las estimaciones energéticas parten de un servidor de $380\text{ W}$ con carga de cómputo aislada del algoritmo. Como lección clave, validar con pruebas unitarias, casos límite y mediciones empíricas evita asumir que una regla simple o heredada escala bien en producción.
* **Recomendación técnica unificada:** Adoptar algoritmos de complejidad $\Theta(N \log N)$ con criterios de desempate explícitos y pruebas automatizadas en el pipeline nocturno, manteniendo trazabilidad de datos y monitoreando el consumo de memoria ante crecimientos de carga como el tamizaje de hipertensión.

### 2. Instrucciones de Reproducción desde Terminal Limpia
Con el repositorio clonado y ubicado en la raíz del proyecto:

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```
   *(En CMD de Windows: `env\Scripts\activate.bat`)*

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar pruebas unitarias y mediciones de ambas operaciones:**
   ```bash
   python src/jornadas_unidades/pruebas.py
   python src/jornadas_unidades/medicion.py
   python src/ordenamiento_llamadas/pruebas.py
   python src/ordenamiento_llamadas/medicion.py
   ```