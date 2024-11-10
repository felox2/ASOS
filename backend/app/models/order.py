import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship
from .product import Product
from .users import User


class OrderItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(foreign_key="order.id")
    product_id: uuid.UUID = Field(foreign_key="product.id")
    quantity: int = Field(default=1, ge=1)
    product: Optional[Product] = Relationship(back_populates="order_items")
    order: "Order" = Relationship(back_populates="items")


class Order(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    items: List[OrderItem] = Relationship(back_populates="order")
    user: Optional[User] = Relationship(back_populates="orders")


class OrderCreate(SQLModel):
    user_id: Optional[uuid.UUID] = None


class OrderRead(SQLModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    created_at: datetime
    modified_at: datetime
    items: List[OrderItem]


class OrderItemCreate(SQLModel):
    product_id: uuid.UUID
    quantity: int


class OrderItemRead(SQLModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    product: Optional[Product]