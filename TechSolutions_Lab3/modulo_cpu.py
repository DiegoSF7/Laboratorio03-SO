import os
from collections import deque
from modulo_archivos import registrar_bitacora, validar_entero

def ingresar_procesos() -> list[dict]:
    n = validar_entero("¿Cuántos procesos desea ingresar? ", minimo=1, maximo=20)
    procesos = []
    for i in range(n):
        nombre = input(f"Nombre proceso {i+1} (Enter = P{i+1}): ").strip()
        if not nombre:
            nombre = f"P{i+1}"
        burst = validar_entero(f"Tiempo de CPU (burst) de {nombre}: ", minimo=1, maximo=999)
        procesos.append({'nombre': nombre, 'burst': burst, 'id': i, 'arrival': 0})
        
    print("\nProcesos ingresados:")
    for p in procesos:
        print(f"  {p['nombre']}: burst={p['burst']}")
    return procesos

def fcfs(procesos: list[dict]) -> dict:
    tiempo_actual = 0
    resultados = []
    for p in procesos:
        inicio = tiempo_actual
        fin = inicio + p['burst']
        espera = inicio
        retorno = fin
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

def sjf(procesos: list[dict]) -> dict:
    ordenados = sorted(procesos, key=lambda x: x['burst'])
    resultado = fcfs(ordenados)
    resultado['algoritmo'] = 'SJF (Shortest Job First)'
    return resultado

def round_robin(procesos: list[dict], quantum: int) -> dict:
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
        retorno = fin
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

def mostrar_resultados(resultado: dict) -> None:
    print(f"\n{'='*60}")
    print(f"  RESULTADO: {resultado['algoritmo']}")
    print(f"{'='*60}")
    print(f"{'Proceso':<10} {'Burst':>7} {'Inicio':>8} {'Fin':>6} {'Espera':>8} {'Retorno':>9}")
    print("-" * 52)
    for r in resultado['resultados']:
        print(f"{r['nombre']:<10} {r['burst']:>7} {r.get('inicio', '-'):>8} {r['fin']:>6} {r['espera']:>8} {r['retorno']:>9}")
    print("-" * 52)
    print(f"  Promedio de espera:   {resultado['promedio_espera']:.2f} unidades de tiempo")
    print(f"  Promedio de retorno:  {resultado['promedio_retorno']:.2f} unidades de tiempo")
    if 'orden_ejecucion' in resultado:
        print(f"  Orden de ejecución: {' → '.join(resultado['orden_ejecucion'])}")

def comparar_algoritmos(r_fcfs: dict, r_sjf: dict, r_rr: dict) -> None:
    algoritmos = {
        r_fcfs['algoritmo']: r_fcfs['promedio_espera'],
        r_sjf['algoritmo']: r_sjf['promedio_espera'],
        r_rr['algoritmo']: r_rr['promedio_espera']
    }
    mejor = min(algoritmos, key=algoritmos.get)
    
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║            COMPARACIÓN DE ALGORITMOS DE CPU          ║")
    print("╠══════════════════════════╦═══════════╦═══════════════╣")
    print("║ Algoritmo                ║ Prom. Esp ║ Prom. Retorno ║")
    print("╠══════════════════════════╬═══════════╬═══════════════╣")
    print(f"║ {'FCFS':<24} ║ {r_fcfs['promedio_espera']:>9.2f} ║ {r_fcfs['promedio_retorno']:>13.2f} ║")
    print(f"║ {'SJF':<24} ║ {r_sjf['promedio_espera']:>9.2f} ║ {r_sjf['promedio_retorno']:>13.2f} ║")
    print(f"║ {r_rr['algoritmo']:<24} ║ {r_rr['promedio_espera']:>9.2f} ║ {r_rr['promedio_retorno']:>13.2f} ║")
    print("╚══════════════════════════╩═══════════╩═══════════════╝")
    
    print(f"\n  ★ MEJOR ALGORITMO: {mejor}")
    print(f"    Promedio de espera más bajo: {algoritmos[mejor]:.2f} unidades")
    
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
    registrar_bitacora("comparar_algoritmos", f"Mejor: {mejor} ({algoritmos[mejor]:.2f})")

def menu_cpu() -> None:
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║   MÓDULO 4: PLANIFICACIÓN DE CPU     ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. Simular FCFS                      ║")
        print("║ 2. Simular SJF (Shortest Job First)  ║")
        print("║ 3. Simular Round Robin               ║")
        print("║ 4. Comparar los 3 algoritmos         ║")
        print("║ 0. Volver al menú principal          ║")
        print("╚══════════════════════════════════════╝")
        
        op = input("Seleccione una opción: ").strip()
        
        if op == '1':
            procesos = ingresar_procesos()
            if procesos:
                mostrar_resultados(fcfs(procesos))
        elif op == '2':
            procesos = ingresar_procesos()
            if procesos:
                mostrar_resultados(sjf(procesos))
        elif op == '3':
            procesos = ingresar_procesos()
            if procesos:
                q = validar_entero("Ingrese quantum para Round Robin: ", 1, 100)
                mostrar_resultados(round_robin(procesos, q))
        elif op == '4':
            procesos = ingresar_procesos()
            if procesos:
                q = validar_entero("Ingrese quantum para Round Robin: ", 1, 100)
                r_fcfs = fcfs(procesos)
                r_sjf = sjf(procesos)
                r_rr = round_robin(procesos, q)
                mostrar_resultados(r_fcfs)
                mostrar_resultados(r_sjf)
                mostrar_resultados(r_rr)
                comparar_algoritmos(r_fcfs, r_sjf, r_rr)
        elif op == '0':
            break
        else:
            print("⚠ Opción inválida.")
            
        input("\nPresione Enter para continuar...")
