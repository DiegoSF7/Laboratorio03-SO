import os
import sys
from modulo_archivos   import menu_archivos, registrar_bitacora
from modulo_procesos   import menu_procesos
from modulo_cpu        import menu_cpu
from modulo_memoria    import menu_memoria
from modulo_reportes   import informacion_sistema, monitoreo_es, generar_reporte_organizacional

def limpiar_pantalla() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner() -> None:
    try:
        usuario = os.getlogin()
    except:
        usuario = os.environ.get('USERNAME', 'N/A')
    print("╔══════════════════════════════════════════════════════╗")
    print("║    TECHSOLUTIONS CHILE LTDA.                        ║")
    print("║    Sistema de Administración y Monitoreo v1.0       ║")
    print(f"║    Usuario: {usuario:<20} Sistema: {os.name.upper():<6} ║")
    print("╚══════════════════════════════════════════════════════╝")

def menu_principal() -> None:
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

def main() -> None:
    registrar_bitacora("sistema", "Inicio del programa")
    menu_principal()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  ⚠ Programa interrumpido por el usuario (Ctrl+C).")
        registrar_bitacora("sistema", "Interrupción por teclado")
        sys.exit(0)
