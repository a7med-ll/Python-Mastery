# -----------------------------------------------------------------------------
# HTTP Statelessness
# -----------------------------------------------------------------------------

def l4_002StatelessRequest() -> None:
    """Explain a stateless HTTP request."""

    print("Stateless Request")
    print("Each HTTP request is processed independently.")
    print("The server does not remember previous requests.")
    print()


def l4_002ClientProvidesAuthentication() -> None:
    """Explain client authentication."""

    print("Client Authentication")
    print("Each request includes authentication information.")
    print("Example: Authorization: Bearer <JWT_TOKEN>")
    print()


def l4_002BenefitsOfStatelessness() -> None:
    """Explain the benefits of stateless communication."""

    print("Benefits")
    print("- Easy to scale")
    print("- Lower memory usage")
    print("- Better load balancing")
    print("- Independent requests")
    print()


# -----------------------------------------------------------------------------
# Run Statelessness Example
# -----------------------------------------------------------------------------

def run_l4_002Statelessness() -> None:
    """Run all statelessness examples."""

    l4_002StatelessRequest()
    l4_002ClientProvidesAuthentication()
    l4_002BenefitsOfStatelessness()


# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_l4_002Statelessness()