from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import csv
import os

app = Flask(__name__)

# ---------------------------------
# CONFIGURACION BASE DE DATOS
# ---------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventario.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------------------------
# MODELO DE DATOS
# ---------------------------------

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Float)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

# Crear base de datos
with app.app_context():
    db.create_all()

# ---------------------------------
# PAGINA PRINCIPAL
# ---------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------------
# FORMULARIO PRODUCTO
# ---------------------------------

@app.route("/producto")
def producto():
    return render_template("producto_form.html")

# ---------------------------------
# GUARDAR DATOS
# ---------------------------------

@app.route("/guardar_datos", methods=["POST"])
def guardar_datos():

    nombre = request.form["nombre"]
    precio = request.form["precio"]

    # ---------- SQLITE ----------
    nuevo_producto = Producto(nombre=nombre, precio=precio)
    db.session.add(nuevo_producto)
    db.session.commit()

    # ---------- TXT ----------
    with open("inventario/data/datos.txt", "a") as archivo:
        archivo.write(f"{nombre},{precio}\n")

    # ---------- JSON ----------
    datos_json = []

    if os.path.exists("inventario/data/datos.json"):
        with open("inventario/data/datos.json", "r") as archivo:
            try:
                datos_json = json.load(archivo)
            except:
                datos_json = []

    datos_json.append({
        "nombre": nombre,
        "precio": precio
    })

    with open("inventario/data/datos.json", "w") as archivo:
        json.dump(datos_json, archivo, indent=4)

    # ---------- CSV ----------
    with open("inventario/data/datos.csv", "a", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([nombre, precio])

    return "Datos guardados correctamente en TXT, JSON, CSV y SQLite"

# ---------------------------------
# MOSTRAR DATOS SQLITE
# ---------------------------------

@app.route("/datos")
def datos():

    productos = Producto.query.all()

    return render_template("datos.html", productos=productos)

# ---------------------------------
# LEER TXT
# ---------------------------------

@app.route("/leer_txt")
def leer_txt():

    datos = []

    try:
        with open("inventario/data/datos.txt", "r") as archivo:
            for linea in archivo:
                nombre, precio = linea.strip().split(",")
                datos.append({
                    "nombre": nombre,
                    "precio": precio
                })
    except:
        datos = []

    return render_template("datos_archivos.html", datos=datos, tipo="TXT")

# ---------------------------------
# LEER JSON
# ---------------------------------

@app.route("/leer_json")
def leer_json():

    datos = []

    try:
        with open("inventario/data/datos.json", "r") as archivo:
            datos = json.load(archivo)
    except:
        datos = []

    return render_template("datos_archivos.html", datos=datos, tipo="JSON")

# ---------------------------------
# LEER CSV
# ---------------------------------

@app.route("/leer_csv")
def leer_csv():

    datos = []

    try:
        with open("inventario/data/datos.csv", "r") as archivo:
            lector = csv.reader(archivo)

            for fila in lector:
                datos.append({
                    "nombre": fila[0],
                    "precio": fila[1]
                })
    except:
        datos = []

    return render_template("datos_archivos.html", datos=datos, tipo="CSV")

# ---------------------------------
# ABOUT
# ---------------------------------

@app.route("/about")
def about():
    return render_template("about.html")

# ---------------------------------
# EJECUTAR APP
# ---------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)