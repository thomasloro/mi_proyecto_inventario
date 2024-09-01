from inventory import (
    agregar_producto, 
    ver_inventario, 
    actualizar_producto, 
    eliminar_producto, 
    verificar_stock_bajo, 
    generar_reporte_csv,
    registrar_venta,
    generar_reporte_ganancias,
    crear_usuario, 
    verificar_usuario
)
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

def iniciar_sesion():
    print(Fore.YELLOW + "Bienvenido al sistema de gestión de inventarios")
    while True:
        print(Fore.CYAN + "\n=== Autenticación de Usuario ===")
        usuario = input(Fore.CYAN + "Usuario: ")
        contrasena = input(Fore.CYAN + "Contraseña: ")

        if verificar_usuario(usuario, contrasena):
            print(Fore.GREEN + "Inicio de sesión exitoso.")
            return True
        else:
            print(Fore.RED + "Usuario o contraseña incorrectos. Intenta de nuevo.")

def menu():
    print(Fore.CYAN + "\n=== Menú de Gestión de Inventarios ===")
    print(Fore.GREEN + "1. Agregar Producto")
    print(Fore.GREEN + "2. Ver Inventario")
    print(Fore.GREEN + "3. Actualizar Producto")
    print(Fore.GREEN + "4. Eliminar Producto")
    print(Fore.GREEN + "5. Registrar Venta")
    print(Fore.GREEN + "6. Verificar Stock Bajo")
    print(Fore.GREEN + "7. Generar Reporte de Inventario")
    print(Fore.GREEN + "8. Generar Reporte de Ganancias")
    print(Fore.GREEN + "9. Crear Usuario")
    print(Fore.RED + "10. Salir")

def registrar_venta_con_busqueda():
    productos = ver_inventario()
    if not productos:
        print(Fore.RED + "No hay productos en el inventario.")
        return

    print(Fore.CYAN + "\n=== Inventario ===")
    for producto in productos:
        print(Fore.WHITE + f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, "
                           f"Cantidad: {producto[3]}, Precio Venta: {producto[5]}")
    
    id_producto = int(input(Fore.CYAN + "ID del producto vendido: "))
    cantidad_vendida = int(input(Fore.CYAN + "Cantidad vendida: "))
    registrar_venta(id_producto, cantidad_vendida)

def main():
    if iniciar_sesion():
        while True:
            menu()
            opcion = input(Fore.CYAN + "Selecciona una opción: ")

            if opcion == '1':
                nombre = input(Fore.CYAN + "Nombre del producto: ")
                descripcion = input(Fore.CYAN + "Descripción: ")
                cantidad = int(input(Fore.CYAN + "Cantidad: "))
                precio_compra = float(input(Fore.CYAN + "Precio de compra: "))
                precio_venta = float(input(Fore.CYAN + "Precio de venta: "))
                agregar_producto(nombre, descripcion, cantidad, precio_compra, precio_venta)
                print(Fore.GREEN + f"Producto '{nombre}' agregado.")
            elif opcion == '2':
                productos = ver_inventario()
                print(Fore.CYAN + "\n=== Inventario ===")
                for producto in productos:
                    print(Fore.WHITE + f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, "
                                       f"Cantidad: {producto[3]}, Precio Compra: {producto[4]}, Precio Venta: {producto[5]}")
            elif opcion == '3':
                id_producto = int(input(Fore.CYAN + "ID del producto a actualizar: "))
                nombre = input(Fore.CYAN + "Nuevo nombre: ")
                descripcion = input(Fore.CYAN + "Nueva descripción: ")
                cantidad = int(input(Fore.CYAN + "Nueva cantidad: "))
                precio_compra = float(input(Fore.CYAN + "Nuevo precio de compra: "))
                precio_venta = float(input(Fore.CYAN + "Nuevo precio de venta: "))
                actualizar_producto(id_producto, nombre, descripcion, cantidad, precio_compra, precio_venta)
                print(Fore.GREEN + f"Producto ID {id_producto} actualizado.")
            elif opcion == '4':
                id_producto = int(input(Fore.CYAN + "ID del producto a eliminar: "))
                eliminar_producto(id_producto)
                print(Fore.GREEN + f"Producto ID {id_producto} eliminado.")
            elif opcion == '5':
                registrar_venta_con_busqueda()
            elif opcion == '6':
                umbral = int(input(Fore.CYAN + "Ingrese el umbral para el stock bajo: "))
                productos_bajos = verificar_stock_bajo(umbral)
                if productos_bajos:
                    print(Fore.YELLOW + "\n=== Productos con Stock Bajo ===")
                    for producto in productos_bajos:
                        print(Fore.WHITE + f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, "
                                           f"Cantidad: {producto[3]}, Precio Compra: {producto[4]}, Precio Venta: {producto[5]}")
                else:
                    print(Fore.GREEN + "No hay productos con stock bajo.")
            elif opcion == '7':
                nombre_archivo = input(Fore.CYAN + "Nombre del archivo para el reporte de inventario (ejemplo: inventario.csv): ")
                generar_reporte_csv(nombre_archivo)
                print(Fore.GREEN + f"Reporte de inventario '{nombre_archivo}' generado exitosamente.")
            elif opcion == '8':
                nombre_archivo = input(Fore.CYAN + "Nombre del archivo para el reporte de ganancias (ejemplo: ganancias.csv): ")
                generar_reporte_ganancias(nombre_archivo)
                print(Fore.GREEN + f"Reporte de ganancias '{nombre_archivo}' generado exitosamente.")
            elif opcion == '9':
                nuevo_usuario = input(Fore.CYAN + "Ingrese el nuevo nombre de usuario: ")
                nueva_contrasena = input(Fore.CYAN + "Ingrese la nueva contraseña: ")
                crear_usuario(nuevo_usuario, nueva_contrasena)
                print(Fore.GREEN + f"Usuario '{nuevo_usuario}' creado exitosamente.")
            elif opcion == '10':
                print(Fore.YELLOW + "Saliendo del programa.")
                break
            else:
                print(Fore.RED + "Opción no válida. Intenta de nuevo.")

if __name__ == '__main__':
    main()
