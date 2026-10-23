from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
    CheckConstraint,
    func,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.bookly_fastapi.reviews.models import Review
from src.bookly_fastapi.db.main import Base
from src.bookly_fastapi.core.enums import UserRole, UserStatus


class User(Base):

    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "length(trim(username)) > 0",
            name="ck_users_username_not_blank",
        ),
        CheckConstraint(
            "role IN ('reader', 'moderator', 'admin')",
            name="ck_users_role_valid",
        ),
        CheckConstraint(
            "status IN ('pending', 'active', 'banned', 'deactivated')",
            name="ck_users_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    username: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=UserRole.READER.value,
        server_default="reader",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=UserStatus.PENDING.value,
        server_default="pending",
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user_reviews : Mapped[list["Review"]] = relationship("Review", back_populates="user")

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

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
