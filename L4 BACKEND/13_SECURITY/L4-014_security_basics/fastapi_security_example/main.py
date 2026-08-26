from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-014 Security Basics API"
)

# -----------------------------------------------------------------------------
# Secrets Management
# -----------------------------------------------------------------------------

# Secrets should never be hardcoded.
# Application reads sensitive values from environment variables.

APPLICATION_SECRET = os.getenv(
    "APPLICATION_SECRET",
    "development-secret"
)

# -----------------------------------------------------------------------------
# CORS Configuration
# -----------------------------------------------------------------------------

# Define trusted frontend origins.

app.add_middleware(
    CORSMiddleware,

    allow_origins=["http://localhost:3000"],

    allow_credentials=True,

    allow_methods=["GET", "POST"],

    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Security Headers Middleware
# -----------------------------------------------------------------------------

@app.middleware("http")
async def add_security_headers(
    request: Request,
    call_next
):

    # Forward request.
    response = await call_next(request)

    # Prevent browser from guessing content type.
    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    # Prevent application embedding.
    response.headers["X-Frame-Options"] = "DENY"

    # Basic Content Security Policy.
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    return response

# -----------------------------------------------------------------------------
# Request Validation Model
# -----------------------------------------------------------------------------

class UserRequest(BaseModel):

    # Username validation.
    username: str = Field(
        min_length=3,
        max_length=50
    )


    # Age validation.
    age: int = Field(
        gt=0,
        lt=120
    )

# -----------------------------------------------------------------------------
# Secure User Creation Endpoint
# -----------------------------------------------------------------------------

@app.post("/users")
def create_user(
    user: UserRequest
) -> dict:
    """
    Demonstrates input validation.

    Invalid data never reaches
    business logic.
    """

    return {

        "message": "User created successfully",

        "user": {
            "username": user.username,
            "age": user.age
        }
    }

# -----------------------------------------------------------------------------
# SQL Injection Protection Example
# -----------------------------------------------------------------------------

@app.get("/search/{username}")
def search_user(
    username: str
) -> dict:
    """
    Demonstrates validating user input
    before database operations.

    Real applications should use
    parameterized queries.
    """

    # Block suspicious SQL characters.
    if "'" in username or ";" in username:
        raise HTTPException(
            status_code=400,
            detail="Invalid input detected"
        )

    return {

        "message": "Safe search executed",

        "username": username
    }

# -----------------------------------------------------------------------------
# Security Health Check
# -----------------------------------------------------------------------------

@app.get("/")
def security_status() -> dict:

    return {

        "application": "L4-014 Security Basics API",

        "status": "running",

        "security_features": [

            "Input Validation",

            "CORS Protection",

            "Security Headers",

            "Environment Secrets"

        ]

    }


