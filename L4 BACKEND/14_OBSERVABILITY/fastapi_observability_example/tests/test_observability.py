from fastapi.testclient import TestClient

from fastapi_observability_example.main import app


# -----------------------------------------------------------------------------
# Create Test Client
# -----------------------------------------------------------------------------

client = TestClient(app)


# -----------------------------------------------------------------------------
# Test Root Endpoint
# -----------------------------------------------------------------------------

def test_l4_015RootEndpoint():

    """
    Verify that root endpoint is running.
    """

    response = client.get("/")


    assert response.status_code == 200


    assert response.json() == {
        "application": "L4-015 Observability Basics",
        "status": "running"
    }


# -----------------------------------------------------------------------------
# Test Health Check Endpoint
# -----------------------------------------------------------------------------

def test_l4_015HealthCheck():

    """
    Verify application health endpoint.
    """

    response = client.get("/health")


    assert response.status_code == 200


    assert response.json()["status"] == "healthy"



# -----------------------------------------------------------------------------
# Test Metrics Endpoint
# -----------------------------------------------------------------------------

def test_l4_015MetricsEndpoint():

    """
    Verify metrics collection endpoint.
    """

    # Generate API request
    client.get("/")


    # Request metrics
    response = client.get("/metrics/")


    assert response.status_code == 200


    metrics = response.json()


    assert "total_requests" in metrics

    assert "successful_requests" in metrics

    assert "failed_requests" in metrics

    assert "average_duration_ms" in metrics


# -----------------------------------------------------------------------------
# Test Failed Request Metrics
# -----------------------------------------------------------------------------

def test_l4_015FailedRequestMetrics():

    """
    Verify failed requests are tracked.
    """

    response = client.get("/invalid-route")


    assert response.status_code == 404


    metrics_response = client.get("/metrics/")


    metrics = metrics_response.json()


    assert metrics["failed_requests"] >= 1