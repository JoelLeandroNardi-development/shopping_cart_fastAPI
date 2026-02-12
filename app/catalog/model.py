from sqlalchemy import Column, Integer, String, Numeric
from app.core.database import Base

class CatalogItem(Base):
    __tablename__ = "catalog_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    def update(self, name: str, price: float):
        if not name or not name.strip():
            raise ValueError("Name is required")
        if price <= 0:
            raise ValueError("Price must be greater than zero")
        self.name = name
        self.price = price