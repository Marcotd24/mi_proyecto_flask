from conexion.conexion import conectar

def obtener_productos():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    return cursor.fetchall()

def insertar_producto(nombre, precio, stock):
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
        (nombre, precio, stock)
    )
    con.commit()

def obtener_producto(id):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id,))
    return cursor.fetchone()

def actualizar_producto(id, nombre, precio, stock):
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s",
        (nombre, precio, stock, id)
    )
    con.commit()

def eliminar_producto(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id,))
    con.commit()