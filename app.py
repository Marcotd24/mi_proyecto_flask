from flask import Flask, render_template
from conexion.conexion import conectar

app = Flask(__name__)

@app.route("/")
def inicio():

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    return render_template("usuarios.html", usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)
