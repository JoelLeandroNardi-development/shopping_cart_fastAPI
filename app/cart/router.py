from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from .schema import CartItemCreate, CartResponse
from .service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/{user_id}", response_model=CartResponse)
def create_cart(user_id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.create_cart(user_id)

@router.post("/{cart_id}/items")
def add_item(cart_id: int, data: CartItemCreate, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.add_item(cart_id, data.catalog_item_id, data.quantity)

@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.get_cart(cart_id)