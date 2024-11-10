# routers/cart.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
import uuid

from ..models.cart import Cart, CartRead, CartItem, CartItemCreate, CartItemRead, CartCreate
from ..dependencies import get_current_user_or_session, DbSession

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", response_model=CartRead)
async def create_cart(
    current_user_or_session: str = Depends(get_current_user_or_session),
    db: DbSession = None
):
    cart = CartCreate()
    if isinstance(current_user_or_session, str):
        cart.session_id = current_user_or_session
    else:
        cart.user_id = current_user_or_session.id
    db_cart = Cart.from_orm(cart)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

@router.get("/{cart_id}", response_model=CartRead)
async def read_cart(cart_id: uuid.UUID, db: DbSession = None):
    cart = db.get(Cart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/{cart_id}/items", response_model=CartItemRead)
async def add_item_to_cart(
    cart_id: uuid.UUID,
    item: CartItemCreate,
    db: DbSession = None
):
    cart = db.get(Cart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = CartItem(cart_id=cart_id, **item.dict())
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/{cart_id}/items", response_model=List[CartItemRead])
async def read_cart_items(cart_id: uuid.UUID, db: DbSession = None):
    cart = db.get(Cart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart.items