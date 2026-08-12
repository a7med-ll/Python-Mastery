import json
import redis

from sqlalchemy import Numeric, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# -----------------------------------------------------------------------------
# Database Connection URL
# -----------------------------------------------------------------------------

DATABASE_URL = (
    "postgresql+psycopg://nadalateef@localhost:5432/python_mastery_db"
)

# -----------------------------------------------------------------------------
# Create Database Engine
# -----------------------------------------------------------------------------

engine = create_engine(DATABASE_URL)

# -----------------------------------------------------------------------------
# Create Redis Connection
# -----------------------------------------------------------------------------

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# -----------------------------------------------------------------------------
# Create ORM Base Class
# -----------------------------------------------------------------------------

class Base(DeclarativeBase):
    """Base class for ORM models."""

    pass

# -----------------------------------------------------------------------------
# Customer ORM Model
# -----------------------------------------------------------------------------

class Customer(Base):
    """Map the customers table to Python class."""

    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str | None] = mapped_column(
        String(255)
    )

    country: Mapped[str | None] = mapped_column(
        String(100)
    )

    balance: Mapped[float] = mapped_column(
        Numeric(10, 2)
    )

# -----------------------------------------------------------------------------
# Get Customer Using Cache
# -----------------------------------------------------------------------------

def l4_005GetCustomer(customer_id: int) -> dict | None:
    """Get customer using Redis cache and PostgreSQL."""

    # Create Redis cache key.
    cache_key = f"customer:{customer_id}"

    # Check Redis first.
    cached_customer = redis_client.get(
        cache_key
    )

    # Return cached customer if found.
    if cached_customer is not None:

        print("Cache Hit")

        return json.loads(
            cached_customer
        )

    print("Cache Miss")

    # Open database session.
    with Session(engine) as session:

        # Find customer from PostgreSQL.
        customer = session.get(
            Customer,
            customer_id
        )

        # Check if customer exists.
        if customer is None:
            print("Customer not found.")
            return None

        # Convert ORM object into dictionary.
        customer_data = {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "email": customer.email,
            "country": customer.country,
            "balance": float(customer.balance)
        }

    # Store customer in Redis.
    redis_client.set(
        cache_key,
        json.dumps(customer_data),
        ex=60
    )

    return customer_data

# -----------------------------------------------------------------------------
# Update Customer And Invalidate Cache
# -----------------------------------------------------------------------------

def l4_005UpdateCustomerBalance(
    customer_id: int,
    new_balance: float
) -> None:
    """Update customer balance and remove stale cache."""

    # Open database session.
    with Session(engine) as session:

        # Find customer from PostgreSQL.
        customer = session.get(
            Customer,
            customer_id
        )

        # Check if customer exists.
        if customer is None:
            print("Customer not found.")
            return

        # Update customer balance.
        customer.balance = new_balance

        # Save database changes.
        session.commit()

    # Create Redis cache key.
    cache_key = f"customer:{customer_id}"

    # Delete stale customer cache.
    redis_client.delete(
        cache_key
    )

    print("Customer updated.")
    print("Customer cache invalidated.")

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # First read stores customer in Redis.
    print(
        l4_005GetCustomer(1)
    )

    # Update PostgreSQL and delete Redis cache.
    l4_005UpdateCustomerBalance(
        1,
        9000
    )

    # Next read gets fresh PostgreSQL data.
    print(
        l4_005GetCustomer(1)
    )