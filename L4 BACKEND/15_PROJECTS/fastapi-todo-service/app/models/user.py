# -----------------------------------------------------------------------------
# User Database Model
# -----------------------------------------------------------------------------

from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.todo import Todo


# -----------------------------------------------------------------------------
# User Model
# -----------------------------------------------------------------------------

class User(Base):
    """
    Database model representing application users.
    """

    # -------------------------------------------------------------------------
    # Table Configuration
    # -------------------------------------------------------------------------

    __tablename__ = "users"


    # -------------------------------------------------------------------------
    # Columns
    # -------------------------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        back_populates="owner",
        cascade="all, delete, delete-orphan"
    )