from sqlalchemy.orm import Session
from src.domain.models import Order
from src.infrastructure.orm_models import OrderORM


class SQLAlchemyOrderRepository:
    """El Adaptador que cumple con el Puerto 'OrderRepository' del Módulo 14."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, order: Order) -> None:
        # Convertimos Dominio -> ORM
        db_order = OrderORM(
            id=order.id,
            customer=order.customer,
            amount=order.amount,
            status=order.status,
        )
        self.db.merge(db_order)  # merge funciona como "Insertar o Actualizar"
        self.db.commit()

    def get_by_id(self, order_id: str) -> Order | None:
        db_order = self.db.query(OrderORM).filter(OrderORM.id == order_id).first()
        if db_order:
            # Convertimos ORM -> Dominio
            return Order(
                id=db_order.id,
                customer=db_order.customer,
                amount=db_order.amount,
                status=db_order.status,
            )
        return None

    def list_all(self) -> list[Order]:
        db_orders = self.db.query(OrderORM).all()
        return [
            Order(id=o.id, customer=o.customer, amount=o.amount, status=o.status)
            for o in db_orders
        ]
