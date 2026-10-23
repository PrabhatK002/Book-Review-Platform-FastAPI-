from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.bookly_fastapi.core.config import settings

# 1. Define the Database URL (Using SQLite for this example)



SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL



# 2. Create an ASYNC engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# 3. Create an ASYNC Session factory
AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 4. Create the Declarative Base
class Base(DeclarativeBase):
    pass

# Async dependency to yield database sessions to FastAPI endpoints
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()