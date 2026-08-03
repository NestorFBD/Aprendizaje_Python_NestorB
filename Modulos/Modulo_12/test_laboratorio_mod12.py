from typing import Protocol

# =========================================================
# 1. PATRÓN COMPORTAMIENTO: Strategy (Estrategia)
# Problema: Calcular precios con reglas diferentes sin llenar todo de "ifs"
# =========================================================


class EstrategiaDescuento(Protocol):
    """El contrato para cualquier fórmula de descuento."""

    def aplicar(self, precio: float) -> float:
        ...


class DescuentoVIP:
    """Estrategia 1: 20% de descuento."""

    def aplicar(self, precio: float) -> float:
        return precio * 0.8


class DescuentoNavidad:
    """Estrategia 2: 50% de descuento (mitad de precio)."""

    def aplicar(self, precio: float) -> float:
        return precio * 0.5


class CalculadoraPrecios:
    """El cajero: Toma el precio y le inyecta la estrategia elegida."""

    def calcular_total(self, precio: float, estrategia: EstrategiaDescuento) -> float:
        return estrategia.aplicar(precio)


# =========================================================
# 2. PATRÓN ESTRUCTURAL: Decorator (Decorador - Patrón Idiomático)
# Problema: Queremos recordar (Cachear) un cálculo lento para no repetirlo
# =========================================================


def decorador_cache(func):
    """Guarda en memoria las respuestas de una función para darlas al instante."""
    memoria_cache = {}

    def envoltura(numero):
        if numero in memoria_cache:
            # ¡Si ya lo calculó antes, lo saca del caché!
            return memoria_cache[numero]

        # Si es la primera vez, ejecuta la función original y lo guarda
        resultado = func(numero)
        memoria_cache[numero] = resultado
        return resultado

    return envoltura


@decorador_cache
def calculo_pesado(numero: int) -> str:
    """Simula una tarea lenta."""
    return f"Procesado: {numero}"


# =========================================================
# 3. PATRÓN ESTRUCTURAL: Adapter (Adaptador)
# Problema: Un proveedor externo de datos nos manda información en un formato raro
# =========================================================


class ProveedorExternoFeo:
    """Imagina que no podemos modificar esta clase porque es de un tercero."""

    def get_info_rara(self) -> str:
        return "100.50|USD|LAPTOP"


class AdaptadorProveedor:
    """El Adaptador: Traduce el formato raro a un diccionario limpio para nuestro código."""

    def __init__(self, proveedor_externo: ProveedorExternoFeo):
        self.proveedor = proveedor_externo

    def obtener_datos_limpios(self) -> dict:
        datos_crudos = self.proveedor.get_info_rara()
        precio, moneda, producto = datos_crudos.split(
            "|"
        )  # Separamos por la línea vertical
        return {"producto": producto, "precio": float(precio), "moneda": moneda}


# =========================================================
# PRUEBAS AUTOMATIZADAS (Pytest)
# =========================================================


def test_patron_strategy():
    calculadora = CalculadoraPrecios()
    precio_base = 100.0

    # Cambiamos la "estrategia matemática" sobre la marcha
    assert calculadora.calcular_total(precio_base, DescuentoVIP()) == 80.0
    assert calculadora.calcular_total(precio_base, DescuentoNavidad()) == 50.0


def test_patron_decorator_cache():
    # La primera vez lo procesa normal
    assert calculo_pesado(5) == "Procesado: 5"
    # La segunda vez entra al caché (aunque no podamos medir el tiempo aquí, sabemos que la lógica funciona)
    assert calculo_pesado(5) == "Procesado: 5"


def test_patron_adapter():
    # Enchufamos la clase fea dentro de nuestro adaptador bonito
    proveedor_feo = ProveedorExternoFeo()
    mi_adaptador = AdaptadorProveedor(proveedor_feo)

    resultado = mi_adaptador.obtener_datos_limpios()

    # Verificamos que el adaptador hizo bien su traducción
    assert resultado["producto"] == "LAPTOP"
    assert resultado["precio"] == 100.50
    assert resultado["moneda"] == "USD"
