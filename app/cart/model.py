from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="carts")
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )

    def replace_items(self, items: list["CartItem"]):
        self.items.clear()
        self.items.extend(items)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items)


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    catalog_item_id = Column(Integer, ForeignKey("catalog_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
    catalog_item = relationship("CatalogItem")

    @property
    def total_price(self):
        return float(self.catalog_item.price) * self.quantity

    def update(self, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        self.quantity = quantity