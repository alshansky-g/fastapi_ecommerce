from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy import select

from app.config import ALGORITHM, SECRET_KEY
from app.dependencies import AsyncDBSession, Token
from app.exceptions import BadCredentialsError, ExpiredTokenError, UserNotSellerError
from app.models.users import User as UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Преобразует пароль в хэш с использованием bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие введенного пароля сохранённому кэшу."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """Создаёт JWT с payload(sub, role, id, exp)."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Token, db: AsyncDBSession):
    """Проверяет JWT и возвращает пользователя из базы данных."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise BadCredentialsError
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError from None
    except jwt.PyJWTError:
        raise BadCredentialsError from None
    user = await db.scalar(select(UserModel).where(
        UserModel.email == email, UserModel.is_active))
    if user is None:
        raise BadCredentialsError
    return user


async def get_current_seller(
        current_user: Annotated[UserModel, Depends(get_current_user)]):
    """Проверяет, что роль пользователя 'seller'."""
    if current_user.role != "seller":
        raise UserNotSellerError
    return current_user
