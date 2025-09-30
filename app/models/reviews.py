from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)
    comment_date: Mapped[datetime] = mapped_column(default=datetime.now)
    grade: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
