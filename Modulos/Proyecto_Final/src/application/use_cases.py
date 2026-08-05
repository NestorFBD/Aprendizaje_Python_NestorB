import uuid

from src.application.ports import OrderRepository
from src.domain.models import Order


class OrderService:
    """
    EL GENERAL: Orquesta el trabajo. Recibe la orden del usuario,
    aplica las reglas del Rey (Dominio) y usa a los Guardias (Puertos) para guardar.
    """

    # Inyección de dependencias (DIP): Recibe cualquier base de datos que cumpla el contrato
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, customer: str, amount: float) -> Order:
        # 1. Generamos un ID único automáticamente (ej. "a1b2c3d4")
        order_id = str(uuid.uuid4())[:8]

        # 2. Creamos la entidad
        new_order = Order(id=order_id, customer=customer, amount=amount)

        # 3. Lógica de negocio orquestada: Compras mayores a $1000 tienen 10% de descuento
        if amount > 1000:
            new_order.apply_discount(10.0)

        # 4. Guardamos usando el Puerto
        self.repository.save(new_order)

        return new_order

    def get_order(self, order_id: str) -> Order | None:
        return self.repository.get_by_id(order_id)

    def list_orders(self) -> list[Order]:
        return self.repository.list_all()
