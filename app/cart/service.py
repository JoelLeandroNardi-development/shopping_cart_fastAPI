from sqlalchemy.orm import Session
from .model import ShoppingCart, ShoppingCartItem
from app.catalog.model import CatalogItem

class CartService:
    def __init__(self, db: Session):
        self.db = db

    def create_cart(self, user_id: int):
        cart = ShoppingCart(user_id=user_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def add_item(self, cart_id: int, catalog_item_id: int, quantity: int):
        catalog_item = self.db.get(CatalogItem, catalog_item_id)

        if not catalog_item:
            raise ValueError("Catalog item not found")

        item = ShoppingCartItem(
            cart_id=cart_id,
            catalog_item=catalog_item,
        )
        item.update(quantity)

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_cart(self, cart_id: int):
        return self.db.get(ShoppingCart, cart_id)