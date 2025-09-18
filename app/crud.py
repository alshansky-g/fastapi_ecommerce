from sqlalchemy import select

from app.dependencies import DBSession
from app.exceptions import (
    CategoryNotFound,
    ParentCategoryNotFound,
    ProductCategoryNotFound,
    ProductNotFound,
)
from app.models.categories import Category
from app.models.products import Product


def get_category_or_404(db: DBSession, category_id: int) -> Category:
    category = db.scalar(select(Category).where(
        Category.id == category_id, Category.is_active
    ))
    if category is None:
        raise CategoryNotFound
    return category


def get_parent_category_or_404(db: DBSession, category_id: int) -> Category:
    category = db.scalar(select(Category).where(
        Category.id == category_id, Category.is_active
    ))
    if category is None:
        raise ParentCategoryNotFound
    return category


def get_product_or_404(db: DBSession, product_id: int) -> Product:
    product = db.scalar(select(Product).where(
        Product.id == product_id, Product.is_active
    ))
    if product is None:
        raise ProductNotFound
    return product


def get_product_category_or_400(
        db: DBSession, category_id: int) -> Category:
    category = db.scalar(select(Category).where(
        Category.id == category_id, Category.is_active
    ))
    if category is None:
        raise ProductCategoryNotFound
    return category
