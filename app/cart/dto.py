class CartItemDTO:
    def __init__(
        self,
        id: int,
        catalog_item_id: int,
        quantity: int,
        unit_price: float,
        total_price: float
    ):
        self.id = id
        self.catalog_item_id = catalog_item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price

class CartDTO:
    def __init__(
        self, 
        id: int, 
        user_id: int, 
        total_price: float, 
        items: list[CartItemDTO]
    ):
        self.id = id
        self.user_id = user_id
        self.total_price = total_price
        self.items = items