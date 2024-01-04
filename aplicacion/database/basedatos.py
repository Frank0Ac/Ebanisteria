import os
import sqlite3

def create_tables():
    # Obtener la ruta absoluta al directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta absoluta al archivo de la base de datos
    db_path = os.path.join(script_dir, 'ebanisteria.db')
    print("Esta es la ruta", script_dir)
    print("Esta es la ruta", db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Sentencias SQL para crear las tablas si no existen
    sentencias_sql = """
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY,
            nom_usuario TEXT UNIQUE NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            verificado INTEGER DEFAULT 0,  -- 0: No verificado, 1: Verificado
            contrasenia TEXT NOT NULL,
            admin INTEGER DEFAULT 0  -- 0: Regular user, 1: Admin user
        );

        CREATE TABLE IF NOT EXISTS Tipos (
            id INTEGER PRIMARY KEY,
            tipo TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            unidades INTEGER NOT NULL DEFAULT 1,
            tipo INTEGER NOT NULL,
            costo REAL NOT NULL,
            descripcion TEXT NOT NULL,
            imagen TEXT NOT NULL,
            FOREIGN KEY (tipo) REFERENCES Tipos(id)
        );

        CREATE TABLE IF NOT EXISTS Carrito (
            id INTEGER PRIMARY KEY,
            cantidad INTEGER NOT NULL DEFAULT 1,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Productos(id),
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
    """

    try:
        cursor.executescript(sentencias_sql)
        conn.commit()
        print('Se crearon las tablas...')
    except sqlite3.Error as e:
        print("Error al ejecutar las sentencias SQL:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    print("Creando Tablas")
    create_tables()