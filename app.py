from flask import Flask, render_template, request, redirect, url_for
from conexion.conexion import conectar

#  Flask-Login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Usuario

app = Flask(__name__)
app.secret_key = "clave_secreta"  # IMPORTANTE

#  Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


#  Cargar usuario desde MySQL
@login_manager.user_loader
def load_user(user_id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        return Usuario(user[0], user[1], user[2], user[3])
    return None


#  Ruta protegida
@app.route("/")
@login_required
def inicio():
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    return render_template("usuarios.html", usuarios=usuarios)


#  REGISTRO
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        con = conectar()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        con.commit()

        return redirect(url_for("login"))

    return render_template("registro.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and user[3] == password:
            usuario = Usuario(user[0], user[1], user[2], user[3])
            login_user(usuario)
            return redirect(url_for("inicio"))

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
