from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bookly_fastapi.core.enums import ReviewStatus
from src.bookly_fastapi.db.main import get_db
from src.bookly_fastapi.dependencies.auth import CurrentUser
from src.bookly_fastapi.reviews.models import Review
from src.bookly_fastapi.reviews.schemas import ReviewCreate, ReviewRead, ReviewUpdate

review_router = APIRouter()


@review_router.post(
    "/review_create",
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    review_data: ReviewCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    existing = await db.scalar(
        select(Review).where(
            Review.book_id == review_data.book_id,
            Review.user_id == current_user.id,
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="You have already reviewed this book",
        )

    new_review = Review(
        user_id=current_user.id,
        **review_data.model_dump(),
        status="published",
    )

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    return new_review


@review_router.get(
    "/{review_id}",
    response_model=ReviewRead,
    status_code=status.HTTP_200_OK,
)
async def get_review(
    review_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    review = await db.scalar(
        select(Review).where(
            Review.id == review_id,
            Review.status == ReviewStatus.PUBLISHED.value,
        )
    )

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return review



@review_router.patch(
    "/{review_id}",
    response_model=ReviewRead,
    status_code=status.HTTP_200_OK,
)
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    # Retrieve review by its primary key
    review = await db.scalar(
        select(Review).where(
            Review.id == review_id,
            Review.user_id == current_user.id,
        )
    )

    # Check whether the review exists and belongs to user
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    # Update only submitted fields
    update_data = review_update.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(review, field, value)

    await db.commit()
    await db.refresh(review)

    return review


@review_router.delete( "/{review_id}",
    status_code=status.HTTP_200_OK,)
async def delete_review(
    review_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    # Retrieve review by its primary key
    review = await db.scalar(
        select(Review).where(
            Review.id == review_id,
            Review.user_id == current_user.id,
        )
    )

    # Check whether the review exists and belongs to user
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    await review.delete()
    await db.commit()
