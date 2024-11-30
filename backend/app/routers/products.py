import uuid
from asyncio import sleep
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from sqlalchemy import or_
from sqlalchemy.sql.expression import delete
from sqlmodel import select

from ..dependencies import AdminUser, CurrentUser, DbSession
from ..helpers.s3_connect import S3Connect
from ..models.brand import Brand
from ..models.category import AssociationProductCategory
from ..models.product import Photo, Product, ProductCreate, ProductPublic

router = APIRouter(prefix="/api/products", tags=["products"])

STOCK_LIVE_FREQUENCY_SECONDS = 1


@router.get("", response_model=List[ProductPublic])
async def read_products(
    db: DbSession = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    category_ids: Optional[List[uuid.UUID]] = Query(None),
    brand_ids: Optional[List[uuid.UUID]] = Query(None),
):
    offset = (page - 1) * page_size
    query = select(Product)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(Product.name.ilike(search_term), Product.description.ilike(search_term))
        )

    if category_ids:
        query = query.join(AssociationProductCategory).where(
            AssociationProductCategory.category_id.in_(category_ids)
        )

    if brand_ids:
        query = query.where(Product.brand_id.in_(brand_ids))

    products = db.exec(query.offset(offset).limit(page_size)).all()

    response_products = []
    for product in products:
        photos_query = select(Photo).where(Photo.product_id == product.id)
        additional_photos = db.exec(photos_query).all()

        product_dict = product.model_dump()

        all_photos = []
        all_photos.extend(photo for photo in additional_photos)

        product_dict["photos"] = all_photos

        brand_query = select(Brand).where(Brand.id == product.brand_id)
        brand = db.exec(brand_query).first()
        if brand is not None:
            product_dict["brand"] = brand.model_dump()

        response_products.append(ProductPublic(**product_dict))

    return response_products


@router.post("", response_model=Product)
async def create_product(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    stock_quantity: int = Form(...),
    photo: UploadFile = File(...),
    brand_id: Optional[uuid.UUID] = Form(None),
    category_ids: Optional[List[uuid.UUID]] = Form(None),
    db: DbSession = None,
    user: AdminUser = None,
):
    product_data = ProductCreate(
        name=name,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        brand_id=brand_id,
    )

    product = Product.from_orm(product_data)

    url = S3Connect.uploadFile(photo.file)
    product.photo = url

    db.add(product)
    db.commit()
    db.refresh(product)

    if category_ids:
        for category_id in category_ids:
            association = AssociationProductCategory(
                product_id=product.id, category_id=category_id
            )
            db.add(association)
        db.commit()

    return product


@router.get("/{product_id}", response_model=ProductPublic)
async def read_product(product_id: uuid.UUID, db: DbSession):
    product = db.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    photos_query = select(Photo).where(Photo.product_id == product.id)
    additional_photos = db.exec(photos_query).all()

    product_dict = product.model_dump()
    all_photos = []
    all_photos.extend(photo for photo in additional_photos)
    product_dict["photos"] = all_photos

    brand_query = select(Brand).where(Brand.id == product.brand_id)
    brand = db.exec(brand_query).first()
    if brand is not None:
        product_dict["brand"] = brand.model_dump()

    return ProductPublic(**product_dict)


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: uuid.UUID,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    stock_quantity: Optional[int] = Form(None),
    photo: Optional[UploadFile] = File(None),
    brand_id: Optional[uuid.UUID] = Form(None),
    category_ids: Optional[List[uuid.UUID]] = Form(None),
    db: DbSession = None,
    user: AdminUser = None,
):
    product = db.exec(select(Product).where(Product.id == product_id)).first()
    if product:
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if stock_quantity is not None:
            product.stock_quantity = stock_quantity
        if photo is not None:
            url = S3Connect.uploadFile(photo.file)
            product.photo = url
        if brand_id is not None:
            product.brand_id = brand_id

        if category_ids is not None:
            db.exec(
                delete(AssociationProductCategory).where(
                    AssociationProductCategory.product_id == product_id
                )
            )
            for category_id in category_ids:
                association = AssociationProductCategory(
                    product_id=product_id, category_id=category_id
                )
                db.add(association)

        db.add(product)
        db.commit()
        db.refresh(product)
    return product


@router.delete("/{product_id}", response_model=Product)
async def delete_product(product_id: uuid.UUID, db: DbSession, user: AdminUser = None):
    product = db.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return product


@router.get("/{product_id}/stock")
async def stream_product_stock(product_id: uuid.UUID, db: DbSession):
    async def stock_generator():
        while True:
            product = db.exec(select(Product).where(Product.id == product_id)).first()
            if not product:
                break

            db.refresh(product)
            yield f"event: stockUpdate\ndata: {product.stock_quantity}\n\n"
            await sleep(STOCK_LIVE_FREQUENCY_SECONDS)

    return StreamingResponse(stock_generator(), media_type="text/event-stream")
