import os
import subprocess
import psutil
from modulo_archivos import registrar_bitacora

def listar_procesos() -> None:
    res = subprocess.run('tasklist', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    lista = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            lista.append({
                'pid': p.info['pid'],
                'nombre': p.info['name'],
                'memoria_kb': p.info['memory_info'].rss // 1024
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    lista.sort(key=lambda x: x['memoria_kb'], reverse=True)
    
    print(f"{'PID':>8}  {'Nombre del Proceso':<35}  {'Memoria (KB)':>15}")
    print("-" * 62)
    for p in lista:
        print(f"{p['pid']:>8}  {p['nombre']:<35}  {p['memoria_kb']:>15,}")
        
    print(f"\nTotal: {len(lista)} procesos activos.")
    print("\n--- Salida de TASKLIST (MS-DOS) ---\n", res.stdout[:2000])
    registrar_bitacora("listar_procesos", f"{len(lista)} procesos encontrados")

def buscar_proceso() -> None:
    nombre_busqueda = input("Ingrese nombre del proceso a buscar (ej: chrome, notepad): ").strip().lower()
    if not nombre_busqueda:
        print("⚠ Ingrese un nombre.")
        return
        
    encontrados = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info', 'status']):
        try:
            if p.info['name'] and nombre_busqueda in p.info['name'].lower():
                encontrados.append({
                    'pid': p.info['pid'],
                    'nombre': p.info['name'],
                    'memoria_kb': p.info['memory_info'].rss // 1024,
                    'estado': p.info['status']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
            
    if not encontrados:
        print(f"⚠ No se encontraron procesos con '{nombre_busqueda}'.")
        registrar_bitacora(f"buscar_proceso {nombre_busqueda}", "0 encontrados")
        return
        
    print(f"{'PID':>8}  {'Nombre del Proceso':<35}  {'Memoria (KB)':>15}  {'Estado':<15}")
    print("-" * 79)
    for p in encontrados:
        print(f"{p['pid']:>8}  {p['nombre']:<35}  {p['memoria_kb']:>15,}  {p['estado']:<15}")
        
    registrar_bitacora(f"buscar_proceso {nombre_busqueda}", f"{len(encontrados)} encontrados")

def finalizar_proceso() -> None:
    objetivo = input("Ingrese PID (número) o nombre del proceso a finalizar: ").strip()
    try:
        pid = int(objetivo)
        modo = 'pid'
    except ValueError:
        modo = 'nombre'
        
    if modo == 'pid':
        cmd = f'taskkill /PID {objetivo} /F'
    else:
        cmd = f'taskkill /IM "{objetivo}" /F'
        
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    if res.returncode == 0:
        print("✓ Proceso finalizado exitosamente.")
    elif 'no encontr' in res.stderr.lower() or 'not found' in res.stderr.lower():
        print("⚠ Proceso no encontrado.")
    elif 'acceso denegado' in res.stderr.lower() or 'access denied' in res.stderr.lower():
        print("✗ Acceso denegado (proceso del sistema).")
    else:
        print(f"✗ Error: {res.stderr.strip()}")
        
    registrar_bitacora(f"taskkill {objetivo}", f"{'Éxito' if res.returncode == 0 else res.stderr.strip()}")

def menu_procesos() -> None:
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║     MÓDULO 3: GESTIÓN DE PROCESOS    ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. Listar todos los procesos activos ║")
        print("║ 2. Buscar proceso por nombre         ║")
        print("║ 3. Finalizar proceso                 ║")
        print("║ 0. Volver al menú principal          ║")
        print("╚══════════════════════════════════════╝")
        
        op = input("Seleccione una opción: ").strip()
        
        if op == '1':
            listar_procesos()
        elif op == '2':
            buscar_proceso()
        elif op == '3':
            finalizar_proceso()
        elif op == '0':
            break
        else:
            print("⚠ Opción inválida.")
            
        input("\nPresione Enter para continuar...")
