import tkinter as tk
from tkinter import messagebox
from inventory import agregar_producto, ver_inventario, eliminar_producto

# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Inventario")
root.geometry("500x400")

# Función para agregar un producto
def agregar():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    cantidad = entry_cantidad.get()
    precio_compra = entry_precio_compra.get()
    precio_venta = entry_precio_venta.get()

    if nombre and cantidad.isdigit() and precio_compra.replace('.', '', 1).isdigit() and precio_venta.replace('.', '', 1).isdigit():
        agregar_producto(nombre, descripcion, int(cantidad), float(precio_compra), float(precio_venta))
        messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado.")
        limpiar_campos()
    else:
        messagebox.showerror("Error", "Por favor, ingrese datos válidos.")

# Función para ver los productos
def ver():
    productos = ver_inventario()
    text_output.delete(1.0, tk.END)
    for producto in productos:
        text_output.insert(tk.END, f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}, Precio Venta: {producto[5]}\n")

# Función para eliminar un producto
def eliminar():
    id_producto = entry_id.get()
    if id_producto.isdigit():
        eliminar_producto(int(id_producto))
        messagebox.showinfo("Éxito", f"Producto ID {id_producto} eliminado.")
        ver()
    else:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")

# Función para limpiar los campos de entrada
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_precio_compra.delete(0, tk.END)
    entry_precio_venta.delete(0, tk.END)

# Campos de entrada
tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Descripción:").grid(row=1, column=0, padx=10, pady=10)
entry_descripcion = tk.Entry(root)
entry_descripcion.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Cantidad:").grid(row=2, column=0, padx=10, pady=10)
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Precio Compra:").grid(row=3, column=0, padx=10, pady=10)
entry_precio_compra = tk.Entry(root)
entry_precio_compra.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Precio Venta:").grid(row=4, column=0, padx=10, pady=10)
entry_precio_venta = tk.Entry(root)
entry_precio_venta.grid(row=4, column=1, padx=10, pady=10)

# Botones
tk.Button(root, text="Agregar Producto", command=agregar).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Ver Inventario", command=ver).grid(row=6, column=0, columnspan=2, pady=10)

tk.Label(root, text="ID para eliminar:").grid(row=7, column=0, padx=10, pady=10)
entry_id = tk.Entry(root)
entry_id.grid(row=7, column=1, padx=10, pady=10)
tk.Button(root, text="Eliminar Producto", command=eliminar).grid(row=8, column=0, columnspan=2, pady=10)

# TextBox para mostrar el inventario
text_output = tk.Text(root, height=10, width=50)
text_output.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()
