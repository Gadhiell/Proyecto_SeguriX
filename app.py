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


def create_app():

    app = Flask(__name__)
    
    app.secret_key = "SeguriX_SecureKey_2024"

    app.register_blueprint(api)
    
    repo = UsuarioRepository()

    #Manejo de errores global
    @app.errorhandler(404)
    def no_encontrado(error):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def error_servidor(error):
        return jsonify({"error": "Error interno del servidor"}), 500


    @app.route("/")
    def home():
        try:
            return send_from_directory(".", "index.html")
        except Exception as e:
            print(f"Error cargando home: {e}")
            return jsonify({"error": "No se pudo cargar la página"}), 500


    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":
            try:
                #Obtener datos del formulario
                usuario_input = request.form.get("usuario", "").strip()
                
                #Validar que no esté vacío
                if not usuario_input:
                    return jsonify({"error": "Usuario requerido"}), 400

                #Guardar datos en sesión
                session["usuario_id"] = "USR_TEST"
                session["usuario_nombre"] = usuario_input
                session["usuario_rol"] = "Usuario"
                session["usuario_email"] = f"{usuario_input}@segurix.cl"
                
                return redirect("/panel")
                
            except Exception as e:
                print(f"Error en login: {e}")
                return jsonify({"error": "Error al iniciar sesión"}), 500

        return send_from_directory(".", "login.html")
    
    
    @app.route("/logout")
    def logout():
        try:
            session.clear()
            return redirect("/")
        except Exception as e:
            print(f"Error en logout: {e}")
            return redirect("/")
    
    
    @app.route("/api/sesion")
    def obtener_sesion():
        try:
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
        except Exception as e:
            print(f"Error obteniendo sesión: {e}")
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


    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('Static', filename)


    return app


if __name__ == "__main__":
 
    app = create_app()

    app.run(debug=True)