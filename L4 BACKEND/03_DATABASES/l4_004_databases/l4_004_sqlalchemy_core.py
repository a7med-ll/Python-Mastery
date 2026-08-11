from sqlalchemy import MetaData, Table, create_engine, select

# -----------------------------------------------------------------------------
# Database Connection URL
# -----------------------------------------------------------------------------

DATABASE_URL = (
    "postgresql+psycopg://nadalateef@localhost:5432/python_mastery_db"
)

# -----------------------------------------------------------------------------
# Create Database Engine
# -----------------------------------------------------------------------------

engine = create_engine(DATABASE_URL)    # --> creates SQLAlchemy's connection interface to PostgreSQL.

# -----------------------------------------------------------------------------
# Create Metadata
# -----------------------------------------------------------------------------

metadata = MetaData()    # --> Python-side collection of information about your database schema.

# -----------------------------------------------------------------------------
# Load Existing Customers Table
# -----------------------------------------------------------------------------

customers = Table(
    "customers",
    metadata,
    autoload_with=engine   #--> Connect to PostgreSQL, inspect the existing customers table, and load its structure into this Python Table object.
                           #--> This process is called reflection.
)

# -----------------------------------------------------------------------------
# Read Customers
# -----------------------------------------------------------------------------

def l4_004ReadCustomers() -> None:
    """Read customers using SQLAlchemy Core."""

    # Build SELECT statement.
    statement = select(customers)      # --> SQLAlchemy actually constructing the SQL for you.

    # Open database connection.
    with engine.connect() as connection:

        # Execute statement.
        result = connection.execute(statement)

        # Print returned rows.
        for row in result:
            print(row)

# -----------------------------------------------------------------------------
# Insert Customer
# -----------------------------------------------------------------------------

def l4_004InsertCustomer() -> None:
    """Insert customers using SQLAlchemy Core."""

    statement = customers.insert().values(

        name="Lokesh",
        email="lokesh1234@gmail.com",
        country="UK",
        balance="7000",

    )

    # Begin transaction and automatically commit if successful.
    with engine.begin() as connection:
        connection.execute(statement)

    print("Customer inserted successfully.")

# -----------------------------------------------------------------------------
# Read Customer By ID
# -----------------------------------------------------------------------------

def l4_004ReadCustomerById(customer_id: int) -> None:
    """Read one customer using SQLAlchemy Core."""

    # Build SELECT statement.
    statement = (
        customers
        .select()
        .where(customers.c.customer_id == customer_id)
    )

    # Open database connection.
    with engine.connect() as connection:

        # Execute SELECT statement.
        result = connection.execute(statement)

        # Return the first matching row.
        row = result.first()

        print(row)

# -----------------------------------------------------------------------------
# Update Customer
# -----------------------------------------------------------------------------

def l4_004UpdateCustomer(
    customer_id: int,
    new_balance: float
) -> None:
    """Update a customer's balance using SQLAlchemy Core."""

    # Build UPDATE statement.
    statement = (
        customers
        .update()
        .where(customers.c.customer_id == customer_id)
        .values(balance=new_balance)
    )

    # Execute and commit transaction.
    with engine.begin() as connection:
        result = connection.execute(statement)

    print(f"Updated rows: {result.rowcount}")

# -----------------------------------------------------------------------------
# Delete Customer
# -----------------------------------------------------------------------------

def l4_004DeleteCustomer(customer_id: int) -> None:
    """Delete a customer using SQLAlchemy Core."""

    # Build DELETE statement.
    statement = (
        customers
        .delete()
        .where(customers.c.customer_id == customer_id)
    )

    # Execute and commit transaction.
    with engine.begin() as connection:
        result = connection.execute(statement)

    print(f"Deleted rows: {result.rowcount}")

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    l4_004DeleteCustomer(999)