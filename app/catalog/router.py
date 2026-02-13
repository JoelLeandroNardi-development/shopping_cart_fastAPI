from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from .schema import CatalogCreate, CatalogUpdate, CatalogResponse
from .service import CatalogService

router = APIRouter(prefix="/catalog", tags=["Catalog"])

@router.post("/", response_model=CatalogResponse)
def create(data: CatalogCreate, db: Session = Depends(get_db)):
    return CatalogService(db).create(data.name, data.price)

@router.get("/{item_id}", response_model=CatalogResponse)
def get(item_id: int, db: Session = Depends(get_db)):
    return CatalogService(db).get(item_id)

@router.get("/", response_model=List[CatalogResponse])
def list_all(db: Session = Depends(get_db)):
    return CatalogService(db).list()

@router.put("/{item_id}", response_model=CatalogResponse)
def update(item_id: int, data: CatalogUpdate, db: Session = Depends(get_db)):
    return CatalogService(db).update(item_id, data.name, data.price)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    CatalogService(db).delete(item_id)
    return {"message": "Deleted successfully"}