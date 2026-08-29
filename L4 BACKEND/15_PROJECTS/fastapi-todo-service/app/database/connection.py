# -----------------------------------------------------------------------------
# Database Connection
# -----------------------------------------------------------------------------

from sqlalchemy import create_engine

from app.core.config import settings

# -----------------------------------------------------------------------------
# Database URL
# -----------------------------------------------------------------------------

DATABASE_URL = (
    f"postgresql://"
    f"{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)

# -----------------------------------------------------------------------------
# Create Database Engine
# -----------------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)