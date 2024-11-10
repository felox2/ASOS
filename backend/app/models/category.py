import uuid
from datetime import datetime
from typing import Optional, Self

from pydantic import Field as PydanticField
from sqlmodel import Field, SQLModel



class AssociationProductCategory(SQLModel, table=True):
    product_id: Optional[uuid.UUID] = Field(default=None, foreign_key="product.id", primary_key=True)
    category_id: Optional[uuid.UUID] = Field(default=None, foreign_key="category.id", primary_key=True)

class CategoryPublic(SQLModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    photo: Optional[str] = None

class CategoryBase(SQLModel):
    name: str = Field(min_length=2, index=True)
    description: Optional[str] = Field(default=None, max_length=500, nullable=True)
    photo: Optional[str] = Field(default=None, nullable=True)  


class Category(CategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)


class CategoryCreate(CategoryBase):
    description: Optional[str] = None
    photo: Optional[str] = None
    name: str


class CategoryUpdate(CategoryBase):
    name: Optional[str] = PydanticField(min_length=2)
    description: Optional[str] = PydanticField(max_length=500)
    photo: Optional[str] = PydanticField() 

