import json
import re  # Librería para Expresiones Regulares


def procesar_ventas():
    # 1. Variables e inicialización (Alcance local)
    ventas_totales = 0.0
    ventas_completadas = []  # Esto es una Lista vacía

    # Expresión regular básica para validar correos
    patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    # 2. Control de excepciones (try-except)
    try:
        # Intentamos abrir el archivo JSON
        with open("datos.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)  # Lo convierte en una lista de diccionarios

        # 3. Control de flujo: for
        for venta in datos:
            # Validación con Expresiones Regulares
            if not re.match(patron_correo, venta["cliente"]):
                print(
                    f"⚠️ Alerta: El cliente ID {venta['id']} tiene un correo inválido."
                )

            # 4. Pattern matching (match - case) en lugar de muchos 'if'
            estado = venta.get("estado")
            match estado:
                case "completado":
                    ventas_totales += venta["monto"]
                    ventas_completadas.append(venta)  # Agregamos a la lista
                case "pendiente":
                    print(f"⏳ Venta ID {venta['id']} ignorada por estar pendiente.")
                case _:
                    # El guion bajo '_' significa "cualquier otro caso" (Default)
                    print(f"❓ Estado desconocido para ID {venta['id']}")

        # Mostrar resultados
        print("\n--- RESUMEN ---")
        print(f"Ventas totales confirmadas: ${ventas_totales}")
        print(f"Cantidad de ventas procesadas: {len(ventas_completadas)}")

    # ¡Plan B! Captura de errores específicos
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'datos.json'. Revisa la ruta.")
    except json.JSONDecodeError:
        print("❌ Error: El archivo datos.json está corrupto o mal escrito.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")


# Esto le dice a Python que ejecute la función si corremos este archivo directamente
if __name__ == "__main__":
    procesar_ventas()
