# Importamos las herramientas de tipado avanzado
from typing import Literal, TypedDict


# 1. TypedDict: Definimos la estructura exacta de nuestro diccionario de datos
class Venta(TypedDict):
    id: int
    cliente: str
    # 2. Literal: El estado SOLO puede ser una de estas tres palabras
    estado: Literal["completado", "pendiente", "cancelado"]
    monto: float


# 3. Type hints en funciones:
# Recibe una 'Venta' y devuelve un 'float' O un 'None' (vacío)
def procesar_venta(venta: Venta) -> float | None:
    if venta["estado"] == "completado":
        # Simulamos que le agregamos un impuesto
        total_con_impuesto: float = venta["monto"] * 1.16
        return total_con_impuesto

    # Si no está completado, no hay dinero que sumar
    return None


def main() -> None:  # main no devuelve nada (None)
    # Creamos un dato que cumple perfectamente el TypedDict
    venta_valida: Venta = {
        "id": 1,
        "cliente": "nestor@correo.com",
        "estado": "completado",
        "monto": 100.0,
    }

    print("--- Probando Tipado Estático ---")
    resultado = procesar_venta(venta_valida)
    print(f"Venta válida procesada. Total: ${resultado}")


if __name__ == "__main__":
    main()
