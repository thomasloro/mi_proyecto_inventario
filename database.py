import sqlite3

# Conectar a la base de datos
def connect_db():
    conn = sqlite3.connect('inventario.db')
    return conn

# Crear las tablas necesarias en la base de datos
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Crear la tabla de productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        cantidad INTEGER NOT NULL,
        precio_compra REAL NOT NULL,
        precio_venta REAL NOT NULL
    )
    ''')

    # Crear la tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL
    )
    ''')

    # Crear la tabla de ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER NOT NULL,
        cantidad_vendida INTEGER NOT NULL,
        ganancia REAL NOT NULL,
        FOREIGN KEY (id_producto) REFERENCES productos (id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    create_tables()
