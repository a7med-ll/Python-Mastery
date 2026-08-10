from fastapi import FastAPI
from pydantic import BaseModel

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Employee Model
# -----------------------------------------------------------------------------

class l4_003Employee(BaseModel):

    employee_id: int
    name: str
    department: str
    salary: float
    is_active: bool = True

# -----------------------------------------------------------------------------
# Create Emp Route
# -----------------------------------------------------------------------------

@app.post("/employees")

def l4_003CreateEmployee(
        employee: l4_003Employee
) -> dict:
    """Create a employee using validated request data."""

    return {
        "message": "Employee created successfully",
        "employee": employee
    }











'''from fastapi import FastAPI
from pydantic import BaseModel

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Customer Model
# -----------------------------------------------------------------------------

class l4_003Customer(BaseModel):
    """Define the customer request structure."""

    name: str
    age: int
    country: str


# -----------------------------------------------------------------------------
# Create Customer Route
# -----------------------------------------------------------------------------

@app.post("/customers")
def l4_003CreateCustomer(
    customer: l4_003Customer
) -> dict:
    """Create a customer using validated request data."""

    return {
        "message": "Customer created",
        "customer": customer
    }'''