from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlmodel import select
from sqlalchemy import or_
from typing import List, Optional
from ..models.category import Category, AssociationProductCategory, CategoryPublic, CategoryCreate, CategoryUpdate
from ..models.product import ProductPublic
from ..dependencies import CurrentUser, DbSession
from ..middlewares.is_admin import admin_required
from ..helpers.s3_connect import S3Connect
import uuid
import shutil
import os

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryPublic])
async def read_categories(db: DbSession):
    categories = db.exec(select(Category)).all()
    return categories


@router.post("/", response_model=CategoryPublic, dependencies=[Depends(admin_required)])
async def create_category(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    photo: UploadFile = File(...),
    db: DbSession = None
):
    category_data = CategoryCreate(
        name=name,
        description=description
    )

    category = Category.from_orm(category_data)

    url = S3Connect.upload_fileobj(photo.file, photo.filename)

    category.photo = url
    
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/{category_id}", response_model=CategoryPublic)
async def read_category(category_id: uuid.UUID, db: DbSession ):
    category = db.exec(select(Category).where(Category.id == category_id)).first()
    return category

@router.put("/{category_id}", response_model=CategoryPublic, dependencies=[Depends(admin_required)])
async def update_category(
    category_id: uuid.UUID,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: DbSession = None
):
    category = db.exec(select(Category).where(Category.id == category_id)).first()
    if category:
        if name is not None:
            category.name = name
        if description is not None:
            category.description = description
        if photo is not None:
            url = S3Connect.upload_fileobj(photo.file, photo.filename)
            category.photo = url 

        db.add(category)
        db.commit()
        db.refresh(category)
    return category

@router.delete("/{category_id}", response_model=CategoryPublic, dependencies=[Depends(admin_required)])
async def delete_category(category_id: uuid.UUID, db: DbSession ):
    category = db.exec(select(Category).where(Category.id == category_id)).first()
    if category:
        db.delete(category)
        db.commit()
    return category