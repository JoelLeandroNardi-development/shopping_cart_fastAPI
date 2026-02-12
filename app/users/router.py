from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from .schema import UserCreate, UserUpdate, UserResponse
from .service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create(data: UserCreate, db: Session = Depends(get_db)):
    return UserService(db).create(data.name, data.phone_number)

@router.get("/", response_model=List[UserResponse])
def list_all(db: Session = Depends(get_db)):
    return UserService(db).get_all()

@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return UserService(db).update(user_id, data.name, data.phone_number)

@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    UserService(db).delete(user_id)
    return {"message": "Deleted successfully"}