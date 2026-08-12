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

    customer_id: Mapped[int] = mapped_column(primary_key=True)

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
# Get Customer Using Cache Aside
# -----------------------------------------------------------------------------

def l4_005GetCustomer(customer_id: int) -> dict | None:
    """Get customer using Redis cache and PostgreSQL."""

    # Create Redis cache key.
    cache_key = f"customer:{customer_id}"

    # Check if customer exists in Redis.
    cached_customer = redis_client.get(
        cache_key
    )

    # Return cached data if found.
    if cached_customer is not None:

        print("Cache Hit")

        return json.loads(
            cached_customer
        )

    # Cache does not contain customer.
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

        # Convert customer object into dictionary.
        customer_data = {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "email": customer.email,
            "country": customer.country,
            "balance": float(customer.balance)
        }

    # Store customer data in Redis for 60 seconds.
    redis_client.set(
        cache_key,
        json.dumps(customer_data),
        ex=60
    )

    print("Customer stored in Redis.")

    return customer_data

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    customer = l4_005GetCustomer(1)

    print(customer)