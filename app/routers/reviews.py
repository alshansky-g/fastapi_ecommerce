"""
Модуль с эндпоинтами отзывов к товарам
"""
from typing import Annotated

from fastapi import APIRouter, Body
from sqlalchemy import select

from app.crud import (
    check_review_exists,
    get_product_or_404,
    get_review_or_404,
    update_product_rating,
)
from app.dependencies import AsyncDBSession
from app.models.reviews import Review as ReviewModel
from app.rbac import Admin, Buyer
from app.schemas import Review, ReviewCreate

router = APIRouter(tags=["reviews"])


@router.get("/reviews", response_model=list[Review])
async def get_all_reviews(db: AsyncDBSession):
    """Возвращает список всех отзывов."""
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.is_active))
    return reviews.all()


@router.get("/products/{product_id}/reviews", response_model=list[Review])
async def get_reviews_by_product(product_id: int, db: AsyncDBSession):
    """Возвращает список отзывов к конкретному товару."""
    await get_product_or_404(db, product_id)
    reviews = await db.scalars(select(ReviewModel).where(
        ReviewModel.product_id == product_id, ReviewModel.is_active))
    return reviews.all()


@router.post("/reviews", response_model=Review)
async def create_review(user: Buyer,
                        db: AsyncDBSession,
                        review: Annotated[ReviewCreate, Body()]):
    """Добавляет отзыв к указанному товару."""
    await get_product_or_404(db, review.product_id)
    await check_review_exists(db, user.id, review.product_id)
    review_db = ReviewModel(**review.model_dump(), user_id=user.id)
    db.add(review_db)
    await db.commit()
    await update_product_rating(db=db, product_id=review.product_id)
    return review_db


@router.delete("/reviews/{review_id}")
async def delete_review(review_id: int, db: AsyncDBSession, current_user: Admin):
    """Выполняет мягкое удаление товара, устанавливая is_active = False"""
    review = await get_review_or_404(db, review_id)
    review.is_active = False
    await db.commit()
    await update_product_rating(db=db, product_id=review.product_id)
    return {"message": "Review deleted"}
