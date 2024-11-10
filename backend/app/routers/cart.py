from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
import uuid

from ..models.cart import Cart, CartRead, CartItem, CartItemCreate, CartItemRead, CartCreate
from ..models.order import Order, OrderCreate, OrderItem, OrderItemCreate, OrderRead
from ..dependencies import get_current_user_or_session, DbSession, UserOrSession

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartRead)
async def get_cart(
    current_user_or_session: UserOrSession = Depends(get_current_user_or_session),
    db: DbSession = None
):
    if current_user_or_session.user is None:
        cart = db.exec(select(Cart).where(Cart.session_id == current_user_or_session.session_id, Cart.status == "active")).first()
    else:
        cart = db.exec(select(Cart).where(Cart.user_id == current_user_or_session.user.uid, Cart.status == "active")).first()
    
    if not cart:
        if current_user_or_session.is_session():
            cart = CartCreate(session_id=current_user_or_session.session_id)
        else:
            cart = CartCreate(user_id=current_user_or_session.user.uid)
        db_cart = Cart.from_orm(cart)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        return db_cart
    
    return cart

@router.post("/items", response_model=CartItemRead)
async def add_item_to_cart(
    item: CartItemCreate,
    current_user_or_session: UserOrSession = Depends(get_current_user_or_session),
    db: DbSession = None
):
    if current_user_or_session.user is None:
        cart = db.exec(select(Cart).where(Cart.session_id == current_user_or_session.session_id, Cart.status == "active")).first()
    else:
        cart = db.exec(select(Cart).where(Cart.user_id == current_user_or_session.user.uid, Cart.status == "active")).first()
    
    if not cart:
        if current_user_or_session.is_session():
            cart = CartCreate(session_id=current_user_or_session.session_id)
        else:
            cart = CartCreate(user_id=current_user_or_session.user.uid)
        db_cart = Cart.from_orm(cart)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        cart = db_cart

    if item.quantity == 0:
        cart_item = db.exec(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id)).first()
        if cart_item:
            db.delete(cart_item)
            db.commit()
            return cart_item

    cart_item = CartItem(cart_id=cart.id, **item.dict())
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

@router.post("/order", response_model=OrderRead)
async def create_order_from_cart(
    current_user_or_session: UserOrSession = Depends(get_current_user_or_session),
    db: DbSession = None
):
    if current_user_or_session.user is None:
        cart = db.exec(select(Cart).where(Cart.session_id == current_user_or_session.session_id, Cart.status == "active")).first()
    else:
        cart = db.exec(select(Cart).where(Cart.user_id == current_user_or_session.user.uid, Cart.status == "active")).first()
    
    if not cart or not cart.items:
        raise HTTPException(status_code=404, detail="Cart is empty or not found")

    order = OrderCreate(user_id=current_user_or_session.user.uid if current_user_or_session.is_user() else None)
    db_order = Order.from_orm(order)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for cart_item in cart.items:
        order_item = OrderItem(order_id=db_order.id, product_id=cart_item.product_id, quantity=cart_item.quantity)
        db.add(order_item)
    
    cart.status = "completed"  
    db.commit()
    db.refresh(db_order)
    return db_order