from typing import Annotated

from fastapi import APIRouter, Body, status
from sqlalchemy import select

from app.auth import create_access_token, hash_password, verify_password
from app.dependencies import AsyncDBSession, FormData
from app.exceptions import IncorrectCredentialsError, UserExistsError
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


@router.post("/token")
async def login(form_data: FormData, db: AsyncDBSession):
    """Аутентифицирует пользователя и возвращает JWT с email, role, id."""
    user = await db.scalar(select(UserModel).where(
        UserModel.email == form_data.username, UserModel.is_active))
    if not (user and verify_password(form_data.password, user.hashed_password)):
        raise IncorrectCredentialsError
    access_token = create_access_token(data={
        "sub": user.email, "role": user.role, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
