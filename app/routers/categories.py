from typing import Annotated

from fastapi import APIRouter, Body, status
from sqlalchemy import select, update

from app.crud import get_category_or_404, get_parent_category_or_404
from app.dependencies import DBSession
from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema
from app.schemas import CategoryCreate

router = APIRouter(
    prefix="/categories", tags=["categories"],
)


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: DBSession):
    """Возвращает список всех категорий товаров."""
    stmt = select(CategoryModel).where(CategoryModel.is_active)
    categories = db.scalars(stmt).all()
    return categories


@router.post("/", response_model=CategorySchema,
             status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate,
                          db: DBSession):
    """Создает новую категорию."""
    if category.parent_id is not None:
        get_parent_category_or_404(db, category.parent_id)
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int,
                          category: Annotated[CategoryCreate, Body()],
                          db: DBSession):
    """Обновляет категорию по ее ID"""
    category_from_db = get_category_or_404(db, category_id)
    if category.parent_id is not None:
        get_parent_category_or_404(db, category.parent_id)

    db.execute(update(CategoryModel).where(
        CategoryModel.id == category_id).values(
            **category.model_dump()))
    db.commit()
    db.refresh(category_from_db)
    return category_from_db


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int,
                          db: DBSession):
    """Удаляет категорию по ее ID"""
    get_category_or_404(db, category_id)
    db.execute(update(CategoryModel).where(
        CategoryModel.id == category_id).values(is_active=False))
    db.commit()
    return {"status": "success",
            "message": "Category marked as inactive."}
