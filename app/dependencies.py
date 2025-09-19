from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_depends import get_async_db

AsyncDBSession = Annotated[AsyncSession, Depends(get_async_db)]
