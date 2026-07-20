import http.client
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class Response:
    """Stores HTTP response information."""

    # HTTP status code (200, 404, 500 etc.)
    status: int

    # Response headers
    headers: dict[str, str]

    # Response body content
    body: str


class HttpClient:
    """Simple requests-like HTTP client."""

    def get(self, url: str) -> Response:
        # Break URL into parts
        parsed = urlparse(url)

        connection = None

        try:
            # Create HTTP or HTTPS connection
            if parsed.scheme == "https":
                connection = http.client.HTTPSConnection(
                    parsed.hostname
                )
            else:
                connection = http.client.HTTPConnection(
                    parsed.hostname
                )

            # Send GET request
            connection.request(
                "GET",
                parsed.path or "/"
            )

            # Receive server response
            response = connection.getresponse()

            # Read response body
            body = response.read().decode("utf-8")

            # Convert headers into dictionary
            headers = dict(response.getheaders())

            # Return custom response object
            return Response(
                status=response.status,
                headers=headers,
                body=body,
            )

        except Exception as error:
            # Wrap low-level errors
            raise RuntimeError(
                f"HTTP request failed: {error}"
            ) from error

        finally:
            # Always close the connection
            if connection:
                connection.close()


if __name__ == "__main__":
    client = HttpClient()

    # Make HTTP request
    response = client.get("https://example.com")

    # Display response details
    print("Status:", response.status)

    print("\nHeaders:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    print("\nBody:")
    print(response.body[:200])