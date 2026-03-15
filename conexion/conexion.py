import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pambi-0182",
        database="tienda",
        port=3307
    )

    return conexion
