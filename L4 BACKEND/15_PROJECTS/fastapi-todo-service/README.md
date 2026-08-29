# FastAPI Todo Service

A small production-style Todo REST API built with FastAPI, PostgreSQL,
SQLAlchemy, Alembic, JWT authentication, Redis caching, rate limiting, Docker,
and Nginx.

## Features

- User registration and login
- JWT protected user and todo endpoints
- User profile update and deletion
- Todo create, read, update, delete, and pagination
- Ownership checks between users
- Redis cache with invalidation
- Redis based request rate limiting
- Request IDs, request logging, and consistent validation errors
- PostgreSQL migrations with Alembic
- Isolated automated tests using SQLite and fake Redis

## Run with Docker

Create the environment file:

```bash
cp .env.example .env
```

Change `JWT_SECRET_KEY` in `.env`, then run:

```bash
docker compose up --build
```

The API is available through Nginx at `http://localhost:8080`.

- Swagger UI: `http://localhost:8080/docs`
- Health: `http://localhost:8080/health`
- Readiness: `http://localhost:8080/ready`

Stop the services with:

```bash
docker compose down
```

## Run locally

Start PostgreSQL and Redis, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Run tests

The tests do not require running PostgreSQL or Redis:

```bash
pytest -q
```

## Main endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me`
- `GET /api/v1/users/{user_id}`
- `PUT /api/v1/users/{user_id}`
- `DELETE /api/v1/users/{user_id}`
- `POST /api/v1/todos/`
- `GET /api/v1/todos/`
- `GET /api/v1/todos/{todo_id}`
- `PUT /api/v1/todos/{todo_id}`
- `DELETE /api/v1/todos/{todo_id}`

Successful responses use `success`, `message`, and `data`. Validation and
application errors include an error message and error code.
