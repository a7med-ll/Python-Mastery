from fastapi import FastAPI

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Home Route
# -----------------------------------------------------------------------------

@app.get("/")
def l4_003HomeRoute() -> dict:
    """Return the home page."""

    return{

        "message": "Welcome to FastAPI!"
    }

# -----------------------------------------------------------------------------
# About Route
# -----------------------------------------------------------------------------

@app.get("/about")
def l4_003AboutRoute() -> dict:
    """Return information about the API."""

    return{

        "application": "Python Mastery",
        "module": "L4 Backend Engineering",
    }

# no need for if __name__ == "__main__" because, FastAPI runs the application, not Python directly.

# -----------------------------------------------------------------------------
# To Run The Server:
# --- uvicorn l4_003_basic_routes:app --reload.  ( uvicorn: The ASGI web server that runs FastAPI
#                                                  :app The FastAPI object.
#                                                  --reload Automatically restarts the server whenever you save the file.)
# -----------------------------------------------------------------------------
