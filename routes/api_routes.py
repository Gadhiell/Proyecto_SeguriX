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

    data = request.json

    usuario_id = data.get("usuario_id")
    metodo = data.get("metodo")

    permitido, estado = validar_acceso(
        usuario_id,
        usuarios
    )

    log = EventoAcceso(

        datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        ),

        usuario_id,

        metodo,

        "Vestíbulo Principal",

        estado

    )

    logs.append(
        log.to_dict()
    )

    return jsonify(
        log.to_dict()
    )


@api.route("/logs", methods=["GET"])
def obtener_logs():

    return jsonify(logs)


@api.route("/api/usuarios", methods=["GET"])
def obtener_usuarios():

    return jsonify(
        repo.obtener_todos()
    )


@api.route("/api/estado_sistema", methods=["GET"])
def obtener_estado_sistema():

    accesos_totales = len(logs)
    accesos_permitidos = sum(
        1
        for log in logs
        if log["estado"] == "activo"
    )
    accesos_denegados = accesos_totales - accesos_permitidos

    # Contar métodos desde usuarios registrados (refleja tipos de credenciales activas)
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
    })


@api.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():

    nombre = request.form.get("nombre", "").strip()
    rut = request.form.get("rut", "").strip()
    empresa = request.form.get("empresa", "").strip()
    email = request.form.get("email", "").strip()
    rol = request.form.get("rol", "Empleado").strip()
    metodo = request.form.get("metodo", "").strip()
    credencial = request.form.get("credencial", "").strip()
    expiracion = request.form.get("expiracion", "").strip()
    zonas = request.form.get("zonas", "").strip()

    # Validaciones básicas
    if not nombre or not rut:
        return jsonify({"error": "Nombre y RUT requeridos"}), 400

    # Normalizar método
    metodo_normalizado = normalizar_metodo(metodo)
    if not metodo_normalizado:
        return jsonify({"error": "Método de acceso no válido"}), 400

    nuevo_id = str(
        len(usuarios) + 1
    )

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

    repo.agregar(
        nuevo_usuario
    )

    return """
    <script>
        window.location.href='/usuarios';
    </script>
    """


def normalizar_metodo(metodo_input):
    """Normaliza los valores de método de acceso."""
    if not metodo_input:
        return None

    metodo_lower = metodo_input.lower()

    if "qr" in metodo_lower:
        return "Código QR"
    elif "tarjeta" in metodo_lower or "card" in metodo_lower or "rfid" in metodo_lower:
        return "Tarjeta"
    elif "huella" in metodo_lower or "finger" in metodo_lower:
        return "Huella Digital"

    return None
@api.route("/auditoria_datos")
def auditoria_datos():

    resultado = []

    for log in logs:

        usuario = repo.obtener_por_id(
            log["usuario_id"]
        )

        if usuario is None:

            usuario = {}

        resultado.append({

            "fecha": log["fecha"],

            "usuario_id":
            log["usuario_id"],

            "nombre":
            usuario.get(
                "nombre",
                "Desconocido"
            ),

            "rol":
            usuario.get(
                "rol",
                "Sin Rol"
            ),

            "metodo":
            log["metodo"],

            "ubicacion":
            log["ubicacion"],

            "estado":
            log["estado"]

        })

    return jsonify(resultado)