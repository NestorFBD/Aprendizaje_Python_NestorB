from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database import Base


class OrderORM(Base):
    """La representación de la tabla 'orders' en la base de datos."""

    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    customer: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="PENDING")
