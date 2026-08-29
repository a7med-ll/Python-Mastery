# -----------------------------------------------------------------------------
# FastAPI Application Entry Point
# -----------------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError


from sqlalchemy import text

from app.core.config import settings
from app.database.session import SessionLocal
from app.api.v1.router import api_router

from app.middleware.logging_middleware import request_logging_middleware
from app.middleware.error_handler import global_exception_handler
from app.middleware.validation_handler import (
    validation_exception_handler
)

from app.middleware.request_id import RequestIDMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.cache.redis import redis_client


# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION
)

app.include_router(
    api_router,
    prefix="/api/v1"
)

app.middleware(
    "http"
)(request_logging_middleware)


app.add_exception_handler(
    Exception,
    global_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_middleware(
    RequestIDMiddleware
)

app.add_middleware(
    RateLimitMiddleware,
    requests_limit=60,
    window_seconds=60
)


# -----------------------------------------------------------------------------
# Root Endpoint
# -----------------------------------------------------------------------------

@app.get("/")
def root() -> dict:

    return {

        "message": "FastAPI Todo Service is running"

    }


# -----------------------------------------------------------------------------
# Health Check Endpoint
# -----------------------------------------------------------------------------

@app.get("/health")
def health_check() -> dict:

    return {

        "status": "healthy",

        "application": settings.APP_NAME,

        "version": settings.APP_VERSION

    }


# -----------------------------------------------------------------------------
# Readiness Check Endpoint
# -----------------------------------------------------------------------------

@app.get("/ready")
def readiness_check() -> dict:

    database = SessionLocal()

    try:

        database.execute(text("SELECT 1"))

        database_ready = True

    except Exception:

        database_ready = False

    finally:

        database.close()


    redis_ready = redis_client.ping()


    return {
        "status": "ready" if database_ready and redis_ready else "not_ready",
        "database": database_ready,
        "redis": redis_ready
    }


# -----------------------------------------------------------------------------
# Database Connection Test
# -----------------------------------------------------------------------------

@app.get("/database-check")
def database_check() -> dict:

    database = SessionLocal()

    try:

        database.execute(text("SELECT 1"))

        return {

            "database": "connected"

        }


    finally:

        database.close()
