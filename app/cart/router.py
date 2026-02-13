from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from .schema import CartCreate, CartUpdate, CartResponse
from .service import CartService

router = APIRouter(prefix="/carts", tags=["Carts"])

@router.post("/", response_model=CartResponse)
def create(data: CartCreate, db: Session = Depends(get_db)):
    return CartService(db).create(data.user_id, data.items)

@router.get("/{cart_id}", response_model=CartResponse)
def get(cart_id: int, db: Session = Depends(get_db)):
    return CartService(db).get(cart_id)

@router.get("/", response_model=List[CartResponse])
def list_all(db: Session = Depends(get_db)):
    return CartService(db).list()

@router.put("/{cart_id}", response_model=CartResponse)
def update(cart_id: int, data: CartUpdate, db: Session = Depends(get_db)):
    return CartService(db).update(cart_id, data.items)

@router.delete("/{cart_id}")
def delete(cart_id: int, db: Session = Depends(get_db)):
    CartService(db).delete(cart_id)
    return {"message": "Deleted successfully"}