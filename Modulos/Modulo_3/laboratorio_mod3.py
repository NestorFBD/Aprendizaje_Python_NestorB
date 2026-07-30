from dataclasses import dataclass

from pydantic import BaseModel, ValidationError, field_validator


# ---------------------------------------------------------
# 1. ENTIDAD INTERNA (Dataclass)
# Aquí vive la lógica de negocio (Cálculos y comparaciones)
# ---------------------------------------------------------
@dataclass
class Order:
    producto_id: str
    precio: float
    cantidad: int

    # Propiedad calculada automáticamente
    @property
    def total(self) -> float:
        return self.precio * self.cantidad

    # Dunder method (__gt__ = Greater Than) para comparar dos órdenes
    def __gt__(self, otra_orden):
        return self.total > otra_orden.total


# ---------------------------------------------------------
# 2. MODELOS PYDANTIC (Validación y Serialización)
# Son los "filtros" de entrada y salida
# ---------------------------------------------------------


class OrderIn(BaseModel):
    """Filtro de Entrada: Valida datos crudos"""

    producto_id: str
    precio: float
    cantidad: int

    # Validamos que no nos vendan cantidades negativas o cero
    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(cls, valor):
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        return valor


class OrderOut(BaseModel):
    """Filtro de Salida: Lo que mostraremos al final"""

    producto_id: str
    total_a_pagar: float
    mensaje: str = "Gracias por su compra"


# ---------------------------------------------------------
# FLUJO DE TRABAJO
# ---------------------------------------------------------
def procesar_pedido(dato_crudo: dict):
    print(f"\n--- Procesando: {dato_crudo.get('producto_id', 'Desconocido')} ---")
    try:
        # 1. VALIDAR ENTRADA (OrderIn)
        entrada_validada = OrderIn(**dato_crudo)  # Desempaqueta el diccionario
        print("✅ Entrada válida:", entrada_validada.model_dump())

        # 2. CONVERTIR A ENTIDAD DE NEGOCIO (Dataclass Order)
        orden = Order(
            producto_id=entrada_validada.producto_id,
            precio=entrada_validada.precio,
            cantidad=entrada_validada.cantidad,
        )
        print(f"🧮 Lógica interna: Calculando total de la orden -> ${orden.total}")

        # 3. EMPAQUETAR PARA SALIDA (OrderOut)
        salida = OrderOut(producto_id=orden.producto_id, total_a_pagar=orden.total)
        # Serializamos (convertimos a texto JSON) para enviarlo
        print("📦 JSON de salida final:", salida.model_dump_json())

        return orden  # Devolvemos la entidad para poder compararla luego

    except ValidationError as e:
        # Pydantic nos dirá exactamente qué dato falló
        print("❌ Error de validación en los datos:")
        for error in e.errors():
            print(f"  - Campo '{error['loc'][0]}': {error['msg']}")
        return None


def main():
    # Simulamos datos crudos llegando desde una web o API
    datos_buenos = {"producto_id": "LAPTOP-X1", "precio": 1500.00, "cantidad": 2}
    datos_malos = {"producto_id": "MOUSE-BT", "precio": 25.50, "cantidad": 0}  # ¡Falla!

    orden_1 = procesar_pedido(datos_buenos)
    procesar_pedido(datos_malos)  # Lo ejecutamos solo para ver cómo falla Pydantic

    # Vamos a crear una tercera orden a mano para probar nuestro "Dunder method" de comparación
    orden_3 = Order(producto_id="TECLADO", precio=100.0, cantidad=5)  # Total 500

    if orden_1 and orden_3:
        print("\n--- Comparación usando Dunder Methods (__gt__) ---")
        if orden_1 > orden_3:
            print(
                f"La orden de {orden_1.producto_id} (${orden_1.total}) es MAYOR que la de {orden_3.producto_id} (${orden_3.total})"
            )
        else:
            print("La orden 3 es mayor.")


if __name__ == "__main__":
    main()
