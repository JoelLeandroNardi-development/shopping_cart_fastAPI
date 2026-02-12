from sqlalchemy.orm import Session
from .model import CatalogItem

class CatalogService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, price: float):
        item = CatalogItem()
        item.update(name, price)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_all(self):
        return self.db.query(CatalogItem).all()

    def get(self, item_id: int):
        return self.db.get(CatalogItem, item_id)

    def update(self, item_id: int, name: str, price: float):
        item = self.get(item_id)
        if not item:
            raise ValueError("Catalog item not found")
        item.update(name, price)
        self.db.commit()
        return item

    def delete(self, item_id: int):
        item = self.get(item_id)
        if not item:
            raise ValueError("Catalog item not found")
        self.db.delete(item)
        self.db.commit()