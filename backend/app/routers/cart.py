import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..dependencies import DbSession, UserOrSession, get_current_user_or_session
from ..models.cart import (
    Cart,
    CartCreate,
    CartItem,
    CartItemCreate,
    CartItemRead,
    CartRead,
)

from ..models.product import Product
from ..models.order import Order, OrderCreate, OrderItem, OrderItemCreate, OrderRead

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("", response_model=CartRead)
async def get_cart(
    current_user_or_session: UserOrSession = Depends(get_current_user_or_session),
    db: DbSession = None,
):
    if current_user_or_session.user is None:
        cart = db.exec(
            select(Cart).where(
                Cart.session_id == current_user_or_session.session_id,
                Cart.status == "active",
            )
        ).first()
    else:
        cart = db.exec(
            select(Cart).where(
                Cart.user_id == current_user_or_session.user.uid,
                Cart.status == "active",
            )
        ).first()

    if not cart:
        if current_user_or_session.session_id:
            cart = CartCreate(session_id=current_user_or_session.session_id)
        else:
            cart = CartCreate(user_id=current_user_or_session.user.uid)
        db_cart = Cart.from_orm(cart)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        return db_cart

    return cart


@router.post("/items", response_model=Optional[CartItemRead])
async def add_item_to_cart(
    item: CartItemCreate,
    current_user_or_session: UserOrSession = Depends(get_current_user_or_session),
    db: DbSession = None,
):
    if current_user_or_session.user is None:
        cart = db.exec(
            select(Cart).where(
                Cart.session_id == current_user_or_session.session_id,
                Cart.status == "active",
            )
        ).first()
    else:
        cart = db.exec(
            select(Cart).where(
                Cart.user_id == current_user_or_session.user.uid,
                Cart.status == "active",
            )
        ).first()

    if not cart:
        if current_user_or_session.session_id is not None:
            cart = CartCreate(session_id=current_user_or_session.session_id)
        else:
            cart = CartCreate(user_id=current_user_or_session.user.uid)
        db_cart = Cart.from_orm(cart)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        cart = db_cart

    if item.quantity == 0:
        cart_item = db.exec(
            select(CartItem).where(
                CartItem.cart_id == cart.id, CartItem.product_id == item.product_id
            )
        ).first()
        if cart_item:
            db.delete(cart_item)
            db.commit()

            return None

    try:
        existing_item = next(x for x in cart.items if x.product_id == item.product_id)
    except StopIteration:
        existing_item = None

    if existing_item is None:
        cart_item = CartItem(cart_id=cart.id, **item.dict())

        db.add(cart_item)
        db.commit()

        return cart_item

    existing_item.quantity = item.quantity

    db.add(existing_item)
    db.commit()

    return existing_item


@router.get("/{cart_id}/items", response_model=List[CartItemRead])
async def read_cart_items(cart_id: uuid.UUID, db: DbSession = None):
    cart = db.get(Cart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart.items


@router.post("/order", response_model=OrderRead)
async def create_order_from_cart(
    current_user_or_session: UserOrSession = Depends(get_current_user_or_session),
    db: DbSession = None,
):
    if current_user_or_session.user is None:
        cart = db.exec(
            select(Cart).where(
                Cart.session_id == current_user_or_session.session_id,
                Cart.status == "active",
            )
        ).first()
    else:
        cart = db.exec(
            select(Cart).where(
                Cart.user_id == current_user_or_session.user.uid,
                Cart.status == "active",
            )
        ).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=404, detail="Cart is empty or not found")

    order = OrderCreate(
        user_id=current_user_or_session.user.uid
        if current_user_or_session.user
        else None
    )
    db_order = Order.from_orm(order)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product.stock_quantity -= cart_item.quantity

        order_item = OrderItem(
            order_id=db_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
        )
        db.add(order_item)

    cart.status = "completed"
    db.commit()
    db.refresh(db_order)
    return db_order
