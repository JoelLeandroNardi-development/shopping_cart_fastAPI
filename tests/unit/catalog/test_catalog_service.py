import pytest

from app.catalog.service import CatalogService
from app.catalog.dto import CatalogDTO
from app.core.exceptions import NotFoundException

class FakeItem:
    def __init__(self, name: str = None, price: float = None):
        self.id = None
        self.name = name
        self.price = price

    def update(self, name: str, price: float):
        if not name.strip():
            raise ValueError("Name is required")
        if price <= 0:
            raise ValueError("Price must be greater than zero")
        self.name = name
        self.price = price

class FakeQuery:
    def __init__(self, storage):
        self._storage = storage

    def all(self):
        return list(self._storage.values())

class FakeSession:
    def __init__(self):
        self.added = []
        self.committed = False
        self.refreshed = []
        self.storage = {}
        self.next_id = 1
        self.deleted = []

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        if getattr(obj, "id", None) is None:
            obj.id = self.next_id
            self.next_id += 1
        self.storage[obj.id] = obj
        self.refreshed.append(obj)

    def get(self, model, id_):
        return self.storage.get(id_)

    def query(self, model):
        return FakeQuery(self.storage)

    def delete(self, obj):
        if getattr(obj, "id", None) in self.storage:
            del self.storage[obj.id]
            self.deleted.append(obj)

def test_create_persists_and_returns_dto(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    dto = svc.create("Item A", 9.99)
    assert isinstance(dto, CatalogDTO)
    assert dto.id == 1
    assert dto.name == "Item A"
    assert dto.price == 9.99
    assert db.committed is True
    assert 1 in db.storage

def test_create_raises_on_invalid_price(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    with pytest.raises(ValueError):
        svc.create("Good", 0)

def test_get_returns_dto_when_exists(monkeypatch):
    db = FakeSession()
    itm = FakeItem("B", 5.5)
    itm.id = 11
    db.storage[11] = itm
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    dto = svc.get(11)
    assert isinstance(dto, CatalogDTO)
    assert dto.id == 11
    assert dto.name == "B"

def test_get_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    with pytest.raises(NotFoundException):
        svc.get(1)

def test_list_returns_all_items(monkeypatch):
    db = FakeSession()
    a = FakeItem("A", 1.0)
    a.id = 1
    b = FakeItem("B", 2.0)
    b.id = 2
    db.storage[1] = a
    db.storage[2] = b
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    result = svc.list()
    assert isinstance(result, list)
    assert len(result) == 2
    assert {r.id for r in result} == {1, 2}

def test_update_updates_and_commits(monkeypatch):
    db = FakeSession()
    item = FakeItem("Old", 3.3)
    item.id = 20
    db.storage[20] = item
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    dto = svc.update(20, "New", 4.4)
    assert dto.id == 20
    assert dto.name == "New"
    assert dto.price == 4.4
    assert db.committed is True

def test_update_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    with pytest.raises(NotFoundException):
        svc.update(999, "x", 1.0)

def test_update_raises_on_invalid_input(monkeypatch):
    db = FakeSession()
    item = FakeItem("Ok", 2.0)
    item.id = 30
    db.storage[30] = item
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    with pytest.raises(ValueError):
        svc.update(30, "", 1.0)

def test_delete_removes_and_commits(monkeypatch):
    db = FakeSession()
    item = FakeItem("Del", 7.0)
    item.id = 40
    db.storage[40] = item
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    svc.delete(40)
    assert 40 not in db.storage
    assert db.committed is True

def test_delete_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeItem)
    svc = CatalogService(db)
    with pytest.raises(NotFoundException):
        svc.delete(777)