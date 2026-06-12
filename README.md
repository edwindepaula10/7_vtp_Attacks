# VTP VLAN Manipulation Attacks

**Autor:** Edwin (Matrícula: 2024-2415)  
**Institución:** Instituto Tecnológico de las Américas (ITLA)  
**Curso:** Seguridad de Redes
**Fecha:** 12 de Junio de 2026

---

## Descripción General

Este repositorio contiene scripts y documentación técnica para demostrar vulnerabilidades en el protocolo VTP (VLAN Trunking Protocol) de Cisco. Se incluyen ataques de manipulación de VLAN mediante inyección de Subset Advertisements falsos.

**Ataques demostrados:**
- Agregar una VLAN no autorizada al dominio VTP
- Borrar una VLAN existente del dominio VTP

---

## Objetivo del Laboratorio

Demostrar las vulnerabilidades inherentes del protocolo VTP v1 en equipos Cisco:

1. VTP confía ciegamente en el número de revisión sin validar origen
2. No existe validación de autenticidad del origen del paquete
3. Los cambios se propagan automáticamente a toda la red
4. Un único paquete malicioso puede afectar la infraestructura completa

---

## Videos Demostrativos

**Video:** Demostración práctica de ataques VTP (Agregar y Borrar VLAN)

[Ver en YouTube](https://youtube.com/watch?v=XXXXX)  
Duración: 5 minutos  
Contenido: Topología, explicación, ejecución del ataque, análisis de resultados

*Nota: Reemplazar XXXXX con el ID del video de YouTube después de subir*

---

## Requisitos

### Software
- Python 3.7 o superior
- Linux (Parrot OS, Kali, Ubuntu, etc.)
- Scapy 2.4 o superior

### Hardware
- Interfaz de red conectada a un puerto trunk VTP
- Acceso a switches Cisco con VTP configurado

### Instalación de dependencias

```bash
sudo apt update
sudo apt install python3-scapy -y
```

Verificar instalación:
```bash
python3 -c "from scapy.all import *; print('Scapy OK')"
```

---

## Estructura del Repositorio

```
vtp-vlan-manipulation-attacks/
├── vtp_attacks_interactive.py          Script principal (interactivo)
├── VTP_VLAN_Attacks_Documentation.md   Documentación técnica completa
├── README.md                           Este archivo
└── videos/
    ├── vtp_attack_demo.mp4             Video demostrativo (5 min)
    └── README.md                       Descripción de videos
```

---

## Uso Rápido

### Instalación

```bash
git clone https://github.com/edwinxxx/vtp-vlan-manipulation-attacks.git
cd vtp-vlan-manipulation-attacks
pip install -r requirements.txt
```

### Ejecución

```bash
sudo python3 vtp_attacks_interactive.py
```

El script presentará un menú interactivo:

```
[1] AGREGAR VLAN
    Inyecta una VLAN nueva en el dominio VTP

[2] BORRAR VLAN
    Elimina una VLAN existente del dominio VTP

[0] Salir
```

Selecciona una opción y sigue las instrucciones para configurar los parámetros del ataque.

---

## Documentación Técnica

Ver archivo completo: `VTP_VLAN_Attacks_Documentation.md`

Contiene:
- Fundamentos técnicos de VTP
- Estructura detallada de Subset Advertisements
- Documentación de red (topología, direccionamiento, VLANs)
- Pasos de ejecución con ejemplos
- Capturas de pantalla y logs
- Contra-medidas y mitigaciones

---

## Parámetros Configurables

El script permite personalizar los siguientes parámetros:

```
Dominio VTP              [ITLA-NET]
Interfaz de red          [ens33]
Revisión VTP             [2147483647]
VLAN ID (agregar)        [50]
Nombre VLAN (agregar)    [VLAN_ESTUDIANTES_2024]
VLAN ID (borrar)         [15]
Nombre VLAN (borrar)     [VLAN_USERS]
```

Todos los valores tienen defaults. Presionar ENTER usa el valor sugerido.

---

## Fundamentos Técnicos

### Protocolo VTP

VTP es un protocolo propietario de Cisco que sincroniza automáticamente la configuración de VLANs entre switches en el mismo dominio.

**Tipos de anuncios VTP:**

| Tipo | Código | Descripción |
|------|--------|-------------|
| Summary Advertisement | 0x01 | Anuncia la revisión actual del dominio |
| Subset Advertisement | 0x02 | Contiene la lista completa o parcial de VLANs |
| Advertisement Request | 0x03 | Solicitud de información completa del dominio |

### Mecanismo de Aceptación

Los switches aceptan actualizaciones basándose en el Configuration Revision Number:

```
Si (revision_recibida > revision_local):
    Aplicar cambios de VLAN
    Actualizar revision_local
Else:
    Descartar anuncio
```

**Vulnerabilidad:** No existe validación de origen legítimo; solo se valida el número de revisión.

### Flujo del Ataque

1. Construir Subset Advertisement con revisión muy alta
2. Incluir VLAN a agregar/borrar en el TLV
3. Encapsular en LLC/SNAP y Ethernet
4. Enviar a dirección MAC multicast VTP (01:00:0c:cc:cc:cc)
5. Switch recibe, detecta revisión más alta
6. Switch aplica cambios (si no hay validación MD5)

---

## Contra-Medidas

### Nivel 1: VTP Password (Recomendado)

```cisco
SW(config)# vtp password MiContrasena
```

Obliga al atacante a conocer la contraseña para forjar paquetes válidos.

**Efectividad:** Alta  
**Complejidad:** Baja

### Nivel 2: VTP Version 3

```cisco
SW(config)# vtp version 3
```

Añade autenticación mejorada y Primary Server designado.

**Efectividad:** Muy alta  
**Complejidad:** Media

### Nivel 3: VTP Transparent Mode

```cisco
SW(config)# vtp mode transparent
```

Aislamiento local; cambios no se propagan.

**Efectividad:** Alta (aislamiento local)  
**Complejidad:** Baja

### Nivel 4: DTP Disable

```cisco
SW(config-if)# switchport nonegotiate
```

Desactiva negotiación automática de trunks.

**Efectividad:** Alta (previene negotiation)  
**Complejidad:** Muy baja

### Nivel 5: Port Security

```cisco
SW(config-if)# switchport mode access
```

Previene que un puerto access sea convertido a trunk.

**Efectividad:** Alta (previene acceso)  
**Complejidad:** Baja

---

## Topología del Laboratorio

```
┌─────────────────┐
│   PARROT OS     │
│ 172.24.15.129   │ Atacante
└────────┬────────┘
         │ (trunk Et0/2)
┌────────▼────────┐         ┌──────────────┐
│  SW-ACCESO      │ Et0/1──┤  SW-CORE     │
│  172.24.15.15   │────────┤  172.24.15.24│
└─────────────────┘         └──────────────┘

VTP Domain: ITLA-NET
VLANs: 1 (default), 15 (VLAN_USERS), 24 (VLAN_MGMT)
Native VLAN: 24 (SW-ACCESO Et0/2)
```

---

## Impacto

### Agregar VLAN
- Los atacantes pueden crear VLANs para acceder a cualquier parte de la red
- Riesgo de robo de información
- Acceso no autorizado a recursos

### Borrar VLAN
- Interrupción de servicio para todos los usuarios en esa VLAN
- Downtime a nivel de dominio
- Impacto propagado automáticamente a todos los switches

---

## Limitaciones Conocidas

- MD5 Validation: Si está habilitada, rechaza paquetes con MD5 incorrecto
- VTP Password: Hace imposible forjar paquetes sin conocer la contraseña
- VTP Version 3: Implementa autenticación más robusta
- El script requiere acceso a un puerto trunk

---

## Referencias

- Cisco VTP (VLAN Trunking Protocol) Documentation
- IEEE 802.1Q (VLAN Tagging Specification)
- RFC 3580 - Remote Authentication Dial In User Service (RADIUS)
- "VLAN Attacks" - Network Penetration Testing Frameworks
- Scapy Documentation: https://scapy.readthedocs.io/

---

## Notas Importantes

Este código es para fines educativos exclusivamente. Solo para uso en laboratorios autorizados de ITLA.

Prohibido usar en redes de producción o sin autorización explícita.

---

## Autor

Edwin  
Matrícula: 2024-2415  
Curso: Seguridad de Redes
Instituto Tecnológico de las Américas (ITLA)  

---

**Última actualización:** 12 de Junio de 2026
**Versión:** 1.0
