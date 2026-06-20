import os
import subprocess
import datetime
import psutil
from modulo_archivos import registrar_bitacora

def informacion_sistema() -> None:
    res_ver  = subprocess.run('ver',        shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    res_sys  = subprocess.run('systeminfo', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    res_host = subprocess.run('hostname',   shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    res_who  = subprocess.run('whoami',     shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    
    campos = {'so': '', 'version': '', 'arquitectura': ''}
    for linea in res_sys.stdout.split('\n'):
        if 'Nombre del SO' in linea or 'OS Name' in linea:
            campos['so'] = linea.split(':', 1)[1].strip()
        elif 'Versión del SO' in linea or 'OS Version' in linea:
            campos['version'] = linea.split(':', 1)[1].strip()
        elif 'Tipo de sistema' in linea or 'System Type' in linea:
            campos['arquitectura'] = linea.split(':', 1)[1].strip()
            
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║     MÓDULO 1: INFORMACIÓN DEL SISTEMA OPERATIVO      ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  Sistema Operativo:  {campos['so']:<31} ║")
    print(f"║  Versión:            {campos['version']:<31} ║")
    print(f"║  Arquitectura:       {campos['arquitectura']:<31} ║")
    print(f"║  Nombre del equipo:  {res_host.stdout.strip():<31} ║")
    print(f"║  Usuario activo:     {res_who.stdout.strip():<31} ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  Salida de VER:      {res_ver.stdout.strip():<31} ║")
    print("╚══════════════════════════════════════════════════════╝")
    
    print("\n--- Salida completa de SYSTEMINFO ---")
    lineas_sys = res_sys.stdout.split('\n')
    for linea in lineas_sys[:25]:
        print(linea)
        
    registrar_bitacora("informacion_sistema", f"SO: {campos['so']}")

def monitoreo_es() -> None:
    res_wmic = subprocess.run('wmic logicaldisk get caption,description,freespace,size', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
    particiones = psutil.disk_partitions(all=False)
    
    print(f"\n{'Unidad':<10} {'FS':^8} {'Total(GB)':>12} {'Usado(GB)':>12} {'Libre(GB)':>12} {'Uso%':>7}")
    print("-" * 65)
    
    for part in particiones:
        try:
            uso = psutil.disk_usage(part.mountpoint)
            total_gb = uso.total / (1024**3)
            used_gb = uso.used / (1024**3)
            free_gb = uso.free / (1024**3)
            print(f"{part.device:<10} {part.fstype:^8} {total_gb:>12.2f} {used_gb:>12.2f} {free_gb:>12.2f} {uso.percent:>6.1f}%")
        except PermissionError:
            continue
            
    print("\n--- Salida de WMIC (MS-DOS) ---")
    print(res_wmic.stdout.strip())
    
    registrar_bitacora("monitoreo_es", f"{len(particiones)} unidades encontradas")

def generar_reporte_organizacional() -> None:
    try:
        usuario = os.getlogin()
    except:
        usuario = os.environ.get('USERNAME', 'N/A')
        
    fecha = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporte = f"""
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
"""
    print(reporte)
    guardar = input("\n¿Desea guardar este reporte en archivo? (s/n): ").strip().lower()
    if guardar == 's':
        timestamp_archivo = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"reporte_organizacional_{timestamp_archivo}.txt"
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(reporte)
        print(f"✓ Reporte guardado en: {nombre_archivo}")
        
    registrar_bitacora("reporte_organizacional", "Generado exitosamente")

def menu_informacion() -> None:
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║ MÓDULO 1: INFORMACIÓN DEL SISTEMA    ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. Ver información completa          ║")
        print("║ 2. Ver solo hostname y usuario       ║")
        print("║ 0. Volver al menú principal          ║")
        print("╚══════════════════════════════════════╝")
        
        op = input("Seleccione una opción: ").strip()
        
        if op == '1':
            informacion_sistema()
        elif op == '2':
            res_host = subprocess.run('hostname', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
            res_who  = subprocess.run('whoami', shell=True, capture_output=True, text=True, encoding='cp850', errors='replace')
            print(f"\n  Nombre del equipo: {res_host.stdout.strip()}")
            print(f"  Usuario activo:    {res_who.stdout.strip()}")
            registrar_bitacora("informacion_sistema_reducida", "Ejecutado")
        elif op == '0':
            break
        else:
            print("⚠ Opción inválida.")
            
        input("\nPresione Enter para continuar...")
