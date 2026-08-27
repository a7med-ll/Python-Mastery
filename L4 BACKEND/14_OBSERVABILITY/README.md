# L4-015 Observability Basics

## Overview

This project demonstrates basic backend observability concepts using
FastAPI.

Implemented concepts:

-   Structured logging
-   Application lifecycle events
-   Request logging middleware
-   Health checks
-   Metrics collection
-   Automated API testing

## Run Application

Create virtual environment:

``` bash
python3 -m venv .venv
```

Activate:

``` bash
source .venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Start application:

``` bash
uvicorn main:app --reload --port 8000
```

## Endpoints

Root:

    GET /

Health:

    GET /health

Metrics:

    GET /metrics

## Run Tests

``` bash
pytest tests/test_observability.py -v
```

Expected:

    4 passed

## Learning Objective

This module demonstrates backend observability fundamentals:

-   Logs show application events
-   Metrics show system performance
-   Health checks show service availability
-   Middleware captures request lifecycle information
