"""
Модуль с функциями crud.
Основное предназначение - проверка существования или активности
товара/категории товаров. Если не существует, возбуждается
соответствующее исключение. Если существует - возвращается
соответствующий объект.
"""
from sqlalchemy import select

from app.dependencies import AsyncDBSession
from app.exceptions import (
    CategoryNotFound,
    ParentCategoryNotFound,
    ProductCategoryNotFound,
    ProductNotFound,
)
from app.models.categories import Category
from app.models.products import Product


async def get_category_or_404(db: AsyncDBSession, category_id: int) -> Category:
    """
    Проверка, активна ли категория товара.
    """
    category = await db.scalar(select(Category).where(
        Category.id == category_id, Category.is_active
    ))
    if category is None:
        raise CategoryNotFound
    return category


async def get_parent_category_or_404(db: AsyncDBSession, category_id: int) -> Category:
    """
    Проверка, активна ли родительская категория.
    """
    category = await db.scalar(select(Category).where(
        Category.id == category_id, Category.is_active
    ))
    if category is None:
        raise ParentCategoryNotFound
    return category


async def get_product_or_404(db: AsyncDBSession, product_id: int) -> Product:
    """
    Проверка, существует ли товар.
    """
    product = await db.scalar(select(Product).where(
        Product.id == product_id, Product.is_active
    ))
    if product is None:
        raise ProductNotFound
    return product


async def get_product_category_or_400(
        db: AsyncDBSession, category_id: int) -> Category:
    """
    Проверка, активна ли категория найденного товара.
    """
    category = await db.scalar(select(Category).where(
        Category.id == category_id, Category.is_active
    ))
    if category is None:
        raise ProductCategoryNotFound
    return category
