from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone_number = Column(String(50), nullable=False)

    carts = relationship("Cart", back_populates="user")

    def update(self, name: str, phone_number: str):
        if not name.strip():
            raise ValueError("Name is required")
        self.name = name
        self.phone_number = phone_number