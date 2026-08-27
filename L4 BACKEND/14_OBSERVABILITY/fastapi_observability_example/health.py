"""
Health check endpoints.

Purpose:

Expose application health information
for monitoring systems.

Examples:

Kubernetes probes:
- Liveness probe
- Readiness probe
"""


from fastapi import APIRouter

# -----------------------------------------------------------------------------
# Router Creation
# -----------------------------------------------------------------------------

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)

# -----------------------------------------------------------------------------
# Overall Health Check
# -----------------------------------------------------------------------------

@health_router.get("")
async def l4_015HealthCheck() -> dict:
    """Overall health check used by monitoring/tests."""

    return {
        "status": "healthy"
    }

# -----------------------------------------------------------------------------
# Liveness Check
# -----------------------------------------------------------------------------

@health_router.get("/live")
async def l4_015LivenessCheck() -> dict:
    """Check whether application process is alive."""

    return {
        "status": "alive"
    }

# -----------------------------------------------------------------------------
# Readiness Check
# -----------------------------------------------------------------------------

@health_router.get("/ready")
async def l4_015ReadinessCheck() -> dict:
    """Checks whether application is ready to receive traffic."""

    return {
        "status": "ready"
    }