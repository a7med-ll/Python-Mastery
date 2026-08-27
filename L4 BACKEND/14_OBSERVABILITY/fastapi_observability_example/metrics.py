"""
Application metrics.

Responsible for collecting
basic application performance data.

Examples:

- Request count
- Successful requests
- Failed requests
- Request duration
"""


from fastapi import APIRouter

# -----------------------------------------------------------------------------
# Metrics Storage
# -----------------------------------------------------------------------------

application_metrics = {

    "total_requests": 0,

    "successful_requests": 0,

    "failed_requests": 0,

    "total_duration_ms": 0,

}

# -----------------------------------------------------------------------------
# Router Creation
# -----------------------------------------------------------------------------

metrics_router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

# -----------------------------------------------------------------------------
# Update Metrics
# -----------------------------------------------------------------------------

def l4_015UpdateMetrics(
    status_code: int,
    duration_ms: float
) -> None:
    """
    Updates application metrics after every request.
    """


    application_metrics["total_requests"] += 1


    application_metrics["total_duration_ms"] += duration_ms


    if status_code < 400:

        application_metrics["successful_requests"] += 1

    else:

        application_metrics["failed_requests"] += 1

# -----------------------------------------------------------------------------
# Metrics Endpoint
# -----------------------------------------------------------------------------

@metrics_router.get("/")
async def l4_015MetricsEndpoint() -> dict:
    """
    Returns current application metrics.
    """


    total_requests = (
        application_metrics["total_requests"]
    )


    average_duration = 0


    if total_requests > 0:

        average_duration = (
            application_metrics["total_duration_ms"]
            /
            total_requests
        )


    return {

        "total_requests": total_requests,

        "successful_requests":
            application_metrics["successful_requests"],

        "failed_requests":
            application_metrics["failed_requests"],

        "average_duration_ms":
            round(
                average_duration,
                2
            )
    }