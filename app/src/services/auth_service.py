from sqlalchemy.orm import Session

from src.core.auth import create_access_token, get_password_hash, verify_password
from src.core.exceptions import InvalidCredentialsException, UserAlreadyExistsException, UserNotFoundException
from src.schemas.user import UserRegister
from src.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def authenticate_user(self, db: Session, email: str, password: str) -> dict:
        user = self.repository.get_by_email(db, email)
        if not user:
            raise UserNotFoundException(email)
          
        if not verify_password(password, user.password):
            raise InvalidCredentialsException()

        token = create_access_token(subject=user.id)
        return {"access_token": token, "token_type": "bearer"}

    def register_user(self, db: Session, user_data: UserRegister) -> dict:
        existing_user = self.repository.get_by_email(db, user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(user_data.email)

        hashed = get_password_hash(user_data.password)
        created_user = self.repository.create(db, user_data, hashed)
        return {
            "message": "User registered successfully",
            "created_at": created_user.created_at,
        }
