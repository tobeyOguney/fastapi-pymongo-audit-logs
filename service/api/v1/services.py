"""Service business logic."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from service.core.config import settings
from service.db import get_client
from service.schemas import TokenData, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> Any:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> Any:
    return pwd_context.hash(password)


def get_user(username: str) -> Optional[User]:
    with get_client() as client:
        db = client[settings.DB_NAME]
        user = db.users.find_one({"username": username})

    return user


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = get_user(username)

    if not user or not verify_password(password, user["hashed_password"]):
        return None

    return user


def create_access_token(
    data: Dict[Any, Any], expires_delta: Union[timedelta, None] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
