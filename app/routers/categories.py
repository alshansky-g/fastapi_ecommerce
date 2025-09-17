from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db_depends import get_db
from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema
from app.schemas import CategoryCreate

router = APIRouter(
    prefix="/categories", tags=["categories"],
)


@router.get("/")
async def get_all_categories():
    """Возвращает список всех категорий товаров."""
    return {"message": 'заглушка'}


@router.post("/", response_model=CategoryModel,
             status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate,
                          db: Annotated[Session, Depends(get_db)]):
    """Создает новую категорию."""
    if category.parent_id is not None:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id, CategoryModel.is_active)
        parent = db.scalars(stmt).first()
        if parent is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Parent category not found")
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/{category_id}")
async def update_category(category_id: int):
    """Обновляет категорию по ее ID"""
    return {"message": f"Категория с ID={category_id} обновлена."}


@router.delete("/{category_id}")
async def delete_category(category_id: int):
    """Удаляет категорию по ее ID"""
    return {"message": f"Категория с ID={category_id} удалена."}
