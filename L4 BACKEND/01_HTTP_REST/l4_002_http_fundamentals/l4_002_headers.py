# -----------------------------------------------------------------------------
# HTTP Headers
# -----------------------------------------------------------------------------

def l4_002HostHeader() -> None:
    """Explain the Host header."""

    print("Host")
    print("Identifies the server receiving the request.")
    print("Example: Host: api.bank.com")
    print()


def l4_002AuthorizationHeader() -> None:
    """Explain the Authorization header."""

    print("Authorization")
    print("Sends authentication credentials to the server.")
    print("Example: Authorization: Bearer <JWT_TOKEN>")
    print()


def l4_002ContentTypeHeader() -> None:
    """Explain the Content-Type header."""

    print("Content-Type")
    print("Specifies the format of the request body.")
    print("Example: Content-Type: application/json")
    print()


def l4_002AcceptHeader() -> None:
    """Explain the Accept header."""

    print("Accept")
    print("Specifies the response format expected from the server.")
    print("Example: Accept: application/json")
    print()


def l4_002UserAgentHeader() -> None:
    """Explain the User-Agent header."""

    print("User-Agent")
    print("Identifies the client sending the request.")
    print("Example: User-Agent: PayNow Mobile App")
    print()


# -----------------------------------------------------------------------------
# Run HTTP Headers Example
# -----------------------------------------------------------------------------

def run_l4_002HttpHeaders() -> None:
    """Run all HTTP header examples."""

    l4_002HostHeader()
    l4_002AuthorizationHeader()
    l4_002ContentTypeHeader()
    l4_002AcceptHeader()
    l4_002UserAgentHeader()


# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_l4_002HttpHeaders()