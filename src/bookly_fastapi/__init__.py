from fastapi import FastAPI
from src.bookly_fastapi.books.routes import book_router


app = FastAPI(
    title="Book Review Platform",
    description="Book Review Platform using FastAPI"
)


app.include_router(book_router, prefix = "/api/v1/books", tags=['books'])