from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, DateTime, func, Table, Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.modules.product.model import Product

# Tabla de asociación Muchos a Muchos entre Listas de Favoritos y Productos
favorite_list_products = Table(
    "favorite_list_products",
    Base.metadata,
    Column(
        "favorite_list_id",
        PG_UUID(as_uuid=True),
        ForeignKey("favorite_lists.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "product_id",
        PG_UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True
    )
)

class FavoriteList(Base):
    __tablename__ = "favorite_lists"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    # Relación Muchos a Muchos con los productos guardados en esta lista
    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary=favorite_list_products,
        lazy="selectin"
    )