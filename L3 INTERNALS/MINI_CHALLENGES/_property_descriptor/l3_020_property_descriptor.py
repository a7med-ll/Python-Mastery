from typing import Any, Callable

# -----------------------------------------------------------------------------
# Property Descriptor Implementation
# -----------------------------------------------------------------------------

class l3_020Property:

    def __init__(self, getter=None) -> None:

        # Store getter function.
        self._getter = getter

        # Store setter function.
        self._setter = None

    def __get__(self, instance, owner) -> Any:

        # Return descriptor when accessed from class.
        if instance is None:
            return self

        # Return value using getter function.
        return self._getter(instance)

    def __set__(self, instance, value: Any) -> None:
        # Check if setter exists.
        if self._setter is None:
            raise AttributeError("Property has no setter")

        # Set value using setter function.
        self._setter(instance, value)

    def setter(self, setter: Callable) -> "l3_020Property":

        # Create new property descriptor.
        property_copy = l3_020Property(self._getter)

        # Store setter function.
        property_copy._setter = setter

        # Return updated descriptor.
        return property_copy

# -----------------------------------------------------------------------------
# Example Class Using Descriptor
# -----------------------------------------------------------------------------

class l3_020Person:

    @l3_020Property
    def age(self) -> int:

        # Return stored age value.
        return self._age


    @age.setter
    def age(self, value: int) -> None:

        # Validate age range.
        if value < 0 or value > 120:
            raise ValueError("Age must be between 0 and 120")

        # Store age value.
        self._age = value

# -----------------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------------

def run_l3_020PropertyDescriptor() -> None:

    print("=" * 70)
    print("L3-020 Custom Property Descriptor")
    print("=" * 70)


    # -------------------------------------------------------------------------
    # Test 1: Valid Property Assignment
    # -------------------------------------------------------------------------

    print("\n[TEST 1] Valid Age Assignment")
    print("-" * 70)

    # Create person object.
    person = l3_020Person()

    # Set age value.
    person.age = 30

    # Read age value.
    print(f"Person Age: {person.age}")


    # -------------------------------------------------------------------------
    # Test 2: Property Validation
    # -------------------------------------------------------------------------

    print("\n[TEST 2] Property Validation")
    print("-" * 70)

    try:

        # Set invalid age.
        person.age = 150

    except ValueError as exception:

        print(f"Caught Exception: {exception}")


    # -------------------------------------------------------------------------
    # Test 3: Descriptor Access
    # -------------------------------------------------------------------------

    print("\n[TEST 3] Descriptor Object Access")
    print("-" * 70)

    # Access descriptor from class.
    descriptor = l3_020Person.age

    print(f"Descriptor Type: {type(descriptor).__name__}")

    print("=" * 70)



if __name__ == "__main__":
    run_l3_020PropertyDescriptor()


