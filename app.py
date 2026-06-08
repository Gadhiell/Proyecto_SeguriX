import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from flask import (
    Flask,
    send_from_directory,
    request,
    redirect,
    session,
    jsonify
)

from routes.api_routes import api
from repositories.usuario_repository import UsuarioRepository
from data import memory_db


def create_app():

    app = Flask(__name__)
    
    app.secret_key = "SeguriX_SecureKey_2024"

    app.register_blueprint(api)
    
    repo = UsuarioRepository()

    @app.route("/")
    def home():

        return send_from_directory(".", "index.html")


    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":
            
            # En modo desarrollo, acepta cualquier usuario y contraseña
            usuario_input = request.form.get("usuario", "Usuario Test")
            
            # Crear sesión con usuario genérico
            session["usuario_id"] = "USR_TEST"
            session["usuario_nombre"] = usuario_input or "Usuario SeguriX"
            session["usuario_rol"] = "Usuario"
            session["usuario_email"] = f"{usuario_input}@segurix.cl"
            
            return redirect("/panel")

        return send_from_directory(".", "login.html")
    
    
    @app.route("/logout")
    def logout():
        
        session.clear()
        return redirect("/")
    
    
    @app.route("/api/sesion")
    def obtener_sesion():
        
        if "usuario_id" in session:
            return jsonify({
                "usuario_id": session.get("usuario_id"),
                "usuario_nombre": session.get("usuario_nombre"),
                "usuario_rol": session.get("usuario_rol"),
                "usuario_email": session.get("usuario_email"),
                "logueado": True
            })
        else:
            return jsonify({"logueado": False}), 401


    @app.route("/password_reset")
    def nueva_contraseña():

        return send_from_directory(".", "password_reset.html")


    @app.route("/panel")
    def panel():
        
        if "usuario_id" not in session:
            return redirect("/login")

        return send_from_directory(".", "Panel.html")


    @app.route("/usuarios")
    def usuarios():
        
        if "usuario_id" not in session:
            return redirect("/login")

        return send_from_directory(".", "usuarios.html")


    @app.route("/auditoria")
    def auditoria():
        
        if "usuario_id" not in session:
            return redirect("/login")

        return send_from_directory(".", "auditoria.html")


    @app.route("/estadosys")
    def estadosys():
        
        if "usuario_id" not in session:
            return redirect("/login")

        return send_from_directory(".", "estadosys.html")
    
    
    @app.route("/dashboard.html")
    def dashboard():
        return send_from_directory(".", "dashboard.html")
    
    
    @app.route("/dashboard.js")
    def dashboard_js():
        response = send_from_directory(".", "dashboard.js")
        response.headers["Content-Type"] = "application/javascript"
        return response
    
    
    @app.route("/dashboard.css")
    def dashboard_css():
        response = send_from_directory(".", "dashboard.css")
        response.headers["Content-Type"] = "text/css"
        return response


    return app


if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)