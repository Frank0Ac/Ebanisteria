# se define funciones para hacer consultas en la BD en la tabla proudctos
import sqlite3
from flask import current_app

def obtener_usuarios(page=1, per_page=10):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()
    cursor.execute('SELECT User.id, User.correo, User.nom_usuario, User.admin FROM User')
    usuarios = cursor.fetchall()
    conexion.close()

    # Manually handle pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_usuarios = usuarios[start_idx:end_idx]

    # Return a tuple with the paginated list and the total number of users
    return paginated_usuarios, len(usuarios)

def obtener_usuario_por_id(user_id):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM User WHERE id = ?', (user_id,))
    usuario = cursor.fetchone()
    conexion.close()

    return usuario

def editar_usuario(user_id, nom_usuario = None, admin = 0):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    # Build the SQL UPDATE query dynamically based on provided fields
    update_query = 'UPDATE User SET '
    updates = []

    if nom_usuario is not None:
        updates.append(f"nom_usuario = '{nom_usuario}'")
    
    updates.append(f"admin = {admin}")

    update_query += ', '.join(updates) + f" WHERE id = {user_id};"

    cursor = conexion.cursor()
    cursor.execute(update_query)
    conexion.commit()
    conexion.close()

def borrar_usuario(user_id):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect(ruta)

    cursor = conexion.cursor()
    cursor.execute('DELETE FROM User WHERE id=?', (user_id,))
    conexion.commit()
    conexion.close()