from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://gleb:81972651@localhost:5433/ecommerce_db"

async_engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False,
                                         class_=AsyncSession)


class Base(DeclarativeBase):
    pass
