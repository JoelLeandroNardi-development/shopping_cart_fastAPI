class CatalogDTO:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = float(price)