import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

import httpx

# =========================================================
# PARTE 1: E/S BOUND (Descargas de Internet)
# =========================================================
# Usamos un servidor de prueba que tarda 1 segundo exacto en responder
URL_API = "https://httpbin.org/delay/1"
CANTIDAD_PETICIONES = 5


def descargar_sincrono():
    """Modo normal (Síncrono): Espera a que termine una para iniciar otra."""
    print("Iniciando descargas SÍNCRONAS...")
    with httpx.Client() as cliente:
        for i in range(CANTIDAD_PETICIONES):
            cliente.get(URL_API)
            print(f"  - Descarga {i + 1} terminada.")


async def descargar_un_archivo(
    cliente: httpx.AsyncClient, i: int, semaforo: asyncio.Semaphore
):
    """Tarea individual del chef (Asíncrona)."""
    # El semáforo controla que no saturemos la red
    async with semaforo:
        await cliente.get(URL_API)
        print(f"  - Descarga {i + 1} asíncrona terminada.")


async def descargar_asincrono():
    """Modo chef (Concurrencia): Lanza todas juntas y aprovecha los tiempos muertos."""
    print("\nIniciando descargas ASÍNCRONAS (asyncio)...")
    semaforo = asyncio.Semaphore(10)  # Máximo 10 a la vez

    async with httpx.AsyncClient(timeout=20.0) as cliente:
        # Preparamos todas las tareas a la vez
        tareas = [
            descargar_un_archivo(cliente, i, semaforo)
            for i in range(CANTIDAD_PETICIONES)
        ]
        # ¡Las lanzamos todas al mismo tiempo!
        await asyncio.gather(*tareas)


# =========================================================
# PARTE 2: CPU BOUND (Cálculos Matemáticos)
# =========================================================
def calculo_matematico_pesado(numero: int) -> int:
    """Una tarea que hace sufrir al procesador (suma de cuadrados)."""
    return sum(i * i for i in range(numero))


def procesar_cpu_paralelo():
    """Paralelismo real: Usa los núcleos de tu computadora para dividir el trabajo."""
    print("\nIniciando cálculo matemático en PARALELO...")
    numeros = [10_000_000, 10_000_000, 10_000_000, 10_000_000]  # 4 tareas pesadas

    # ProcessPoolExecutor crea "clones" de tu programa en diferentes núcleos del CPU
    with ProcessPoolExecutor() as ejecutor:
        # map() reparte los números entre los núcleos automáticamente
        resultados = list(ejecutor.map(calculo_matematico_pesado, numeros))
    print(f"  - Resultados de los cálculos: {resultados}")


# =========================================================
# EJECUCIÓN PRINCIPAL CON CRONÓMETRO (timeit casero)
# =========================================================
def main():
    print("--- PRUEBA DE RENDIMIENTO ---")

    # 1. Prueba Síncrona
    inicio_sync = time.time()
    descargar_sincrono()
    print(f"⏳ Tiempo Síncrono: {time.time() - inicio_sync:.2f} segundos")

    # 2. Prueba Asíncrona (¡Mira la magia de la velocidad!)
    inicio_async = time.time()
    asyncio.run(descargar_asincrono())  # Así se arranca una función 'async'
    print(f"⏳ Tiempo Asíncrono: {time.time() - inicio_async:.2f} segundos")

    # 3. Prueba Paralela (CPU)
    inicio_cpu = time.time()
    procesar_cpu_paralelo()
    print(f"⏳ Tiempo Paralelo: {time.time() - inicio_cpu:.2f} segundos")


# En Windows, usar multiprocessing obliga a tener esta línea sí o sí
if __name__ == "__main__":
    main()
