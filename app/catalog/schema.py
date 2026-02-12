from pydantic import BaseModel, Field

class CatalogItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class CatalogItemUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class CatalogItemResponse(BaseModel):
    id: int
    name: str
    price: float
    class Config:
        from_attributes = True