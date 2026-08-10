# -----------------------------------------------------------------------------
# HTTP Methods
# -----------------------------------------------------------------------------

def l4_002GetMethod() -> None:
    """Explain the GET HTTP method."""

    print("GET")
    print("Used to retrieve data from the server.")
    print("Example: GET /users/10")
    print()

def l4_002PostMethod() -> None:
    """Explain the POST HTTP method."""

    print("POST")
    print("Used to create a new resource.")
    print("Example: POST /users")
    print()


def l4_002PutMethod() -> None:
    """Explain the PUT HTTP method."""

    print("PUT")
    print("Used to replace an existing resource completely.")
    print("Example: PUT /users/10")
    print()


def l4_002PatchMethod() -> None:
    """Explain the PATCH HTTP method."""

    print("PATCH")
    print("Used to update part of an existing resource.")
    print("Example: PATCH /users/10")
    print()


def l4_002DeleteMethod() -> None:
    """Explain the DELETE HTTP method."""

    print("DELETE")
    print("Used to remove a resource.")
    print("Example: DELETE /users/10")
    print()


# -----------------------------------------------------------------------------
# Run HTTP Methods Example
# -----------------------------------------------------------------------------

def run_l4_002HttpMethods() -> None:
    """Run all HTTP method examples."""

    l4_002GetMethod()
    l4_002PostMethod()
    l4_002PutMethod()
    l4_002PatchMethod()
    l4_002DeleteMethod()


# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_l4_002HttpMethods()