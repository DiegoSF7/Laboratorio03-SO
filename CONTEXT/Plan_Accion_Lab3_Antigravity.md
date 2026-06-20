# PLAN DE ACCIÓN — Lab Eval 3 — TechSolutions Chile
## Para: Antigravity IDE — Generación automática de código
### Meta: 100% de la evaluación (40% de la asignatura)

---

## CONFIGURACIÓN INICIAL

| Parámetro | Valor |
|---|---|
| Lenguaje | Python 3.12+ |
| OS Target | Windows 10/11 |
| Dependencia externa | `pip install psutil` |
| Carpeta raíz | `TechSolutions_Lab3/` |
| Encoding archivos propios | UTF-8 |
| Encoding subprocess Windows | cp850 |

---

## ESTRUCTURA DE ARCHIVOS A GENERAR (en este orden)

```
TechSolutions_Lab3/
├── modulo_archivos.py     ← PRIMERO (todos los demás lo importan)
├── modulo_procesos.py     ← SEGUNDO
├── modulo_cpu.py          ← TERCERO
├── modulo_memoria.py      ← CUARTO
├── modulo_reportes.py     ← QUINTO
├── main.py                ← ÚLTIMO (importa todos)
└── bitacora.txt           ← Auto-generado en runtime
```

---

## PATRÓN GLOBAL (aplicar en TODOS los módulos)

### Patrón subprocess estándar
```python
resultado = subprocess.run(
    comando_string,
    shell=True,
    capture_output=True,
    text=True,
    encoding='cp850',
    errors='replace'
)
# Revisar resultado.returncode, resultado.stdout, resultado.stderr
```

### Patrón manejo de errores (wrap TODAS las operaciones críticas)
```python
try:
    # operación principal
except FileNotFoundError:
    print("✗ Archivo o directorio no encontrado.")
    registrar_bitacora(op, "Error: no encontrado")
except PermissionError:
    print("✗ Permisos insuficientes.")
    registrar_bitacora(op, "Error: permisos")
except ValueError:
    print("✗ Valor inválido.")
except subprocess.CalledProcessError as e:
    print(f"✗ Error al ejecutar comando: {e}")
```

### Función helper de validación (definir en `modulo_archivos.py`, importar donde se necesite)
```python
def validar_entero(prompt: str, minimo: int = 1, maximo: int = 9999) -> int:
    while True:
        try:
            valor = int(input(prompt))
            if minimo <= valor <= maximo:
                return valor
            print(f"⚠ Ingrese un valor entre {minimo} y {maximo}")
        except ValueError:
            print("⚠ Ingrese un número entero válido.")
```

---

## ARCHIVO 1: `modulo_archivos.py`

### Imports
```python
import os
import subprocess
import datetime
import shutil
```

---

### Función: `registrar_bitacora(operacion: str, resultado: str) -> None`

**Propósito:** Logger central. Todas las operaciones del sistema deben llamarla.

**Pasos exactos:**
1. `timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')`
2. `try: usuario = os.getlogin()` / `except: usuario = os.environ.get('USERNAME', 'Desconocido')`
3. `linea = f"[{timestamp}] | Usuario: {usuario} | Operación: {operacion} | Resultado: {resultado}\n"`
4. Abrir `"bitacora.txt"` en modo `'a'`, encoding `'utf-8'`
5. Escribir línea y cerrar
6. Envolver en `try/except OSError` → imprimir advertencia pero no detener ejecución

---

### Función: `validar_entero(prompt, minimo=1, maximo=9999) -> int`
(ver patrón global arriba — copiar aquí literalmente)

---

### Función: `crear_directorio() -> None`

**Pasos:**
1. `nombre = input("Ingrese nombre del directorio a crear: ").strip()`
2. Si `nombre` vacío: print "⚠ Nombre inválido." y return
3. `res = subprocess.run(f'mkdir "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
4. Si `res.returncode == 0`: print `f"✓ Directorio '{nombre}' creado exitosamente."` → `registrar_bitacora(f"mkdir {nombre}", "Éxito")`
5. Si `'ya existe'` in `res.stderr.lower()` o `'already exists'` in `res.stderr.lower()`: print "⚠ El directorio ya existe." → `registrar_bitacora(f"mkdir {nombre}", "Error: ya existe")`
6. Else: print `f"✗ Error: {res.stderr.strip()}"` → `registrar_bitacora(f"mkdir {nombre}", f"Error: {res.stderr.strip()}")`

---

### Función: `eliminar_directorio() -> None`

**Pasos:**
1. `nombre = input("Ingrese nombre del directorio a eliminar: ").strip()`
2. `if not os.path.isdir(nombre): print("⚠ El directorio no existe."); registrar_bitacora(f"rmdir {nombre}", "Error: no existe"); return`
3. `confirm = input(f"¿Eliminar '{nombre}' y todo su contenido? (s/n): ").strip().lower()`
4. Si `confirm != 's'`: print "Operación cancelada." y return
5. `res = subprocess.run(f'rmdir /s /q "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
6. Verificar `returncode` y registrar igual que `crear_directorio`

---

### Función: `crear_archivo() -> None`

**Pasos:**
1. `nombre = input("Ingrese nombre del archivo (con extensión, ej: datos.txt): ").strip()`
2. Si `nombre` vacío: return con advertencia
3. `contenido = input("Ingrese contenido inicial (Enter para archivo vacío): ")`
4. Si `contenido` vacío:
   `res = subprocess.run(f'type nul > "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
5. Si tiene contenido:
   `res = subprocess.run(f'echo {contenido} > "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
6. Verificar con `os.path.exists(nombre)` para confirmar creación real
7. Registrar en bitácora

---

### Función: `listar_contenido() -> None`

**Pasos:**
1. `ruta = input("Ingrese ruta a listar (Enter = directorio actual): ").strip()`
2. Si vacía: `ruta = os.getcwd()`
3. `if not os.path.exists(ruta): print("⚠ Ruta no existe."); return`
4. `subprocess.run(f'dir "{ruta}"', shell=True, text=True, encoding='cp850', errors='replace')`  ← sin capture_output para imprimir directo
5. Registrar en bitácora: `f"dir {ruta}"`, `"Ejecutado"`

---

### Función: `copiar_archivo() -> None`

**Pasos:**
1. `origen = input("Ruta del archivo origen: ").strip()`
2. `if not os.path.exists(origen): print("⚠ Archivo origen no encontrado."); registrar_bitacora(...); return`
3. `destino = input("Ruta de destino: ").strip()`
4. `res = subprocess.run(f'copy "{origen}" "{destino}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
5. Si `res.returncode == 0`: print `f"✓ Archivo copiado a '{destino}'"`
6. Else: print `f"✗ Error: {res.stderr.strip()}"`
7. Registrar en bitácora

---

### Función: `mover_archivo() -> None`

Idéntica a `copiar_archivo()` pero con comando `move "{origen}" "{destino}"` y mensaje "movido".

---

### Función: `renombrar_archivo() -> None`

**Pasos:**
1. `actual = input("Nombre actual del archivo: ").strip()`
2. `if not os.path.exists(actual): print("⚠ Archivo no encontrado."); return`
3. `nuevo = input("Nuevo nombre: ").strip()`
4. `res = subprocess.run(f'rename "{actual}" "{nuevo}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
5. Verificar returncode y registrar en bitácora

---

### Función: `eliminar_archivo() -> None`

**Pasos:**
1. `nombre = input("Ingrese nombre del archivo a eliminar: ").strip()`
2. `if not os.path.exists(nombre): print("⚠ Archivo no encontrado."); registrar_bitacora(...); return`
3. Confirmación con input
4. `res = subprocess.run(f'del "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
5. Verificar con `not os.path.exists(nombre)` para confirmar eliminación
6. Registrar en bitácora

---

### Función: `menu_archivos() -> None`

Bucle `while True`. Mostrar este menú exacto:

```
╔══════════════════════════════════════╗
║     MÓDULO 2: GESTIÓN DE ARCHIVOS    ║
╠══════════════════════════════════════╣
║ 1. Crear directorio                  ║
║ 2. Eliminar directorio               ║
║ 3. Crear archivo                     ║
║ 4. Listar contenido                  ║
║ 5. Copiar archivo                    ║
║ 6. Mover archivo                     ║
║ 7. Renombrar archivo                 ║
║ 8. Eliminar archivo                  ║
║ 0. Volver al menú principal          ║
╚══════════════════════════════════════╝
```

Usar `if/elif/else` mapeando cada número a su función. Si ValueError o número fuera de rango: "⚠ Opción inválida."  
Después de cada operación: `input("\nPresione Enter para continuar...")`.  
Opción 0: `break` del while.

---

## ARCHIVO 2: `modulo_procesos.py`

### Imports
```python
import os
import subprocess
import psutil
from modulo_archivos import registrar_bitacora
```

---

### Función: `listar_procesos() -> None`

**Pasos:**
1. Ejecutar: `subprocess.run('tasklist', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')` → guardar stdout para mostrar el output crudo de MS-DOS al final
2. Usar `psutil.process_iter(['pid', 'name', 'memory_info'])` para tabla formateada
3. Inicializar `lista = []`
4. Loop con `try/except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): continue`
5. Cada proceso: `{'pid': p.info['pid'], 'nombre': p.info['name'], 'memoria_kb': p.info['memory_info'].rss // 1024}`
6. Append a `lista`
7. Ordenar por memoria descendente: `lista.sort(key=lambda x: x['memoria_kb'], reverse=True)`
8. Imprimir encabezado: `f"{'PID':>8}  {'Nombre del Proceso':<35}  {'Memoria (KB)':>15}"`
9. Separador: `"-" * 62`
10. Loop imprimiendo cada proceso: `f"{p['pid']:>8}  {p['nombre']:<35}  {p['memoria_kb']:>15,}"`
11. Al final: `print(f"\nTotal: {len(lista)} procesos activos.")`
12. Mostrar también el output de tasklist: `print("\n--- Salida de TASKLIST (MS-DOS) ---\n", res.stdout[:2000])`
13. `registrar_bitacora("listar_procesos", f"{len(lista)} procesos encontrados")`

---

### Función: `buscar_proceso() -> None`

**Pasos:**
1. `nombre_busqueda = input("Ingrese nombre del proceso a buscar (ej: chrome, notepad): ").strip().lower()`
2. Si vacío: print "⚠ Ingrese un nombre." y return
3. `encontrados = []`
4. Loop `psutil.process_iter(['pid', 'name', 'memory_info', 'status'])` con try/except igual que listar_procesos
5. Filtro: `if nombre_busqueda in p.info['name'].lower()` → append
6. Si `not encontrados`: print `f"⚠ No se encontraron procesos con '{nombre_busqueda}'."` → registrar y return
7. Imprimir tabla igual que listar_procesos + columna Estado: `f"{'Estado':<15}"`
8. `registrar_bitacora(f"buscar_proceso {nombre_busqueda}", f"{len(encontrados)} encontrados")`

---

### Función: `finalizar_proceso() -> None`

**Pasos:**
1. `objetivo = input("Ingrese PID (número) o nombre del proceso a finalizar: ").strip()`
2. `try: pid = int(objetivo); modo = 'pid'` / `except ValueError: modo = 'nombre'`
3. Si `modo == 'pid'`: `cmd = f'taskkill /PID {objetivo} /F'`
4. Si `modo == 'nombre'`: `cmd = f'taskkill /IM "{objetivo}" /F'`
5. `res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
6. Si `res.returncode == 0`: print `"✓ Proceso finalizado exitosamente."`
7. Si `'no encontr'` in `res.stderr.lower()` o `'not found'` in `res.stderr.lower()`: print `"⚠ Proceso no encontrado."`
8. Si `'acceso denegado'` in `res.stderr.lower()` o `'access denied'` in `res.stderr.lower()`: print `"✗ Acceso denegado (proceso del sistema)."`
9. Else error: print `f"✗ Error: {res.stderr.strip()}"`
10. `registrar_bitacora(f"taskkill {objetivo}", f"{'Éxito' if res.returncode == 0 else res.stderr.strip()}")`

---

### Función: `menu_procesos() -> None`

Mismo patrón de submenú que `menu_archivos`. Opciones:
```
1. Listar todos los procesos activos
2. Buscar proceso por nombre
3. Finalizar proceso (por PID o nombre)
0. Volver al menú principal
```

---

## ARCHIVO 3: `modulo_cpu.py`

### Imports
```python
import os
from collections import deque
from modulo_archivos import registrar_bitacora, validar_entero
```

---

### Función: `ingresar_procesos() -> list[dict]`

**Pasos:**
1. `n = validar_entero("¿Cuántos procesos desea ingresar? ", minimo=1, maximo=20)`
2. `procesos = []`
3. Loop `for i in range(n)`:
   - `nombre = input(f"Nombre proceso {i+1} (Enter = P{i+1}): ").strip()`
   - Si vacío: `nombre = f"P{i+1}"`
   - `burst = validar_entero(f"Tiempo de CPU (burst) de {nombre}: ", minimo=1, maximo=999)`
   - `procesos.append({'nombre': nombre, 'burst': burst, 'id': i, 'arrival': 0})`
4. Confirmar: imprimir lista ingresada con `f"  {p['nombre']}: burst={p['burst']}"`
5. Return `procesos`

---

### Función: `fcfs(procesos: list[dict]) -> dict`

**Algoritmo exacto (no modificar):**
```python
def fcfs(procesos):
    tiempo_actual = 0
    resultados = []
    for p in procesos:  # orden de llegada = orden de lista
        inicio = tiempo_actual
        fin = inicio + p['burst']
        espera = inicio              # arrival = 0 para todos
        retorno = fin                # turnaround = fin - arrival = fin
        tiempo_actual = fin
        resultados.append({
            'nombre': p['nombre'],
            'burst': p['burst'],
            'inicio': inicio,
            'fin': fin,
            'espera': espera,
            'retorno': retorno
        })
    prom_espera = sum(r['espera'] for r in resultados) / len(resultados)
    prom_retorno = sum(r['retorno'] for r in resultados) / len(resultados)
    return {
        'algoritmo': 'FCFS',
        'resultados': resultados,
        'promedio_espera': prom_espera,
        'promedio_retorno': prom_retorno
    }
```

---

### Función: `sjf(procesos: list[dict]) -> dict`

**Algoritmo:**
1. `ordenados = sorted(procesos, key=lambda x: x['burst'])`  ← ordena de menor a mayor burst
2. `resultado = fcfs(ordenados)`  ← misma lógica FCFS aplicada al orden SJF
3. `resultado['algoritmo'] = 'SJF (Shortest Job First)'`
4. Return `resultado`

---

### Función: `round_robin(procesos: list[dict], quantum: int) -> dict`

**Algoritmo exacto (no modificar):**
```python
def round_robin(procesos, quantum):
    cola = deque([{**p, 'restante': p['burst']} for p in procesos])
    tiempo_actual = 0
    tiempos_fin = {}
    orden_ejecucion = []

    while cola:
        p = cola.popleft()
        ejecucion = min(p['restante'], quantum)
        tiempo_actual += ejecucion
        p['restante'] -= ejecucion
        orden_ejecucion.append(f"{p['nombre']}({ejecucion})")
        if p['restante'] > 0:
            cola.append(p)
        else:
            tiempos_fin[p['nombre']] = tiempo_actual

    resultados = []
    for proc in procesos:
        fin = tiempos_fin[proc['nombre']]
        retorno = fin                        # arrival = 0
        espera = retorno - proc['burst']
        resultados.append({
            'nombre': proc['nombre'],
            'burst': proc['burst'],
            'fin': fin,
            'espera': espera,
            'retorno': retorno
        })

    prom_espera = sum(r['espera'] for r in resultados) / len(resultados)
    prom_retorno = sum(r['retorno'] for r in resultados) / len(resultados)
    return {
        'algoritmo': f'Round Robin (Quantum={quantum})',
        'resultados': resultados,
        'promedio_espera': prom_espera,
        'promedio_retorno': prom_retorno,
        'orden_ejecucion': orden_ejecucion
    }
```

---

### Función: `mostrar_resultados(resultado: dict) -> None`

**Pasos:**
1. `print(f"\n{'='*60}")`
2. `print(f"  RESULTADO: {resultado['algoritmo']}")`
3. `print(f"{'='*60}")`
4. Encabezado: `f"{'Proceso':<10} {'Burst':>7} {'Inicio':>8} {'Fin':>6} {'Espera':>8} {'Retorno':>9}"`
5. Separador: `"-" * 52`
6. Loop por `resultado['resultados']`: imprimir con mismo formato `f"{r['nombre']:<10} {r['burst']:>7} ..."`
7. Separador al final
8. `print(f"  Promedio de espera:   {resultado['promedio_espera']:.2f} unidades de tiempo")`
9. `print(f"  Promedio de retorno:  {resultado['promedio_retorno']:.2f} unidades de tiempo")`
10. Si `'orden_ejecucion'` en resultado (solo Round Robin): `print(f"  Orden de ejecución: {' → '.join(resultado['orden_ejecucion'])}")`

---

### Función: `comparar_algoritmos(r_fcfs: dict, r_sjf: dict, r_rr: dict) -> None`

**Pasos:**
1. Crear dict: `algoritmos = {r_fcfs['algoritmo']: r_fcfs['promedio_espera'], r_sjf['algoritmo']: r_sjf['promedio_espera'], r_rr['algoritmo']: r_rr['promedio_espera']}`
2. `mejor = min(algoritmos, key=algoritmos.get)`
3. Imprimir tabla comparativa:
```
╔══════════════════════════════════════════════════════╗
║            COMPARACIÓN DE ALGORITMOS DE CPU          ║
╠══════════════════════════╦═══════════╦═══════════════╣
║ Algoritmo                ║ Prom. Esp ║ Prom. Retorno ║
╠══════════════════════════╬═══════════╬═══════════════╣
║ FCFS                     ║   X.XX    ║     X.XX      ║
║ SJF                      ║   X.XX    ║     X.XX      ║
║ Round Robin (Q=X)        ║   X.XX    ║     X.XX      ║
╚══════════════════════════╩═══════════╩═══════════════╝
```
4. `print(f"\n  ★ MEJOR ALGORITMO: {mejor}")`
5. `print(f"    Promedio de espera más bajo: {algoritmos[mejor]:.2f} unidades")`
6. Imprimir ventajas/desventajas hardcodeadas:
```
print("""
VENTAJAS Y DESVENTAJAS:
  FCFS:
    + Simple de implementar, sin cálculos adicionales.
    - Efecto convoy: procesos cortos esperan por largos.

  SJF:
    + Minimiza el tiempo promedio de espera globalmente.
    - Puede causar inanición (starvation) en procesos largos.
    - Requiere conocer el burst time de antemano.

  Round Robin:
    + Equitativo: todos los procesos reciben tiempo de CPU.
    + Buen tiempo de respuesta en sistemas interactivos.
    - Mayor overhead por cambios de contexto (context switch).
    - El rendimiento depende fuertemente del quantum elegido.
""")
```
7. `registrar_bitacora("comparar_algoritmos", f"Mejor: {mejor} ({algoritmos[mejor]:.2f})")`

---

### Función: `menu_cpu() -> None`

Submenú estándar. Opciones:
```
1. Simular FCFS
2. Simular SJF (Shortest Job First)
3. Simular Round Robin
4. Comparar los 3 algoritmos (ingreso único)
0. Volver al menú principal
```

**Lógica de opción 4 (comparación completa):**
```python
procesos = ingresar_procesos()
quantum = validar_entero("Ingrese quantum para Round Robin: ", 1, 100)
r_fcfs = fcfs(procesos)
r_sjf = sjf(procesos)
r_rr = round_robin(procesos, quantum)
mostrar_resultados(r_fcfs)
mostrar_resultados(r_sjf)
mostrar_resultados(r_rr)
comparar_algoritmos(r_fcfs, r_sjf, r_rr)
```

**Opciones 1, 2, 3:** llamar `ingresar_procesos()` individualmente, pedir quantum solo para RR.

---

## ARCHIVO 4: `modulo_memoria.py`

### Imports
```python
import psutil
from modulo_archivos import registrar_bitacora, validar_entero
```

---

### Función: `mostrar_memoria_real() -> None`

**Pasos:**
1. `mem = psutil.virtual_memory()`
2. Conversiones: `total_gb = round(mem.total / (1024**3), 2)`, `used_gb = ...`, `free_gb = ...`
3. `porcentaje = mem.percent`
4. Barra visual: `bloques = int(porcentaje / 5)`, `barra = "█" * bloques + "░" * (20 - bloques)`
5. Imprimir:
```
╔══════════════════════════════════════╗
║     MÓDULO 5: MEMORIA RAM REAL       ║
╠══════════════════════════════════════╣
║  Total:      X.XX GB                 ║
║  Usada:      X.XX GB                 ║
║  Libre:      X.XX GB                 ║
║  Uso:        XX.X%                   ║
║  [████████████░░░░░░░░] XX%          ║
╚══════════════════════════════════════╝
```
6. `registrar_bitacora("ver_memoria_real", f"Uso: {porcentaje}%")`

---

### Función: `ingresar_procesos_memoria() -> tuple[int, list[dict]]`

**Pasos:**
1. `memoria_total = validar_entero("Ingrese memoria total para simulación (MB): ", 64, 65536)`
2. `n = validar_entero("¿Cuántos procesos a cargar en memoria? ", 1, 20)`
3. `procesos = []`
4. Loop: `nombre = input(f"Nombre proceso {i+1}: ")`, `tamaño = validar_entero(f"Tamaño de {nombre} (MB): ", 1, memoria_total)`
5. Append `{'nombre': nombre, 'tamaño': tamaño}`
6. Return `(memoria_total, procesos)`

---

### Función: `simular_particiones_fijas(memoria_total: int, procesos: list[dict]) -> None`

**Algoritmo exacto:**
```python
# Dividir memoria en 4 particiones iguales automáticamente
tam_part = memoria_total // 4
particiones = [
    {'id': i+1, 'tamaño': tam_part, 'proceso': None, 'tam_proceso': 0}
    for i in range(4)
]

sin_asignar = []
for proc in procesos:
    asignado = False
    for part in particiones:
        if part['proceso'] is None and part['tamaño'] >= proc['tamaño']:
            part['proceso'] = proc['nombre']
            part['tam_proceso'] = proc['tamaño']
            asignado = True
            break
    if not asignado:
        sin_asignar.append(proc['nombre'])

# Imprimir tabla:
# Partición | Tamaño(MB) | Proceso | Ocupado(MB) | Libre(MB) | Frag.Interna
# Si proceso es None → mostrar "--- Libre ---"
frag_total = sum(p['tamaño'] - p['tam_proceso'] for p in particiones if p['proceso'])
print(f"\n  Fragmentación interna total: {frag_total} MB")
if sin_asignar:
    print(f"  ✗ Sin partición disponible: {', '.join(sin_asignar)}")
```

---

### Función: `simular_particiones_variables(memoria_total: int, procesos: list[dict]) -> None`

**Algoritmo First-Fit exacto:**
```python
bloques = [{'inicio': 0, 'tamaño': memoria_total, 'libre': True, 'proceso': None}]

for proc in procesos:
    asignado = False
    for i, bloque in enumerate(bloques):
        if bloque['libre'] and bloque['tamaño'] >= proc['tamaño']:
            resto = bloque['tamaño'] - proc['tamaño']
            bloques[i] = {
                'inicio': bloque['inicio'],
                'tamaño': proc['tamaño'],
                'libre': False,
                'proceso': proc['nombre']
            }
            if resto > 0:
                bloques.insert(i + 1, {
                    'inicio': bloque['inicio'] + proc['tamaño'],
                    'tamaño': resto,
                    'libre': True,
                    'proceso': None
                })
            asignado = True
            break
    if not asignado:
        print(f"  ✗ No hay espacio contiguo para '{proc['nombre']}' ({proc['tamaño']} MB)")

# Imprimir mapa de memoria:
print(f"\n{'Inicio(MB)':>12} {'Tamaño(MB)':>12} {'Estado':^10} {'Proceso':^15}")
print("-" * 52)
for b in bloques:
    estado = "Libre" if b['libre'] else "Ocupado"
    proc_nombre = b['proceso'] if b['proceso'] else "---"
    print(f"{b['inicio']:>12} {b['tamaño']:>12} {estado:^10} {proc_nombre:^15}")

# Calcular fragmentación externa
bloques_libres = [b for b in bloques if b['libre']]
frag_externa = sum(b['tamaño'] for b in bloques_libres)
print(f"\n  Fragmentación externa: {frag_externa} MB en {len(bloques_libres)} bloque(s) libre(s)")
print(f"  Nota: en particiones variables, la fragmentación externa")
print(f"  puede compactarse moviendo procesos en memoria.")
```

---

### Función: `menu_memoria() -> None`

Opciones:
```
1. Ver memoria RAM real del sistema
2. Simular particiones fijas
3. Simular particiones variables (First-Fit)
0. Volver al menú principal
```
Opciones 2 y 3: llamar `ingresar_procesos_memoria()` primero, luego la simulación correspondiente.

---

## ARCHIVO 5: `modulo_reportes.py`

### Imports
```python
import os
import subprocess
import datetime
import psutil
from modulo_archivos import registrar_bitacora
```

---

### Función: `informacion_sistema() -> None`

**Propósito:** Módulo 1 — Ejecutar los 4 comandos MS-DOS obligatorios.

**Pasos:**
1. Ejecutar los 4 comandos:
   ```python
   res_ver  = subprocess.run('ver',        shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
   res_sys  = subprocess.run('systeminfo', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
   res_host = subprocess.run('hostname',   shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
   res_who  = subprocess.run('whoami',     shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
   ```
2. Parseo de `systeminfo` para extraer campos clave:
   ```python
   campos = {'so': '', 'version': '', 'arquitectura': ''}
   for linea in res_sys.stdout.split('\n'):
       if 'Nombre del SO' in linea or 'OS Name' in linea:
           campos['so'] = linea.split(':', 1)[1].strip()
       elif 'Versión del SO' in linea or 'OS Version' in linea:
           campos['version'] = linea.split(':', 1)[1].strip()
       elif 'Tipo de sistema' in linea or 'System Type' in linea:
           campos['arquitectura'] = linea.split(':', 1)[1].strip()
   ```
3. Imprimir tabla resumen con los valores extraídos:
```
╔══════════════════════════════════════════════════════╗
║     MÓDULO 1: INFORMACIÓN DEL SISTEMA OPERATIVO      ║
╠══════════════════════════════════════════════════════╣
║  Sistema Operativo:  [valor de systeminfo]           ║
║  Versión:            [valor de systeminfo]           ║
║  Arquitectura:       [valor de systeminfo]           ║
║  Nombre del equipo:  [valor de hostname]             ║
║  Usuario activo:     [valor de whoami]               ║
╠══════════════════════════════════════════════════════╣
║  Salida de VER:      [valor de ver]                  ║
╚══════════════════════════════════════════════════════╝
```
4. Luego imprimir: `"\n--- Salida completa de SYSTEMINFO ---"`
5. Imprimir las primeras 25 líneas de `res_sys.stdout`
6. `registrar_bitacora("informacion_sistema", f"SO: {campos['so']}")`

---

### Función: `monitoreo_es() -> None`

**Propósito:** Módulo 6 — Unidades de almacenamiento.

**Pasos:**
1. Ejecutar MS-DOS: `subprocess.run('wmic logicaldisk get caption,description,freespace,size', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')`
2. `particiones = psutil.disk_partitions(all=False)`
3. Imprimir encabezado de tabla:
   `f"{'Unidad':<10} {'FS':^8} {'Total(GB)':>12} {'Usado(GB)':>12} {'Libre(GB)':>12} {'Uso%':>7}"`
4. Loop por particiones con `try/except PermissionError: continue`:
   - `uso = psutil.disk_usage(part.mountpoint)`
   - Calcular todos los valores en GB con `/ (1024**3)`
   - Imprimir fila formateada
5. Mostrar output crudo de wmic al final
6. `registrar_bitacora("monitoreo_es", f"{len(particiones)} unidades encontradas")`

---

### Función: `generar_reporte_organizacional() -> None`

**Propósito:** Módulo 7 — Análisis caso TechSolutions (25 usuarios).

**Pasos:**
1. `try: usuario = os.getlogin()` / `except: usuario = os.environ.get('USERNAME', 'N/A')`
2. `fecha = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')`
3. `reporte = f"""` ← string multilínea con este contenido exacto:

```
═══════════════════════════════════════════════════════════════
          REPORTE ORGANIZACIONAL — TECHSOLUTIONS CHILE LTDA.
            Sistema de Administración y Monitoreo v1.0
═══════════════════════════════════════════════════════════════
Fecha de generación:  {fecha}
Analista:             {usuario}

1. ANÁLISIS DE RECURSOS NECESARIOS
───────────────────────────────────
   Escenario: 25 usuarios simultáneos con uso intensivo.
   
   CPU:         Servidor con mínimo 8 núcleos físicos (Intel Xeon
                E2300 o AMD EPYC). Frecuencia ≥ 3.0 GHz.
   RAM:         Mínimo 32 GB DDR4 ECC. Recomendado 64 GB.
   Almacenamiento: OS: SSD NVMe 500 GB. Datos: HDD 4 TB (RAID 1).
   Red:         Switch Gigabit 48 puertos + acceso WAN ≥ 200 Mbps.
   GPU:         No crítica (uso ofimático), integrada suficiente.

2. PROCESOS CRÍTICOS IDENTIFICADOS
───────────────────────────────────
   - Navegadores web (Chrome/Edge): alta memoria RAM, múltiples
     procesos por usuario. Prioridad media.
   - Videoconferencias (Teams/Zoom): alto consumo CPU + red.
     Prioridad alta durante reuniones.
   - Aplicaciones ofimáticas (Office): I/O intensivo en disco.
     Prioridad normal.
   - Servicios de autenticación (Active Directory): prioridad alta,
     deben ejecutarse sin interrupción.
   - Antivirus/Monitoreo: prioridad baja (background).

3. CONSUMO DE MEMORIA ESTIMADO (25 USUARIOS)
────────────────────────────────────────────
   Sistema Operativo base:          4.0 GB
   Navegadores (25 × 300 MB):       7.5 GB
   Ofimática (25 × 200 MB):         5.0 GB
   Videoconferencias (10 × 400 MB): 4.0 GB
   Servicios del servidor:          2.0 GB
   Buffer y caché del SO:           3.5 GB
   ─────────────────────────────────────────
   TOTAL ESTIMADO:                 ~26 GB
   RECOMENDADO:                     32 GB (margen de seguridad)

4. NECESIDADES DE ALMACENAMIENTO
──────────────────────────────────
   Documentos por usuario (500 MB × 25):  12.5 GB
   Perfiles de usuario (1 GB × 25):       25.0 GB
   Caché navegadores (1 GB × 25):         25.0 GB
   Software y aplicaciones:               15.0 GB
   Logs y bitácoras del sistema:           5.0 GB
   Respaldos diarios:                    100.0 GB
   ──────────────────────────────────────────────
   TOTAL RECOMENDADO:                    ~200 GB activo + 2 TB backup

5. SISTEMA OPERATIVO RECOMENDADO
──────────────────────────────────
   Recomendación: Windows Server 2022 Standard

   Justificación:
   - Soporte nativo para autenticación centralizada (Active Directory).
   - Compatible con licenciamiento CAL (Client Access License) para
     exactamente 25 usuarios.
   - Integración con Microsoft 365 (videoconferencias, ofimática).
   - Herramientas de monitoreo integradas (Task Manager, Perfmon,
     Resource Monitor, PowerShell).
   - Soporte de particiones NTFS con cuotas de disco por usuario.

6. ESTRUCTURA APROPIADA DEL SISTEMA
─────────────────────────────────────
   Arquitectura: Cliente-Servidor centralizado.
   - 1 servidor principal con Windows Server 2022.
   - 25 estaciones cliente con Windows 11 Pro.
   - Dominio Active Directory para gestión centralizada.
   - GPO (Group Policy Objects) para aplicar restricciones.

7. ESTRATEGIA DE ADMINISTRACIÓN DE RECURSOS
────────────────────────────────────────────
   CPU:          Round Robin para equidad entre 25 sesiones de usuario.
                 Priorización manual para procesos críticos (RDP, AD).
   Memoria:      Particiones variables + memoria virtual con archivo
                 de paginación de 32 GB en SSD.
   Almacenamiento: RAID 1 (espejo) para OS. RAID 5 para datos.
                   Backups automáticos diarios a NAS externo.
   Red:          QoS (Quality of Service) para priorizar tráfico de
                 videoconferencias sobre navegación web general.
   Monitoreo:    Windows Admin Center + Performance Monitor + scripts
                 Python de monitoreo (como este sistema).

═══════════════════════════════════════════════════════════════
                    FIN DEL REPORTE
═══════════════════════════════════════════════════════════════
```

4. `print(reporte)`
5. `guardar = input("\n¿Desea guardar este reporte en archivo? (s/n): ").strip().lower()`
6. Si `guardar == 's'`:
   - `timestamp_archivo = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')`
   - `nombre_archivo = f"reporte_organizacional_{timestamp_archivo}.txt"`
   - Abrir y escribir `reporte` en UTF-8
   - `print(f"✓ Reporte guardado en: {nombre_archivo}")`
7. `registrar_bitacora("reporte_organizacional", "Generado exitosamente")`

---

### Función: `menu_informacion() -> None`

Submenú del Módulo 1:
```
1. Ver información completa del sistema (ver + systeminfo + hostname + whoami)
2. Ver solo hostname y usuario activo
0. Volver al menú principal
```
Opción 2: solo ejecutar hostname y whoami, mostrar formato reducido.

---

## ARCHIVO 6: `main.py`

### Imports
```python
import os
import sys
from modulo_archivos   import menu_archivos, registrar_bitacora
from modulo_procesos   import menu_procesos
from modulo_cpu        import menu_cpu
from modulo_memoria    import menu_memoria
from modulo_reportes   import informacion_sistema, monitoreo_es, generar_reporte_organizacional
```

---

### Función: `limpiar_pantalla() -> None`
```python
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
```

---

### Función: `mostrar_banner() -> None`
```python
def mostrar_banner():
    try:
        usuario = os.getlogin()
    except:
        usuario = os.environ.get('USERNAME', 'N/A')
    print("╔══════════════════════════════════════════════════════╗")
    print("║    TECHSOLUTIONS CHILE LTDA.                        ║")
    print("║    Sistema de Administración y Monitoreo v1.0       ║")
    print(f"║    Usuario: {usuario:<20} Sistema: {os.name.upper():<6} ║")
    print("╚══════════════════════════════════════════════════════╝")
```

---

### Función: `menu_principal() -> None`

**Estructura: bucle `while True`**

```python
def menu_principal():
    while True:
        limpiar_pantalla()
        mostrar_banner()
        print("""
╔══════════════════════════════════════╗
║         MENÚ PRINCIPAL               ║
╠══════════════════════════════════════╣
║ 1. Información del Sistema           ║
║ 2. Gestión de Archivos y Directorios ║
║ 3. Gestión de Procesos               ║
║ 4. Planificación de CPU              ║
║ 5. Gestión de Memoria                ║
║ 6. Monitoreo de Entrada/Salida       ║
║ 7. Generar Reporte Organizacional    ║
║ 8. Salir                             ║
╚══════════════════════════════════════╝""")
        opcion = input("  Seleccione una opción [0-8]: ").strip()
        
        if   opcion == '1': informacion_sistema()
        elif opcion == '2': menu_archivos()
        elif opcion == '3': menu_procesos()
        elif opcion == '4': menu_cpu()
        elif opcion == '5': menu_memoria()
        elif opcion == '6': monitoreo_es()
        elif opcion == '7': generar_reporte_organizacional()
        elif opcion == '8':
            print("\n  ¡Hasta luego! Sistema cerrado correctamente.")
            registrar_bitacora("sistema", "Cierre normal del programa")
            sys.exit(0)
        else:
            print("  ⚠ Opción inválida. Intente nuevamente.")
        
        input("\n  Presione Enter para continuar...")
```

---

### Función: `main() -> None`
```python
def main():
    registrar_bitacora("sistema", "Inicio del programa")
    menu_principal()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  ⚠ Programa interrumpido por el usuario (Ctrl+C).")
        registrar_bitacora("sistema", "Interrupción por teclado")
        sys.exit(0)
```

---

## CHECKLIST DE COBERTURA — PUNTAJE 100%

### Módulos vs Resultados de Aprendizaje

| Requisito del Lab | Archivo | ¿Cubierto? |
|---|---|---|
| Comando `ver` | `modulo_reportes.py` → `informacion_sistema()` | ✅ |
| Comando `systeminfo` | `modulo_reportes.py` → `informacion_sistema()` | ✅ |
| Comando `hostname` | `modulo_reportes.py` → `informacion_sistema()` | ✅ |
| Comando `whoami` | `modulo_reportes.py` → `informacion_sistema()` | ✅ |
| mkdir, rmdir, dir, copy, move, rename, del, echo > | `modulo_archivos.py` | ✅ |
| `bitacora.txt` con fecha, hora, usuario, op, resultado | `modulo_archivos.py` → `registrar_bitacora()` | ✅ |
| tasklist con PID, nombre, memoria | `modulo_procesos.py` → `listar_procesos()` | ✅ |
| Búsqueda de procesos por nombre | `modulo_procesos.py` → `buscar_proceso()` | ✅ |
| taskkill para finalizar procesos | `modulo_procesos.py` → `finalizar_proceso()` | ✅ |
| FCFS con espera, retorno, promedio | `modulo_cpu.py` → `fcfs()` | ✅ |
| SJF con espera, retorno, promedio | `modulo_cpu.py` → `sjf()` | ✅ |
| Round Robin con quantum configurable | `modulo_cpu.py` → `round_robin()` | ✅ |
| Comparación de algoritmos | `modulo_cpu.py` → `comparar_algoritmos()` | ✅ |
| psutil memoria total/usada/libre/% | `modulo_memoria.py` → `mostrar_memoria_real()` | ✅ |
| Simulación particiones fijas | `modulo_memoria.py` → `simular_particiones_fijas()` | ✅ |
| Simulación particiones variables | `modulo_memoria.py` → `simular_particiones_variables()` | ✅ |
| psutil.disk_usage() por unidades | `modulo_reportes.py` → `monitoreo_es()` | ✅ |
| Reporte organizacional 25 usuarios | `modulo_reportes.py` → `generar_reporte_organizacional()` | ✅ |
| Manejo de errores (permisos, no existe, inválido) | Todos los módulos | ✅ |
| Menú principal con 8 opciones | `main.py` | ✅ |
| Modularización en 6 archivos .py | Toda la estructura | ✅ |
| Uso de `os`, `subprocess`, `psutil` | Todos los módulos | ✅ |

---

## NOTAS CRÍTICAS PARA EL IDE

1. **Orden de creación de archivos:** `modulo_archivos.py` PRIMERO. `main.py` ÚLTIMO.
2. **Encoding subprocess:** SIEMPRE `encoding='cp850', errors='replace'` en Windows.
3. **Encoding archivos:** SIEMPRE `encoding='utf-8'` al escribir/leer archivos propios.
4. **psutil.process_iter:** Pasar SIEMPRE lista de atributos como parámetro. Envolver en `try/except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess)`.
5. **os.getlogin():** Puede fallar en algunos entornos Windows; siempre usar fallback `os.environ.get('USERNAME', 'Desconocido')`.
6. **bitacora.txt:** Se crea automáticamente en el directorio de trabajo al primer uso. No crear manualmente.
7. **validar_entero():** Definida en `modulo_archivos.py`, importar desde allí en todos los módulos que la necesiten.
8. **Comandos MS-DOS con rutas con espacios:** SIEMPRE envolver rutas en comillas dobles: `f'mkdir "{nombre}"'`.
