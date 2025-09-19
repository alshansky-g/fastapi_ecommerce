"""
Модуль с эндпоинтами для crud операций с категориями товаров.
"""
from typing import Annotated

from fastapi import APIRouter, Body, status
from sqlalchemy import select, update

from app.crud import get_category_or_404, get_parent_category_or_404
from app.dependencies import AsyncDBSession
from app.exceptions import CategorySelfParentError
from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema
from app.schemas import CategoryCreate

router = APIRouter(
    prefix="/categories", tags=["categories"],
)


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: AsyncDBSession):
    """Возвращает список всех категорий товаров."""
    stmt = select(CategoryModel).where(CategoryModel.is_active)
    categories = await db.scalars(stmt)
    return categories.all()


@router.post("/", response_model=CategorySchema,
             status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate,
                          db: AsyncDBSession):
    """Создает новую категорию."""
    if category.parent_id is not None:
        await get_parent_category_or_404(db, category.parent_id)
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    await db.commit()
    return db_category


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int,
                          category: Annotated[CategoryCreate, Body()],
                          db: AsyncDBSession):
    """Обновляет категорию по ее ID"""
    category_from_db = await get_category_or_404(db, category_id)
    if category.parent_id is not None:
        parent_category = await get_parent_category_or_404(db, category.parent_id)
        if parent_category.id == category_id:
            raise CategorySelfParentError

    await db.execute(update(CategoryModel).where(
        CategoryModel.id == category_id).values(
            **category.model_dump(exclude_unset=True)))
    await db.commit()
    await db.refresh(category_from_db)
    return category_from_db


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int,
                          db: AsyncDBSession):
    """Удаляет(деактивирует) категорию по ее ID, устанавливая is_active=False"""
    category = await get_category_or_404(db, category_id)
    await db.execute(update(CategoryModel).where(
        CategoryModel.id == category_id).values(is_active=False))
    await db.commit()
    return category
