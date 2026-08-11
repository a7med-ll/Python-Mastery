# L4-004 — Databases

This module introduces relational databases, PostgreSQL, SQLAlchemy, and Alembic migrations.

---

## Topics Covered

- SQL Basics
- PostgreSQL
- Database Design
- Normalization
- SQLAlchemy Core
- SQLAlchemy ORM
- Relationships
- Database Sessions
- Alembic Migrations

---

## Files

| File | Description |
|------|-------------|
| `l4_004_sqlalchemy_core.py` | SQLAlchemy Core connection, CRUD operations, and SQL execution. |
| `l4_004_sqlalchemy_orm.py` | SQLAlchemy ORM models and CRUD operations using Python objects. |
| `l4_004_relationships.py` | One-to-Many relationships using `relationship()` and `ForeignKey`. |
| `l4_004_database_sessions.py` | Session management, transactions, commit, rollback, and error handling. |
| `alembic/` | Database migration environment and generated migration scripts. |

---

## Install Dependencies

```bash
python3 -m pip install sqlalchemy "psycopg[binary]" alembic
```

---

## Run Examples

### SQLAlchemy Core

```bash
python3 l4_004_sqlalchemy_core.py
```

### SQLAlchemy ORM

```bash
python3 l4_004_sqlalchemy_orm.py
```

### Relationships

```bash
python3 l4_004_relationships.py
```

### Database Sessions

```bash
python3 l4_004_database_sessions.py
```

---

## Alembic Commands

Initialize Alembic:

```bash
python3 -m alembic init alembic
```

Create a migration:

```bash
python3 -m alembic revision -m "migration_name"
```

Apply migrations:

```bash
python3 -m alembic upgrade head
```

Rollback one migration:

```bash
python3 -m alembic downgrade -1
```

View current revision:

```bash
python3 -m alembic current
```

View migration history:

```bash
python3 -m alembic history
```