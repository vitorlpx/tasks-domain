from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserRegister, UserLogin, UserRegisterResponse
from src.services.auth_service import AuthService

router = APIRouter()


def get_auth_service() -> AuthService:
    return AuthService(UserRepository())

@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    return service.authenticate_user(db, data.email, data.password)
  
@router.post("/register", response_model=UserRegisterResponse, status_code=201)
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    return service.register_user(db, data)
