from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from .schema import (
    CatalogItemCreate,
    CatalogItemUpdate,
    CatalogItemResponse,
)
from .service import CatalogService

router = APIRouter(prefix="/catalog", tags=["Catalog"])

@router.post("/", response_model=CatalogItemResponse)
def create(data: CatalogItemCreate, db: Session = Depends(get_db)):
    return CatalogService(db).create(data.name, data.price)

@router.get("/", response_model=List[CatalogItemResponse])
def list_all(db: Session = Depends(get_db)):
    return CatalogService(db).get_all()

@router.put("/{item_id}", response_model=CatalogItemResponse)
def update(item_id: int, data: CatalogItemUpdate, db: Session = Depends(get_db)):
    return CatalogService(db).update(item_id, data.name, data.price)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    CatalogService(db).delete(item_id)
    return {"message": "Deleted successfully"}