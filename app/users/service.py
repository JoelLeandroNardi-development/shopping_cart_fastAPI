from sqlalchemy.orm import Session
from .model import User

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, phone_number: str):
        user = User()
        user.update(name, phone_number)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self):
        return self.db.query(User).all()

    def get(self, user_id: int):
        return self.db.get(User, user_id)

    def update(self, user_id: int, name: str, phone_number: str):
        user = self.get(user_id)
        if not user:
            raise ValueError("User not found")
        user.update(name, phone_number)
        self.db.commit()
        return user

    def delete(self, user_id: int):
        user = self.get(user_id)
        if not user:
            raise ValueError("User not found")
        self.db.delete(user)
        self.db.commit()