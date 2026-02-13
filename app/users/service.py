from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from .model import User
from .dto import UserDTO

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, phone_number: str):
        user = User()
        user.update(name, phone_number)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return UserDTO(user.id, user.name, user.phone_number)

    def get(self, user_id: int):
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserDTO(user.id, user.name, user.phone_number)

    def list(self):
        users = self.db.query(User).all()
        return [UserDTO(u.id, u.name, u.phone_number) for u in users]

    def update(self, user_id: int, name: str, phone_number: str):
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")
        user.update(name, phone_number)
        self.db.commit()
        return UserDTO(user.id, user.name, user.phone_number)

    def delete(self, user_id: int):
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")
        self.db.delete(user)
        self.db.commit()