from datos import generar_solicitudes
from src.jornadas_unidades.estrategia import estrategia_voraz
from src.jornadas_unidades.exhaustivo import exhaustivo
from src.jornadas_unidades.regla_actual import regla_actual

# 1. Generamos los datos (por ejemplo, 15 solicitudes)
solicitudes = generar_solicitudes(n=15)

print(f"Cantidad total de solicitudes generadas: {len(solicitudes)}\n")

# 2. Ejecutamos la regla actual
res_actual = regla_actual(solicitudes)
print(f"Regla actual (orden de llegada): {len(res_actual)} jornadas asignadas.")

# 3. Ejecutamos la estrategia voraz
res_voraz = estrategia_voraz(solicitudes)
print(f"Estrategia Voraz (termina primero): {len(res_voraz)} jornadas asignadas.")

# 4. Ejecutamos la búsqueda exhaustiva (OJO: no poner un N mayor a 20, o se colgará el PC)
# Usamos las primeras 10 solicitudes para que el exhaustivo termine rápido
muestra_pequena = solicitudes[:10]
res_exhaustivo = exhaustivo(muestra_pequena)
print(f"\nBúsqueda Exhaustiva (en una muestra de 10): {len(res_exhaustivo)} jornadas máximo real.")