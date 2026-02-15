from tabulate import tabulate
def mostrar_inventario(inventario):
    if not inventario:
        return None
    return tabulate(inventario, headers="keys", tablefmt="grid")


def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario si no existe previamente.

    Parámetros:
    - inventario (list): lista de diccionarios que representan los productos.
    - nombre (str): nombre del producto a agregar.
    - precio (float o str convertible a float): precio unitario del producto.
    - cantidad (int o str convertible a int): cantidad disponible del producto.

    Retorna:
    - True: si el producto fue agregado correctamente.
    - False: si el producto ya existe en el inventario y no se agregó.
    """
    producto = buscar_producto(inventario, nombre)
    if producto is not None:
        return False

    add_producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }
    inventario.append(add_producto)
    return True


def buscar_producto(inventario, nombre):
    """
    Busca un producto en el inventario por su nombre.

    Parámetros:
    - inventario (list): lista de diccionarios con los productos.
    - nombre (str): nombre del producto a buscar.

    Retorna:
    - dict: el diccionario del producto encontrado.
    - None: si no se encuentra el producto.
    """
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o la cantidad de un producto existente.

    Parámetros:
    - inventario (list): lista de diccionarios con los productos.
    - nombre (str): nombre del producto a actualizar.
    - nuevo_precio (float, opcional): nuevo precio del producto. Si es None, no se actualiza.
    - nueva_cantidad (int, opcional): nueva cantidad del producto. Si es None, no se actualiza.

    Retorna:
    - True: si el producto fue actualizado.
    - False: si no se encontró el producto.
    """
    producto = buscar_producto(inventario, nombre)
    if producto is not None:
        if nuevo_precio is not None:
            producto["precio"] = nuevo_precio
        if nueva_cantidad is not None:
            producto["cantidad"] = nueva_cantidad
        return True
    return False


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por su nombre.

    Parámetros:
    - inventario (list): lista de diccionarios con los productos.
    - nombre (str): nombre del producto a eliminar.

    Retorna:
    - True: si el producto fue eliminado.
    - False: si no se encontró el producto.
    """
    producto = buscar_producto(inventario, nombre)
    if producto is not None:
        inventario.remove(producto)
        return True
    return False


def calcular_estadisticas(inventario):
    """
    Calcula estadísticas del inventario.

    Parámetros:
    - inventario: lista de diccionarios con productos.

    Retorna: diccionario con:
    - unidades_totales: suma de todas las unidades.
    - valor_total: suma de precio * cantidad de todos los productos.
    - producto_mas_caro: dict con nombre y precio del producto más caro.
    - producto_mayor_stock: dict con nombre y cantidad del producto con más unidades.
    """
    unidades_totales = sum(producto["cantidad"] for producto in inventario)
    valor_total = sum(
        producto["precio"] * producto["cantidad"] for producto in inventario
    )
    producto_mas_caro = max(inventario, key=lambda p: p["precio"], default=None)
    if producto_mas_caro:
        producto_mas_caro = {
            "nombre": producto_mas_caro["nombre"],
            "precio": producto_mas_caro["precio"],
        }
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"], default=None)
    if producto_mayor_stock:
        producto_mayor_stock = {
            "nombre": producto_mayor_stock["nombre"],
            "cantidad": producto_mayor_stock["cantidad"],
        }
    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock,
    }
