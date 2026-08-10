# -----------------------------------------------------------------------------
# HTTP Status Codes
# -----------------------------------------------------------------------------

def l4_002InformationalStatusCodes() -> None:
    """Explain 1xx informational status codes."""

    print("1xx - Informational")
    print("100 Continue")
    print("The request has been received and the client can continue.")
    print()


def l4_002SuccessStatusCodes() -> None:
    """Explain 2xx success status codes."""

    print("2xx - Success")
    print("200 OK        -> Request completed successfully.")
    print("201 Created   -> New resource created successfully.")
    print("204 No Content-> Request completed successfully with no response body.")
    print()


def l4_002RedirectionStatusCodes() -> None:
    """Explain 3xx redirection status codes."""

    print("3xx - Redirection")
    print("301 Moved Permanently -> Resource has been moved permanently.")
    print("302 Found             -> Resource is temporarily located elsewhere.")
    print()


def l4_002ClientErrorStatusCodes() -> None:
    """Explain 4xx client error status codes."""

    print("4xx - Client Errors")
    print("400 Bad Request  -> Invalid request sent by the client.")
    print("401 Unauthorized -> Authentication is required.")
    print("403 Forbidden    -> Client is authenticated but lacks permission.")
    print("404 Not Found    -> Requested resource does not exist.")
    print()


def l4_002ServerErrorStatusCodes() -> None:
    """Explain 5xx server error status codes."""

    print("5xx - Server Errors")
    print("500 Internal Server Error -> Unexpected server error.")
    print("503 Service Unavailable   -> Server is temporarily unavailable.")
    print()


# -----------------------------------------------------------------------------
# Run HTTP Status Codes Example
# -----------------------------------------------------------------------------

def run_l4_002HttpStatusCodes() -> None:
    """Run all HTTP status code examples."""

    l4_002InformationalStatusCodes()
    l4_002SuccessStatusCodes()
    l4_002RedirectionStatusCodes()
    l4_002ClientErrorStatusCodes()
    l4_002ServerErrorStatusCodes()


# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_l4_002HttpStatusCodes()