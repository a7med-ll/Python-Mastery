# -----------------------------------------------------------------------------
# Database Session Management
# -----------------------------------------------------------------------------

from sqlalchemy.orm import sessionmaker

from app.database.connection import engine

from app.models.user import User
from app.models.todo import Todo


# -----------------------------------------------------------------------------
# Session Factory
# -----------------------------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)