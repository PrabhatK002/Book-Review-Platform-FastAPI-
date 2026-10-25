from fastapi import FastAPI
from src.bookly_fastapi.books.routes import book_router
from src.bookly_fastapi.users.routes import user_router
from src.bookly_fastapi.reviews.routes import review_router

app = FastAPI(
    title="Book Review Platform",
    description="Book Review Platform using FastAPI"
)


app.include_router(book_router, prefix = "/api/books", tags=['books'])
app.include_router(user_router, prefix="/api/users", tags=['users'])
app.include_router(review_router, prefix="/api/reviews", tags=['reviews'])