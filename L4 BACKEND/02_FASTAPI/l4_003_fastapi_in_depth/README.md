# L4-003 — FastAPI in Depth

This module introduces the core concepts required to build backend APIs using FastAPI.

---

# Topics Covered

- Basic Routes
- Path Parameters
- Query Parameters
- Dependency Injection
- Pydantic Models
- Request Validation
- Response Validation
- Middleware
- Background Tasks

---

# Folder Structure

```text
l4_003_fastapi_in_depth/
│
├── README.md
├── l4_003_basic_routes.py
├── l4_003_path_parameters.py
├── l4_003_query_parameters.py
├── l4_003_dependency_injection.py
├── l4_003_pydantic_models.py
├── l4_003_request_validation.py
├── l4_003_response_validation.py
├── l4_003_middleware.py
└── l4_003_background_tasks.py
```

---

# Prerequisites

- Python 3.12+
- Virtual Environment (.venv)
- FastAPI
- Uvicorn
- Pydantic

---

# Activate Virtual Environment

## macOS / Linux

```bash
source /path/to/Python-Mastery/.venv/bin/activate
```

Verify Python:

```bash
which python3
```

Expected output (example):

```text
/path/to/Python-Mastery/.venv/bin/python3
```

---

# Install Dependencies

```bash
python3 -m pip install fastapi uvicorn pydantic
```

Verify installation:

```bash
python3 -m pip show fastapi
python3 -m pip show uvicorn
python3 -m pip show pydantic
```

---

# Running the Examples

Navigate to the folder:

```bash
cd l4_003_fastapi_in_depth
```

Run any lesson using:

```bash
python3 -m uvicorn <filename_without_py>:app --reload
```

Example:

```bash
python3 -m uvicorn l4_003_basic_routes:app --reload
```

---

# Run Commands

## Basic Routes

```bash
python3 -m uvicorn l4_003_basic_routes:app --reload
```

---

## Path Parameters

```bash
python3 -m uvicorn l4_003_path_parameters:app --reload
```

---

## Query Parameters

```bash
python3 -m uvicorn l4_003_query_parameters:app --reload
```

---

## Dependency Injection

```bash
python3 -m uvicorn l4_003_dependency_injection:app --reload
```

---

## Pydantic Models

```bash
python3 -m uvicorn l4_003_pydantic_models:app --reload
```

---

## Request Validation

```bash
python3 -m uvicorn l4_003_request_validation:app --reload
```

---

## Response Validation

```bash
python3 -m uvicorn l4_003_response_validation:app --reload
```

---

## Middleware

```bash
python3 -m uvicorn l4_003_middleware:app --reload
```

---

## Background Tasks

```bash
python3 -m uvicorn l4_003_background_tasks:app --reload
```

---

# Open the API

After running any file:

```text
http://127.0.0.1:8000
```

---

# Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

Swagger allows you to:

- Test API endpoints
- Send request bodies
- Enter path parameters
- Enter query parameters
- View response data
- View response headers
- View automatically generated schemas

---

# Open OpenAPI Specification

```text
http://127.0.0.1:8000/openapi.json
```

---

# Stop the Server

Press:

```text
CTRL + C
```

---

# Understanding the Uvicorn Command

Example:

```bash
python3 -m uvicorn l4_003_basic_routes:app --reload
```

Breakdown:

```text
python3 -m uvicorn
```

Runs the Uvicorn ASGI server.

```text
l4_003_basic_routes
```

The Python filename (without `.py`).

```text
:app
```

The FastAPI application object.

```python
app = FastAPI()
```

```text
--reload
```

Automatically reloads the server whenever the source code changes.

---

# Concepts

## Basic Routes

Maps an HTTP request to a Python function.

Example:

```python
@app.get("/")
def home():
    ...
```

---

## Path Parameters

Used to identify a specific resource.

Example:

```text
/customers/15
```

FastAPI:

```python
@app.get("/customers/{customer_id}")
```

---

## Query Parameters

Used for:

- Filtering
- Searching
- Pagination
- Sorting

Example:

```text
/customers?country=UAE&limit=10
```

---

## Dependency Injection

Provides reusable functionality to routes.

Example:

```python
Depends(get_current_user)
```

Common uses:

- Authentication
- Authorization
- Database Session
- Current User
- Shared Configuration

Flow:

```text
Route
   ↓
Depends(...)
   ↓
FastAPI executes dependency
   ↓
Dependency result injected
   ↓
Route executes
```

---

## Pydantic Models

Defines structured API data.

Example:

```python
class Customer(BaseModel):
    name: str
    age: int
```

Used for automatic validation and documentation.

---

## Request Validation

Protects the API from invalid client input.

Example:

```python
age: int = Field(ge=18, le=65)
```

Useful validation options:

- `gt` → Greater Than
- `ge` → Greater Than or Equal
- `lt` → Less Than
- `le` → Less Than or Equal
- `min_length`
- `max_length`

Invalid requests return:

```text
422 Unprocessable Entity
```

---

## Response Validation

Controls the data returned to clients.

Example:

```python
@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse
)
```

Useful for:

- Hiding passwords
- Removing internal fields
- Returning only public data

---

## Middleware

Middleware runs before and after every request.

Flow:

```text
Request
    ↓
Middleware
    ↓
Route
    ↓
Middleware
    ↓
Response
```

Typical uses:

- Logging
- Execution timing
- CORS
- Security Headers
- Request IDs
- Correlation IDs

Core line:

```python
response = await call_next(request)
```

---

## Background Tasks

Execute lightweight tasks after the response has been sent.

Flow:

```text
Request
    ↓
Route
    ↓
Return Response
    ↓
Background Task Executes
```

Examples:

- Send email
- Write audit log
- Send notification

Example:

```python
background_tasks.add_task(send_email, email)
```

For long-running or distributed jobs, use:

- Celery
- RabbitMQ
- Redis Queue (RQ)

---

# FastAPI Request Lifecycle

```text
Client
   │
   ▼
Uvicorn
   │
   ▼
FastAPI
   │
   ▼
Middleware
   │
   ▼
Dependencies
   │
   ▼
Request Validation
   │
   ▼
Route Function
   │
   ▼
Business Logic
   │
   ▼
Response Validation
   │
   ▼
Middleware
   │
   ▼
Uvicorn
   │
   ▼
Client
```

---

# Common Errors

## Module Could Not Be Imported

```
Error loading ASGI app.
Could not import module "filename"
```

**Solution**

- Make sure you're inside the folder containing the file.
- Remove the `.py` extension from the command.

Correct:

```bash
python3 -m uvicorn l4_003_basic_routes:app --reload
```

Incorrect:

```bash
python3 -m uvicorn l4_003_basic_routes.py:app --reload
```

---

## ModuleNotFoundError

```
No module named 'fastapi'
```

**Solution**

Activate your virtual environment.

```bash
source /path/to/.venv/bin/activate
```

---

## Port Already in Use

Run on another port:

```bash
python3 -m uvicorn l4_003_basic_routes:app --reload --port 8001
```

Open:

```text
http://127.0.0.1:8001/docs
```

---

# Summary

Throughout this lesson you learned:

- Creating API routes
- Path parameters
- Query parameters
- Dependency Injection
- Pydantic models
- Request validation
- Response validation
- Middleware
- Background tasks

These concepts form the foundation of building production-ready APIs with FastAPI and prepare you for database integration, authentication, testing, Docker, and deployment in the upcoming L4 lessons.