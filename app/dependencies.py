from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_depends import get_async_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

AsyncDBSession = Annotated[AsyncSession, Depends(get_async_db)]
Token = Annotated[str, Depends(oauth2_scheme)]
FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
