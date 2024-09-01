import sqlite3
import hashlib
import csv

# Conectar a la base de datos
def connect_db():
    conn = sqlite3.connect('inventario.db')
    return conn

# Crear un nuevo producto en la base de datos
def agregar_producto(nombre, descripcion, cantidad, precio_compra, precio_venta):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO productos (nombre, descripcion, cantidad, precio_compra, precio_venta)
    VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio_compra, precio_venta))
    conn.commit()
    conn.close()

# Obtener todos los productos del inventario
def ver_inventario():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Actualizar la información de un producto existente
def actualizar_producto(id, nombre, descripcion, cantidad, precio_compra, precio_venta):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE productos
    SET nombre = ?, descripcion = ?, cantidad = ?, precio_compra = ?, precio_venta = ?
    WHERE id = ?
    ''', (nombre, descripcion, cantidad, precio_compra, precio_venta, id))
    conn.commit()
    conn.close()

# Eliminar un producto de la base de datos
def eliminar_producto(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Registrar una venta y actualizar el inventario
def registrar_venta(id_producto, cantidad_vendida):
    conn = connect_db()
    cursor = conn.cursor()

    # Verificar si el producto existe y tiene suficiente stock
    cursor.execute('SELECT cantidad, precio_venta, precio_compra FROM productos WHERE id = ?', (id_producto,))
    producto = cursor.fetchone()
    
    if producto and producto[0] >= cantidad_vendida:
        nueva_cantidad = producto[0] - cantidad_vendida
        cursor.execute('UPDATE productos SET cantidad = ? WHERE id = ?', (nueva_cantidad, id_producto))
        
        # Calcular la ganancia
        ganancia = (producto[1] - producto[2]) * cantidad_vendida

        # Registrar la venta
        cursor.execute('''
        INSERT INTO ventas (id_producto, cantidad_vendida, ganancia)
        VALUES (?, ?, ?)
        ''', (id_producto, cantidad_vendida, ganancia))

        conn.commit()
        print(f"Venta registrada: {cantidad_vendida} unidades del producto ID {id_producto}. Ganancia: {ganancia:.2f}")
    else:
        print("Error: Producto no encontrado o cantidad insuficiente.")

    conn.close()

# Verificar si hay productos con stock bajo
def verificar_stock_bajo(umbral=10):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE cantidad <= ?', (umbral,))
    productos_bajos = cursor.fetchall()
    conn.close()
    return productos_bajos

# Generar un reporte del inventario en un archivo CSV
def generar_reporte_csv(nombre_archivo='reporte_inventario.csv'):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()

    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nombre', 'Descripción', 'Cantidad', 'Precio Compra', 'Precio Venta'])
        writer.writerows(productos)

    print(f"Reporte generado: {nombre_archivo}")

# Generar un reporte de ganancias en un archivo CSV
def generar_reporte_ganancias(nombre_archivo='reporte_ganancias.csv'):
    conn = connect_db()
    cursor = conn.cursor()

    # Obtener las ventas agrupadas por producto
    cursor.execute('SELECT id_producto, SUM(cantidad_vendida), SUM(ganancia) FROM ventas GROUP BY id_producto')
    ventas = cursor.fetchall()

    # Ordenar por cantidad vendida para identificar más y menos vendidos
    productos_mas_vendidos = sorted(ventas, key=lambda x: x[1], reverse=True)
    productos_menos_vendidos = sorted(ventas, key=lambda x: x[1])

    conn.close()

    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID Producto', 'Total Vendido', 'Ganancia Total'])
        for venta in ventas:
            writer.writerow(venta)

        # Añadir secciones para más y menos vendidos
        if productos_mas_vendidos:
            writer.writerow([])
            writer.writerow(['Productos Más Vendidos'])
            writer.writerow(['ID Producto', 'Total Vendido'])
            for producto in productos_mas_vendidos[:5]:  # Mostrar los 5 más vendidos
                writer.writerow([producto[0], producto[1]])

        if productos_menos_vendidos:
            writer.writerow([])
            writer.writerow(['Productos Menos Vendidos'])
            writer.writerow(['ID Producto', 'Total Vendido'])
            for producto in productos_menos_vendidos[:5]:  # Mostrar los 5 menos vendidos
                writer.writerow([producto[0], producto[1]])

    print(f"Reporte de ganancias generado: {nombre_archivo}")


    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID Producto', 'Total Vendido', 'Ganancia Total'])
        for venta in ventas:
            writer.writerow(venta)

    print(f"Reporte de ganancias generado: {nombre_archivo}")

# Crear un nuevo usuario en la base de datos
def crear_usuario(usuario, contrasena):
    # Encriptar la contraseña usando SHA-256
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Insertar el nuevo usuario en la base de datos
        cursor.execute('''
        INSERT INTO usuarios (usuario, contrasena)
        VALUES (?, ?)
        ''', (usuario, contrasena_hash))
        conn.commit()
        print(f"Usuario '{usuario}' creado exitosamente.")
    except sqlite3.IntegrityError:
        print(f"Error: El nombre de usuario '{usuario}' ya existe.")
    finally:
        conn.close()

# Verificar las credenciales de un usuario
def verificar_usuario(usuario, contrasena):
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?
    ''', (usuario, contrasena_hash))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None
