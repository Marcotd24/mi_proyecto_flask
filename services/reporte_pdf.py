from fpdf import FPDF
from conexion.conexion import conectar

def generar_reporte_productos():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="REPORTE DE PRODUCTOS", ln=True, align='C')
    pdf.ln(10)

    # Encabezados
    pdf.cell(50, 10, "Nombre", 1)
    pdf.cell(40, 10, "Precio", 1)
    pdf.cell(40, 10, "Stock", 1)
    pdf.ln()

    # Datos
    for p in productos:
        pdf.cell(50, 10, str(p["nombre"]), 1)
        pdf.cell(40, 10, str(p["precio"]), 1)
        pdf.cell(40, 10, str(p["stock"]), 1)
        pdf.ln()

    pdf.output("reporte_productos.pdf")