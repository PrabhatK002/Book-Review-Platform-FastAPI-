import uuid
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
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import FetchedValue
from bookly_fastapi.authors.models import Author
from bookly_fastapi.reviews.models import Review
from src.bookly_fastapi.db.main import Base
from src.bookly_fastapi.core.enums import CatalogStatus


class Book(Base):

    __tablename__ = "books"

    __table_args__ = (
        CheckConstraint(
            "first_publication_year > 0",
            name="ck_books_publication_year_positive",
        ),
        CheckConstraint(
            "version >= 1",
            name="ck_books_version_positive",
        ),
        CheckConstraint(
            "char_length(description) <= 20000",
            name="ck_books_description_length",
        ),
        CheckConstraint(
            "char_length(trim(title)) > 0",
            name="ck_books_title_not_blank",
        ),
        CheckConstraint(
            "status IN ('active', 'archived')",
            name="ck_books_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    original_language: Mapped[str | None] = mapped_column(
        String(35),
        nullable=True,
    )

    first_publication_year: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=CatalogStatus.ACTIVE.value,
        server_default="active",
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default="1",
    )

    search_document: Mapped[str | None] = mapped_column(
        TSVECTOR,
        nullable=True,
    )

    author_links: Mapped[list["BookAuthor"]] = relationship(
        "BookAuthor",
        back_populates="book",
    )

    book_reviews: Mapped[list["Review"]] = relationship("Review", back_populates="book")

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


class BookAuthor(Base):

    __tablename__ = "book_authors"

    __table_args__ = (
        UniqueConstraint(
            "book_id",
            "author_id",
            name="uq_book_author_pair",
        ),
        UniqueConstraint(
            "book_id",
            "position",
            name="uq_book_author_position",
        ),
        CheckConstraint(
            "position >= 0",
            name="ck_book_author_position",
        ),
        CheckConstraint(
            "contributor_role IN " "('author', 'translator', 'editor', 'illustrator')",
            name="ck_book_author_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="RESTRICT"),
        nullable=False,
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    contributor_role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="author",
        server_default="author",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="author_links",
    )

    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="book_links",
    )


# class BookAuthor(Base):

#     __tablename__ = "book_authors"

#     __table_args__ = (
#         CheckConstraint(
#             "position >= 0",
#             name="ck_book_authors_position",
#         ),
#         UniqueConstraint(
#             "book_id",
#             "position",
#             name="uq_book_authors_book_position",
#         ),
#     )

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

#     book_id: Mapped[int] = mapped_column(
#         ForeignKey("books.id", ondelete="CASCADE"),
#         primary_key=True,
#     )

#     author_id: Mapped[int] = mapped_column(
#         ForeignKey("authors.id", ondelete="RESTRICT"),
#         primary_key=True,
#     )

#     position: Mapped[int] = mapped_column(
#         Integer,
#         nullable=False,
#     )

#     contributor_role: Mapped[str] = mapped_column(
#         String(30),
#         nullable=False,
#         default="author",
#         server_default="author",
#     )

#     book: Mapped["Book"] = relationship(
#         "Book",
#         back_populates="author_links",
#     )

#     author: Mapped["Author"] = relationship(
#         "Author",
#         back_populates="book_links",
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )
