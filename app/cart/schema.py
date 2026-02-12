from pydantic import BaseModel, Field
from typing import List

class CartItemCreate(BaseModel):
    catalog_item_id: int
    quantity: int = Field(..., gt=0)

class CartItemResponse(BaseModel):
    id: int
    catalog_item_id: int
    quantity: int
    total_price: float
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    items: List[CartItemResponse]
    class Config:
        from_attributes = True