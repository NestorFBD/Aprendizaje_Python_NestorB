def aplicar_descuento(precio: float, porcentaje_descuento: float) -> float:
    """Aplica un descuento a un precio. (Validando que no haya precios negativos)"""
    if precio < 0 or porcentaje_descuento < 0 or porcentaje_descuento > 100:
        raise ValueError("Valores inválidos para el descuento")

    descuento = precio * (porcentaje_descuento / 100)
    return precio - descuento


def consultar_precio_en_bd(item_id: int) -> float:
    """Imagina que esta función hace un 'SELECT' lentísimo a una Base de Datos real."""
    # Como es un ejemplo, esto daría error si lo corremos de verdad
    raise NotImplementedError("No hay base de datos conectada")


def obtener_precio_final(item_id: int, descuento: float) -> float:
    """Busca el precio en la BD y le aplica el descuento."""
    precio_base = consultar_precio_en_bd(item_id)
    return aplicar_descuento(precio_base, descuento)
