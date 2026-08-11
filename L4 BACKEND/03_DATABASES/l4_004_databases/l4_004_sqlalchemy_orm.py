from decimal import Decimal

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
# Create ORM Base Class
# -----------------------------------------------------------------------------

class Base(DeclarativeBase):      # --> creates the base class used by ORM models.
    """Base class for ORM models."""

    pass

# -----------------------------------------------------------------------------
# Customer ORM Model
# -----------------------------------------------------------------------------

class Customer(Base):      #--> this Python class represents a database table.
    """Map the customers table to a Python class."""

    __tablename__ = "customers"     # --> tells SQLAlchemy which table it maps to.

    customer_id: Mapped[int] = mapped_column(primary_key=True)    # --> maps a Python attribute to the database's primary key column.
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    country: Mapped[str | None] = mapped_column(String(100))
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)

# -----------------------------------------------------------------------------
# Read Customers
# -----------------------------------------------------------------------------


def l4_004ReadCustomersOrm() -> None:
    """Read customers using SQLAlchemy ORM."""

    with Session(engine) as session:

        customers = session.query(Customer).all()    # --> give me all rows from the customers table as Customer objects

        for customer in customers:
            print(
                customer.customer_id,
                customer.name,
                customer.email,
                customer.country,
                customer.balance
            )

# -----------------------------------------------------------------------------
# Insert Customer
# -----------------------------------------------------------------------------

def l4_004InsertCustomerOrm() -> None:
    """Insert a customer using SQLAlchemy ORM."""

    # Create Python object.
    customer = Customer(
        name="Sara",
        email="sara@example.com",
        country="Canada",
        balance=4000
    )

    # Open ORM session.
    with Session(engine) as session:

        # Add object to session.
        session.add(customer)

        # Save transaction permanently.
        session.commit()

        # Refresh object with database-generated values.
        session.refresh(customer)

        print(
            customer.customer_id,
            customer.name,
            customer.email,
            customer.country,
            customer.balance
        )

# -----------------------------------------------------------------------------
# Read Customer By ID
# -----------------------------------------------------------------------------

def l4_004ReadCustomerByIdOrm(customer_id: int) -> None:
    """Read one customer using SQLAlchemy ORM."""

    with Session(engine) as session:

        customer = session.get(Customer, customer_id)

        print(customer)


# -----------------------------------------------------------------------------
# Update Customer
# -----------------------------------------------------------------------------

def l4_004UpdateCustomerOrm(
    customer_id: int,
    new_balance: float
) -> None:
    """Update a customer using SQLAlchemy ORM."""

    with Session(engine) as session:

        customer = session.get(Customer, customer_id)

        if customer is None:
            print("Customer not found.")
            return

        customer.balance = new_balance

        session.commit()

        print("Customer updated successfully.")


# -----------------------------------------------------------------------------
# Delete Customer
# -----------------------------------------------------------------------------

def l4_004DeleteCustomerOrm(customer_id: int) -> None:
    """Delete a customer using SQLAlchemy ORM."""

    with Session(engine) as session:

        customer = session.get(Customer, customer_id)

        if customer is None:
            print("Customer not found.")
            return

        session.delete(customer)

        session.commit()

        print("Customer deleted successfully.")

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    l4_004DeleteCustomerOrm(4)