# L4-008 — Background Jobs & Queues

This module covers background task processing and task queues using FastAPI, Celery, and Redis.

## Topics Covered

- FastAPI BackgroundTasks
- Celery Fundamentals
- Redis Message Broker
- Producer → Broker → Worker Architecture
- FastAPI + Celery Queue
- Celery Task Retries

---

# Project Structure

```text
l4_008_background_jobs/
│
├── l4_008_fastapi_background_tasks.py
├── l4_008_celery_basic.py
├── l4_008_celery_queue.py
├── l4_008_task_retries.py
└── README.md
```

---

# 1. FastAPI BackgroundTasks

File:

```text
l4_008_fastapi_background_tasks.py
```

FastAPI `BackgroundTasks` allows non-critical work to execute after the HTTP response is handled.

Example:

```text
POST /orders
      ↓
Create Order
      ↓
Register Background Task
      ↓
Return HTTP Response
      ↓
Background Task
      ↓
Send Confirmation Email
```

The client does not need to wait for the simulated email operation to finish.

## Important

FastAPI `BackgroundTasks` does not create a separate distributed worker or Redis queue.

```text
FastAPI Process
    │
    ├── Handle HTTP Request
    │
    └── Execute Background Task
```

For durable/distributed background jobs, Celery and Redis can be used.

## Run

```bash
python3 l4_008_fastapi_background_tasks.py
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Test:

```text
POST /orders
```

Request:

```json
{
    "customer_name": "Ahmed",
    "product": "Laptop"
}
```

Expected API response:

```json
{
    "message": "Order created successfully.",
    "customer_name": "Ahmed",
    "product": "Laptop"
}
```

Watch the terminal.

First:

```text
Order created for Ahmed: Laptop
Background task started.
```

Approximately 5 seconds later:

```text
Confirmation email sent to Ahmed for Laptop.
```

---

# 2. Celery Fundamentals

File:

```text
l4_008_celery_basic.py
```

Celery allows background jobs to be executed by separate worker processes.

The architecture contains three important components:

```text
Producer
   ↓
Broker
   ↓
Worker
```

For this project:

```text
Python Producer
      ↓
Redis Broker
      ↓
Celery Worker
      ↓
Python Task
```

## Producer

The producer creates and submits the task.

Example:

```python
l4_008SendConfirmationEmail.delay(
    "Ahmed",
    "Laptop"
)
```

`.delay()` submits the Celery task instead of executing the function directly.

## Broker

Redis acts as the message broker.

```text
Producer
   ↓
Redis
```

Redis transports/holds the queued task message until a worker consumes it.

## Worker

The Celery worker listens for tasks:

```text
Redis
   ↓
Celery Worker
   ↓
Execute Task
```

---

## Check Redis

Before running Celery:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

If Redis was installed using Homebrew and is not running:

```bash
brew services start redis
```

Then check again:

```bash
redis-cli ping
```

---

## Run Celery Basic

This example requires two terminals.

### Terminal 1 — Celery Worker

Move to the project directory:

```bash
cd "/Users/nadalateef/Desktop/Python Mastery/TASKS/L4 BACKEND/07_BACKGROUND_JOBS/l4_008_background_jobs"
```

Activate the virtual environment:

```bash
source "/Users/nadalateef/Desktop/Python Mastery/.venv/bin/activate"
```

Start the Celery worker:

```bash
celery -A l4_008_celery_basic:celery_app worker --loglevel=info
```

The worker should show the registered task:

```text
[tasks]
  . l4_008_celery_basic.l4_008SendConfirmationEmail
```

Leave this terminal running.

### Terminal 2 — Producer

Move to the same directory and activate the virtual environment.

Run:

```bash
python3 l4_008_celery_basic.py
```

Expected output:

```text
Task submitted to Celery.
Task ID: <task-id>
```

Now watch Terminal 1.

Expected worker output:

```text
Task ... received

Sending confirmation email to Ahmed...

Confirmation email sent to Ahmed for Laptop.

Task ... succeeded
```

## Workflow

```text
Terminal 2
Python Producer
      │
      │ .delay()
      ↓
    Redis
      │
      ↓
Terminal 1
Celery Worker
      │
      ↓
Execute Task
```

---

# 3. FastAPI + Celery Queue

File:

```text
l4_008_celery_queue.py
```

This example connects FastAPI to Celery.

FastAPI becomes the producer.

```text
Client
   ↓
POST /orders
   ↓
FastAPI
   ↓
Create Order
   ↓
Submit Celery Task
   ↓
Redis
   ↓
Celery Worker
   ↓
Send Confirmation Email
```

FastAPI can return the HTTP response without waiting for the Celery worker to finish the background task.

## Complete Workflow

```text
                 POST /orders
                      ↓
                   FastAPI
                      │
             ┌────────┴────────┐
             ↓                 ↓
       HTTP Response       Celery Task
             ↓                 ↓
          Client             Redis
                               ↓
                         Celery Worker
                               ↓
                          Background Job
```

---

## Run FastAPI + Celery

Make sure Redis is running:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

This example requires two terminals.

### Terminal 1 — Celery Worker

Run:

```bash
celery -A l4_008_celery_queue:celery_app worker --loglevel=info
```

Expected registered task:

```text
[tasks]
  . l4_008_celery_queue.l4_008SendConfirmationEmail
```

Leave this terminal running.

### Terminal 2 — FastAPI

Run:

```bash
python3 l4_008_celery_queue.py
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Test:

```text
POST /orders
```

Request:

```json
{
    "customer_name": "Ahmed",
    "product": "Laptop"
}
```

Expected FastAPI response:

```json
{
    "message": "Order created successfully.",
    "customer_name": "Ahmed",
    "product": "Laptop",
    "task_id": "<celery-task-id>"
}
```

### View FastAPI Output

Terminal 2 should show:

```text
Order created for Ahmed: Laptop
```

and the HTTP request:

```text
POST /orders HTTP/1.1 200 OK
```

### View Celery Output

Terminal 1 should separately show:

```text
Task ... received

Sending confirmation email to Ahmed...
```

Approximately 5 seconds later:

```text
Confirmation email sent to Ahmed for Laptop.

Task ... succeeded
```

This proves FastAPI and the Celery worker are executing in separate processes.

---

# 4. Celery Task Retries

File:

```text
l4_008_task_retries.py
```

Task retries allow Celery to retry jobs that fail because of temporary problems.

Examples of potentially retryable failures:

```text
Network timeout
Temporary database connection failure
HTTP 503
External service unavailable
Rate limiting
```

Permanent errors generally should not be retried blindly.

Examples:

```text
Invalid input
Invalid email
Missing required data
Unsupported operation
```

---

# Retry Workflow

```text
Task
 ↓
Attempt
 ↓
Success?
  │
  ├── YES → Done
  │
  └── NO
       ↓
   Retryable Error?
       │
       ├── NO → Failed
       │
       └── YES
            ↓
          Wait
            ↓
          Retry
```

Our example intentionally behaves like this:

```text
Initial Execution
retry_count = 0
       ↓
      FAIL
       ↓
Wait 5 Seconds
       ↓
Retry 1
retry_count = 1
       ↓
      FAIL
       ↓
Wait 5 Seconds
       ↓
Retry 2
retry_count = 2
       ↓
     SUCCESS
```

---

## Important Retry Concepts

### `bind=True`

```python
@celery_app.task(
    bind=True,
    max_retries=3
)
```

`bind=True` gives the function access to the current Celery task through:

```python
self
```

This allows:

```python
self.request.retries
```

and:

```python
self.retry()
```

### Retry Count

```python
self.request.retries
```

returns the number of retries that have already occurred.

Example:

```text
Initial execution → 0
First retry       → 1
Second retry      → 2
Third retry       → 3
```

### Maximum Retries

```python
max_retries=3
```

means Celery can perform:

```text
Initial Execution
+
Up to 3 Retries
```

### Retry Delay

```python
countdown=5
```

means:

```text
Wait approximately 5 seconds before retrying.
```

---

# Run Task Retries

Make sure Redis is running:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

### Terminal 1 — Celery Worker

Stop any previous worker with:

```text
CTRL + C
```

Start the retry worker:

```bash
celery -A l4_008_task_retries:celery_app worker --loglevel=info
```

Expected registered task:

```text
[tasks]
  . l4_008_task_retries.l4_008SendConfirmationEmail
```

Leave Terminal 1 running.

### Terminal 2 — Producer

Run:

```bash
python3 l4_008_task_retries.py
```

Expected:

```text
Task submitted to Celery.
Task ID: <task-id>
```

Now watch Terminal 1.

### First Execution

```text
Executing email task. Retry count: 0

Task failed: Email service temporarily unavailable.

Task ... retry: Retry in 5s
```

### First Retry

Approximately 5 seconds later:

```text
Executing email task. Retry count: 1

Task failed: Email service temporarily unavailable.

Task ... retry: Retry in 5s
```

### Second Retry

Approximately another 5 seconds later:

```text
Executing email task. Retry count: 2

Confirmation email sent to Ahmed for Laptop.

Task ... succeeded
```

---

# Complete L4-008 Workflow

The concepts build on each other.

```text
1. FastAPI BackgroundTasks

Client
   ↓
FastAPI
   ↓
Critical Work
   ↓
Return Response
   ↓
FastAPI Background Task
```

Then:

```text
2. Celery Basic

Python Producer
      ↓
Redis Broker
      ↓
Celery Worker
      ↓
Background Task
```

Then:

```text
3. FastAPI + Celery Queue

Client
   ↓
FastAPI
   ↓
Celery Task
   ↓
Redis Broker
   ↓
Celery Worker
   ↓
Background Task
```

Then:

```text
4. Task Retries

Client / Producer
       ↓
      Redis
       ↓
Celery Worker
       ↓
Execute Task
       ↓
Temporary Failure
       ↓
Wait
       ↓
Retry
       ↓
Success
```

---

# FastAPI BackgroundTasks vs Celery

```text
FastAPI BackgroundTasks

FastAPI
   ├── HTTP Request
   └── Background Work
```

The background work is still associated with the FastAPI application's process.

Celery provides separation:

```text
FastAPI
   ↓
Redis
   ↓
Celery Worker
   ↓
Background Work
```

Celery is more suitable when the application requires features such as:

```text
Separate workers
Task queues
Retries
Longer-running jobs
Distributed processing
Scheduling
Worker scaling
```

---

# Running From the Project Folder

Move into the directory:

```bash
cd "/Users/nadalateef/Desktop/Python Mastery/TASKS/L4 BACKEND/07_BACKGROUND_JOBS/l4_008_background_jobs"
```

Activate the virtual environment:

```bash
source "/Users/nadalateef/Desktop/Python Mastery/.venv/bin/activate"
```

Check Redis:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

---

# Commands Summary

## FastAPI BackgroundTasks

```bash
python3 l4_008_fastapi_background_tasks.py
```

View:

```text
http://127.0.0.1:8000/docs
```

---

## Celery Basic

Terminal 1:

```bash
celery -A l4_008_celery_basic:celery_app worker --loglevel=info
```

Terminal 2:

```bash
python3 l4_008_celery_basic.py
```

Watch Terminal 1 for task execution.

---

## FastAPI + Celery Queue

Terminal 1:

```bash
celery -A l4_008_celery_queue:celery_app worker --loglevel=info
```

Terminal 2:

```bash
python3 l4_008_celery_queue.py
```

View:

```text
http://127.0.0.1:8000/docs
```

Watch:

```text
Terminal 2 → FastAPI request
Terminal 1 → Celery background task
```

---

## Task Retries

Terminal 1:

```bash
celery -A l4_008_task_retries:celery_app worker --loglevel=info
```

Terminal 2:

```bash
python3 l4_008_task_retries.py
```

Watch Terminal 1 for:

```text
retry_count = 0 → FAIL
retry_count = 1 → FAIL
retry_count = 2 → SUCCESS
```

---

# Important Rule

When switching between Celery examples, stop the old worker:

```text
CTRL + C
```

Then start the worker that belongs to the file being tested.

For example:

```bash
celery -A l4_008_task_retries:celery_app worker --loglevel=info
```

The module name and registered task must match.

---

# Final Architecture

```text
                         CLIENT
                            │
                            │ HTTP Request
                            ↓
                       ┌─────────┐
                       │ FastAPI │
                       └────┬────┘
                            │
                      Submit Task
                            │
                            ↓
                       ┌─────────┐
                       │  Redis  │
                       │ Broker  │
                       └────┬────┘
                            │
                      Consume Task
                            │
                            ↓
                    ┌───────────────┐
                    │ Celery Worker │
                    └───────┬───────┘
                            │
                       Execute Job
                            │
                    ┌───────┴────────┐
                    │                │
                 Success          Failure
                    │                │
                   Done          Retryable?
                                     │
                              ┌──────┴──────┐
                              │             │
                             Yes            No
                              │             │
                             Wait         Failed
                              │
                            Retry
```

---

# L4-008 Concepts Completed

```text
BackgroundTasks
      ↓
Basic Background Execution

Celery
      ↓
Distributed Task Processing

Redis
      ↓
Message Broker

.delay()
      ↓
Submit Asynchronous Task

Celery Worker
      ↓
Consume and Execute Task

Task ID
      ↓
Identify Asynchronous Job

bind=True
      ↓
Access Current Task

self.request.retries
      ↓
Read Retry Count

self.retry()
      ↓
Schedule Retry

max_retries
      ↓
Limit Retry Attempts

countdown
      ↓
Delay Before Retry
```

The main architecture to remember is:

```text
Producer → Broker → Worker
```

For this project:

```text
FastAPI → Redis → Celery Worker
```