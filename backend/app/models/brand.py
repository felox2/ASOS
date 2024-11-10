import uuid
from datetime import datetime
from typing import Optional, Self, List

from pydantic import Field as PydanticField
from sqlmodel import Field, SQLModel, Relationship


class BrandPublic(SQLModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    photo: Optional[str] = None


class BrandBase(SQLModel):
    name: str = Field(min_length=2, index=True)
    description: Optional[str] = Field(default=None, max_length=500, nullable=True)
    photo: Optional[str] = Field(default=None, nullable=True)  


class Brand(BrandBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    products: List["Product"] = Relationship(back_populates="brand")

    


class BrandCreate(BrandBase):
    description: Optional[str] = None
    photo: Optional[str] = None
    name: str


class BrandUpdate(BrandBase):
    name: Optional[str] = PydanticField(min_length=2)
    description: Optional[str] = PydanticField(max_length=500)
    photo: Optional[str] = PydanticField() 


