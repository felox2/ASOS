import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import or_
from sqlmodel import select

from ..dependencies import AdminUser, CurrentUser, DbSession
from ..helpers.s3_connect import S3Connect
from ..middlewares.is_admin import admin_required
from ..models.brand import Brand, BrandCreate, BrandPublic, BrandUpdate
from ..models.product import ProductPublic

router = APIRouter(prefix="/api/brands", tags=["brands"])


@router.get("", response_model=List[BrandPublic])
async def read_brands(db: DbSession):
    brands = db.exec(select(Brand)).all()
    return brands


async def create_brand(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    photo: UploadFile = File(...),
    db: DbSession = None,
    user: AdminUser = None,
):
    brand_data = BrandCreate(name=name, description=description)

    brand = Brand.from_orm(brand_data)

    url = S3Connect.uploadFile(photo.file)

    brand.photo = url

    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@router.get("/{brand_id}", response_model=BrandPublic)
async def read_brand(brand_id: uuid.UUID, db: DbSession):
    brand = db.exec(select(Brand).where(Brand.id == brand_id)).first()
    return brand


@router.put("/{brand_id}", response_model=Brand)
async def update_brand(
    brand_id: uuid.UUID,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: DbSession = None,
    user: AdminUser = None,
):
    brand = db.exec(select(Brand).where(Brand.id == brand_id)).first()
    if brand:
        if name is not None:
            brand.name = name
        if description is not None:
            brand.description = description
        if photo is not None:
            url = S3Connect.uploadFile(photo.file)
            brand.photo = url

        db.add(brand)
        db.commit()
        db.refresh(brand)
    return brand


@router.delete("/{brand_id}", response_model=Brand)
async def delete_brand(brand_id: uuid.UUID, db: DbSession, user: AdminUser = None):
    brand = db.exec(select(Brand).where(Brand.id == brand_id)).first()
    if brand:
        db.delete(brand)
        db.commit()
    return brand
