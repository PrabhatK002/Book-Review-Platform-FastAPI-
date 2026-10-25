from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class BookAuthorInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    author_id: int

    position: int = Field(ge=0)

    contributor_role: str = "author"


class BookCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=300)

    description: str | None = Field(
        default=None,
        max_length=20000,
    )

    original_language: str | None = Field(
        default=None,
        max_length=35,
    )

    first_publication_year: int | None = Field(
        default=None,
        ge=1,
        le=32767,
    )

    authors: list[BookAuthorInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_authors(self):
        author_ids = [a.author_id for a in self.authors]
        positions = [a.position for a in self.authors]

        if len(author_ids) != len(set(author_ids)):
            raise ValueError("Duplicate authors are not allowed")

        if len(positions) != len(set(positions)):
            raise ValueError("Duplicate author positions are not allowed")

        return self


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
