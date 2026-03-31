from datetime import datetime, timedelta, timezone
from settings import settings
from typing import Any, Union

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pwdlib import PasswordHash
from src.core.exceptions import (
    AuthorizationException,
    TokenGenerationException,
    TokenValidationException,
)

password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta | None = None) -> str:
    try:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expire, "sub": str(subject)}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception as exc:
        raise TokenGenerationException(str(exc))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError as exc:
        raise TokenValidationException(str(exc))

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
    if credentials is None:
        raise AuthorizationException("Missing bearer token")

    try:
        payload = decode_token(credentials.credentials)
        sub = payload.get("sub")
        if sub is None:
            raise TokenValidationException("Missing sub claim")
        return int(sub)
    except (ValueError, TypeError) as exc:
        raise TokenValidationException(str(exc))
