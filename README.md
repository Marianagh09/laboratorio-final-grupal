# Proyecto Final - Analisis de algoritmos 

## Plataforma Pulso

**Integrantes**
* Mariana Garcia
* Maria Fernanda Muñoz
* Diego Alejandro Quintero 
* Roberto Echeverri 

---

## Instrucciones de reproduccion para el proyecto 

para activar el entorno virtual de trabajo y ejecutar:

1. **Ubicarse en la raiz del repositorio:**
    ```bash
    cd laboratorio-final-grupal
    .\env\Scripts\Activate.ps1

2. **Instalar las dependencias**
    pip install -r requirements.txt


--------------------------------------------------------------------------------------

# Analisis del problema 

## Entradas, Salidas y Restricciones del negocio
* **Entradas**
    * Un conjuto de $N$ solicitudes de jornadas de valoracion recibidas durante el mes en una subregion especifica ($N$ varia entre 40 y 120 solicitudes por subregion al mes).
    * Cada solicitud $i$ viene representada por una tupla: ($(\text{inicio}_i, \text{fin}_i, \text{pacientes}_i)$), donde $\text{inicio}_i$ y $\text{fin}_i$ se expresa en minutos acumulados del mes ($0 \le \text{inicio}_i < \text{fin}_i \le 43.200\text{ min}$) e incluye el tiempo de desplazamiento de la unidad. $\text{pacientes}_i$ indica el numero de pacientes de alto riesgo en el municipio.

* **Salida**
    * Un subconjunto optimo de solicitudes aceptadas, ordenadas por hora de inicio, que se asignan a la unidad de movilidad sin generar solapamientos del tiempo.

* **Restriccion del negocio**
    * **Sin Traslapes**: La programacion de la unidad movil nunca  puede tener 2 jornadas que se crucen en el tiempo.
    * **Capacidad unica**: Cada subregion dispone de exactamente de una unidad movil de valoracion. 

### Supuesto tecnicos adoptados 

1. **Criterio de Solapamiento en fronteras:** Si una jornada finaliza en el minuto $M$ ($\text{fin}_1 = M$) y otra jornada inicia exactamente en el mismo minuto $M$ ($\text{inicio}_2 = M$), no se considera cruce de horario, ya que el tiempo de desplazamiento e inspeccion previa esta incluido en el calculo del limite $M$.

2. **Criterio de optimizacion elegido:** El equipo selecciona la *Estrategia voraz de seleccion de actividades* (ordenando por menor hora de fianlizacion) para maximizar la cantidad total de jornadas atendidas por la unidad movil en la subregion.


# Analisis comparativo 

## Descripcion del fallo de la regla actual 

el procedimiento actual asigna las jornadas por orden de llegada de las solicitudes y rechaza automaticamente cualquier solicitud que se cruce con una previamente aceptada. Esta regla es ineficiente porque si una solicitud que llega temprano abarca un rango de tiempo excesivamente largo, bloquea multiples jornadas mas cortas que podrian haberse atendido en ese mismo intervalo. 

## Instancia del contraejemplo calculo a mano

Considere la siguiente secuencia de 4 solicitudes que llegan a la plataforma en el orden 
$S_1, S_2, S_3, S_4$:
* Solicitud 1 ($S_1$): Inicio = 09:00 (540 min), Fin = 17:00 (1020 min), Pacientes = 40.
* Solicitud 2 ($S_2$): Inicio = 08:00 (480 min), Fin = 10:00 (600 min), Pacientes = 25.
* Solicitud 3 ($S_3$): Inicio = 10:00 (600 min), Fin = 12:00 (720 min), Pacientes = 30.
* Solicitud 4 ($S_4$): Inicio = 12:00 (720 min), Fin = 14:00 (840 min), Pacientes = 35.

1. **Procesamiento con la regal actual (Orden de llegada)**
* Evalúa $S_1$ (09:00 - 17:00): Aceptada.
* Evalúa $S_2$ (08:00 - 10:00): Se cruza con $S_1$ (09:00 - 17:00) $\rightarrow$ Rechazada.
* Evalúa $S_3$ (10:00 - 12:00): Se cruza con $S_1$ (09:00 - 17:00) $\rightarrow$ Rechazada.
* Evalúa $S_4$ (12:00 - 14:00): Se cruza con $S_1$ (09:00 - 17:00) $\rightarrow$ Rechazada.
* Resultado de la Regla Actual: Atiende 1 sola jornada ($S_1$).

2. **Procesamiento con la estrategia voraz optima**
* Ordena las solicitudes por hora de finalización: $S_2$ (Fin: 10:00), $S_3$ (Fin: 12:00), $S_4$ (Fin: 14:00), $S_1$ (Fin: 17:00).
* Selecciona $S_2$ (08:00 - 10:00) $\rightarrow$ Aceptada.
* Selecciona $S_3$ (10:00 - 12:00) $\rightarrow$ No se cruza con $S_2$ $\rightarrow$ Aceptada.
* Selecciona $S_4$ (12:00 - 14:00) $\rightarrow$ No se cruza con $S_3$ $\rightarrow$ Aceptada.
* Evalúa $S_1$ (09:00 - 17:00) $\rightarrow$ Se cruza con las anteriores $\rightarrow$ Rechazada.
*   * Resultado de la Solución Óptima: Atiende 3 jornadas ($S_2, S_3, S_4$).

**Cuantificacion del impacto**
    * **Diferencia absoluta:** La regla actual deja de atender 2 jornadas completas en la subregion.
    * **perdida relativa:** El procedimiento del coordinador desperdicia un 66.6% de la capacidad operativa de la unidad movil en esta instancia.


**Condicion contraria**
Para que la programacion dinamiaca de intervalos ponderados fuera la estrategia adecuada en lugar de la estrategia voraz de seleccion de actividades, el objetivo del negocio tendria que cambiar de maximizar la cantida de jornadas a maximizar el numero total de pacientes de alto riesgo atendidos, donde cada jornada tiene un peso diferente ($\text{pacientes}_i$) y elegir la jornada de menor duracion no garantiza acumular el mayor numero de pacientes. 

---

## Evaluación del desempeño (Operación 3: Jornadas de unidades móviles)

### 1. Complejidad teórica
- **Estrategia Voraz (Terminación más temprana):** $\Theta(n \log n)$ en tiempo (dominado por el ordenamiento por hora de finalización, seguido de una pasada lineal $\Theta(n)$) y $\Theta(n)$ en espacio auxiliar.
- **Enfoque Exhaustivo (Fuerza bruta):** $\Theta(n \cdot 2^n)$ en tiempo (evalúa los $2^n$ subconjuntos posibles y valida compatibilidad en hasta $n$ pasos) y $\Theta(n)$ en espacio.
- **Regla Actual (Orden de llegada):** $\Theta(n)$ en tiempo y $\Theta(n)$ en espacio, pero subóptima en calidad de solución.

### 2. Verificación experimental y pruebas unitarias
La corrección funcional se validó mediante [`pruebas.py`](src/jornadas_unidades/pruebas.py) y [`datos.py`](src/jornadas_unidades/datos.py) (semilla fija `2026`), cubriendo:
- Casos límite: lista vacía, una sola solicitud, solicitudes totalmente traslapadas y jornadas encadenadas en los extremos ($s_i = f_{i-1}$).
- El contraejemplo calculado a mano ($S_1, S_2, S_3, S_4$), confirmando que la regla actual acepta 1 jornada mientras la estrategia voraz obtiene las 3 óptimas sin cruces.
- 25 instancias aleatorias pequeñas donde `estrategia_voraz` iguala exactamente el número máximo de jornadas hallado por `exhaustivo` sin producir solapamientos.

### 3. Resultados experimentales y contraste empírico
Las mediciones se realizaron en [`medicion.py`](src/jornadas_unidades/medicion.py) cronometrando únicamente la ejecución algorítmica con `time.perf_counter()` (promediando 10 repeticiones para la voraz y 3 para la exhaustiva) y contando comparaciones elementales.

#### Experimento A: Comparación directa frente al enfoque exhaustivo
| $N$ (solicitudes) | Voraz (ms) | Exhaustivo (ms) | Regla Actual (ms) | Ops Voraz | Ops Exhaustivo |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 0.0021 | 0.0136 | 0.0009 | 8 | 40 |
| 6 | 0.0022 | 0.0360 | 0.0007 | 14 | 232 |
| 8 | 0.0028 | 0.1745 | 0.0007 | 24 | 1,712 |
| 10 | 0.0018 | 0.5749 | 0.0009 | 30 | 8,216 |
| 12 | 0.0024 | 1.8519 | 0.0007 | 38 | 48,192 |
| 14 | 0.0027 | 7.4732 | 0.0011 | 51 | 258,432 |
| 16 | 0.0051 | 25.2141 | 0.0010 | 62 | 1,272,832 |

#### Experimento B: Escalabilidad de la estrategia voraz al duplicar $N$
| $N$ (solicitudes) | Voraz (ms) | Factor tiempo | Ops Voraz | Factor operaciones |
| :---: | :---: | :---: | :---: | :---: |
| 100 | 0.0137 | — | 635 | — |
| 1,000 | 0.1425 | — | 9,714 | — |
| 2,000 | 0.4084 | $2.87\times$ | 21,405 | $2.20\times$ |
| 4,000 | 1.1598 | $2.84\times$ | 46,879 | $2.19\times$ |
| 8,000 | 2.4323 | $2.10\times$ | 101,589 | $2.17\times$ |
| 16,000 | 6.0262 | $2.48\times$ | 219,316 | $2.16\times$ |
| 32,000 | 10.5287 | $1.75\times$ | 470,712 | $2.15\times$ |
| 64,000 | 28.7519 | $2.73\times$ | 1,004,920 | $2.13\times$ |

**Contraste teórico vs. empírico:**
- **Enfoque Exhaustivo:** Al pasar de $N = 8$ ($0.1745\text{ ms}$, $1.712\text{ ops}$) a $N = 16$ ($25.2141\text{ ms}$, $1.272.832\text{ ops}$), el tiempo se multiplicó por $144.5\times$ (cercano al factor teórico $2 \cdot 2^8 = 512\times$ de $\Theta(n \cdot 2^n)$), confirmando el crecimiento exponencial.
- **Estrategia Voraz:** Al duplicar $N$ (por ejemplo, de $8.000$ a $16.000$ y de $32.000$ a $64.000$), las operaciones elementales crecen por un factor estable de **$2.13\times$ a $2.20\times$** ("un poco más del doble"), coincidiendo exactamente con la firma matemática $\frac{2n \log_2(2n)}{n \log_2 n} = 2\left(1 + \frac{1}{\log_2 n}\right)$ de $\Theta(n \log n)$.

![Tiempo vs N](graficas/jornadas_unidades/tiempo_vs_n.png)

![Operaciones vs N](graficas/jornadas_unidades/operaciones_vs_n.png)

### 4. Extrapolación al volumen real y consumo energético (Implicaciones ambientales)
- **Volumen real del caso:** 9 subregiones, con entre $40$ y $120$ solicitudes mensuales cada una (peor caso: $N = 120$ por subregión), ejecutado en un servidor de $380\text{ W}$ ($0.38\text{ kW}$). Como referencia operativa, la programación mensual debe resolverse dentro de una ventana de planeación nocturna de $1\text{ hora}$ ($3.600\text{ s}$).
- **Estimación Estrategia Voraz:** Partiendo de la medición empírica para $N = 100$ ($0.0137\text{ ms}$) y escalando bajo $\Theta(n \log n)$ hasta $N = 120$, cada subregión toma $\approx 0.017\text{ ms}$. Para las 9 subregiones en conjunto, el tiempo total mensual es de **$0.15\text{ ms}$ ($0.00015\text{ s}$)**, cumpliendo ampliamente con la ventana operativa.
  - *Consumo energético:* $0.38\text{ kW} \times \frac{0.00015}{3600}\text{ h} \approx 1.58 \times 10^{-8}\text{ kWh/mes}$ ($1.90 \times 10^{-7}\text{ kWh/año}$).
- **Estimación Regla Actual:** Con complejidad $\Theta(n)$, para $N = 120$ en 9 subregiones tarda $\approx 0.010\text{ ms}$ totales ($1.06 \times 10^{-8}\text{ kWh/mes}$ o $1.27 \times 10^{-7}\text{ kWh/año}$). La diferencia anual de consumo eléctrico frente a la estrategia voraz es despreciable ($\approx 6.3 \times 10^{-8}\text{ kWh/año}$), pero la estrategia voraz elimina el desperdicio operativo de unidades móviles subutilizadas.
- **Estimación Enfoque Exhaustivo:** Partiendo de $N = 16$ ($25.21\text{ ms}$) y proyectando bajo $\Theta(n \cdot 2^n)$ hasta $N = 120$, el factor de crecimiento es $\frac{120}{16} \cdot 2^{104} \approx 1.52 \times 10^{32}$. Una sola subregión tardaría $\approx 1.2 \times 10^{23}\text{ años}$, por lo que **sencillamente no terminaría** y es inviable para operación real.

---

## Instrucciones de ejecución (Pruebas y Medición)
Con el entorno virtual activado y las dependencias instaladas (`pip install -r requirements.txt`):
- **Ejecutar pruebas unitarias:** `python3 src/jornadas_unidades/pruebas.py`
- **Ejecutar experimentos y regenerar gráficas:** `python3 src/jornadas_unidades/medicion.py`

