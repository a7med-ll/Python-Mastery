from models import L3_017Product, L3_017User


#-------------------------------------------------------------------------
# Test ORM Models
#-------------------------------------------------------------------------

def run_l3_017ORMDemo() -> None:
    """Run the mini ORM descriptor example."""

    # Create a valid user object.
    user = L3_017User(
        username="Ahmed",
        age=30,
        email="ahmed@example.com",
    )

    print(user)

    # Create a valid product object.
    product = L3_017Product(
        name="Laptop",
        price=999.99,
        stock=10,
    )

    print(product)

    # Test invalid type validation.
    try:
        invalid_user = L3_017User(
            username="Ahmed",
            age="thirty",
        )

    except TypeError as error:
        print(f"Type Error: {error}")

    # Test required field validation.
    try:
        missing_user = L3_017User(
            username=None,
            age=30,
        )

    except ValueError as error:
        print(f"Value Error: {error}")


#-------------------------------------------------------------------------
# Program Entry Point
#-------------------------------------------------------------------------

def main() -> None:
    """Program entry point."""

    run_l3_017ORMDemo()


if __name__ == "__main__":
    main()