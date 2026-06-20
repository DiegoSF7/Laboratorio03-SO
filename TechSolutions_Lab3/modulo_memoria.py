import psutil
from modulo_archivos import registrar_bitacora, validar_entero

def mostrar_memoria_real() -> None:
    mem = psutil.virtual_memory()
    total_gb = round(mem.total / (1024**3), 2)
    used_gb = round(mem.used / (1024**3), 2)
    free_gb = round(mem.available / (1024**3), 2)
    porcentaje = mem.percent
    
    bloques = int(porcentaje / 5)
    barra = "█" * bloques + "░" * (20 - bloques)
    
    print("\n╔══════════════════════════════════════╗")
    print("║     MÓDULO 5: MEMORIA RAM REAL       ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  Total:      {total_gb:>6.2f} GB                 ║")
    print(f"║  Usada:      {used_gb:>6.2f} GB                 ║")
    print(f"║  Libre:      {free_gb:>6.2f} GB                 ║")
    print(f"║  Uso:        {porcentaje:>6.1f}%                   ║")
    print(f"║  [{barra}] {porcentaje:5.1f}%          ║")
    print("╚══════════════════════════════════════╝")
    
    registrar_bitacora("ver_memoria_real", f"Uso: {porcentaje}%")

def ingresar_procesos_memoria() -> tuple[int, list[dict]]:
    memoria_total = validar_entero("Ingrese memoria total para simulación (MB): ", 64, 65536)
    n = validar_entero("¿Cuántos procesos a cargar en memoria? ", 1, 20)
    procesos = []
    for i in range(n):
        nombre = input(f"Nombre proceso {i+1}: ").strip()
        if not nombre:
            nombre = f"P{i+1}"
        tamaño = validar_entero(f"Tamaño de {nombre} (MB): ", 1, memoria_total)
        procesos.append({'nombre': nombre, 'tamaño': tamaño})
    return (memoria_total, procesos)

def simular_particiones_fijas(memoria_total: int, procesos: list[dict]) -> None:
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

    print(f"\n{'Partición':<10} | {'Tamaño(MB)':<10} | {'Proceso':<15} | {'Ocupado(MB)':<12} | {'Libre(MB)':<10} | {'Frag.Interna':<12}")
    print("-" * 80)
    for p in particiones:
        proc_nombre = p['proceso'] if p['proceso'] else "--- Libre ---"
        libre = p['tamaño'] - p['tam_proceso'] if p['proceso'] else p['tamaño']
        frag = p['tamaño'] - p['tam_proceso'] if p['proceso'] else 0
        print(f"{p['id']:<10} | {p['tamaño']:<10} | {proc_nombre:<15} | {p['tam_proceso']:<12} | {libre:<10} | {frag:<12}")

    frag_total = sum(p['tamaño'] - p['tam_proceso'] for p in particiones if p['proceso'])
    print(f"\n  Fragmentación interna total: {frag_total} MB")
    if sin_asignar:
        print(f"  ✗ Sin partición disponible: {', '.join(sin_asignar)}")

def simular_particiones_variables(memoria_total: int, procesos: list[dict]) -> None:
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

    print(f"\n{'Inicio(MB)':>12} {'Tamaño(MB)':>12} {'Estado':^10} {'Proceso':^15}")
    print("-" * 52)
    for b in bloques:
        estado = "Libre" if b['libre'] else "Ocupado"
        proc_nombre = b['proceso'] if b['proceso'] else "---"
        print(f"{b['inicio']:>12} {b['tamaño']:>12} {estado:^10} {proc_nombre:^15}")

    bloques_libres = [b for b in bloques if b['libre']]
    frag_externa = sum(b['tamaño'] for b in bloques_libres)
    print(f"\n  Fragmentación externa: {frag_externa} MB en {len(bloques_libres)} bloque(s) libre(s)")
    print(f"  Nota: en particiones variables, la fragmentación externa")
    print(f"  puede compactarse moviendo procesos en memoria.")

def menu_memoria() -> None:
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║     MÓDULO 5: GESTIÓN DE MEMORIA     ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. Ver memoria RAM real del sistema  ║")
        print("║ 2. Simular particiones fijas         ║")
        print("║ 3. Simular particiones variables     ║")
        print("║ 0. Volver al menú principal          ║")
        print("╚══════════════════════════════════════╝")
        
        op = input("Seleccione una opción: ").strip()
        
        if op == '1':
            mostrar_memoria_real()
        elif op == '2':
            mem_tot, procs = ingresar_procesos_memoria()
            simular_particiones_fijas(mem_tot, procs)
        elif op == '3':
            mem_tot, procs = ingresar_procesos_memoria()
            simular_particiones_variables(mem_tot, procs)
        elif op == '0':
            break
        else:
            print("⚠ Opción inválida.")
            
        input("\nPresione Enter para continuar...")
