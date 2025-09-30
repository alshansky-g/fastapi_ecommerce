"""
Модуль с функциями crud.
Основное предназначение - проверка существования или активности
товара/категории товаров. Если не существует, возбуждается
соответствующее исключение. Если существует - возвращается
соответствующий объект.
"""
from sqlalchemy import func, select, update

from app.dependencies import AsyncDBSession
from app.exceptions import (
    CategoryNotFound,
    ParentCategoryNotFound,
    ProductCategoryNotFound,
    ProductNotFound,
    ReviewAlreadyExists,
)
from app.models.categories import Category
from app.models.products import Product
from app.models.reviews import Review


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


async def update_product_rating(db: AsyncDBSession, product_id: int) -> None:
    avg_grade = await db.scalar(select(func.avg(Review.grade)).where(
        Review.is_active))
    await db.execute(update(Product).where(Product.id == product_id)
                     .values(rating=avg_grade))
    await db.commit()


async def check_review_exists(db, user_id: int, product_id: int) -> None:
    review_exists = await db.scalar(select(Review).where(
        Review.user_id == user_id, Review.product_id == product_id
    ))
    if review_exists:
        raise ReviewAlreadyExists
