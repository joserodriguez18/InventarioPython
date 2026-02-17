import csv

GUARDADO = "guardado"
INVENTARIO_VACIO = "inventario_vacio"
ERROR_RUTA = "ruta"
ERROR_PERMISO = "permiso"
ERROR_DATOS = "datos"
ERROR_GENERAL = "general"


def guardar_csv(inventario, ruta, incluir_header=True):
    if not inventario:
        return INVENTARIO_VACIO
    try:
        with open(ruta, mode="w", newline="", encoding="utf-8") as f:
            fieldnames = ["nombre", "precio", "cantidad"]
            w = csv.DictWriter(f, fieldnames=fieldnames)
            if incluir_header:
                w.writeheader()
            w.writerows(inventario)
        return GUARDADO
    except FileNotFoundError:
        return ERROR_RUTA
    except PermissionError:
        return ERROR_PERMISO
    except ValueError:
        return ERROR_DATOS
    except Exception:
        return ERROR_GENERAL


def cargar_csv(ruta):
    inventario = []
    filas_invalidas = 0

    try:
        with open(ruta, newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            # Validar encabezado
            encabezados = lector.fieldnames
            if encabezados != ["nombre", "precio", "cantidad"]:
                print("Encabezado inválido. Debe ser: nombre, precio, cantidad")
                return []

            for fila in lector:
                # Validar que tenga 3 columnas
                if len(fila) != 3:
                    filas_invalidas += 1
                    continue

                try:
                    precio = float(fila["precio"])
                    cantidad = int(fila["cantidad"])

                    if precio < 0 or cantidad < 0:
                        filas_invalidas += 1
                        continue

                    inventario.append(
                        {
                            "nombre": fila["nombre"],
                            "precio": precio,
                            "cantidad": cantidad,
                        }
                    )

                except ValueError:
                    filas_invalidas += 1
                    continue

        print(f"Filas inválidas omitidas: {filas_invalidas}")
        return inventario

    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []
    except UnicodeDecodeError:
        print("Error de codificación en el archivo.")
        return []
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return []
