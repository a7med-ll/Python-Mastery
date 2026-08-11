from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

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

class Base(DeclarativeBase):
    """Base class for ORM models."""

    pass

# -----------------------------------------------------------------------------
# Customer ORM Model
# -----------------------------------------------------------------------------

class Customer(Base):
    """Map the customers table."""

    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)

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

    # One customer can have many wallets.
    wallets: Mapped[list["Wallet"]] = relationship(
        back_populates="customer"
    )

# -----------------------------------------------------------------------------
# Wallet ORM Model
# -----------------------------------------------------------------------------

class Wallet(Base):
    """Map the wallets table."""

    __tablename__ = "wallets"

    wallet_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.customer_id")
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0
    )

    # Each wallet belongs to one customer.
    customer: Mapped["Customer"] = relationship(
        back_populates="wallets"
    )

# -----------------------------------------------------------------------------
# Create Missing Tables
# -----------------------------------------------------------------------------

Base.metadata.create_all(engine)

# -----------------------------------------------------------------------------
# Insert Wallet
# -----------------------------------------------------------------------------

def l4_004InsertWallet(
    customer_id: int,
    balance: float
) -> None:
    """Insert a wallet for a customer."""

    # Create wallet object.
    wallet = Wallet(
        customer_id=customer_id,
        balance=balance
    )

    # Open database session.
    with Session(engine) as session:

        # Add wallet to session.
        session.add(wallet)

        # Save changes.
        session.commit()

        # Refresh object with generated wallet ID.
        session.refresh(wallet)

        print(
            "Wallet inserted successfully:",
            wallet.wallet_id
        )

# -----------------------------------------------------------------------------
# Read Customer Wallets
# -----------------------------------------------------------------------------

def l4_004ReadCustomerWallets(
    customer_id: int
) -> None:
    """Read customer and related wallets."""

    # Open database session.
    with Session(engine) as session:

        # Find customer by primary key.
        customer = session.get(
            Customer,
            customer_id
        )

        # Check if customer exists.
        if customer is None:
            print("Customer not found.")
            return

        # Print customer information.
        print(f"Customer: {customer.name}")

        # Print all wallets belonging to customer.
        for wallet in customer.wallets:
            print(
                f"Wallet ID: {wallet.wallet_id}",
                f"Balance: {wallet.balance}"
            )

# -----------------------------------------------------------------------------
# Read Wallet Customer
# -----------------------------------------------------------------------------

def l4_004ReadWalletCustomer(
    wallet_id: int
) -> None:
    """Read a wallet and its related customer."""

    # Open database session.
    with Session(engine) as session:

        # Find wallet by primary key.
        wallet = session.get(
            Wallet,
            wallet_id
        )

        # Check if wallet exists.
        if wallet is None:
            print("Wallet not found.")
            return

        # Access related customer object.
        print(
            f"Wallet ID: {wallet.wallet_id}",
            f"Balance: {wallet.balance}"
        )

        print(
            f"Customer ID: {wallet.customer.customer_id}",
            f"Customer Name: {wallet.customer.name}"
        )

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Run only one function at a time while testing.

    # Insert wallet for customer 1.
    # l4_004InsertWallet(1, 2500)

    # Read all wallets belonging to customer 1.
    l4_004ReadCustomerWallets(1)

    # Read wallet and its customer.
    # l4_004ReadWalletCustomer(1)