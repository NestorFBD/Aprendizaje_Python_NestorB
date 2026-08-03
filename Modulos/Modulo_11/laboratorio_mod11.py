import sqlite3
from typing import Protocol


# =========================================================
# 1. EL ENCHUFE (Protocolo - Letra 'D' y 'I' de SOLID)
# =========================================================
class RepositorioOrdenes(Protocol):
    """Contrato: Cualquiera que quiera guardar órdenes DEBE tener este método exacto."""

    def guardar(self, orden: dict[str, str]) -> None:
        ...  # Los puntos suspensivos significan que aquí solo definimos la regla, no el código


# =========================================================
# 2. LOS ADAPTADORES (Letra 'O' y 'L' de SOLID)
# =========================================================
class RepositorioMemoria:
    """Opción A: Guarda datos en una lista temporal en la RAM."""

    def __init__(self) -> None:
        self.datos: list[dict[str, str]] = []

    def guardar(self, orden: dict[str, str]) -> None:
        self.datos.append(orden)
        print(f"📦 [Memoria RAM] Orden de '{orden['producto']}' guardada.")


class RepositorioSQLite:
    """Opción B: Guarda datos en una Base de Datos real."""

    def __init__(self) -> None:
        # Crea una DB en memoria que se borra al cerrar
        self.conexion = sqlite3.connect(":memory:")
        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS ordenes (id TEXT, producto TEXT)"
        )

    def guardar(self, orden: dict[str, str]) -> None:
        self.conexion.execute(
            "INSERT INTO ordenes VALUES (?, ?)", (orden["id"], orden["producto"])
        )
        self.conexion.commit()
        print(f"💽 [Base de Datos] Orden de '{orden['producto']}' guardada.")


# =========================================================
# 3. EL CÓDIGO PRINCIPAL (Letra 'S' de SOLID)
# =========================================================
class ServicioProcesadorOrdenes:
    """Responsabilidad Única: Solo procesa la orden lógica, no le importa cómo se guarda."""

    # INVERSIÓN DE DEPENDENCIAS: En lugar de "casarse" con SQLite o Memoria,
    # acepta cualquier cosa que cumpla con el Protocolo 'RepositorioOrdenes'
    def __init__(self, repositorio: RepositorioOrdenes) -> None:
        self.repositorio = repositorio

    def procesar(self, id_orden: str, producto: str) -> None:
        print(f"\n⚙️ Procesando nueva orden: {id_orden}...")

        # Aquí iría la lógica de negocio (validar precios, aplicar descuentos, etc.)
        orden_formateada = {"id": id_orden, "producto": producto}

        # Delegamos la responsabilidad de guardar al repositorio que nos hayan enchufado
        self.repositorio.guardar(orden_formateada)


# =========================================================
# EJECUCIÓN (El "Ensamblador")
# =========================================================
def main() -> None:
    print("--- INICIANDO SISTEMA CON ARQUITECTURA SOLID ---")

    # CASO 1: Para hacer pruebas rápidas, le enchufamos la Memoria
    repo_memoria = RepositorioMemoria()
    servicio_pruebas = ServicioProcesadorOrdenes(repo_memoria)
    servicio_pruebas.procesar("001", "Laptop")

    # CASO 2: Para producción, cambiamos a SQLite.
    # ¡OJO! No tuvimos que modificar ni una sola línea de la clase ServicioProcesadorOrdenes.
    # Eso demuestra que cumplimos el principio Open/Closed (Abierto/Cerrado).
    repo_sql = RepositorioSQLite()
    servicio_produccion = ServicioProcesadorOrdenes(repo_sql)
    servicio_produccion.procesar("002", "Monitor de 27 pulgadas")


if __name__ == "__main__":
    main()
