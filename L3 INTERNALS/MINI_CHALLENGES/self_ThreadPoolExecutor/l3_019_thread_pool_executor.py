import threading
import queue
import time

from typing import Any, Callable

# -----------------------------------------------------------------------------
# Future Implementation
# -----------------------------------------------------------------------------

class l3_019Future:

    def __init__(self) -> None:

        # Store task result.
        self._result: Any = None

        # Store task exception.
        self._exception: Exception | None = None

        # Track task completion status.
        self._completed = False

        # Synchronize result availability.
        self._event = threading.Event()

    # Worker completed successfully.

    def _set_result(self, result: Any) -> None:

        self._result = result  # --> Store calculated value.

        self._completed = True  # --> Mark task as completed.

        self._event.set()  # --> Release waiting thread.

    # Worker failed with exception.

    def _set_exception(self, exception: Exception) -> None:

        self._exception = exception  # --> Store error.

        self._completed = True  # --> Mark task as completed.

        self._event.set()  # --> Release waiting thread.

    def result(self) -> Any:

        # Wait until worker finishes.
        self._event.wait()

        # Check if exception exists.
        if self._exception is not None:
            raise self._exception

        # Return successful result.
        return self._result

# -----------------------------------------------------------------------------
# ThreadPool Implementation
# -----------------------------------------------------------------------------

class l3_019ThreadPoolExecutorLite:
    """implementation of thread pool executor"""

    def __init__(self, max_workers: int) -> None:

        # Validate worker count.
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than zero")

        # Initialize max worker count.
        self._max_workers = max_workers

        # Create task queue.
        self._task_queue: queue.Queue = queue.Queue()

        # Create workers list.
        self._workers: list[threading.Thread] = []

        # Track executor shutdown status.
        self._shutdown = False

        # Create worker threads.
        self._create_workers()

    # -------------------------------------------------------------------------
    # Worker Management
    # -------------------------------------------------------------------------

    def _worker_loop(self) -> None:

        while True:

            # Wait for a task from the queue.
            task = self._task_queue.get()

            # Check shutdown signal.
            if task is None:
                break

            # Get function and arguments.
            function, args, kwargs, future = task

            try:

                # Execute task.
                result = function(*args, **kwargs)

                # Store successful result.
                future._set_result(result)

            except Exception as exception:

                # Store task failure.
                future._set_exception(exception)

            finally:

                # Mark task as completed.
                self._task_queue.task_done()


    # -------------------------------------------------------------------------
    # Create Workers
    # -------------------------------------------------------------------------

    def _create_workers(self) -> None:

        for worker_id in range(self._max_workers):

            # Create threading.Thread.
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"l3_019-worker-{worker_id + 1}"
            )

            # Start worker thread.
            worker.start()

            # Store worker reference.
            self._workers.append(worker)

    # -------------------------------------------------------------------------
    # Submit Task
    # -------------------------------------------------------------------------

    def submit(self, function: Callable[..., Any], *args: Any, **kwargs: Any) -> l3_019Future:

        # Create future object.
        future = l3_019Future()

        # Package the task
        self._task_queue.put((function, args, kwargs, future))

        # Return the future.
        return future

    # -------------------------------------------------------------------------
    # Shutdown Executor
    # -------------------------------------------------------------------------

    def shutdown(self) -> None:
        # Mark executor as shutdown.
        self._shutdown = True

        # Send stop signal to workers.
        for _ in range(self._max_workers):
            self._task_queue.put(None)

        # Wait for workers to finish.
        for worker in self._workers:
            worker.join()

# -----------------------------------------------------------------------------
# Task Functions
# -----------------------------------------------------------------------------

def l3_019CalculateSquare(number: int) -> int:
    """Calculate square value."""

    return number ** 2


def l3_019SlowTask(number: int) -> int:
    """Simulate slow task."""

    time.sleep(2)

    return number


def l3_019FailingTask() -> None:
    """Generate task exception."""

    raise ValueError("Task failed intentionally")

# -----------------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------------

def run_l3_019ThreadPoolExecutorLite() -> None:

    print("=" * 70)
    print("L3-019 ThreadPoolExecutor Lite")
    print("=" * 70)


    # -------------------------------------------------------------------------
    # Test 1: Submit Multiple Tasks
    # -------------------------------------------------------------------------

    print("\n[TEST 1] Multiple Task Execution")
    print("-" * 70)

    # Create thread pool.
    executor = l3_019ThreadPoolExecutorLite(
        max_workers=3
    )

    # Submit square calculation tasks.
    future_1 = executor.submit(
        l3_019CalculateSquare,
        5
    )

    future_2 = executor.submit(
        l3_019CalculateSquare,
        10
    )

    future_3 = executor.submit(
        l3_019CalculateSquare,
        20
    )

    # Get task results.
    result_1 = future_1.result()
    result_2 = future_2.result()
    result_3 = future_3.result()

    print(f"Square Result 5  : {result_1}")
    print(f"Square Result 10 : {result_2}")
    print(f"Square Result 20 : {result_3}")


    # -------------------------------------------------------------------------
    # Test 2: Parallel Execution
    # -------------------------------------------------------------------------

    print("\n[TEST 2] Parallel Execution Timing")
    print("-" * 70)

    # Measure execution time.
    start_time = time.perf_counter()

    # Store futures.
    futures = []

    # Submit slow tasks.
    for number in range(5):

        future = executor.submit(
            l3_019SlowTask,
            number
        )

        futures.append(future)

    # Wait for all tasks.
    for future in futures:
        future.result()

    # Calculate elapsed time.
    elapsed_time = time.perf_counter() - start_time

    print(f"Completed Tasks : {len(futures)}")
    print(f"Elapsed Time    : {elapsed_time:.2f} seconds")


    # -------------------------------------------------------------------------
    # Test 3: Exception Handling
    # -------------------------------------------------------------------------

    print("\n[TEST 3] Exception Handling")
    print("-" * 70)

    # Submit failing task.
    future_error = executor.submit(
        l3_019FailingTask
    )

    try:

        # Get result.
        future_error.result()

    except ValueError as exception:

        print(f"Caught Exception: {exception}")


    # -------------------------------------------------------------------------
    # Shutdown Executor
    # -------------------------------------------------------------------------

    print("\n[SHUTDOWN] Closing Thread Pool")
    print("-" * 70)

    executor.shutdown()

    print("Thread pool shutdown completed.")

    print("=" * 70)


if __name__ == "__main__":
    run_l3_019ThreadPoolExecutorLite()