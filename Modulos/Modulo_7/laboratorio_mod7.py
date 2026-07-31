from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


# ---------------------------------------------------------
# 1. CONFIGURACIÓN BASE (El molde principal del ORM)
# ---------------------------------------------------------
class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# 2. MODELADO DE ENTIDADES (Tablas de la Base de Datos)
# ---------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    # Columnas
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    # Relación: Un usuario tiene MUCHAS órdenes (Lista)
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relación: Una orden pertenece a UN usuario
    user: Mapped["User"] = relationship(back_populates="orders")
    # Relación: Una orden tiene MUCHOS ítems (Lista)
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_name: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int]

    # Relación: Un ítem pertenece a UNA orden
    order: Mapped["Order"] = relationship(back_populates="items")


# ---------------------------------------------------------
# 3. EJECUCIÓN DEL CRUD EN SQLITE EN MEMORIA
# ---------------------------------------------------------
def ejecutar_crud() -> None:
    # Creamos el motor de Base de Datos (en la memoria RAM)
    engine = create_engine("sqlite:///:memory:", echo=False)

    # Alembic se usa para bases de datos reales.
    # Para pruebas en memoria, le decimos a SQLAlchemy que cree las tablas directamente:
    Base.metadata.create_all(engine)
    print("✅ Tablas creadas en la memoria RAM.")

    # Abrimos una Sesión (nuestra conexión para hablar con la base de datos)
    with Session(engine) as session:
        # --- C: CREATE (Crear) ---
        print("\n--- CREATE ---")
        nuevo_usuario = User(name="Néstor")
        nueva_orden = Order(user=nuevo_usuario)
        OrderItem(product_name="Monitor 27 pulgadas", quantity=2, order=nueva_orden)
        OrderItem(product_name="Teclado Mecánico", quantity=1, order=nueva_orden)

        # Guardamos en la base de datos
        session.add(nuevo_usuario)
        session.commit()
        print(f"Usuario {nuevo_usuario.name} guardado con el ID {nuevo_usuario.id}")

        # --- R: READ (Leer) ---
        print("\n--- READ ---")
        # Hacemos un SELECT * FROM users WHERE name = 'Néstor'
        consulta = select(User).where(User.name == "Néstor")
        usuario_db = session.execute(consulta).scalar_one()

        print(f"Usuario encontrado: {usuario_db.name}")
        for orden in usuario_db.orders:
            print(f"  Orden ID {orden.id} tiene {len(orden.items)} ítems:")
            for item in orden.items:
                print(f"    - {item.quantity}x {item.product_name}")

        # --- U: UPDATE (Actualizar) ---
        print("\n--- UPDATE ---")
        item_a_modificar = usuario_db.orders[0].items[0]
        item_a_modificar.quantity = 5  # Cambiamos la cantidad de 2 a 5
        session.commit()
        print(
            f"Cantidad actualizada de {item_a_modificar.product_name} a {item_a_modificar.quantity}"
        )

        # --- D: DELETE (Borrar) ---
        print("\n--- DELETE ---")
        session.delete(
            usuario_db
        )  # Por el cascade="all", borrará también las órdenes e ítems
        session.commit()
        print("Usuario borrado de la base de datos.")

    print(
        "\n✅ Fin de la prueba. Al cerrarse el script, la base de datos en RAM desapareció."
    )


if __name__ == "__main__":
    ejecutar_crud()
