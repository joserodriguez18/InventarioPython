import servicios as servicio
inventario = []

def pedir_float_positivo(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor <= 0:
                print("Debe ingresar un número mayor a 0")
                continue
            return valor
        except ValueError:
            print("Entrada no válida. Debe ser un número.")

def pedir_int_positivo(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 0:
                print("Debe ingresar un número entero mayor a 0")
                continue
            return valor
        except ValueError:
            print("Entrada no válida. Debe ser un número.")


def pedir_string_no_vacio(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("No puede estar vacío")

def mostrar_inventario():
    respuesta = servicio.mostrar_inventario(inventario)

    if respuesta is not None:
        print(respuesta)
    else:
        print("El inventario está vacío.")

def agregar_al_inventario():
    nombre = pedir_string_no_vacio("Ingrese el nombre del producto: ")
    precio = pedir_float_positivo("Ingrese el precio del producto: ")
    cantidad = pedir_int_positivo("Ingrese la cantidad del producto: ")

    respuesta = servicio.agregar_producto(inventario, nombre, precio, cantidad)
    if respuesta:
        print("Producto agregado con exito")
    else:
        print("No se pudo agregar el producto")
    
def buscar_en_inventario():
    nombre = pedir_string_no_vacio("Ingrese el nombre del producto a buscar: ")
    resultado = servicio.buscar_producto(inventario, nombre)

    if resultado:
        print(resultado)
    else:
        print("Producto no encontrado.")

def eliminar_del_inventario():
    nombre = pedir_string_no_vacio("Ingrese el nombre del producto a eliminar: ")
    resultado = servicio.eliminar_producto(inventario, nombre)

    if resultado:
        print("El producto fue eliminado.")
    else:
        print("El producto no existe")



acciones = {
    1: agregar_al_inventario,
    2: mostrar_inventario,
    3: buscar_en_inventario,
    # 4: actualizar_inventario,
    5: eliminar_del_inventario,
    # 6: estadísticas,
    # 7: guardar_en_CSV,
    # 8: cargar_desde_CSV
}
    

# Menú conceptual de la aplicación
     
while True:
    try:
        print(
            """
SISTEMA DE INVENTARIO
  1. Agregar al inventario
  2. Mostrar inventario
  3. Buscar en inventario
  4. Actualizar inventario
  5. Eliminar del inventario
  6. Estadísticas
  7. Guardar en CSV
  8. Cargar desde CSV
  9. Salir
"""
        )
        opc = input("Ingrese una opción (1-9): ")
        if not opc.isdigit():
            raise ValueError
        opc = int(opc)
        if opc in acciones:
            acciones[opc]()
        elif opc == 9:
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

    except ValueError:
        print("Opción inválida. Debe ser un número entero")