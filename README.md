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
        * **Diferencia absoluta:** La regla actual deja de atender 2 jornadas completas en la subregion 
        * **perdida relativa:** El procedimiento del coordinador desperdicia un 66.6% de la capacidad operativa de la unidad movil en esta instancia.


**Condicion contraria**
Para que la programacion dinamiaca de intervalos ponderados fuera la estrategia adecuada en lugar de la estrategia voraz de seleccion de actividades, el objetivo del negocio tendria que cambiar de maximizar la cantida de jornadas a maximizar el numero total de pacientes de alto riesgo atendidos, donde cada jornada tiene un peso diferente ($\text{pacientes}_i$) y elegir la jornada de menor duracion no garantiza acumular el mayor numero de pacientes. 