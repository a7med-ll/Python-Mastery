from decimal import Decimal

from sqlalchemy import Numeric, String, create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

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
# Create Session Factory
# -----------------------------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine
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
    """Map the customers table."""

    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True
    )

    country: Mapped[str | None] = mapped_column(
        String(100)
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0
    )

# -----------------------------------------------------------------------------
# Read Customers Using Session
# -----------------------------------------------------------------------------

def l4_004ReadCustomersSession() -> None:
    """Read customers using a database session."""

    # Create session.
    with SessionLocal() as session:

        # Build SELECT statement.
        statement = select(Customer)

        # Execute query and return ORM objects.
        customers = session.scalars(statement).all()

        # Print customers.
        for customer in customers:
            print(
                customer.customer_id,
                customer.name,
                customer.email,
                customer.country,
                customer.balance
            )

# -----------------------------------------------------------------------------
# Insert Customer Using Session
# -----------------------------------------------------------------------------

def l4_004InsertCustomerSession() -> None:
    """Insert customer with commit and rollback handling."""

    customer = Customer(
        name="Michael",
        email="michael@example.com",
        country="USA",
        balance=6000
    )

    # Create session.
    with SessionLocal() as session:

        try:

            # Add object to session.
            session.add(customer)

            # Commit transaction.
            session.commit()

            # Reload generated values.
            session.refresh(customer)

            print(
                "Customer inserted:",
                customer.customer_id,
                customer.name
            )

        except SQLAlchemyError as error:

            # Undo transaction if something fails.
            session.rollback()

            print(
                "Database error:",
                error
            )

# -----------------------------------------------------------------------------
# Update Customer Using Session
# -----------------------------------------------------------------------------

def l4_004UpdateCustomerSession(
    customer_id: int,
    new_balance: float
) -> None:
    """Update customer balance using a session."""

    with SessionLocal() as session:

        try:

            customer = session.get(
                Customer,
                customer_id
            )

            if customer is None:
                print("Customer not found.")
                return

            customer.balance = new_balance

            session.commit()

            print("Customer updated successfully.")

        except SQLAlchemyError as error:

            session.rollback()

            print(
                "Database error:",
                error
            )

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Run one example at a time.

    l4_004ReadCustomersSession()

    # l4_004InsertCustomerSession()

    # l4_004UpdateCustomerSession(
    #     1,
    #     9000
    # )