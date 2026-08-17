# L4-007 — API Design

This module covers important API design concepts using FastAPI.

## Topics Covered

- API Versioning
- Pagination
- Filtering
- Idempotency
- Error Response Conventions
- OpenAPI / Swagger Documentation

---

## Files

```text
l4_007_api_design/
│
├── l4_007_api_versioning.py
├── l4_007_pagination.py
├── l4_007_filtering.py
├── l4_007_idempotency.py
├── l4_007_error_responses.py
├── l4_007_openapi_docs.py
└── README.md
```

---

# 1. API Versioning

File:

```text
l4_007_api_versioning.py
```

API versioning allows an API to introduce breaking changes without breaking existing clients.

Example:

```text
/api/v1/customers
/api/v2/customers
```

V1 and V2 can return different response structures while both versions continue working.

### Flow

```text
Client
  ↓
API Version
  ↓
/api/v1/customers
OR
/api/v2/customers
  ↓
Version-Specific Response
```

### Run

```bash
python3 l4_007_api_versioning.py
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# 2. Pagination

File:

```text
l4_007_pagination.py
```

Pagination divides a large collection of records into smaller pages.

Example:

```text
GET /customers?page=1&size=10
```

### Calculation

```text
offset = (page - 1) * size
```

Example:

```text
page = 2
size = 10

offset = (2 - 1) * 10
       = 10
```

The API returns customers 11–20.

### Flow

```text
HTTP Request
     ↓
page + size
     ↓
Calculate Offset
     ↓
Select Required Records
     ↓
Return Page
```

### Run

```bash
python3 l4_007_pagination.py
```

Test:

```text
/customers?page=1&size=10
/customers?page=2&size=10
/customers?page=3&size=10
```

---

# 3. Filtering

File:

```text
l4_007_filtering.py
```

Filtering returns only records that match conditions provided by the client.

Example:

```text
GET /customers?country=UAE
```

Multiple filters can also be combined:

```text
GET /customers?country=UAE&status=active
```

### Flow

```text
HTTP Request
     ↓
All Customers
     ↓
Apply Filters
     ↓
Matching Customers
     ↓
Return Response
```

### Run

```bash
python3 l4_007_filtering.py
```

Test:

```text
/customers
/customers?country=UAE
/customers?status=active
/customers?country=UAE&status=active
```

---

# 4. Idempotency

File:

```text
l4_007_idempotency.py
```

Idempotency prevents the same operation from accidentally being processed multiple times.

This is especially important for:

```text
Payments
Transfers
Orders
Withdrawals
Wallet Transactions
```

The client sends an idempotency key:

```text
Idempotency-Key: transfer-001
```

### First Request

```text
Request
   ↓
Idempotency Key
   ↓
Key Exists?
   ↓
NO
   ↓
Process Operation
   ↓
Store Result
   ↓
Return Response
```

### Duplicate Request

```text
Request
   ↓
Same Idempotency Key
   ↓
Key Exists?
   ↓
YES
   ↓
Do Not Process Again
   ↓
Return Stored Response
```

### Run

```bash
python3 l4_007_idempotency.py
```

Test using Swagger:

```text
POST /transfers

amount = 500
Idempotency-Key = transfer-001
```

Send the same request again with the same key.

The operation should not be processed again.

---

# 5. Error Response Conventions

File:

```text
l4_007_error_responses.py
```

APIs should use consistent error response structures.

Example:

```json
{
    "error": {
        "code": "CUSTOMER_NOT_FOUND",
        "message": "Customer was not found.",
        "status": 404
    }
}
```

### Common HTTP Status Codes

```text
400 → Bad Request
401 → Unauthorized
403 → Forbidden
404 → Not Found
409 → Conflict
422 → Validation Error
500 → Internal Server Error
```

### Error Structure

```text
HTTP Status
     +
Application Error Code
     +
Human-Readable Message
```

Example:

```text
404
CUSTOMER_NOT_FOUND
Customer was not found.
```

### Run

```bash
python3 l4_007_error_responses.py
```

Test:

```text
GET /customers/1
GET /customers/99
POST /customers/1/activate
POST /customers/2/activate
```

---

# 6. OpenAPI / Swagger Documentation

File:

```text
l4_007_openapi_docs.py
```

FastAPI automatically generates an OpenAPI specification from the application.

Swagger UI uses the OpenAPI specification to provide interactive API documentation.

### Flow

```text
FastAPI Code
     ↓
Type Hints
     +
Pydantic Models
     +
Endpoint Metadata
     ↓
OpenAPI Specification
     ↓
Swagger UI
     ↓
Interactive Documentation
```

Important FastAPI documentation features include:

```python
FastAPI(
    title="Customer API",
    description="Customer API description.",
    version="1.0.0"
)
```

Response models:

```python
response_model=CustomerResponse
```

Tags:

```python
tags=["Customers"]
```

Summary:

```python
summary="Get customer"
```

Additional responses:

```python
responses={
    404: {
        "description": "Customer not found."
    }
}
```

### Run

```bash
python3 l4_007_openapi_docs.py
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Test:

```text
GET /customers/1
GET /customers/2
GET /customers/99
```

---

# Running the Examples

Activate the project virtual environment first.

From the project root:

```bash
source ".venv/bin/activate"
```

Move into the API Design directory:

```bash
cd "TASKS/L4 BACKEND/06_API_DESIGN/l4_007_api_design"
```

Run any example:

```bash
python3 l4_007_api_versioning.py
```

or:

```bash
python3 l4_007_pagination.py
```

or:

```bash
python3 l4_007_filtering.py
```

or:

```bash
python3 l4_007_idempotency.py
```

or:

```bash
python3 l4_007_error_responses.py
```

or:

```bash
python3 l4_007_openapi_docs.py
```

Only run one example at a time because each example uses:

```text
127.0.0.1:8000
```

Stop the currently running server before starting another one:

```text
CTRL + C
```

Then open Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# L4-007 Workflow Summary

```text
API Design
│
├── Versioning
│     └── Maintain different API contracts
│
├── Pagination
│     └── Divide large datasets into pages
│
├── Filtering
│     └── Return records matching conditions
│
├── Idempotency
│     └── Prevent duplicate operations
│
├── Error Responses
│     └── Provide predictable error contracts
│
└── OpenAPI / Swagger
      └── Document and expose the API contract
```

## Completed Concepts

After completing L4-007:

```text
API Versioning        → /v1 and /v2
Pagination            → page + size
Filtering             → query parameters
Idempotency           → Idempotency-Key
Error Conventions     → consistent error structure
OpenAPI               → API specification
Swagger               → interactive API documentation
```