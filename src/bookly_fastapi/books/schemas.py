from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class BookCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: str
    original_language: str
    first_publication_year: int
    status: str
    version: int



class BookUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None
    description: str | None
    original_language: str | None
    first_publication_year: int | None
    status: str | None
    version: int | None


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    original_language: str
    first_publication_year: int
    status: str
    version: int

    created_at: datetime
    updated_at: datetime
    