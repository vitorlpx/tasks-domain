from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserRegister

class UserRepository:
    def __init__(self):
      pass

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user: UserRegister, hashed_password: str) -> User:
        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
