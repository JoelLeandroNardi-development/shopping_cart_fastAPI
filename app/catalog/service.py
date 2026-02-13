from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from .model import CatalogItem
from .dto import CatalogDTO

class CatalogService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, price: float):
        item = CatalogItem()
        item.update(name, price)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return CatalogDTO(item.id, item.name, item.price)

    def get(self, item_id: int):
        item = self.db.get(CatalogItem, item_id)
        if not item:
            raise NotFoundException("Catalog item not found")
        return CatalogDTO(item.id, item.name, item.price)

    def list(self):
        items = self.db.query(CatalogItem).all()
        return [CatalogDTO(i.id, i.name, i.price) for i in items]

    def update(self, item_id: int, name: str, price: float):
        item = self.db.get(CatalogItem, item_id)
        if not item:
            raise NotFoundException("Catalog item not found")
        item.update(name, price)
        self.db.commit()
        return CatalogDTO(item.id, item.name, item.price)

    def delete(self, item_id: int):
        item = self.db.get(CatalogItem, item_id)
        if not item:
            raise NotFoundException("Catalog item not found")
        self.db.delete(item)
        self.db.commit()