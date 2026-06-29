from datetime import datetime

from flask import Blueprint, jsonify, request

from data.memory_db import logs, usuarios
from models.evento_acceso import EventoAcceso
from repositories.usuario_repository import UsuarioRepository
from services.auth_service import validar_acceso
from services.usuario_service import crear_usuario_desde_datos, obtener_estado_sistema as obtener_estado_sistema_datos

api = Blueprint("api", __name__)
repo = UsuarioRepository()


@api.route("/acceso", methods=["POST"])
def acceso():
    try:
        #datos del request
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Datos inválidos"}), 400

        usuario_id = data.get("usuario_id")
        metodo = data.get("metodo")

        #valida que vengan datos
        if not usuario_id or not metodo:
            return jsonify({"error": "Usuario y método requeridos"}), 400

        #valida acceso con strategy
        _, estado = validar_acceso(usuario_id, usuarios, metodo)

        #registra el evento
        log = EventoAcceso(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            usuario_id,
            metodo,
            "Vestíbulo Principal",
            estado,
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

        usuario, error = crear_usuario_desde_datos(data)
        if error:
            return jsonify({"error": error}), 400

        return jsonify({"success": True, "usuario": usuario}), 201

    except Exception as e:
        print(f"Error creando usuario: {e}")
        return jsonify({"error": "Error creando usuario"}), 500


@api.route("/api/estado_sistema", methods=["GET"])
def obtener_estado_sistema():
    try:
        estado = obtener_estado_sistema_datos()
        return jsonify(estado), 200

    except Exception as e:
        print(f"Error obteniendo estado: {e}")
        return jsonify({"error": "Error obteniendo estado"}), 500


@api.route("/auditoria_datos")
def auditoria_datos():
    try:
        resultado = []

        for log in logs:
            #busca datos del usuario
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
                "placeholder": bool(log.get("placeholder") or usuario.get("placeholder")),
            })

        return jsonify(resultado), 200

    except Exception as e:
        print(f"Error obteniendo auditoría: {e}")
        return jsonify({"error": "Error obteniendo auditoría"}), 500
