import pytest

from app.catalog.service import CatalogService
from app.catalog.dto import CatalogDTO
from app.core.exceptions import NotFoundException

from tests.helpers.fake_catalog import FakeCatalogItem
from tests.helpers.fake_session import FakeSession

def test_create_persists_and_returns_dto(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
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
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    with pytest.raises(ValueError):
        svc.create("Good", 0)

def test_get_returns_dto_when_exists(monkeypatch):
    db = FakeSession()
    itm = FakeCatalogItem(11, 5.5)
    itm.id = 11
    db.storage[11] = itm
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    dto = svc.get(11)
    assert isinstance(dto, CatalogDTO)
    assert dto.id == 11

def test_get_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    with pytest.raises(NotFoundException):
        svc.get(1)

def test_list_returns_all_items(monkeypatch):
    db = FakeSession()
    a = FakeCatalogItem(1, 1.0)
    a.id = 1
    if FakeCatalogItem.__name__ not in db.model_storage:
        db.model_storage[FakeCatalogItem.__name__] = {}
    db.model_storage[FakeCatalogItem.__name__][1] = a
    db.storage[1] = a
    b = FakeCatalogItem(2, 2.0)
    b.id = 2
    db.model_storage[FakeCatalogItem.__name__][2] = b
    db.storage[2] = b  
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    result = svc.list()
    assert isinstance(result, list)
    assert len(result) == 2
    assert {r.id for r in result} == {1, 2}

def test_update_updates_and_commits(monkeypatch):
    db = FakeSession()
    item = FakeCatalogItem(20, 3.3)
    item.id = 20
    db.storage[20] = item
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    dto = svc.update(20, "New", 4.4)
    assert dto.id == 20
    assert dto.price == 4.4
    assert db.committed is True

def test_update_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    with pytest.raises(NotFoundException):
        svc.update(999, "x", 1.0)

def test_update_raises_on_invalid_input(monkeypatch):
    db = FakeSession()
    item = FakeCatalogItem(30, 2.0)
    item.id = 30
    db.storage[30] = item
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    with pytest.raises(ValueError):
        svc.update(30, "", 1.0)

def test_delete_removes_and_commits(monkeypatch):
    db = FakeSession()
    item = FakeCatalogItem(40, 7.0)
    item.id = 40
    db.storage[40] = item
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    svc.delete(40)
    assert 40 not in db.storage
    assert db.committed is True

def test_delete_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.catalog.service.CatalogItem", FakeCatalogItem)
    svc = CatalogService(db)
    with pytest.raises(NotFoundException):
        svc.delete(777)