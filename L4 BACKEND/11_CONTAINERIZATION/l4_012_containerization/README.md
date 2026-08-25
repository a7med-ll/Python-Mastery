# L4-012 Containerization

## Objective

Learn how to package and run a FastAPI application using Docker
containers and Docker Compose.

Topics covered:

-   Docker images
-   Docker containers
-   Dockerfile
-   Port mapping
-   Docker Compose
-   Basic container orchestration

------------------------------------------------------------------------

## Project Structure

    L4-012_containerization

    ├── fastapi_container_example
    │   ├── Dockerfile
    │   ├── main.py
    │   └── requirements.txt
    │
    ├── docker-compose.yml
    ├── knowledge_l4_012.py
    └── README.md

------------------------------------------------------------------------

## Docker Concept

Docker packages an application with its runtime environment and
dependencies.

Without Docker:

    Application
    Python Version
    Libraries
    Operating System Dependencies

With Docker:

    Docker Image

    +
    Python Runtime
    +
    Dependencies
    +
    Application Code

            |
            v

    Docker Container

------------------------------------------------------------------------

## Dockerfile

Dockerfile defines how the application image is created.

Flow:

    Dockerfile
        |
        v
    Docker Image
        |
        v
    Docker Container
        |
        v
    Running FastAPI Application

------------------------------------------------------------------------

## Build Docker Image

Navigate into:

    fastapi_container_example

Run:

``` bash
docker build -t l4-012-fastapi-app .
```

------------------------------------------------------------------------

## Run Docker Container

Run:

``` bash
docker run -p 8000:8000 l4-012-fastapi-app
```

Port mapping:

    Host Machine 8000
            |
            v
    Container 8000

Application:

    http://localhost:8000

------------------------------------------------------------------------

## Docker Compose

Docker Compose manages containers using:

    docker-compose.yml

Instead of manually running multiple Docker commands:

``` bash
docker run ...
docker run ...
```

we run:

``` bash
docker compose up
```

------------------------------------------------------------------------

## Docker Compose Workflow

    docker-compose.yml

            |
            v

    Build Image

            |
            v

    Create Network

            |
            v

    Create Container

            |
            v

    Start Application

------------------------------------------------------------------------

## Run Docker Compose

From the L4-012 containerization folder:

``` bash
docker compose up
```

Docker will:

1.  Build the image
2.  Create the network
3.  Create the container
4.  Start FastAPI

------------------------------------------------------------------------

## Verify Application

Open:

    http://localhost:8000

Expected:

``` json
{
  "application": "L4-012 Containerization API",
  "status": "running",
  "environment": "FastAPI"
}
```

------------------------------------------------------------------------

## Useful Commands

View containers:

``` bash
docker ps
```

View images:

``` bash
docker images
```

Stop container:

``` bash
docker stop <container_id>
```

Stop compose:

``` bash
docker compose down
```

Run compose in background:

``` bash
docker compose up -d
```

------------------------------------------------------------------------

## Key Learning

Completed:

-   Docker image creation
-   Docker container execution
-   FastAPI containerization
-   Port mapping
-   Docker Compose basics
-   Basic container orchestration

Next concepts build on this foundation:

-   Nginx reverse proxy
-   Kubernetes
-   CI/CD deployment
-   Cloud infrastructure
