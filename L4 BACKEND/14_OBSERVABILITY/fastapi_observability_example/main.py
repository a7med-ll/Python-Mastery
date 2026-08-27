"""OBJECTIVE: Create a FastAPI application that demonstrates"""
import time

# --> Application creation
# --> Startup lifecycle event
# --> Shutdown lifecycle event
# --> Basic API endpoint
# --> Future connection point for: Logger, Metrics, Health Checks, Middleware

from fastapi import FastAPI, Request
from .logger import application_logger
from .health import health_router
from .metrics import l4_015UpdateMetrics, metrics_router

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-015 Observability Basics",
    description="Learning backend observability concepts with FastAPI",
    version="1.0.0"
)

app.include_router(
    health_router
)

app.include_router(
    metrics_router
)

# -----------------------------------------------------------------------------
# Request Logging Middleware
# -----------------------------------------------------------------------------

@app.middleware("http")
async def l4_015RequestLoggingMiddleware(request: Request, call_next):

    """
    Middleware executes before and after every request.
    """

    # Capture request startup time
    start_time = time.perf_counter()


    # Process request
    response = await call_next(request)


    # Calculate request duration
    duration_ms = (
        time.perf_counter() - start_time
    ) * 1000


    # Update metrics
    l4_015UpdateMetrics(
        status_code=response.status_code,
        duration_ms=duration_ms
    )


    # Create structured request log
    application_logger.info(
        "HTTP request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
        }
    )


    # Return response
    return response

# -----------------------------------------------------------------------------
# Application Startup Event
# -----------------------------------------------------------------------------

@app.on_event("startup")
async def l4_015ApplicationStartup() -> None:
    """ Executes when FastAPI application starts."""

    application_logger.info(
        "Application startup completed"
    )

# -----------------------------------------------------------------------------
# Application Shutdown Event
# -----------------------------------------------------------------------------

@app.on_event("shutdown")
async def l4_015ApplicationShutdown() -> None:
    """ Executes when FastAPI application shuts down."""

    application_logger.info(
        "Application shutdown completed"
    )

# -----------------------------------------------------------------------------
# Root Endpoint
# -----------------------------------------------------------------------------

@app.get("/")
async def l4_015RootEndpoint() -> dict:
    """Basic API endpoint. Used to verify that application is running"""

    return {
        "application": "L4-015 Observability Basics",
        "status": "running"
    }
