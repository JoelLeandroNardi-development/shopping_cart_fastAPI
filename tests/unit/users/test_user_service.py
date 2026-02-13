import pytest

from app.users.service import UserService
from app.core.exceptions import NotFoundException
from app.users.dto import UserDTO

from tests.helpers.fake_user import FakeUser
from tests.helpers.fake_session import FakeSession

def test_create_persists_and_returns_dto(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.users.service.User", FakeUser)
    svc = UserService(db)
    dto = svc.create("Alice", "123")
    assert isinstance(dto, UserDTO)
    assert dto.id == 1
    assert dto.name == "Alice"
    assert dto.phone_number == "123"
    assert db.committed is True
    assert 1 in db.storage

def test_get_returns_dto_when_exists(monkeypatch):
    db = FakeSession()
    user = FakeUser("Bob", "222")
    user.id = 5
    db.storage[5] = user
    monkeypatch.setattr("app.users.service.User", FakeUser)
    svc = UserService(db)
    dto = svc.get(5)
    assert isinstance(dto, UserDTO)
    assert dto.id == 5
    assert dto.name == "Bob"

def test_get_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.users.service.User", FakeUser)
    svc = UserService(db)
    with pytest.raises(NotFoundException):
        svc.get(1)

def test_list_returns_all_users(monkeypatch):
    db = FakeSession()
    u1 = FakeUser("A", "1")
    u1.id = 1
    if FakeUser.__name__ not in db.model_storage:
        db.model_storage[FakeUser.__name__] = {}
    db.model_storage[FakeUser.__name__][1] = u1
    db.storage[1] = u1
    u2 = FakeUser("B", "2")
    u2.id = 2
    db.model_storage[FakeUser.__name__][2] = u2
    db.storage[2] = u2
    monkeypatch.setattr("app.users.service.User", FakeUser)
    svc = UserService(db)
    result = svc.list()
    assert isinstance(result, list)
    assert len(result) == 2
    assert {r.id for r in result} == {1, 2}

def test_update_updates_and_commits(monkeypatch):
    db = FakeSession()
    u = FakeUser("Old", "000")
    u.id = 10
    db.storage[10] = u
    monkeypatch.setattr("app.users.service.User", FakeUser)
    svc = UserService(db)
    dto = svc.update(10, "New", "999")
    assert dto.id == 10
    assert dto.name == "New"
    assert dto.phone_number == "999"
    assert db.committed is True

def test_update_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.users.service.User", FakeUser)
    svc = UserService(db)
    with pytest.raises(NotFoundException):
        svc.update(123, "x", "y")

def test_delete_removes_and_commits(monkeypatch):
    db = FakeSession()
    u = FakeUser("Rem", "000")
    u.id = 8
    db.storage[8] = u
    monkeypatch.setattr("app.users.service.User", FakeUser)
    svc = UserService(db)
    svc.delete(8)
    assert 8 not in db.storage
    assert db.committed is True

def test_delete_raises_not_found(monkeypatch):
    db = FakeSession()
    monkeypatch.setattr("app.users.service.User", FakeUser)
    svc = UserService(db)
    with pytest.raises(NotFoundException):
        svc.delete(999)