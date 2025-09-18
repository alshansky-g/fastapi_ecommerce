from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_depends import get_db
from app.models import Category, Product
from app.schemas import Product as ProductSchema
from app.schemas import ProductCreate

router = APIRouter(
    prefix="/products", tags=["products"]
)


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: Annotated[Session, Depends(get_db)]):
    """Возвращает список всех товаров."""
    products = db.scalars(select(Product).where(Product.is_active)).all()
    return products


@router.post("/", response_model=ProductSchema)
async def create_product(product: Annotated[ProductCreate, Body()],
                         db: Annotated[Session, Depends(get_db)]):
    """Создаёт новый товар."""
    category = db.scalar(select(Category).where(
        Category.id == product.category_id))
    if category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Category not found")
    product_db = Product(**product.model_dump())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(
    category_id: int,
    db: Annotated[Session, Depends(get_db)]):
    """Возвращает список товаров в указанной категории."""
    category = db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found")
    products = db.scalars(select(Product).where(
        Product.category_id == category_id)).all()
    return products


@router.get("/{product_id}")
async def get_product(product_id: int):
    """Возвращает детальную информацию о товаре по его ID"""
    return {"message": f"Детали товара {product_id}."}


@router.put("/{product_id}")
async def update_product(product_id: int):
    """Обновляет товар по его ID"""
    return {"message": f"Товар {product_id} обновлен."}


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """Удаляет товар по его ID"""
    return {"message": f"Товар {product_id} удален."}
