from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.')

#"Base de datos"
logs = []

usuarios = {
    1: {"nombre": "Juan", "activo": True},
    2: {"nombre": "Maria", "activo": False},
}


#Validaciones
def validar_acceso(usuario_id):
    usuario = usuarios.get(usuario_id)

    if not usuario:
        return False, "Usuario no existe"

    if not usuario["activo"]:
        return False, "Usuario inactivo"

    return True, "Acceso permitido"


#Rutas para la pagina
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route('/logo.png')
def logo():
    return send_from_directory(".", "logo.png")

#Siguiente pagina, el panel
@app.route("/panel")
def panel():
    return send_from_directory(".", "panel.html")



#Simular acceso
@app.route("/acceso", methods=["POST"])
def acceso():
    data = request.json

    usuario_id = data.get("usuario_id")
    metodo = data.get("metodo")

    permitido, mensaje = validar_acceso(usuario_id)

    log = {
        "usuario_id": usuario_id,
        "metodo": metodo,
        "estado": mensaje
    }

    logs.append(log)

    return jsonify(log)


#funcion para los logs
@app.route("/logs", methods=["GET"])
def obtener_logs():
    return jsonify(logs)


if __name__ == "__main__":
    app.run(debug=True)