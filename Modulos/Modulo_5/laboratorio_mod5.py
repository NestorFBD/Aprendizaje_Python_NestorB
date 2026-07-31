import csv
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DEL LOGGING (Bitácora)
# ---------------------------------------------------------
# Configuramos la bitácora para que muestre: [Fecha/Hora] - [Nivel] - [Mensaje]
logging.basicConfig(
    level=logging.INFO,  # Mostramos desde INFO hacia arriba (INFO, WARNING, ERROR)
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ---------------------------------------------------------
# 2. MANEJO DE RUTAS UNIVERSALES CON PATHLIB
# ---------------------------------------------------------
# __file__ es este script. parent es la carpeta donde está (Modulo_5)
CARPETA_ACTUAL = Path(__file__).parent
ARCHIVO_ENTRADA = CARPETA_ACTUAL / "datos.csv"
ARCHIVO_SALIDA = CARPETA_ACTUAL / "reporte.json"


def procesar_inventario():
    logging.info("Iniciando el proceso de ingesta de datos.")

    # Verificamos que el CSV exista antes de intentar leerlo
    if not ARCHIVO_ENTRADA.exists():
        logging.error(f"No se encontró el archivo: {ARCHIVO_ENTRADA.name}")
        return

    datos_procesados = []
    total_inventario = 0.0

    try:
        # 3. PARSEO DE CSV
        with open(ARCHIVO_ENTRADA, mode="r", encoding="utf-8") as archivo_csv:
            lector = csv.DictReader(archivo_csv)

            for fila in lector:
                # Extraemos y convertimos los datos
                producto = fila["producto"]
                precio = float(fila["precio"])
                cantidad = int(fila["cantidad"])

                if cantidad == 0:
                    logging.warning(f"Producto sin stock detectado: {producto}")
                    continue  # Saltamos este producto

                subtotal = precio * cantidad
                total_inventario += subtotal

                # Agregamos los datos procesados a nuestra lista
                datos_procesados.append(
                    {
                        "producto": producto,
                        "precio_unitario": precio,
                        "stock": cantidad,
                        "subtotal": subtotal,
                    }
                )

        logging.info(
            f"Ingesta exitosa. Se procesaron {len(datos_procesados)} productos."
        )

    except Exception as e:
        logging.error(f"Error al leer el CSV: {e}")
        return

    # 4. EXPORTACIÓN A JSON CON DATETIME
    reporte_final = {
        # Guardamos la fecha/hora exacta en formato universal (UTC)
        "fecha_reporte": datetime.now(UTC).isoformat(),
        "total_valor_inventario": total_inventario,
        "productos": datos_procesados,
    }

    try:
        with open(ARCHIVO_SALIDA, mode="w", encoding="utf-8") as archivo_json:
            json.dump(reporte_final, archivo_json, indent=4)
        logging.info(f"Reporte exportado exitosamente a: {ARCHIVO_SALIDA.name}")

    except Exception as e:
        logging.error(f"Error al exportar el JSON: {e}")


if __name__ == "__main__":
    procesar_inventario()
