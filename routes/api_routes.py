from flask import Blueprint, request, jsonify
from services.auth_service import validar_acceso
from data.memory_db import usuarios, logs
from models.evento_acceso import EventoAcceso
from datetime import datetime
from repositories.usuario_repository import UsuarioRepository

api = Blueprint("api", __name__)
repo = UsuarioRepository()

@api.route("/acceso", methods=["POST"])
def acceso():
    try:
        # Obtener datos del request
        data = request.json
        if not data:
            return jsonify({"error": "Datos inválidos"}), 400

        usuario_id = data.get("usuario_id")
        metodo = data.get("metodo")
        
        # Validar que vengan los datos requeridos
        if not usuario_id or not metodo:
            return jsonify({"error": "Usuario y método requeridos"}), 400

        # Validar acceso del usuario
        permitido, estado = validar_acceso(usuario_id, usuarios)

        # Registrar el evento
        log = EventoAcceso(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            usuario_id,
            metodo,
            "Vestíbulo Principal",
            estado
        )

        logs.append(log.to_dict())

        return jsonify(log.to_dict()), 200
        
    except Exception as e:
        print(f"Error en acceso: {e}")
        return jsonify({"error": "Error procesando acceso"}), 500


@api.route("/logs", methods=["GET"])
def obtener_logs():
    try:
        return jsonify(logs), 200
    except Exception as e:
        print(f"Error obteniendo logs: {e}")
        return jsonify({"error": "Error obteniendo logs"}), 500


def obtener_siguiente_id():
    try:
        return str(max(int(key) for key in usuarios.keys()) + 1)
    except ValueError:
        return "1"


@api.route("/api/usuarios", methods=["GET"])
def obtener_usuarios():
    try:
        return jsonify(repo.obtener_todos()), 200
    except Exception as e:
        print(f"Error obteniendo usuarios: {e}")
        return jsonify({"error": "Error obteniendo usuarios"}), 500


@api.route("/api/usuarios", methods=["POST"])
def crear_usuario():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

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
            return jsonify({"error": "Nombre y RUT son obligatorios"}), 400

        metodo_normalizado = normalizar_metodo(metodo)
        if not metodo_normalizado:
            return jsonify({"error": "Método de acceso no válido"}), 400

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
            "activo": True
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
            "placeholder": False
        })

        return jsonify({"success": True, "usuario": nuevo_usuario}), 201

    except Exception as e:
        print(f"Error creando usuario: {e}")
        return jsonify({"error": "Error creando usuario"}), 500


@api.route("/api/estado_sistema", methods=["GET"])
def obtener_estado_sistema():
    try:
        # Contar accesos
        accesos_totales = len(logs)
        accesos_permitidos = sum(
            1 for log in logs 
            if log.get("estado") == "activo"
        )
        accesos_denegados = accesos_totales - accesos_permitidos

        # Contar métodos disponibles
        metodos = {}
        for usuario in repo.obtener_todos():
            metodo = usuario.get("metodo", "Desconocido")
            metodos[metodo] = metodos.get(metodo, 0) + 1

        return jsonify({
            "total_usuarios": repo.total_usuarios(),
            "personas_dentro": repo.total_activos(),
            "accesos_hoy": accesos_totales,
            "entradas": accesos_permitidos,
            "salidas": accesos_denegados,
            "alertas": accesos_denegados,
            "metodos": metodos,
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo estado: {e}")
        return jsonify({"error": "Error obteniendo estado"}), 500




def normalizar_metodo(metodo_input):
    """Convierte el método de acceso a formato estándar."""
    if not metodo_input:
        return None

    metodo_lower = metodo_input.lower()

    if "qr" in metodo_lower:
        return "Código QR"

    elif "tarjeta" in metodo_lower or "card" in metodo_lower or "rfid" in metodo_lower:
        return "Tarjeta RFID"
    elif "huella" in metodo_lower or "finger" in metodo_lower:
        return "Huella Digital"

    return None


@api.route("/auditoria_datos")
def auditoria_datos():
    try:
        resultado = []

        for log in logs:
            # Buscar datos del usuario
            usuario = repo.obtener_por_id(log.get("usuario_id"))
            if usuario is None:
                usuario = {}

            resultado.append({
                "fecha": log.get("fecha"),
                "usuario_id": log.get("usuario_id"),
                "nombre": usuario.get("nombre", "Desconocido"),
                "rol": usuario.get("rol", "Sin Rol"),
                "metodo": log.get("metodo"),
                "ubicacion": log.get("ubicacion"),
                "estado": log.get("estado"),
                "placeholder": bool(log.get("placeholder") or usuario.get("placeholder"))
            })

        return jsonify(resultado), 200
        
    except Exception as e:
        print(f"Error obteniendo auditoría: {e}")
        return jsonify({"error": "Error obteniendo auditoría"}), 500
