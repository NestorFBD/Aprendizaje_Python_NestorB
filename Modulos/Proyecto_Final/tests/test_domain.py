from src.domain.models import Order


def test_order_creation_is_pending():
    """Prueba que toda orden nueva nazca con status PENDING."""
    order = Order(id="123", customer="Fabian", amount=500.0)
    assert order.status == "PENDING"
    assert order.amount == 500.0


def test_order_apply_discount():
    """Prueba la lógica matemática del descuento."""
    order = Order(id="123", customer="Nestor", amount=1000.0)
    order.apply_discount(10.0)  # 10% de 1000 es 100

    assert order.amount == 900.0  # El monto final debe ser 900


def test_order_mark_as_completed():
    """Prueba el cambio de estado."""
    order = Order(id="123", customer="Evelia", amount=500.0)
    order.mark_as_completed()
    assert order.status == "COMPLETED"
