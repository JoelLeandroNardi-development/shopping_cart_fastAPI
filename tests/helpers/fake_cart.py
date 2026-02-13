class FakeCartItem:
    def __init__(self, cart_id: int, catalog_item_id: int, quantity: int):
        self.id = None
        self.cart_id = cart_id
        self.catalog_item_id = catalog_item_id
        self.quantity = quantity
        self.catalog_item = None

class FakeCart:
    def __init__(self, user_id: int, db=None):
        self.id = None
        self.user_id = user_id
        self.items = []
        self.total_price = 0.0
        self._db = db

    def replace_items(self, items):
        for idx, it in enumerate(items, start=1):
            it.id = getattr(it, "id", None) or idx
            catalog = self._db.storage.get(it.catalog_item_id)
            it.catalog_item = catalog
        self.items = items
        self.total_price = sum(float(i.catalog_item.price) * i.quantity for i in items)
