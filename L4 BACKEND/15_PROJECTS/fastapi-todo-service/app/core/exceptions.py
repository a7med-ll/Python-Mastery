# -----------------------------------------------------------------------------
# Application Exceptions
# -----------------------------------------------------------------------------

from fastapi import HTTPException, status



# -----------------------------------------------------------------------------
# Authentication Exception
# -----------------------------------------------------------------------------

def authentication_exception(
        detail: str = "Authentication failed"
):
    """
    Create authentication exception.
    """

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": detail,
            "error_code": "AUTHENTICATION_FAILED"
        }
    )



# -----------------------------------------------------------------------------
# Authorization Exception
# -----------------------------------------------------------------------------

def authorization_exception(
        detail: str = "Not authorized"
):
    """
    Create authorization exception.
    """

    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "message": detail,
            "error_code": "FORBIDDEN"
        }
    )



# -----------------------------------------------------------------------------
# Not Found Exception
# -----------------------------------------------------------------------------

def not_found_exception(
        detail: str = "Resource not found"
):
    """
    Create not found exception.
    """

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "message": detail,
            "error_code": "NOT_FOUND"
        }
    )



# -----------------------------------------------------------------------------
# Bad Request Exception
# -----------------------------------------------------------------------------

def bad_request_exception(
        detail: str = "Bad request"
):
    """
    Create bad request exception.
    """

    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "message": detail,
            "error_code": "BAD_REQUEST"
        }
    )