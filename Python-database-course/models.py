from datetime import datetime
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy import ForeignKey, BIGINT, INTEGER
from sqlalchemy import String
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declared_attr
from typing_extensions import Annotated
from typing import Optional

# User ForeignKey
user_fk = Annotated[int, mapped_column(
    BIGINT, ForeignKey("users.telegram_id", ondelete="CASCADE"))]

# integer primary key
int_pk = Annotated[int, mapped_column(INTEGER, primary_key=True)]

# string column with length 255
str_255 = Annotated[str, mapped_column(String(255))]


# Creating a base class
class Base(DeclarativeBase):
    pass


class TableNameMixin:

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now())


class User(Base, TableNameMixin, TimestampMixin):
    """Users table"""

    telegram_id: Mapped[int] = mapped_column(
        BIGINT, nullable=False, primary_key=True)
    full_name: Mapped[str_255]
    username: Mapped[Optional[str_255]]
    language_code: Mapped[str_255]
    referrer_id: Mapped[Optional[user_fk]]
    order_id = Mapped[int_pk]
    user_id = Mapped[user_fk]


class Product(Base, TimestampMixin, TableNameMixin):
    """Products table"""

    product_id: Mapped[int_pk]
    title: Mapped[str_255]
    description: Mapped[str]


class Order(Base, TimestampMixin, TableNameMixin):
    """Orders table"""

    order_id: Mapped[int_pk]
    user_id: Mapped[user_fk]


class OrderProduct(Base, TableNameMixin):
    """Association table for Orders """

    order_id: Mapped[int] = mapped_column(INTEGER, ForeignKey(
        "orders.order_id", ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[int] = mapped_column(INTEGER, ForeignKey(
        "products.product_id", ondelete="RESTRICT"), primary_key=True)
    quantity: Mapped[int]

    # order = relationship("Order", back_populates="order_products")
    # product = relationship("Product", back_populates="order_products")
