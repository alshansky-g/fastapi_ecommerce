"""
Модуль с эндпоинтами для crud операций с товарами.
"""
from typing import Annotated

from fastapi import APIRouter, Body, status
from sqlalchemy import select, update

from app.crud import (
    get_category_or_404,
    get_product_category_or_400,
    get_product_or_404,
)
from app.dependencies import DBSession
from app.models import Product
from app.models.categories import Category
from app.schemas import Product as ProductSchema
from app.schemas import ProductCreate

router = APIRouter(
    prefix="/products", tags=["products"]
)


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: DBSession):
    """Возвращает список всех товаров."""
    products = db.scalars(
        select(Product).join(Category).where(
            Product.is_active, Category.is_active, Product.stock > 0)).all()
    return products


@router.post("/", response_model=ProductSchema,
             status_code=status.HTTP_201_CREATED)
async def create_product(product: Annotated[ProductCreate, Body()],
                         db: DBSession):
    """Создаёт новый товар."""
    get_product_category_or_400(db, product.category_id)
    product_db = Product(**product.model_dump())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(category_id: int, db: DBSession):
    """Возвращает список товаров в указанной категории."""
    get_category_or_404(db, category_id)
    products = db.scalars(select(Product).where(
        Product.category_id == category_id, Product.is_active)).all()
    return products


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: DBSession):
    """Возвращает детальную информацию о товаре по его ID"""
    product = get_product_or_404(db, product_id)
    get_product_category_or_400(db, product.category_id)
    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int,
                         product: Annotated[ProductCreate, Body()],
                         db: DBSession):
    """Обновляет товар по его ID"""
    product_db = get_product_or_404(db, product_id)
    get_product_category_or_400(db, product.category_id)
    db.execute(update(Product).where(Product.id == product_id)
               .values(**product.model_dump()))
    db.commit()
    db.refresh(product_db)
    return product_db


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: DBSession):
    """Удаляет товар по его ID"""
    product = get_product_or_404(db, product_id)
    get_product_category_or_400(db, product.category_id)
    product.is_active = False
    db.commit()
    return {"status": "success", "message": "Product marked as inactive."}
