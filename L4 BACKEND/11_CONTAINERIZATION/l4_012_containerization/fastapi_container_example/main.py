from fastapi import FastAPI

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-012 Containerization API",
    description="FastAPI application running inside Docker",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Health Check Endpoint
# -----------------------------------------------------------------------------

@app.get("/")
def l4_012HealthCheck() -> dict:
    """Check Application status"""

    return {

        "application": "L4-012 Containerization API",

        "status": "running",

        "environment": "FastAPI"
    }

# -----------------------------------------------------------------------------
# Container Information Endpoint
# -----------------------------------------------------------------------------

@app.get("/container")
def l4_012ContainerInfo() -> dict:
    """Return containerization information."""

    return {

        "message": "Application is ready for Docker",

        "concept": "Containerization",

        "deployment": "Docker"
    }

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    import uvicorn


    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )