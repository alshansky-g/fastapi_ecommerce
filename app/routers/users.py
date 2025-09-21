from typing import Annotated

from fastapi import APIRouter, Body, status
from sqlalchemy import select

from app.auth import hash_password
from app.dependencies import AsyncDBSession
from app.exceptions import UserExistsError
from app.models.users import User as UserModel
from app.schemas import User as UserSchema
from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: Annotated[UserCreate, Body()], db: AsyncDBSession):
    """Регистрирует нового пользователя с ролью 'buyer' или 'seller'."""
    user_db = await db.scalar(select(UserModel).where(
        UserModel.email == user.email))
    if user_db:
        raise UserExistsError

    user_db = UserModel(email=user.email,
                        hashed_password=hash_password(user.password),
                        role=user.role)
    db.add(user_db)
    await db.commit()
    return user_db
