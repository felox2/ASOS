import os
import shutil
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import or_
from sqlmodel import select

from ..dependencies import AdminUser, CurrentUser, DbSession
from ..helpers.s3_connect import S3Connect
from ..middlewares.is_admin import admin_required
from ..models.category import (
    AssociationProductCategory,
    Category,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
)
from ..models.product import ProductPublic

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=List[CategoryPublic])
async def read_categories(db: DbSession):
    categories = db.exec(select(Category)).all()
    return categories


@router.post("", response_model=Category)
async def create_category(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    photo: UploadFile = File(...),
    db: DbSession = None,
    user: AdminUser = None,
):
    category_data = CategoryCreate(name=name, description=description)

    category = Category.from_orm(category_data)

    url = S3Connect.uploadFile(photo.file)

    category.photo = url

    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/{category_id}", response_model=CategoryPublic)
async def read_category(category_id: uuid.UUID, db: DbSession):
    category = db.exec(select(Category).where(Category.id == category_id)).first()
    return category


@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: uuid.UUID,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: DbSession = None,
    user: AdminUser = None,
):
    category = db.exec(select(Category).where(Category.id == category_id)).first()
    if category:
        if name is not None:
            category.name = name
        if description is not None:
            category.description = description
        if photo is not None:
            url = S3Connect.uploadFile(photo.file)
            category.photo = url

        db.add(category)
        db.commit()
        db.refresh(category)
    return category


@router.delete("/{category_id}", response_model=CategoryPublic)
async def delete_category(
    category_id: uuid.UUID, db: DbSession, user: AdminUser = None
):
    category = db.exec(select(Category).where(Category.id == category_id)).first()
    if category:
        db.delete(category)
        db.commit()
    return category
