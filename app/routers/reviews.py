from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy import select

from app.auth import get_current_buyer
from app.crud import check_review_exists, get_product_or_404, update_product_rating
from app.dependencies import AsyncDBSession
from app.models.reviews import Review as ReviewModel
from app.models.users import User
from app.schemas import Review, ReviewCreate

router = APIRouter(tags=["reviews"])

Buyer = Annotated[User, Depends(get_current_buyer)]


@router.get("/reviews", response_model=list[Review])
async def get_all_reviews(db: AsyncDBSession):
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.is_active))
    return reviews.all()


@router.get("/products/{product_id}/reviews", response_model=list[Review])
async def get_reviews_by_product(product_id: int, db: AsyncDBSession):
    await get_product_or_404(db, product_id)
    reviews = await db.scalars(select(ReviewModel).where(
        ReviewModel.product_id == product_id, ReviewModel.is_active))
    return reviews.all()


@router.post("/reviews", response_model=Review)
async def create_review(user: Buyer, db: AsyncDBSession,
                        review: Annotated[ReviewCreate, Body()]):
    await get_product_or_404(db, review.product_id)
    await check_review_exists(db, user.id, review.product_id)
    review_db = ReviewModel(**review.model_dump(), user_id=user.id)
    db.add(review_db)
    await db.commit()
    await update_product_rating(db=db, product_id=review.product_id)
    return review_db
