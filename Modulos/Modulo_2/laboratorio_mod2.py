import time
from contextlib import contextmanager
from functools import wraps


# ---------------------------------------------------------
# 1. CONTEXT MANAGER: Temporizador
# ---------------------------------------------------------
@contextmanager
def temporizador(nombre_proceso):
    """Mide cuánto tarda en ejecutarse un bloque de código."""
    inicio = time.time()
    yield  # Aquí es donde ocurre la magia (el código dentro del 'with')
    fin = time.time()
    print(f"⏱️ [Temporizador] '{nombre_proceso}' tomó {fin - inicio:.4f} segundos.\n")


# ---------------------------------------------------------
# 2. DECORADOR: Reintentos con Backoff
# ---------------------------------------------------------
def reintentar_con_backoff(intentos=3, espera_inicial=1):
    """Si una función falla, lo vuelve a intentar esperando cada vez más tiempo."""

    def decorador(func):
        @wraps(func)
        def envoltura(*args, **kwargs):
            espera = espera_inicial
            for i in range(intentos):
                try:
                    # Intenta ejecutar la función original
                    return func(*args, **kwargs)
                except Exception as e:
                    print(
                        f"⚠️ Intento {i + 1} falló: {e}. Reintentando en {espera}s..."
                    )
                    time.sleep(espera)
                    espera *= 2  # Backoff: multiplicamos el tiempo por 2

            # Si agota los intentos, lanza un error final
            raise Exception("❌ La función falló después de todos los reintentos.")

        return envoltura

    return decorador


# ---------------------------------------------------------
# 3. GENERADOR: Procesador por lotes (Batches)
# ---------------------------------------------------------
def generador_lotes(datos, tamaño_lote):
    """Toma una lista gigante y la entrega en pedazos (lotes)."""
    for i in range(0, len(datos), tamaño_lote):
        # 'yield' devuelve el lote y pausa la función hasta que se pida el siguiente
        yield datos[i : i + tamaño_lote]


# =========================================================
# PRUEBA DEL LABORATORIO
# =========================================================


# Simulamos una función inestable (ej. descargar datos de una API que se cae)
# Le aplicamos nuestro decorador simplemente poniéndolo arriba con un '@'
@reintentar_con_backoff(intentos=3, espera_inicial=1)
def descargar_datos_inestables():
    # Simulamos un fallo usando un poco de lógica aleatoria
    import random

    if random.choice([True, False]):
        raise ValueError("¡Error de conexión con la base de datos!")
    return [
        "Dato " + str(i) for i in range(1, 106)
    ]  # Comprensión de lista (Crea 105 datos)


def main():
    print("--- INICIANDO LABORATORIO MÓDULO 2 ---\n")

    # Usamos nuestro Context Manager con la palabra 'with'
    with temporizador("Proceso completo de descarga y guardado"):
        try:
            print("1. Intentando descargar datos...")
            datos_completos = descargar_datos_inestables()
            print("✅ Datos descargados exitosamente.\n")

            print("2. Procesando datos por lotes (Generador)...")
            # Usamos el generador para iterar sobre lotes de 20 en 20
            for numero_lote, lote in enumerate(
                generador_lotes(datos_completos, tamaño_lote=20), start=1
            ):
                print(f"📦 Guardando Lote {numero_lote} con {len(lote)} registros.")
                time.sleep(0.1)  # Simulamos que tarda un poco en guardar

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
