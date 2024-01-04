# se define funciones para hacer consultas en la BD en la tabla proudctos
import sqlite3
from flask import current_app
import os

def obtenerproductos(page=1, per_page=10):
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','')
    print(ruta)
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()#para relizar consultas mediante un cursor
    cursor.execute("""SELECT Productos.id, Productos.nombre, Productos.unidades, Tipos.tipo, Productos.costo, Productos.descripcion, Productos.imagen
        FROM Productos
        INNER JOIN Tipos ON Productos.tipo = Tipos.id;
        """)
    productos=cursor.fetchall()
    conexion.close()

    # Manually handle pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = productos[start_idx:end_idx]

    #retornar productos
    return paginated_products, len(productos)

def obtener_producto_por_id(product_id):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Productos WHERE id = ?', (product_id,))
    producto = cursor.fetchone()
    conexion.close()

    return producto

def obtener_tipos():
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','')
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()
    cursor.execute('SELECT Tipos.id, Tipos.tipo FROM Tipos')
    tipos = cursor.fetchall()
    conexion.close()

    return tipos

def editar_producto(product_id, cantidad=None, nombre=None, tipo=None, costo=None, desc=None, img=None):

    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    # Build the SQL UPDATE query dynamically based on provided fields
    update_query = 'UPDATE Productos SET '
    updates = []

    if nombre is not None:
        updates.append(f"nombre = '{nombre}'")
    if desc is not None:
        updates.append(f"descripcion = '{desc}'")
    if costo is not None:
        updates.append(f"costo = {costo}")
    if tipo is not None:
        updates.append(f"tipo = {tipo}")
    if cantidad is not None:
        updates.append(f"unidades = {cantidad}")
    if img is not None:
        updates.append(f"imagen = '{img}'")

    update_query += ', '.join(updates) + f" WHERE id = {product_id};"
    
    # Execute the UPDATE query
    cursor.execute(update_query)
    
    # Commit the changes to the database
    conexion.commit()
    conexion.close()

def borrar_producto(product_id):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Productos WHERE id=?', (product_id,))
    conexion.commit()
    conexion.close()

def editar_tipo(type_id, tipo):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    cursor.execute('UPDATE Tipos SET tipo=? WHERE id=?', (tipo, type_id))
    conexion.commit()
    conexion.close()

def borrar_tipo(id):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Productos WHERE tipo=?', (id,))
    cursor.execute('DELETE FROM Tipos WHERE id=?', (id,))
    conexion.commit()
    conexion.close()

def crear_tipo(nombre):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    cursor.execute('INSERT INTO Tipos (tipo) VALUES (?)',(nombre,))
    conexion.commit()
    conexion.close()

def crear_producto(nombre, cantidad, tipo, costo, desc, img):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    cursor.execute('INSERT INTO Productos (nombre, tipo, costo, descripcion, imagen, unidades) VALUES (?, ?, ?, ?, ?, ?)', 
                   (nombre, tipo, costo, desc, img, cantidad))
    
    conexion.commit()
    conexion.close()