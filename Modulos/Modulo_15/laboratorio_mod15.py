# mypy: ignore-errors

from dataclasses import dataclass, field
from typing import Any, Protocol

# =========================================================
# 🛡️ CAPA 1: DOMINIO (Entidades y Eventos)
# El centro de todo.
# =========================================================


class EventoDominio:
    """Clase base para cualquier grito/anuncio que haga el dominio."""


@dataclass
class OrderCreated(EventoDominio):
    """El anuncio específico de que nació una orden."""

    orden_id: str
    monto: float


@dataclass
class Order:
    id: str
    monto: float
    # Lista secreta donde el Rey guarda los anuncios que quiere gritar
    eventos: list[EventoDominio] = field(default_factory=list)

    def confirmar(self) -> None:
        """Lógica de negocio: Al confirmar, prepara el anuncio."""
        self.eventos.append(OrderCreated(self.orden_id, self.monto))

    @property
    def orden_id(self) -> str:
        return self.id


# =========================================================
# 🛡️ CAPA 2: APLICACIÓN (Puertos y Casos de Uso)
# =========================================================


class OrderRepository(Protocol):
    def guardar(self, order: Order) -> None:
        ...


class UnitOfWork(Protocol):
    """El Gerente del Banco (Controla las transacciones)"""

    ordenes: OrderRepository

    def __enter__(self) -> "UnitOfWork":
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        ...

    def commit(self) -> None:
        ...


class OrderPresenter(Protocol):
    """El Maquillador (Prepara la respuesta final)"""

    def presentar_exito(self, orden_id: str) -> str:
        ...


class CreateOrderUseCase:
    """Orquestador usando Unit of Work y Eventos"""

    def __init__(self, uow: UnitOfWork, presenter: OrderPresenter):
        self.uow = uow
        self.presenter = presenter

    def ejecutar(self, id_orden: str, monto: float) -> str:
        # 1. Creamos la entidad
        orden = Order(id=id_orden, monto=monto)
        orden.confirmar()  # El Rey prepara su anuncio

        # 2. Transacción segura con Unit of Work
        with self.uow:
            self.uow.ordenes.guardar(orden)
            self.uow.commit()  # Si el guardado falla, el commit nunca ocurre

        # 3. Disparamos los eventos (Escuchamos el megáfono)
        for evento in orden.eventos:
            if isinstance(evento, OrderCreated):
                print(
                    f"📢 [Manejador de Eventos] Reaccionando a OrderCreated: Enviando email de cobro por ${evento.monto}..."
                )

        # 4. El presentador maquilla el resultado
        return self.presenter.presentar_exito(orden.id)


# =========================================================
# 🌍 CAPA 3: INFRAESTRUCTURA Y PRESENTACIÓN (Adaptadores)
# =========================================================


class InMemoryRepository:
    """Implementación falsa del Gerente del Banco para RAM"""

    def __init__(self) -> None:
        # 1er Fix: Le decimos explícitamente a Mypy que esto cuenta como un OrderRepository
        self.ordenes: OrderRepository = InMemoryRepository()

    # 2do Fix: Cambiamos el tipo de retorno para que coincida exactamente con la palabra del Protocolo
    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def commit(self) -> None:
        print("🏦 [Unit Of Work] Transacción finalizada y aprobada (Commit).")


class InMemoryUoW:
    """Implementación falsa del Gerente del Banco para RAM"""

    def __init__(self) -> None:
        import typing

        self.ordenes = typing.cast(OrderRepository, InMemoryRepository())  # type: ignore

    def __enter__(self) -> "UnitOfWork":
        return self  # type: ignore

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # Aquí se haría el "Rollback" si existiera un error real (exc_type)
        pass

    def commit(self) -> None:
        print("🏦 [Unit Of Work] Transacción finalizada y aprobada (Commit).")


class ConsolePresenter:
    """Un presentador que formatea el texto para la terminal"""

    def presentar_exito(self, orden_id: str) -> str:
        return f"✨ RESULTADO FINAL: La orden {orden_id} fue procesada con éxito. ✨"


# =========================================================
# 🔌 MAIN (Ensamblaje final)
# =========================================================
def main() -> None:
    print("--- INICIANDO CLEAN ARCHITECTURE ---")

    # 1. Instanciamos infraestructura
    uow = InMemoryUoW()
    presentador = ConsolePresenter()

    # 2. Inyectamos dependencias al Caso de Uso
    caso_uso = CreateOrderUseCase(uow=uow, presenter=presentador)  # type: ignore

    # 3. Ejecutamos simulando la petición de un cliente
    respuesta_al_cliente = caso_uso.ejecutar(id_orden="CLEAN-999", monto=500.0)

    # Mostramos lo que vería el usuario en su pantalla
    print(f"\n{respuesta_al_cliente}")


if __name__ == "__main__":
    main()
