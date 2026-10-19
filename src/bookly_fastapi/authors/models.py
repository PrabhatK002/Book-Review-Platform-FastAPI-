from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
    SmallInteger,
    CheckConstraint,
    ForeignKey,
    func,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.bookly_fastapi.db.main import Base
from src.bookly_fastapi.core.enums import CatalogStatus
from src.bookly_fastapi.books.models import BookAuthor


class Author(Base):

    __tablename__ = "authors"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_authors_name_not_blank",
        ),
        CheckConstraint(
            "char_length(bio) <= 5000",
            name="ck_authors_bio_length",
        ),
        CheckConstraint(
            "status IN ('active', 'archived')",
            name="ck_authors_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text(5000), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=CatalogStatus.ACTIVE.value,
        server_default="active",
    )

    book_links: Mapped[list["BookAuthor"]] = relationship(
    "BookAuthor",
    back_populates="author",
)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
