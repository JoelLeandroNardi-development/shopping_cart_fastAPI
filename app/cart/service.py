from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.users.model import User
from app.catalog.model import CatalogItem
from .model import Cart, CartItem
from .dto import CartDTO, CartItemDTO

class CartService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, items_data: list):
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")
        cart = Cart(user_id=user_id)
        self.db.add(cart)
        self.db.flush()
        cart_items = self._build_cart_items(cart.id, items_data)
        cart.replace_items(cart_items)
        self.db.commit()
        self.db.refresh(cart)
        return self._map_to_dto(cart)

    def get(self, cart_id: int):
        cart = self.db.get(Cart, cart_id)
        if not cart:
            raise NotFoundException("Cart not found")
        return self._map_to_dto(cart)

    def list(self):
        carts = self.db.query(Cart).all()
        return [self._map_to_dto(c) for c in carts]

    def update(self, cart_id: int, items_data: list):
        cart = self.db.get(Cart, cart_id)
        if not cart:
            raise NotFoundException("Cart not found")
        cart_items = self._build_cart_items(cart.id, items_data)
        cart.replace_items(cart_items)
        self.db.commit()
        self.db.refresh(cart)
        return self._map_to_dto(cart)

    def delete(self, cart_id: int):
        cart = self.db.get(Cart, cart_id)
        if not cart:
            raise NotFoundException("Cart not found")
        self.db.delete(cart)
        self.db.commit()

    def _build_cart_items(self, cart_id: int, items_data: list):
        cart_items = []
        for item in items_data:
            catalog_item = self.db.get(CatalogItem, item.catalog_item_id)
            if not catalog_item:
                raise NotFoundException("Catalog item not found")
            cart_item = CartItem(
                cart_id=cart_id,
                catalog_item_id=item.catalog_item_id,
                quantity=item.quantity
            )
            cart_items.append(cart_item)
        return cart_items

    def _map_to_dto(self, cart: Cart):
        items_dto = []
        for item in cart.items:
            unit_price = float(item.catalog_item.price)
            total = unit_price * item.quantity
            items_dto.append(
                CartItemDTO(
                    id=item.id,
                    catalog_item_id=item.catalog_item_id,
                    quantity=item.quantity,
                    unit_price=unit_price,
                    total_price=total
                )
            )
        return CartDTO(
            id=cart.id,
            user_id=cart.user_id,
            total_price=cart.total_price,
            items=items_dto
        )