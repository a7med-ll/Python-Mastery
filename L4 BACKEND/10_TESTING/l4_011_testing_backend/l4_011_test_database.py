from sqlalchemy import create_engine, text

# -----------------------------------------------------------------------------
# Database Connection URL
# -----------------------------------------------------------------------------

DATABASE_URL = (
    "postgresql+psycopg://nadalateef@localhost:5432/python_mastery_db"
)

# -----------------------------------------------------------------------------
# Create Database Engine
# -----------------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL
)

# -----------------------------------------------------------------------------
# Test Database Connection
# -----------------------------------------------------------------------------

def test_l4_011DatabaseConnection() -> None:
    """Verify database connection works."""

    # Open database connection.
    with engine.connect() as connection:

        # Execute simple SQL query.
        result = connection.execute(
            text(
                "SELECT 1"
            )
        )

        # Get returned value.
        value = result.scalar()

    # Verify database returned expected value.
    assert value == 1

# -----------------------------------------------------------------------------
# Test Insert Transaction
# -----------------------------------------------------------------------------

def test_l4_011InsertTransaction() -> None:
    """Verify transaction insert works."""

    # Begin database transaction.
    with engine.begin() as connection:

        # Execute INSERT query.
        result = connection.execute(
            text(
                """
                INSERT INTO transactions_testing
                (
                    customer_name,
                    amount,
                    status
                )
                VALUES
                (
                    'Lokesh',
                    7000,
                    'COMPLETED'
                )
                RETURNING transaction_id
                """
            )
        )

        # Get generated transaction id.
        transaction_id = result.scalar()

    # Verify insert created a record.
    assert transaction_id is not None

# -----------------------------------------------------------------------------
# Test Read Transaction
# -----------------------------------------------------------------------------

def test_l4_011ReadTransaction() -> None:
    """Verify transaction read works."""

    # Open database connection.
    with engine.connect() as connection:

        # Execute SELECT query.
        result = connection.execute(
            text(
                """
                SELECT customer_name,
                       amount,
                       status
                FROM transactions_testing
                WHERE customer_name = 'Lokesh'
                ORDER BY transaction_id DESC LIMIT 1
                """
            )
        )

        # Fetch first matching row.
        row = result.first()

    # Verify returned data.
    assert row is not None
    assert row.customer_name == "Lokesh"
    assert row.amount == 7000
    assert row.status == "COMPLETED"

# -----------------------------------------------------------------------------
# Test Update Transaction
# -----------------------------------------------------------------------------

def test_l4_011UpdateTransaction() -> None:
    """Verify transaction update works."""

    # Begin transaction.
    with engine.begin() as connection:

        # Execute UPDATE query.
        result = connection.execute(
            text(
                """
                UPDATE
                    transactions_testing
                SET
                    amount = 9000
                WHERE
                    customer_name = 'Lokesh'
                """
            )
        )

    # Verify one row updated.
    assert result.rowcount >= 1

# -----------------------------------------------------------------------------
# Test Delete Transaction
# -----------------------------------------------------------------------------

def test_l4_011DeleteTransaction() -> None:
    """Verify transaction delete works."""

    with engine.begin() as connection:

        # Insert temporary record
        connection.execute(
            text(
                """
                INSERT INTO transactions_testing
                (
                    customer_name,
                    amount,
                    status
                )
                VALUES
                (
                    'Delete_Test_User',
                    1000,
                    'PENDING'
                )
                """
            )
        )


        # Delete temporary record
        result = connection.execute(
            text(
                """
                DELETE FROM
                    transactions_testing
                WHERE
                    customer_name = 'Delete_Test_User'
                """
            )
        )


    assert result.rowcount == 1