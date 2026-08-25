# L4-011 Backend Testing

## Overview

This module covers backend testing fundamentals using:

- pytest
- FastAPI TestClient
- SQLAlchemy
- PostgreSQL

The goal is to understand how production backend systems test different layers of an application.

---

# Testing Layers Covered

## 1. Basic Testing

File:

```
l4_011_test_basic.py
```

Purpose:

Tests simple Python logic and validates expected outputs.

Concepts learned:

- pytest test functions
- Assertions
- Expected vs actual values
- Test execution flow

Run:

```bash
pytest l4_011_test_basic.py -v
```

---

# 2. API Testing

File:

```
l4_011_test_api.py
```

Purpose:

Tests FastAPI endpoints without starting a real web server.

Concepts learned:

- FastAPI TestClient
- HTTP request testing
- Status code validation
- JSON response validation

Run:

```bash
pytest l4_011_test_api.py -v
```

---

# 3. Database Testing

File:

```
l4_011_test_database.py
```

Purpose:

Tests database operations using PostgreSQL.

Database:

```
PostgreSQL
```

Test table:

```
transactions_testing
```

Operations tested:

- Database connection
- Insert transaction
- Read transaction
- Update transaction
- Delete transaction

Concepts learned:

- SQLAlchemy engine
- Database connections
- SQL execution
- Transactions
- CRUD testing

Run:

```bash
pytest l4_011_test_database.py -v
```

---

# 4. Contract Testing

File:

```
l4_011_test_contract.py
```

Purpose:

Ensures API responses follow the expected structure.

Example:

```json
{
    "customer_id": 1001,
    "name": "Ahmed",
    "status": "ACTIVE"
}
```

Validated:

- Required fields
- Data types
- Response stability

Run:

```bash
pytest l4_011_test_contract.py -v
```

---

# Run All Tests

```bash
pytest -v
```

Expected:

```
5 passed
```

---

# Required Packages

```bash
pip install pytest
pip install fastapi
pip install httpx
pip install sqlalchemy
pip install psycopg[binary]
```

---

# Project Structure

```
l4_011_testing_backend

│
├── l4_011_test_basic.py
├── l4_011_test_api.py
├── l4_011_test_database.py
├── l4_011_test_contract.py
├── results/
└── README.md
```

---

# Testing Flow

```
Application Code
        |
        v
Automated Tests
        |
        v
Validation
        |
        v
Safe Deployment
```

---

# Key Takeaways

After completing L4-011:

- Understand pytest based backend testing
- Test FastAPI endpoints
- Validate API contracts
- Test PostgreSQL operations
- Understand different backend testing layers

Testing helps maintain reliability as backend systems grow and change.
