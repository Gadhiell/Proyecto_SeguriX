funcion para los logs
@app.route("/logs", methods=["GET"])
def obtener_logs():
    return jsonify(logs)


if __name__ == "__main__":
    app.run(debug=True)