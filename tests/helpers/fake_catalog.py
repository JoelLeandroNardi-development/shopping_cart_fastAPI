class FakeCatalogItem:
    def __init__(self, id_=None, price=None):
        self.id = id_
        self.price = price
        self.name = None

    def update(self, name: str, price: float):
        if not name.strip():
            raise ValueError("Name is required")
        if price <= 0:
            raise ValueError("Price must be greater than zero")
        self.name = name
        self.price = price
