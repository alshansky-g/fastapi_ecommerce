from warnings import deprecated

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def has_password(password: str) -> str:
    """Преобразует пароль в хэш с использованием bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие введенного пароля сохранённому кэшу."""
    return pwd_context.verify(plain_password, hashed_password)
