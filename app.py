import servicios as servicio
import archivos as archivo
from tabulate import tabulate
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

def pedir_opcion_si_no(mensaje):
    while True:
        opcion = input(mensaje).strip().lower()
        if opcion in ("s", "n"):
            return opcion
        print("Ingrese 's' o 'n'.")

def mostrar_inventario():
    respuesta = servicio.mostrar_inventario(inventario)

    if respuesta is not None:
        print(tabulate(respuesta, headers="keys", tablefmt="grid"))
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

def actualizar_inventario():
    nombre = pedir_string_no_vacio("Ingrese el nombre del producto que desea actualizar: ")
    opc_precio = pedir_opcion_si_no("¿Desea modificar el precio? (s/n): ")
    if opc_precio.lower() == "s":
        precio = pedir_float_positivo("Nuevo precio: ")
    else:
        precio = None
    opc_cantidad = pedir_opcion_si_no("¿Desea modificar la cantidad? (s/n): ")
    if opc_cantidad.lower() == "s":
        cantidad = pedir_float_positivo("Nueva cantidad: ")
    else:
        cantidad = None
    repuesta = servicio.actualizar_producto(inventario, nombre, precio, cantidad)
    if repuesta == servicio.SIN_CAMBIOS:
        print("El producto no se actualizó")
    elif repuesta == servicio.ACTUALIZADO:
        print("Actualizó con éxito")
    elif repuesta == servicio.NO_ENCONTRADO:
        print("Producto no encontrado")


def guardar_en_CSV():
    ruta = input("Ruta del archivo: ")
    estado = archivo.guardar_csv(inventario, ruta)

    if estado == archivo.GUARDADO:
        print(f"Inventario guardado en: {ruta}")
    elif estado == archivo.INVENTARIO_VACIO:
        print("No hay productos para guardar.")
    elif estado == archivo.ERROR_RUTA:
        print("Ruta inválida")
    elif estado == archivo.ERROR_PERMISO:
        print("Archivo en uso o sin permisos")
    elif estado == archivo.ERROR_DATOS:
        print("Datos inválidos")
    elif estado == archivo.ERROR_GENERAL:
        print("Error inesperado")
    else:
        print("Estado desconocido")

def cargar_desde_CSV():
    global inventario
    ruta = input("Ingrese la ruta del archivo CSV: ")
    respuesta = archivo.cargar_csv(ruta)
    if respuesta is None:
        print("No se encontraron productos válidos para cargar")
        return
    
    resp = input("¿Sobrescribir inventario actual? (S/N): ").strip().lower()
    agregados = 0
    actualizados = 0

    if resp == "s":
        inventario = respuesta
        agregados = len(respuesta)
        print(f"Inventario reemplazdo con {agregados} productos cargados desde csv")
    elif resp == "n":
        for fila in respuesta:
            producto = servicio.buscar_producto(inventario, fila["nombre"])
            if producto is not None:
                producto["cantidad"] += fila["cantidad"]
                if producto["precio"] != fila["precio"]:
                    producto["precio"] = fila["precio"]
                actualizados += 1
            else:
                inventario.append(fila)
                agregados += 1
        print(f"{agregados} productos agregados, {actualizados} productos actualizados desde CSV.")
                    
def estadísticas():
    respuesta = servicio.calcular_estadisticas(inventario)

    if not respuesta:
        print("No hay datos para mostrar.")
        return

    tabla = [
        ["Unidades totales", respuesta["unidades_totales"]],
        ["Valor total", respuesta["valor_total"]],
        ["Producto más caro", 
            respuesta["producto_mas_caro"]["nombre"] if respuesta["producto_mas_caro"] else "N/A"],
        ["Precio más caro", 
            respuesta["producto_mas_caro"]["precio"] if respuesta["producto_mas_caro"] else "N/A"],
        ["Producto mayor stock", 
            respuesta["producto_mayor_stock"]["nombre"] if respuesta["producto_mayor_stock"] else "N/A"],
        ["Cantidad mayor stock", 
            respuesta["producto_mayor_stock"]["cantidad"] if respuesta["producto_mayor_stock"] else "N/A"],
    ]

    print(tabulate(tabla, headers=["Estadística", "Valor"], tablefmt="grid"))



acciones = {
    1: agregar_al_inventario,
    2: mostrar_inventario,
    3: buscar_en_inventario,
    4: actualizar_inventario,
    5: eliminar_del_inventario,
    6: estadísticas,
    7: guardar_en_CSV,
    8: cargar_desde_CSV
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