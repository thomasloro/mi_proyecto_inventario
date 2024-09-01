from inventory import crear_usuario

# Solicitar el nombre de usuario y la contraseña
nuevo_usuario = input("Ingrese el nombre de usuario: ")
nueva_contrasena = input("Ingrese la contraseña: ")

# Crear el nuevo usuario
crear_usuario(nuevo_usuario, nueva_contrasena)
