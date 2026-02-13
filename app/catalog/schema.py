from pydantic import BaseModel, Field

class CatalogCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class CatalogUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class CatalogResponse(BaseModel):
    id: int
    name: str
    price: float