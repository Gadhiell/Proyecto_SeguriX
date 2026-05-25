import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


from flask import (
    Flask, 
    send_from_directory,
    request,
    redirect,
    render_template_string
)

from routes.api_routes import api


def create_app():

    app = Flask(__name__)

    app.register_blueprint(api)


    # ---------------LOGS TEST----------------

    logs = [

        {
            "fecha": "00:30-19/05/2025",
            "usuario": "J. Troncoso",
            "tipo": "Empleado",
            "metodo": "QR",
            "ubicacion": "Vestíbulo Principal",
            "estado": "ACTIVO"
        },

        {
            "fecha": "18:48-18/05/2025",
            "usuario": "I. Rivera",
            "tipo": "Proveedor",
            "metodo": "Tarjeta",
            "ubicacion": "Entrada lateral",
            "estado": "ACTIVO"
        },

        {
            "fecha": "11:22-18/05/2025",
            "usuario": "E. Díaz",
            "tipo": "Visitante",
            "metodo": "Huella",
            "ubicacion": "Entrada principal",
            "estado": "INACTIVO"
        },

        {
            "fecha": "22:58-17/05/2025",
            "usuario": "L. Cepeda",
            "tipo": "Proveedor",
            "metodo": "QR",
            "ubicacion": "Muelle de carga",
            "estado": "ACTIVO"
        }

    ]


    # ---------------- HOME ----------------

    @app.route("/")
    def home():

        return send_from_directory(".", "index.html")


    # ---------------- LOGIN ----------------

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            return redirect("/panel")

        return send_from_directory(".", "login.html")


    # ---------------- RESET PASSWORD ----------------

    @app.route("/password_reset")
    def nueva_contraseña():

        return send_from_directory(".", "password_reset.html")


    # ---------------- PANEL ----------------

    @app.route("/panel")
    def panel():

        return send_from_directory(".", "panel.html")


    # ---------------- USUARIOS ----------------

    @app.route("/usuarios")
    def usuarios():

        return send_from_directory(".", "usuarios.html")


    # ---------------- ESTADO SISTEMA ----------------

    @app.route("/estadosys")
    def estadosys():

        return send_from_directory(".", "estadosys.html")


    # ---------------- AUDITORIA ----------------

    @app.route("/auditoria")
    def auditoria():

        tipo = request.args.get("tipo", "todos")
        metodo = request.args.get("metodo", "todos")
        ubicacion = request.args.get("ubicacion", "todos")
        estado = request.args.get("estado", "todos")

        logs_filtrados = logs


        # FILTRO TIPO
        if tipo != "todos":

            logs_filtrados = [

                log for log in logs_filtrados
                if log["tipo"] == tipo

            ]


        # FILTRO METODO
        if metodo != "todos":

            logs_filtrados = [

                log for log in logs_filtrados
                if log["metodo"] == metodo

            ]


        # FILTRO UBICACION
        if ubicacion != "todos":

            logs_filtrados = [

                log for log in logs_filtrados
                if log["ubicacion"] == ubicacion

            ]


        # FILTRO ESTADO
        if estado != "todos":

            logs_filtrados = [

                log for log in logs_filtrados
                if log["estado"] == estado

            ]


        # ABRIR HTML
        with open("auditoria.html", "r", encoding="utf-8") as file:

            html = file.read()


        # REEMPLAZAR TABLA
        filas = ""

        for log in logs_filtrados:

            if log["metodo"] == "QR":

                icono = "bi bi-qr-code-scan"

            elif log["metodo"] == "Huella":

                icono = "bi bi-fingerprint"

            else:

                icono = "bi bi-credit-card-2-front-fill"


            estado_class = (
                "activo"
                if log["estado"] == "ACTIVO"
                else "inactivo"
            )


            filas += f"""

            <tr>

                <td>{log['fecha']}</td>

                <td>
                    {log['usuario']} ({log['tipo']})
                </td>

                <td class="method-cell">

                    <i class="{icono}"></i>

                    <div>

                        <strong>
                            {log['metodo']}
                        </strong>

                    </div>

                </td>

                <td>
                    {log['ubicacion']}
                </td>

                <td>

                    <span class="badge {estado_class}">
                        {log['estado']}
                    </span>

                </td>

            </tr>

            """


        html = html.replace(
            "<tbody id=\"audit-body\"></tbody>",
            f"<tbody id='audit-body'>{filas}</tbody>"
        )

        return render_template_string(html)


    return app


if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)