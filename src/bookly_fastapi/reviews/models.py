from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
    SmallInteger,
    CheckConstraint,
    UniqueConstraint,
    ForeignKey,
    func,
    DateTime,
    Boolean,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

#from src.bookly_fastapi.books.models import Book
#from bookly_fastapi.users.models import User
from src.bookly_fastapi.db.main import Base
from src.bookly_fastapi.core.enums import ReviewStatus


class Review(Base):

    __tablename__ = "reviews"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "book_id",
            name="uq_reviews_user_book",
        ),
        CheckConstraint(
            "rating BETWEEN 1 AND 5",
            name="ck_reviews_rating_range",
        ),
        CheckConstraint(
            "char_length(body) <= 20000",
            name="ck_reviews_body_length",
        ),
        CheckConstraint(
            "char_length(title) <= 200",
            name="ck_reviews_title_length",
        ),
        CheckConstraint(
            "status IN ( 'published', 'flagged', 'hidden', 'deleted')",
            name="ck_reviews_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="RESTRICT"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    contains_spoilers: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=ReviewStatus.PUBLISHED.value,
        server_default="pending",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="book_reviews",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_reviews",
    )
