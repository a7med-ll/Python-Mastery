from fastapi import FastAPI
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Student Request Model
# -----------------------------------------------------------------------------

class l4_003StudentRequest(BaseModel):

    student_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge = 18, le = 60)
    course: str = Field(min_length=3)
    email: str = Field(min_length=8)
    is_active: bool = Field(default=True)

# -----------------------------------------------------------------------------
# Student Response Model
# -----------------------------------------------------------------------------

class l4_003StudentResponse(BaseModel):

    student_id: int
    name: str
    course: str
    is_active: bool

# -----------------------------------------------------------------------------
# Student Route
# -----------------------------------------------------------------------------

@app.post(
    "/students",
    response_model=l4_003StudentResponse
)
def l4_003CreateStudent(
    student: l4_003StudentRequest
) -> dict:
    """Create a student and return validated response data."""

    return {
        "student_id": student.student_id,
        "name": student.name,
        "course": student.course,
        "is_active": student.is_active,
        "age": student.age,
        "email": student.email
    }


