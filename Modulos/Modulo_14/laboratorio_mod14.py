from dataclasses import dataclass
from typing import Protocol

# =========================================================
# 🛡️ CAPA 1: DOMINIO (El Núcleo / El Rey)
# Cero librerías externas. Python puro. Reglas de negocio.
# =========================================================


@dataclass
class Order:
    id: str
    cliente: str
    monto: float

    def aplicar_descuento_cliente_frecuente(self) -> None:
        """Regla de negocio: Si el monto es mayor a 100, se descuenta 10%"""
        if self.monto > 100:
            self.monto = self.monto * 0.90


# =========================================================
# 🛡️ CAPA 2: PUERTOS (Los Guardias de la fortaleza)
# Definimos CÓMO debe comunicarse el mundo exterior con nosotros.
# =========================================================


class OrderRepository(Protocol):
    """Puerto para hablar con la Base de Datos"""

    def guardar(self, order: Order) -> None:
        ...


class NotificationService(Protocol):
    """Puerto para hablar con el sistema de correos o alertas"""

    def enviar_alerta(self, mensaje: str) -> None:
        ...


# =========================================================
# 🛡️ CAPA 3: APLICACIÓN (Casos de Uso / Los Generales)
# Orquestan el proceso usando los Puertos.
# =========================================================


class CreateOrderUseCase:
    # INYECCIÓN DE DEPENDENCIAS: Le pasamos los puertos por el constructor
    def __init__(self, repo: OrderRepository, notifier: NotificationService):
        self.repo = repo
        self.notifier = notifier

    def ejecutar(self, id_orden: str, cliente: str, monto: float) -> Order:
        print("\n⚙️ [Caso de Uso] Iniciando creación de orden...")

        # 1. Creamos la entidad del Dominio
        nueva_orden = Order(id=id_orden, cliente=cliente, monto=monto)

        # 2. Aplicamos lógica de negocio (Dominio)
        nueva_orden.aplicar_descuento_cliente_frecuente()

        # 3. Usamos la Infraestructura a través de los Puertos
        self.repo.guardar(nueva_orden)
        self.notifier.enviar_alerta(
            f"Nueva orden creada para {cliente} por ${nueva_orden.monto:.2f}"
        )

        return nueva_orden


# =========================================================
# 🌍 CAPA 4: INFRAESTRUCTURA (Los Adaptadores / El Mundo Exterior)
# Aquí va el código "sucio" (Bases de datos reales, APIs, etc.)
# =========================================================


class InMemoryOrderRepository:
    """Adaptador de Base de Datos temporal (Para desarrollo/Pruebas)"""

    def __init__(self) -> None:
        self.db: list[Order] = []

    def guardar(self, order: Order) -> None:
        self.db.append(order)
        print(f"💽 [Infra - BD Memoria] Orden {order.id} guardada en RAM.")


class HttpNotificationMock:
    """Adaptador de Notificaciones (Simula enviar un Whatsapp o Email HTTP)"""

    def enviar_alerta(self, mensaje: str) -> None:
        # Aquí usaríamos la librería 'httpx' del Módulo 6 para hacer un POST a una API real
        print(f"📱 [Infra - API Externa] Haciendo POST HTTP simulado: '{mensaje}'")


# =========================================================
# 🔌 MAIN (El "Wiring" o Ensamblador)
# El único lugar donde juntamos todas las piezas reales.
# =========================================================
def main() -> None:
    print("--- ARQUITECTURA HEXAGONAL INICIADA ---")

    # 1. Preparamos los Adaptadores de Infraestructura (Instanciamos)
    repositorio_real = InMemoryOrderRepository()
    notificador_real = HttpNotificationMock()

    # 2. Inyectamos los adaptadores en nuestro Caso de Uso (Wiring)
    caso_uso = CreateOrderUseCase(repo=repositorio_real, notifier=notificador_real)

    # 3. Ejecutamos como si fuéramos un usuario desde una web o consola
    # Al ser >100, se le aplicará el descuento del 10%
    caso_uso.ejecutar(id_orden="A-001", cliente="Néstor", monto=150.0)

    # Al ser <100, no se le aplica descuento
    caso_uso.ejecutar(id_orden="A-002", cliente="Nubia", monto=80.0)


if __name__ == "__main__":
    main()
