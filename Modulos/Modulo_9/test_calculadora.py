from unittest.mock import patch

import pytest
from calculadora import aplicar_descuento, obtener_precio_final
from hypothesis import given
from hypothesis import strategies as st


# ---------------------------------------------------------
# 1. PARAMETRIZACIÓN (Probar varios escenarios a la vez)
# ---------------------------------------------------------
@pytest.mark.parametrize(
    "precio_inicial, descuento, precio_esperado",
    [
        (100.0, 20.0, 80.0),  # Caso normal
        (50.0, 0.0, 50.0),  # Sin descuento
        (200.0, 100.0, 0.0),  # Todo gratis
    ],
)
def test_aplicar_descuento_casos_normales(precio_inicial, descuento, precio_esperado):
    resultado = aplicar_descuento(precio_inicial, descuento)
    assert resultado == precio_esperado


def test_aplicar_descuento_errores():
    # Probamos que nuestra función SÍ lance un error si le metemos basura
    with pytest.raises(ValueError):
        aplicar_descuento(-50.0, 10.0)


# ---------------------------------------------------------
# 2. MOCKING (Simular la Base de Datos con un doble de acción)
# ---------------------------------------------------------
# Le decimos que "falsifique" (patch) la función 'consultar_precio_en_bd'
@patch("calculadora.consultar_precio_en_bd")
def test_obtener_precio_final_con_mock(mock_bd):
    # Le decimos al actor falso: "Cuando te llamen, responde que el precio es 1000"
    mock_bd.return_value = 1000.0

    # Llamamos a la función. ¡No se conectará a la BD real, usará el actor falso!
    resultado = obtener_precio_final(item_id=99, descuento=10.0)

    assert resultado == 900.0
    # Verificamos que nuestro código sí intentó llamar a la BD con el ID 99
    mock_bd.assert_called_once_with(99)


# ---------------------------------------------------------
# 3. HYPOTHESIS (Property-based testing: números aleatorios)
# ---------------------------------------------------------
# Hypothesis generará cientos de precios (entre 0 y 1 millón) y descuentos (0 a 100)
@given(
    precio=st.floats(min_value=0.0, max_value=1000000.0),
    descuento=st.floats(min_value=0.0, max_value=100.0),
)
def test_propiedad_descuento_nunca_aumenta_precio(precio, descuento):
    """Propiedad matemática: Un precio con descuento NUNCA puede ser mayor al precio original."""
    precio_final = aplicar_descuento(precio, descuento)
    assert precio_final <= precio
