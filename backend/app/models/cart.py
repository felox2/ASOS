import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


class CartItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cart_id: uuid.UUID = Field(foreign_key="cart.id")
    product_id: uuid.UUID = Field(foreign_key="product.id")
    quantity: int = Field(default=1, ge=1)
    product: Optional["Product"] = Relationship(back_populates="cart_items")
    cart: "Cart" = Relationship(back_populates="items")


class Cart(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    session_id: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    items: List["CartItem"] = Relationship(back_populates="cart")
    user: Optional["User"] = Relationship(back_populates="cart")


class CartCreate(SQLModel):
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[str] = None


class CartRead(SQLModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    session_id: Optional[str]
    created_at: datetime
    modified_at: datetime
    items: List["CartItem"]


class CartItemCreate(SQLModel):
    product_id: uuid.UUID
    quantity: int = 1


class CartItemRead(SQLModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    product: Optional["Product"]

from .product import Product
from .users import User


