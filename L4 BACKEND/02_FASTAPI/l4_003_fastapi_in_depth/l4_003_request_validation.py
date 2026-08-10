from fastapi import FastAPI
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Product Request Validation
# -----------------------------------------------------------------------------

class l4_003ProductRequest(BaseModel):

    product_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=300)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    category: str = Field(min_length=3)
    in_stock: bool = True

# -----------------------------------------------------------------------------
# Product Route
# -----------------------------------------------------------------------------

@app.post("/products")
def l4_003CreateProduct(
    product: l4_003ProductRequest
) -> dict:
    """Create an product using validated request data."""

    return {
        "message": "Product created successfully",
        "product": product
    }

