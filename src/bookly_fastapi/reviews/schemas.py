from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class ReviewCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    book_id = int

    rating: int = Field(strict=True, ge=1, le=5)

    title: str | None = Field(
        default=None,
        max_length=200,
    )

    body: str | None = Field(
        default=None,
        max_length=20000,
    )

    contains_spoilers: bool = False


class ReviewUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")


    rating: int | None = Field(
        default=None,
        strict=True,
        ge=1,
        le=5,
    )

    title: str | None = Field(
        default=None,
        max_length=200,
    )

    body: str | None = Field(
        default=None,
        max_length=20000,
    )

    contains_spoilers: bool | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")

        if "rating" in self.model_fields_set and self.rating is None:
            raise ValueError("Rating cannot be null")

        if (
            "contains_spoilers" in self.model_fields_set
            and self.contains_spoilers is None
        ):
            raise ValueError("contains_spoilers cannot be null")

        return self


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    user_id: int

    rating: int
    title: str | None
    body: str | None
    contains_spoilers: bool

    status: str

    created_at: datetime
    updated_at: datetime


q
