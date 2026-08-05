from dataclasses import dataclass


@dataclass
class Order:
    """
    EL REY: La entidad central de nuestro sistema.
    Representa una Orden de compra.
    """

    id: str
    customer: str
    amount: float
    status: str = "PENDING"  # Toda orden nace como 'Pendiente'

    def apply_discount(self, percentage: float) -> None:
        """Regla de negocio 1: Aplicar descuentos válidos."""
        if percentage > 0 and self.amount > 0:
            descuento = self.amount * (percentage / 100)
            self.amount -= descuento

    def mark_as_completed(self) -> None:
        """Regla de negocio 2: Completar la orden."""
        self.status = "COMPLETED"
