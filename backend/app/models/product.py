import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import Field as PydanticField, root_validator
from sqlmodel import Field, SQLModel, Relationship



class Photo(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str = Field(nullable=False)
    product_id: uuid.UUID = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="photos")


class ProductBase(SQLModel):
    name: str = Field(min_length=2, index=True)
    description: Optional[str] = Field(default=None, max_length=500, nullable=True)
    price: float = Field(gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    photo: Optional[str] = Field(default=None, nullable=True)
    brand_id: Optional[uuid.UUID] = Field(default=None, foreign_key="brand.id")


class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    brand: Optional["Brand"] = Relationship(back_populates="products")
    photos: List[Photo] = Relationship(back_populates="product")
    cart_items: List["CartItem"] = Relationship(back_populates="product") 


class ProductPublic(ProductBase):
    id: uuid.UUID
    created_at: datetime
    modified_at: datetime
    brand: Optional["BrandPublic"]
    additional_photos: List[str]
    
    @root_validator(pre=True)
    def populate_fields(cls, values):
        brand = values.get('brand')
        photos = values.get('photos', [])
        values['brand'] = BrandPublic(**brand) if brand else None
        values['additional_photos'] = [photo.url for photo in photos]
        return values


class ProductCreate(SQLModel):
    name: str
    description: Optional[str] = Field(default=None, max_length=500, nullable=True)
    price: float = Field(gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    photo: Optional[str] = Field(default=None, nullable=True)
    brand_id: Optional[uuid.UUID] = Field(default=None)


from .brand import Brand
from .brand import BrandPublic
from .cart import CartItem


