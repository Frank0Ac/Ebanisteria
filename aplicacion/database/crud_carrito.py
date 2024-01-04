import sqlite3
from flask import current_app
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO

def generate_pdf_bill(productos, total_to_pay):
    
    buffer = BytesIO()

    # Create a PDF document
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Add content to the PDF
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(300, 750, "Ebanisteria JyF")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(100, 730, f"Transaction Number: 435A-45B4-54D4-89F4")

    data = [["Product", "Quantity", "Unit Price", "Total"]]
    for product in productos:
        data.append([product[1], product[2], f"${product[3]:.2f}", f"${product[2] * product[3]:.2f}"])

    # Create a table for the product details
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Calculate the total height required for the table
    table_height = len(data) * 20

    # Draw the table on the PDF
    table.wrapOn(pdf, 400, table_height)
    table.drawOn(pdf, 100, 600 - table_height)

    # Add total amount
    pdf.drawString(100, 550 - table_height, f"Total Amount: ${total_to_pay:.2f}")

    # Add bank details
    pdf.drawString(100, 530 - table_height, "Bank Details:")
    banks = ["Bancolombia", "BBVA", "Davivienda", "Banco de Bogotá", "Banco de Occidente"]
    for i, bank in enumerate(banks, start=1):
        pdf.drawString(120, 510 - table_height - (i * 12), f"{i}. {bank}")

    # Save the PDF to the buffer
    pdf.save()

    # Move the buffer position to the beginning
    buffer.seek(0)

    return buffer

def ver_carrito(user_id):
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','')
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()#para relizar consultas mediante un cursor
    cursor.execute("""
        SELECT Carrito.id, Productos.nombre, Carrito.cantidad, Productos.costo, Productos.imagen
        FROM Carrito
        INNER JOIN Productos ON Carrito.product_id = Productos.id
        WHERE Carrito.user_id = ?;
    """, (user_id,))
    productos=cursor.fetchall()
    conexion.close()

    #retornar productos
    return productos

def agregar_al_carrito(user_id, product_id, cantidad):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    # Check if the product is already in the cart for the given user
    cursor.execute('SELECT id, cantidad FROM Carrito WHERE user_id = ? AND product_id = ?', (user_id, product_id))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # If the product is already in the cart, update the quantity
        new_quantity = existing_entry[1] + cantidad
        cursor.execute('UPDATE Carrito SET cantidad = ? WHERE id = ?', (new_quantity, existing_entry[0]))
    else:
        # If the product is not in the cart, insert a new entry
        cursor.execute('INSERT INTO Carrito (user_id, product_id, cantidad) VALUES (?, ?, ?)', (user_id, product_id, cantidad))

    conexion.commit()
    conexion.close()

def vaciar_carrito(user_id):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Carrito WHERE user_id = ?', (user_id,))
    conexion.commit()
    conexion.close()

def remove_product(product_id):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Carrito WHERE id = ?', (product_id,))
    conexion.commit()
    conexion.close()

def editar_cantidad(id, new_quantity):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()

    cursor.execute('UPDATE Carrito SET cantidad = ? WHERE id = ?', (new_quantity, id))

    conexion.commit()
    conexion.close()