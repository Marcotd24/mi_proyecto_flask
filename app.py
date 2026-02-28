import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ----------------------------------
# CLASE PRODUCTO (POO)
# ----------------------------------
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} - {self.cantidad} - {self.precio}"


# ----------------------------------
# CREAR TABLA SQLITE
# ----------------------------------
def crear_tabla():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


crear_tabla()


# ----------------------------------
# MOSTRAR PRODUCTOS (READ)
# ----------------------------------
@app.route('/')
def inicio():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    filas = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()

    productos = []

    for fila in filas:
        producto = Producto(
            fila['id'],
            fila['nombre'],
            fila['cantidad'],
            fila['precio']
        )
        productos.append(producto)

    return render_template('index.html', productos=productos)


# ----------------------------------
# AGREGAR PRODUCTO (CREATE)
# ----------------------------------
@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)',
        (nombre, cantidad, precio)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# ----------------------------------
# ELIMINAR PRODUCTO (DELETE)
# ----------------------------------
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))

    conn.commit()
    conn.close()

    return redirect('/')


# ----------------------------------
# FORMULARIO EDITAR
# ----------------------------------
@app.route('/editar/<int:id>')
def editar_form(id):
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    fila = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()

    if fila is None:
        return redirect('/')

    producto = Producto(
        fila['id'],
        fila['nombre'],
        fila['cantidad'],
        fila['precio']
    )

    return render_template('editar.html', producto=producto)


# ----------------------------------
# ACTUALIZAR PRODUCTO (UPDATE)
# ----------------------------------
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE productos
        SET nombre = ?, cantidad = ?, precio = ?
        WHERE id = ?
    ''', (nombre, cantidad, precio, id))

    conn.commit()
    conn.close()

    return redirect('/')


# ----------------------------------
# ABOUT
# ----------------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# ----------------------------------
# CONFIGURACIÓN PARA RENDER
# ----------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )