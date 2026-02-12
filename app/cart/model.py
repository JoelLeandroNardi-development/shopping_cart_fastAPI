from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="shopping_carts")
    items = relationship(
        "ShoppingCartItem",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items)


class ShoppingCartItem(Base):
    __tablename__ = "shopping_cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"))
    catalog_item_id = Column(Integer, ForeignKey("catalog_items.id"))
    quantity = Column(Integer)

    catalog_item = relationship("CatalogItem")

    @property
    def total_price(self):
        return float(self.catalog_item.price) * self.quantity

    def update(self, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        self.quantity = quantity