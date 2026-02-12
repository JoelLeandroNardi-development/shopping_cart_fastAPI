from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    shopping_carts = relationship("ShoppingCart", back_populates="user")

    def update(self, name: str, phone_number: str):
        if not name or not name.strip():
            raise ValueError("Name is required")
        self.name = name
        self.phone_number = phone_number