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
