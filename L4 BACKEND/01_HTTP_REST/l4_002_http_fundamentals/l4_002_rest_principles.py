# -----------------------------------------------------------------------------
# REST Principles
# -----------------------------------------------------------------------------

def l4_002ClientServerPrinciple() -> None:
    """Explain client-server separation."""

    print("Client-Server Separation")
    print("The client handles the user interface.")
    print("The server processes business logic and data.")
    print()


def l4_002StatelessPrinciple() -> None:
    """Explain stateless communication."""

    print("Stateless Communication")
    print("Each request is independent.")
    print("The server does not remember previous requests.")
    print()


def l4_002ResourceBasedUrls() -> None:
    """Explain resource-based URLs."""

    print("Resource-Based URLs")
    print("Good : /customers")
    print("Good : /transactions")
    print("Bad  : /getCustomer")
    print()


def l4_002HttpMethodsPrinciple() -> None:
    """Explain proper HTTP method usage."""

    print("HTTP Methods")
    print("GET    -> Read")
    print("POST   -> Create")
    print("PATCH  -> Update")
    print("DELETE -> Delete")
    print()


def l4_002StatusCodesPrinciple() -> None:
    """Explain proper status code usage."""

    print("HTTP Status Codes")
    print("200 -> Success")
    print("201 -> Created")
    print("400 -> Bad Request")
    print("404 -> Not Found")
    print("500 -> Internal Server Error")
    print()


# -----------------------------------------------------------------------------
# Run REST Principles Example
# -----------------------------------------------------------------------------

def run_l4_002RestPrinciples() -> None:
    """Run all REST principle examples."""

    l4_002ClientServerPrinciple()
    l4_002StatelessPrinciple()
    l4_002ResourceBasedUrls()
    l4_002HttpMethodsPrinciple()
    l4_002StatusCodesPrinciple()


# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_l4_002RestPrinciples()