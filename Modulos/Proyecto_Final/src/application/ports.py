from typing import Protocol

from src.domain.models import Order


class OrderRepository(Protocol):
    """
    EL PUERTO: El contrato de seguridad de la fortaleza.
    Cualquier base de datos (SQLite, Postgres, Memoria) que quiera conectarse
    a nuestro sistema, DEBE tener estas 3 funciones exactas.
    """

    def save(self, order: Order) -> None:
        ...

    def get_by_id(self, order_id: str) -> Order | None:
        ...

    def list_all(self) -> list[Order]:
        ...
