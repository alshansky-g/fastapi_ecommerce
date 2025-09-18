from typing import Annotated

from fastapi import APIRouter, Body
from sqlalchemy import select

from app.crud import (
    get_category_or_404,
    get_product_category_or_400,
    get_product_or_404,
)
from app.dependencies import DBSession
from app.models import Product
from app.schemas import Product as ProductSchema
from app.schemas import ProductCreate

router = APIRouter(
    prefix="/products", tags=["products"]
)


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: DBSession):
    """Возвращает список всех товаров."""
    products = db.scalars(select(Product).where(Product.is_active)).all()
    return products


@router.post("/", response_model=ProductSchema)
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
        Product.category_id == category_id)).all()
    return products


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: DBSession):
    """Возвращает детальную информацию о товаре по его ID"""
    product = get_product_or_404(db, product_id)
    return product


@router.put("/{product_id}")
async def update_product(product_id: int):
    """Обновляет товар по его ID"""
    return {"message": f"Товар {product_id} обновлен."}


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """Удаляет товар по его ID"""
    return {"message": f"Товар {product_id} удален."}
