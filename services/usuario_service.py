from datetime import datetime

from data.memory_db import logs, usuarios
from repositories.usuario_repository import UsuarioRepository

repo = UsuarioRepository()


def obtener_siguiente_id():
    try:
        return str(max(int(key) for key in usuarios.keys()) + 1)
    except ValueError:
        return "1"


def normalizar_metodo(metodo_input):
    """Normaliza el método de acceso."""
    if not metodo_input:
        return None

    metodo_lower = str(metodo_input).lower()

    if "qr" in metodo_lower:
        return "Código QR"
    if "tarjeta" in metodo_lower or "card" in metodo_lower or "rfid" in metodo_lower:
        return "Tarjeta RFID"
    if "huella" in metodo_lower or "finger" in metodo_lower:
        return "Huella Digital"

    return None


def crear_usuario_desde_datos(data):
    nombre = data.get("nombre", "").strip()
    rut = data.get("rut", "").strip()
    empresa = data.get("empresa", "").strip()
    email = data.get("email", "").strip()
    rol = data.get("rol", "Empleado").strip()
    metodo = data.get("metodo", "").strip()
    credencial = data.get("credencial", "").strip()
    expiracion = data.get("expiracion", "").strip()
    zonas = data.get("zonas", "").strip()

    if not nombre or not rut:
        return None, "Nombre y RUT son obligatorios"

    metodo_normalizado = normalizar_metodo(metodo)
    if not metodo_normalizado:
        return None, "Método de acceso no válido"

    nuevo_id = obtener_siguiente_id()
    nuevo_usuario = {
        "id": nuevo_id,
        "nombre": nombre,
        "rut": rut,
        "empresa": empresa,
        "email": email,
        "rol": rol,
        "metodo": metodo_normalizado,
        "credencial": credencial,
        "expiracion": expiracion,
        "zonas": zonas,
        "activo": True,
    }

    repo.agregar(nuevo_usuario)
    logs.append({
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "usuario_id": nuevo_id,
        "nombre": nombre,
        "rol": rol,
        "metodo": metodo_normalizado,
        "ubicacion": "Registro de Usuario",
        "estado": "activo",
        "placeholder": False,
    })

    return nuevo_usuario, None


def obtener_estado_sistema():
    accesos_totales = len(logs)
    accesos_permitidos = sum(1 for log in logs if log.get("estado") == "activo")
    accesos_denegados = accesos_totales - accesos_permitidos

    metodos = {}
    for usuario in repo.obtener_todos():
        metodo = usuario.get("metodo", "Desconocido")
        metodos[metodo] = metodos.get(metodo, 0) + 1

    return {
        "total_usuarios": repo.total_usuarios(),
        "personas_dentro": repo.total_activos(),
        "accesos_hoy": accesos_totales,
        "entradas": accesos_permitidos,
        "salidas": accesos_denegados,
        "alertas": accesos_denegados,
        "metodos": metodos,
    }
