# -----------------------------------------------------------------------------
# Alembic Environment Configuration
# -----------------------------------------------------------------------------

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# -----------------------------------------------------------------------------
# Application Imports
# -----------------------------------------------------------------------------

from app.core.config import settings

from app.database.base import Base

# Import models so Alembic can detect them
from app.models import User, Todo


# -----------------------------------------------------------------------------
# Alembic Config Object
# -----------------------------------------------------------------------------

config = context.config


# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# -----------------------------------------------------------------------------
# Database URL Configuration
# -----------------------------------------------------------------------------

DATABASE_URL = (
    f"postgresql://"
    f"{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)


config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL
)


# -----------------------------------------------------------------------------
# Alembic Metadata
# -----------------------------------------------------------------------------

target_metadata = Base.metadata


# -----------------------------------------------------------------------------
# Offline Migration
# -----------------------------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.

    This configures Alembic using only the database URL.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# -----------------------------------------------------------------------------
# Online Migration
# -----------------------------------------------------------------------------

def run_migrations_online() -> None:
    """
    Run migrations in online mode.

    This creates a database connection and applies migrations.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():

            context.run_migrations()


# -----------------------------------------------------------------------------
# Execute Migration
# -----------------------------------------------------------------------------

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()