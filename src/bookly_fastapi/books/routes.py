from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.bookly_fastapi.authors.models import Author
from src.bookly_fastapi.books.models import Book, BookAuthor
from src.bookly_fastapi.books.schemas import BookCreate, BookRead, BookUpdate
from src.bookly_fastapi.core.enums import CatalogStatus, UserRole
from src.bookly_fastapi.db.main import get_db
from src.bookly_fastapi.dependencies.auth import CurrentUser

book_router = APIRouter()


@book_router.post(
    "",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book_data: BookCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    # 1. Check admin permission
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create books.",
        )

    # 2. Separate author information
    book_fields = book_data.model_dump(
        exclude={"authors"}
    )

    # 3. Validate author IDs
    author_ids = [
        author.author_id
        for author in book_data.authors
    ]

    result = await db.execute(
        select(Author.id).where(
            Author.id.in_(author_ids)
        )
    )

    existing_ids = set(result.scalars().all())

    missing_ids = set(author_ids) - existing_ids

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Authors not found: {sorted(missing_ids)}",
        )

    # 4. Create Book object
    new_book = Book(**book_fields)

    # 5. Create associations through ORM relationship
    for author_data in book_data.authors:
        link = BookAuthor(
            author_id=author_data.author_id,
            position=author_data.position,
            contributor_role=author_data.contributor_role,
        )

        new_book.author_links.append(link)

    # 6. Save Book and associations
    db.add(new_book)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    # 7. Refresh Book
    await db.refresh(new_book)

    return new_book


@book_router.get(
    "/{book_id}",
    response_model=BookRead,
    status_code=status.HTTP_200_OK,
)
async def get_book(book_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Book).where(Book.id == book_id))

    book = result.scalar_one_or_none

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The book with provided book id doesn't exist.",
        )

    return book


@book_router.patch(
    "/{book_id}", response_model=BookRead, status_code=status.HTTP_200_OK
)
async def update_book(
    current_user: CurrentUser,
    book_id: int,
    book_data: BookUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.role == UserRole.READER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this part.",
        )
    result = await db.execute(select(Book).where(Book.id == book_id))

    book = result.scalar_one_or_none

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The book with provided book id doesn't exist.",
        )

    update_data = book_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    await db.commit()
    await db.refresh(book)

    return book


@book_router.patch("/{book_id}", status_code=status.HTTP_200_OK)
async def archive_book(
    current_user: CurrentUser,
    book_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.role == UserRole.READER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this part."
        )


    result = await db.execute(select(Book).where(Book.id==book_id))

    book = result.scalar_one_or_none

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book with provided book id doesn't exist."
        )

    book.status = CatalogStatus.ARCHIVED.value

    await db.commit()
    await db.refresh(book)

    return book
