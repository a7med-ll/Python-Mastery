# L4-013 Nginx Reverse Proxy

## Objective

Understand how Nginx works as a reverse proxy and how it is used with a
FastAPI backend in a containerized environment.

## Architecture

    Client Browser
          |
          v
    Nginx Reverse Proxy :80
          |
          v
    FastAPI Application :8000

The client request reaches Nginx first. Nginx forwards the request
internally to the FastAPI backend.

## Nginx Concept

Nginx can work as:

### 1. Web Server

Nginx can serve static files directly:

-   HTML
-   CSS
-   JavaScript
-   Images
-   Static assets

This provides fast responses for static content.

### 2. Reverse Proxy Server

Nginx acts as an entry point between clients and backend services.

Flow:

    User Request
          |
          v
    Nginx
          |
          v
    Backend API
          |
          v
    Response

Benefits:

-   Hides backend infrastructure
-   Adds a security layer
-   Supports load balancing
-   Supports caching
-   Centralizes routing
-   Handles SSL termination

## Project Structure

    L4-013_nginx_reverse_proxy/

    ├── docker-compose.yml
    ├── README.md
    │
    ├── fastapi_app/
    │   ├── Dockerfile
    │   └── main.py
    │
    └── nginx/
        └── nginx.conf

## Running the Application

Navigate to the project folder:

``` bash
cd L4-013_nginx_reverse_proxy
```

Start containers:

``` bash
docker compose up
```

Run in background:

``` bash
docker compose up -d
```

## Testing

Open:

    http://localhost

Expected response:

``` json
{
  "application": "L4-013 FastAPI Backend",
  "status": "running",
  "service": "backend"
}
```

## Docker Commands

Check containers:

``` bash
docker ps
```

Stop application:

``` bash
docker compose down
```

View logs:

``` bash
docker compose logs
```

## Key Learning

Production pattern:

    Client
     |
     v
    Nginx Reverse Proxy
     |
     v
    FastAPI Backend

Nginx provides the gateway layer while FastAPI focuses on application
logic.
