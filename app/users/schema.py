from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    phone_number: str

class UserUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    phone_number: str

class UserResponse(BaseModel):
    id: int
    name: str
    phone_number: str