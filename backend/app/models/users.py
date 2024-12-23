import uuid
from datetime import datetime
from typing import Optional, Self, List

from pydantic import BaseModel, EmailStr, model_validator
from pydantic import Field as PydanticField
from sqlmodel import Field, Relationship, SQLModel, Relationship


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    name: str = Field(min_length=2)


class UserTokenData(UserBase):
    uid: uuid.UUID
    is_admin: bool


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: uuid.UUID = Field(unique=True, index=True)
    password_hash: str = Field()
    is_admin: bool = Field(default=False)

    sessions: list["Session"] = Relationship(back_populates="user")

    created_at: datetime = Field(default=datetime.now())
    modified_at: datetime = Field(default=datetime.now())
    cart: "Cart" = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    uid: uuid.UUID
    is_admin: bool


class UserCreate(UserBase):
    password: str = PydanticField(min_length=6)
    password_repeat: str = PydanticField()

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("passwords do not match")
        return self


class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    refresh_token: str = Field()

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="sessions")

    expires_at: datetime = Field()
    created_at: datetime = Field(default=datetime.now())
    modified_at: datetime = Field(default=datetime.now())

from .cart import Cart
from .order import Order
