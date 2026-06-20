import os
import subprocess
import datetime
import shutil

def registrar_bitacora(operacion: str, resultado: str) -> None:
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        usuario = os.getlogin()
    except:
        usuario = os.environ.get('USERNAME', 'Desconocido')
    linea = f"[{timestamp}] | Usuario: {usuario} | Operación: {operacion} | Resultado: {resultado}\n"
    try:
        with open("bitacora.txt", 'a', encoding='utf-8') as f:
            f.write(linea)
    except OSError:
        print("⚠ Advertencia: No se pudo escribir en la bitácora.")

def validar_entero(prompt: str, minimo: int = 1, maximo: int = 9999) -> int:
    while True:
        try:
            valor = int(input(prompt))
            if minimo <= valor <= maximo:
                return valor
            print(f"⚠ Ingrese un valor entre {minimo} y {maximo}")
        except ValueError:
            print("⚠ Ingrese un número entero válido.")

def crear_directorio() -> None:
    nombre = input("Ingrese nombre del directorio a crear: ").strip()
    if not nombre:
        print("⚠ Nombre inválido.")
        return
    res = subprocess.run(f'mkdir "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    if res.returncode == 0:
        print(f"✓ Directorio '{nombre}' creado exitosamente.")
        registrar_bitacora(f"mkdir {nombre}", "Éxito")
    elif 'ya existe' in res.stderr.lower() or 'already exists' in res.stderr.lower():
        print("⚠ El directorio ya existe.")
        registrar_bitacora(f"mkdir {nombre}", "Error: ya existe")
    else:
        print(f"✗ Error: {res.stderr.strip()}")
        registrar_bitacora(f"mkdir {nombre}", f"Error: {res.stderr.strip()}")

def eliminar_directorio() -> None:
    nombre = input("Ingrese nombre del directorio a eliminar: ").strip()
    if not os.path.isdir(nombre):
        print("⚠ El directorio no existe.")
        registrar_bitacora(f"rmdir {nombre}", "Error: no existe")
        return
    confirm = input(f"¿Eliminar '{nombre}' y todo su contenido? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operación cancelada.")
        return
    res = subprocess.run(f'rmdir /s /q "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    if res.returncode == 0:
        print(f"✓ Directorio '{nombre}' eliminado exitosamente.")
        registrar_bitacora(f"rmdir {nombre}", "Éxito")
    else:
        print(f"✗ Error: {res.stderr.strip()}")
        registrar_bitacora(f"rmdir {nombre}", f"Error: {res.stderr.strip()}")

def crear_archivo() -> None:
    nombre = input("Ingrese nombre del archivo (con extensión, ej: datos.txt): ").strip()
    if not nombre:
        print("⚠ Nombre inválido.")
        return
    contenido = input("Ingrese contenido inicial (Enter para archivo vacío): ")
    if not contenido:
        res = subprocess.run(f'type nul > "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    else:
        res = subprocess.run(f'echo {contenido} > "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    
    if os.path.exists(nombre):
        print(f"✓ Archivo '{nombre}' creado exitosamente.")
        registrar_bitacora(f"crear_archivo {nombre}", "Éxito")
    else:
        print("✗ Error al crear archivo.")
        registrar_bitacora(f"crear_archivo {nombre}", "Error")

def listar_contenido() -> None:
    ruta = input("Ingrese ruta a listar (Enter = directorio actual): ").strip()
    if not ruta:
        ruta = os.getcwd()
    if not os.path.exists(ruta):
        print("⚠ Ruta no existe.")
        return
    subprocess.run(f'dir "{ruta}"', shell=True, text=True, encoding='cp850', errors='replace')
    registrar_bitacora(f"dir {ruta}", "Ejecutado")

def copiar_archivo() -> None:
    origen = input("Ruta del archivo origen: ").strip()
    if not os.path.exists(origen):
        print("⚠ Archivo origen no encontrado.")
        registrar_bitacora(f"copiar {origen}", "Error: no encontrado")
        return
    destino = input("Ruta de destino: ").strip()
    res = subprocess.run(f'copy "{origen}" "{destino}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    if res.returncode == 0:
        print(f"✓ Archivo copiado a '{destino}'")
        registrar_bitacora(f"copiar {origen} a {destino}", "Éxito")
    else:
        print(f"✗ Error: {res.stderr.strip()}")
        registrar_bitacora(f"copiar {origen} a {destino}", f"Error: {res.stderr.strip()}")

def mover_archivo() -> None:
    origen = input("Ruta del archivo origen: ").strip()
    if not os.path.exists(origen):
        print("⚠ Archivo origen no encontrado.")
        registrar_bitacora(f"mover {origen}", "Error: no encontrado")
        return
    destino = input("Ruta de destino: ").strip()
    res = subprocess.run(f'move "{origen}" "{destino}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    if res.returncode == 0:
        print(f"✓ Archivo movido a '{destino}'")
        registrar_bitacora(f"mover {origen} a {destino}", "Éxito")
    else:
        print(f"✗ Error: {res.stderr.strip()}")
        registrar_bitacora(f"mover {origen} a {destino}", f"Error: {res.stderr.strip()}")

def renombrar_archivo() -> None:
    actual = input("Nombre actual del archivo: ").strip()
    if not os.path.exists(actual):
        print("⚠ Archivo no encontrado.")
        registrar_bitacora(f"renombrar {actual}", "Error: no encontrado")
        return
    nuevo = input("Nuevo nombre: ").strip()
    res = subprocess.run(f'rename "{actual}" "{nuevo}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    if res.returncode == 0:
        print(f"✓ Archivo renombrado a '{nuevo}'")
        registrar_bitacora(f"renombrar {actual} a {nuevo}", "Éxito")
    else:
        print(f"✗ Error: {res.stderr.strip()}")
        registrar_bitacora(f"renombrar {actual} a {nuevo}", f"Error: {res.stderr.strip()}")

def eliminar_archivo() -> None:
    nombre = input("Ingrese nombre del archivo a eliminar: ").strip()
    if not os.path.exists(nombre):
        print("⚠ Archivo no encontrado.")
        registrar_bitacora(f"eliminar {nombre}", "Error: no encontrado")
        return
    confirm = input(f"¿Eliminar '{nombre}'? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operación cancelada.")
        return
    res = subprocess.run(f'del "{nombre}"', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    if not os.path.exists(nombre):
        print(f"✓ Archivo '{nombre}' eliminado exitosamente.")
        registrar_bitacora(f"eliminar {nombre}", "Éxito")
    else:
        print(f"✗ Error: {res.stderr.strip()}")
        registrar_bitacora(f"eliminar {nombre}", f"Error: {res.stderr.strip()}")

def menu_archivos() -> None:
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║     MÓDULO 2: GESTIÓN DE ARCHIVOS    ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. Crear directorio                  ║")
        print("║ 2. Eliminar directorio               ║")
        print("║ 3. Crear archivo                     ║")
        print("║ 4. Listar contenido                  ║")
        print("║ 5. Copiar archivo                    ║")
        print("║ 6. Mover archivo                     ║")
        print("║ 7. Renombrar archivo                 ║")
        print("║ 8. Eliminar archivo                  ║")
        print("║ 0. Volver al menú principal          ║")
        print("╚══════════════════════════════════════╝")
        
        try:
            op = input("Seleccione una opción: ").strip()
        except ValueError:
            print("⚠ Opción inválida.")
            continue
            
        if op == '1':
            crear_directorio()
        elif op == '2':
            eliminar_directorio()
        elif op == '3':
            crear_archivo()
        elif op == '4':
            listar_contenido()
        elif op == '5':
            copiar_archivo()
        elif op == '6':
            mover_archivo()
        elif op == '7':
            renombrar_archivo()
        elif op == '8':
            eliminar_archivo()
        elif op == '0':
            break
        else:
            print("⚠ Opción inválida.")
            
        input("\nPresione Enter para continuar...")
