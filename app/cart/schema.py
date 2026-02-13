from pydantic import BaseModel, Field
from typing import List

class CartItemCreate(BaseModel):
    catalog_item_id: int
    quantity: int = Field(..., gt=0)

class CartCreate(BaseModel):
    user_id: int
    items: List[CartItemCreate]

class CartUpdate(BaseModel):
    items: List[CartItemCreate]

class CartItemResponse(BaseModel):
    id: int
    catalog_item_id: int
    quantity: int
    unit_price: float
    total_price: float

class CartResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    items: List[CartItemResponse]