# -----------------------------------------------------------------------------
# Application Configuration
# -----------------------------------------------------------------------------

from pydantic_settings import BaseSettings, SettingsConfigDict

# -----------------------------------------------------------------------------
# Settings Management
# -----------------------------------------------------------------------------

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # -------------------------------------------------------------------------
    # Application Settings
    # -------------------------------------------------------------------------

    APP_NAME: str

    APP_VERSION: str

    ENVIRONMENT: str

    # -------------------------------------------------------------------------
    # Server Settings
    # -------------------------------------------------------------------------

    HOST: str

    PORT: int

    # -------------------------------------------------------------------------
    # Database Settings
    # -------------------------------------------------------------------------

    DATABASE_HOST: str

    DATABASE_PORT: int

    DATABASE_NAME: str

    DATABASE_USER: str

    DATABASE_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    # -----------------------------------------------------------------------------
    # JWT Settings
    # -----------------------------------------------------------------------------

    JWT_SECRET_KEY: str

    JWT_ALGORITHM: str

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # -----------------------------------------------------------------------------
    # Redis Configuration
    # -----------------------------------------------------------------------------

    REDIS_HOST: str = "localhost"

    REDIS_PORT: int = 6379

    REDIS_DB: int = 0

    REDIS_ENABLED: bool = True

    RATE_LIMIT_ENABLED: bool = True


settings = Settings()
