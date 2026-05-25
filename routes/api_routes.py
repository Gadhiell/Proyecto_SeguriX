from flask import Blueprint, request, jsonify
from services.auth_service import validar_acceso
from data.memory_db import usuarios, logs
from models.evento_acceso import EventoAcceso

api = Blueprint("api", __name__)


@api.route("/acceso", methods=["POST"])
def acceso():

    data = request.json

    usuario_id = data.get("usuario_id")
    metodo = data.get("metodo")

    permitido, estado = validar_acceso(usuario_id, usuarios)

    log = EventoAcceso(

        usuario_id,
        metodo,
        estado

    )

    logs.append(log.__dict__)

    return jsonify(log.__dict__)


@api.route("/logs", methods=["GET"])
def obtener_logs():

    return jsonify(logs)