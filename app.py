import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from flask import Flask, send_from_directory, request, redirect
from routes.api_routes import api


def create_app():

    app = Flask(__name__)

    app.register_blueprint(api)


    @app.route("/")
    def home():
        return send_from_directory(".", "index.html")


    @app.route("/login", methods=["GET", "POST"])
    def login():

        #--------------TEST-------------
        # CUANDO APRETAS "INICIAR SESION"
        if request.method == "POST":

            # REDIRIGE AL PANEL
            return redirect("/panel")

        # MUESTRA login.html
        return send_from_directory(".", "login.html")
        #---------------------------------


    @app.route("/password_reset")
    def nueva_contraseña():
        return send_from_directory(".", "password_reset.html")


    @app.route("/panel")
    def panel():
        return send_from_directory(".", "panel.html")


    @app.route("/usuarios")
    def usuarios():
        return send_from_directory(".", "usuarios.html")


    @app.route("/auditoria")
    def auditoria():
        return send_from_directory(".", "auditoria.html")


    @app.route("/estadosys")
    def estadosys():
        return send_from_directory(".", "estadosys.html")


    return app


if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)