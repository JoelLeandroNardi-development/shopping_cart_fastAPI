import pytest

from types import SimpleNamespace

from app.cart.service import CartService
from app.core.exceptions import NotFoundException
from app.cart.dto import CartDTO, CartItemDTO

from tests.helpers.fake_cart import FakeCart, FakeCartItem
from tests.helpers.fake_catalog import FakeCatalogItem
from tests.helpers.fake_session import FakeSession

def make_item_data(catalog_item_id, quantity):
    return SimpleNamespace(catalog_item_id=catalog_item_id, quantity=quantity)

@pytest.fixture
def cart_with_items():
    from app.cart.model import Cart
    from app.catalog.model import CatalogItem
    
    db = FakeSession()
    
    user = SimpleNamespace(id=1)
    user_model_type = type(user).__name__
    if user_model_type not in db.model_storage:
        db.model_storage[user_model_type] = {}
    db.model_storage[user_model_type][1] = user
    db.storage[1] = user

    catalog = FakeCatalogItem(2, 2.5)
    catalog.id = 2
    if CatalogItem.__name__ not in db.model_storage:
        db.model_storage[CatalogItem.__name__] = {}
    db.model_storage[CatalogItem.__name__][2] = catalog
    if FakeCatalogItem.__name__ not in db.model_storage:
        db.model_storage[FakeCatalogItem.__name__] = {}
    db.model_storage[FakeCatalogItem.__name__][2] = catalog
    db.storage[2] = catalog
    cart = FakeCart(user_id=1, db=db)
    cart.id = 7
    ci = FakeCartItem(cart_id=7, catalog_item_id=2, quantity=2)
    ci.id = 33
    ci.catalog_item = catalog
    cart.items = [ci]
    cart.total_price = 5.0
    if Cart.__name__ not in db.model_storage:
        db.model_storage[Cart.__name__] = {}
    db.model_storage[Cart.__name__][7] = cart
    if FakeCart.__name__ not in db.model_storage:
        db.model_storage[FakeCart.__name__] = {}
    db.model_storage[FakeCart.__name__][7] = cart
    db.storage[7] = cart
    
    return db, cart, catalog

def test_create_success(monkeypatch):
    db = FakeSession()
    user = SimpleNamespace(id=1)
    user_model_type = type(user).__name__
    if user_model_type not in db.model_storage:
        db.model_storage[user_model_type] = {}
    db.model_storage[user_model_type][1] = user
    db.storage[1] = user
    catalog = FakeCatalogItem(2, 5.0)
    catalog.id = 2
    db.refresh(catalog)
    monkeypatch.setattr("app.cart.service.Cart", lambda user_id, db=db: FakeCart(user_id, db))
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    svc = CartService(db)
    dto = svc.create(1, [make_item_data(2, 3)])
    assert isinstance(dto, CartDTO)
    assert dto.user_id == 1
    assert dto.total_price == pytest.approx(15.0)
    assert len(dto.items) == 1
    item = dto.items[0]
    assert isinstance(item, CartItemDTO)
    assert item.unit_price == pytest.approx(5.0)
    assert item.total_price == pytest.approx(15.0)

def test_create_user_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.cart.service.Cart", lambda user_id, db=db: FakeCart(user_id, db))
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    svc = CartService(db)
    with pytest.raises(NotFoundException):
        svc.create(999, [])

def test_create_catalog_item_not_found(monkeypatch):
    db = FakeSession()
    user = SimpleNamespace(id=1)
    user_model_type = type(user).__name__
    if user_model_type not in db.model_storage:
        db.model_storage[user_model_type] = {}
    db.model_storage[user_model_type][1] = user
    db.storage[1] = user
    monkeypatch.setattr("app.cart.service.Cart", lambda user_id, db=db: FakeCart(user_id, db))
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    svc = CartService(db)
    with pytest.raises(NotFoundException):
        svc.create(1, [make_item_data(99, 1)])

def test_get_returns_dto_when_exists(monkeypatch, cart_with_items):
    db, cart, _ = cart_with_items
    monkeypatch.setattr("app.cart.service.Cart", lambda user_id, db=db: FakeCart(user_id, db))
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    svc = CartService(db)
    dto = svc.get(7)
    assert dto.id == 7
    assert dto.total_price == pytest.approx(5.0)

def test_list_returns_all_carts(monkeypatch, cart_with_items):
    db, cart, _ = cart_with_items
    fake_cart_constructor = lambda user_id, db=db: FakeCart(user_id, db)
    monkeypatch.setattr("app.cart.service.Cart", fake_cart_constructor)
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    lambda_name = fake_cart_constructor.__name__
    if lambda_name not in db.model_storage:
        db.model_storage[lambda_name] = {}
    db.model_storage[lambda_name][7] = cart
    svc = CartService(db)
    lst = svc.list()
    assert isinstance(lst, list)
    assert len(lst) >= 1

def test_update_success(monkeypatch, cart_with_items):
    db, _, catalog = cart_with_items
    monkeypatch.setattr("app.cart.service.Cart", lambda user_id, db=db: FakeCart(user_id, db))
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    svc = CartService(db)
    updated = svc.update(7, [make_item_data(2, 3)])
    assert updated.total_price == pytest.approx(7.5)

def test_update_cart_not_found(monkeypatch, cart_with_items):
    db, _, _ = cart_with_items
    monkeypatch.setattr("app.cart.service.Cart", lambda user_id, db=db: FakeCart(user_id, db))
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    svc = CartService(db)
    with pytest.raises(NotFoundException):
        svc.update(999, [])

def test_delete_success(monkeypatch, cart_with_items):
    db, _, _ = cart_with_items
    monkeypatch.setattr("app.cart.service.Cart", lambda user_id, db=db: FakeCart(user_id, db))
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    svc = CartService(db)
    svc.delete(7)
    assert 7 not in db.storage

def test_delete_cart_not_found(monkeypatch, cart_with_items):
    db, _, _ = cart_with_items
    monkeypatch.setattr("app.cart.service.Cart", lambda user_id, db=db: FakeCart(user_id, db))
    monkeypatch.setattr("app.cart.service.CartItem", FakeCartItem)
    svc = CartService(db)
    with pytest.raises(NotFoundException):
        svc.delete(999)
