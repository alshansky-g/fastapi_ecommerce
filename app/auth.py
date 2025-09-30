"""
Модуль для основных операций, связанных с аутентификацией.
"""
from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext
from sqlalchemy import select

from app.config import config
from app.dependencies import AsyncDBSession, Token
from app.exceptions import BadCredentialsError, ExpiredTokenError
from app.models.users import User as UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Преобразует пароль в хэш с использованием bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие введенного пароля сохранённому хэшу."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """Создаёт JWT с payload(sub, role, id, exp)."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def create_refresh_token(data: dict):
    """Создаёт refresh-токен с длительным сроком действия."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def get_current_user(token: Token, db: AsyncDBSession):
    """Проверяет JWT и возвращает пользователя из базы данных."""
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
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
