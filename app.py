from flask import Flask, render_template, request, redirect, url_for
from conexion.conexion import conectar

# Flask-Login
from flask_login import LoginManager, login_user, logout_user, login_required
from models import Usuario

# CRUD productos
from services.producto_service import *

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión"


# ==============================
# CARGAR USUARIO
# ==============================
@login_manager.user_loader
def load_user(user_id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        return Usuario(user[0], user[1], user[2], user[3])
    return None


# ==============================
# TEST DE CONEXIÓN
# ==============================
@app.route('/test_db')
def test_db():
    try:
        con = conectar()
        return "Conexión exitosa 🚀"
    except Exception as e:
        return f"Error: {e}"


# ==============================
# INICIO (ARREGLADO)
# ==============================
@app.route("/")
def inicio():
    return redirect("/login")


# ==============================
# CRUD PRODUCTOS
# ==============================

# LISTAR
@app.route('/productos')
@login_required
def productos():
    lista = obtener_productos()
    return render_template('productos/listar.html', productos=lista)


# CREAR
@app.route('/productos/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        insertar_producto(
            request.form['nombre'],
            request.form['precio'],
            request.form['stock']
        )
        return redirect('/productos')

    return render_template('productos/crear.html')


# EDITAR
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = obtener_producto(id)

    if request.method == 'POST':
        actualizar_producto(
            id,
            request.form['nombre'],
            request.form['precio'],
            request.form['stock']
        )
        return redirect('/productos')

    return render_template('productos/editar.html', producto=producto)


# ELIMINAR
@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminar_producto_route(id):
    eliminar_producto(id)
    return redirect('/productos')


# ==============================
# AUTENTICACIÓN
# ==============================

# REGISTRO
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        con = conectar()
        cursor = con.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password)
            )
            con.commit()
            return redirect(url_for("login"))

        except:
            return "⚠️ El correo ya está registrado"

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
            return redirect("/productos")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    app.run(debug=True)