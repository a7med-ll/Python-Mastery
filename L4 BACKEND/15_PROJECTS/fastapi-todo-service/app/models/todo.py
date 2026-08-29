# -----------------------------------------------------------------------------
# Todo Database Model
# -----------------------------------------------------------------------------

from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.user import User


# -----------------------------------------------------------------------------
# Todo Model
# -----------------------------------------------------------------------------

class Todo(Base):
    """
    Database model representing todo items.
    """

    # -------------------------------------------------------------------------
    # Table Configuration
    # -------------------------------------------------------------------------

    __tablename__ = "todos"


    # -------------------------------------------------------------------------
    # Columns
    # -------------------------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )


    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )


    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )


    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="todos"
    )