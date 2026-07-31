import logging
import time
from pathlib import Path

import httpx

# Configuramos la bitácora (logging) del módulo 5
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def descargar_reporte_streaming(url: str, archivo_destino: Path) -> None:
    """
    Descarga un archivo grande desde internet usando streaming (pedazo a pedazo)
    e implementando resiliencia (Timeouts y Reintentos).
    """
    intentos_maximos = 3
    tiempo_espera = 2  # Segundos de espera entre intentos (backoff)

    # 1. TIMEOUTS:
    # 5.0 = Máximo 5 seg para conectar. 10.0 = Máximo 10 seg para leer datos
    timeout_personalizado = httpx.Timeout(5.0, read=10.0)

    for intento in range(1, intentos_maximos + 1):
        try:
            logging.info(
                f"Intento {intento} de {intentos_maximos} - Conectando a la API..."
            )

            # 2. CLIENTE HTTP ROBUSTO con "with" (Context Manager del módulo 2)
            with httpx.Client(timeout=timeout_personalizado) as cliente:
                # 3. STREAMING: Pedimos conectarnos a la URL en modo "fluido"
                with cliente.stream("GET", url) as respuesta:
                    # Verificamos si el servidor respondió con error (ej. Error 404 No Encontrado)
                    respuesta.raise_for_status()

                    # Abrimos un archivo local para escribir 'gota a gota' ('wb' = write binary)
                    with open(archivo_destino, "wb") as archivo_local:
                        # Descargamos en pedacitos (chunks) de 1024 bytes (1 KB) a la vez
                        archivo_local.writelines(respuesta.iter_bytes(chunk_size=1024))

            logging.info(
                f"✅ ¡Éxito! Archivo guardado correctamente en: {archivo_destino.name}"
            )
            return  # Salimos de la función porque ya terminamos

        except httpx.HTTPStatusError as e:
            # Errores del servidor (404, 500, etc.). Aquí no vale la pena reintentar.
            logging.error(f"❌ Error de Servidor. El servidor dijo: {e}")
            break

        except httpx.RequestError as e:
            # Errores de internet o Timeout. Aquí SÍ vale la pena reintentar.
            logging.warning(f"⚠️ Error de red o Timeout: {e}")
            if intento < intentos_maximos:
                logging.info(f"Reintentando en {tiempo_espera} segundos...")
                time.sleep(tiempo_espera)
                tiempo_espera *= 2  # Backoff (Módulo 2)
            else:
                logging.error(
                    "❌ Se agotaron los reintentos. Fallo total en la descarga."
                )


def main() -> None:
    # Ahora usamos una API de la NASA Astronomy Picture of the Day (devuelve un texto JSON)
    url_api = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

    carpeta_actual = Path(__file__).parent
    # Cambiamos el nombre a .json para que VS Code lo entienda
    ruta_guardado = carpeta_actual / "reporte_nasa.json"

    descargar_reporte_streaming(url=url_api, archivo_destino=ruta_guardado)


if __name__ == "__main__":
    main()
