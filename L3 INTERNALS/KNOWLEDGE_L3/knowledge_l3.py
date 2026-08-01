"""
L3 Python Internals — Structured Knowledge Examples

Run one task:
    python knowledge_l3_structured.py l3-002
    python knowledge_l3_structured.py l3-009

Run every task:
    python knowledge_l3_structured.py all

Important:
- Imports appear once.
- Every executable example is inside a function.
- There is only one program entry point.
- Multiprocessing worker functions are defined at module level.
- No demonstration code runs when child processes import this module.
"""

from __future__ import annotations
from typing import Protocol, runtime_checkable

import argparse
import asyncio
import dis
import gc
import multiprocessing
import sys
import threading
import time
import cProfile
import pstats
import tracemalloc
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable


# =============================================================================
# L3-002 — CPython Internals and Bytecode
# =============================================================================

def add_numbers(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def calculate_constant() -> int:
    """Return an expression that CPython may optimize during compilation."""
    return 10 + 20


def calculate_variables() -> int:
    """Calculate the same result using local variables."""
    x = 10
    y = 20
    return x + y


def run_l3_002() -> None:
    """Display bytecode for several simple functions."""
    print("\n=== L3-002: CPython Internals ===")

    print("\nBytecode for add_numbers():")
    dis.dis(add_numbers)

    print("\nBytecode for calculate_constant():")
    dis.dis(calculate_constant)

    print("\nBytecode for calculate_variables():")
    dis.dis(calculate_variables)


# =============================================================================
# L3-003 — Memory Management
# =============================================================================

class MemoryUser:
    """Simple class used for the circular-reference example."""


def run_l3_003() -> None:
    """Demonstrate reference counting and cyclic garbage collection."""
    print("\n=== L3-003: Memory Management ===")

    values = [1, 2, 3, 4]
    same_values = values

    print("Reference count with two variables:")
    print(sys.getrefcount(values))
    # getrefcount() temporarily adds one extra reference.

    del same_values

    print("Reference count after deleting one variable:")
    print(sys.getrefcount(values))

    first_user = MemoryUser()
    second_user = MemoryUser()

    first_user.friend = second_user
    second_user.friend = first_user

    print("Circular references created.")

    del first_user
    del second_user

    collected_objects = gc.collect()

    print(f"Garbage collector removed {collected_objects} unreachable object(s).")


# =============================================================================
# L3-004 — Descriptors
# =============================================================================

class Salary:
    """Validate and manage an employee salary attribute."""

    def __get__(
        self,
        instance: EmployeeWithDescriptors | None,
        owner: type[EmployeeWithDescriptors],
    ) -> int | Salary:
        if instance is None:
            return self

        return instance._salary

    def __set__(self, instance: EmployeeWithDescriptors, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Salary must be an integer")

        if value < 0:
            raise ValueError("Salary cannot be negative")

        instance._salary = value


class Email:
    """Validate and manage an employee email attribute."""

    def __get__(
        self,
        instance: EmployeeWithDescriptors | None,
        owner: type[EmployeeWithDescriptors],
    ) -> str | Email:
        if instance is None:
            return self

        return instance._email

    def __set__(self, instance: EmployeeWithDescriptors, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Email must be a string")

        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address")

        instance._email = value


class EmployeeWithDescriptors:
    """Employee model whose salary and email use descriptors."""

    salary = Salary()
    email = Email()

    def __init__(self, name: str, salary: int, email: str) -> None:
        self.name = name
        self.salary = salary
        self.email = email


def run_l3_004() -> None:
    """Demonstrate descriptor-controlled attributes."""
    print("\n=== L3-004: Descriptors ===")

    employee = EmployeeWithDescriptors(
        name="Ahmed",
        salary=10_000,
        email="ahmed@gmail.com",
    )

    print("Name:", employee.name)
    print("Salary:", employee.salary)
    print("Email:", employee.email)


# =============================================================================
# L3-005 — Metaclasses
# =============================================================================

MODEL_REGISTRY: dict[str, type] = {}


class ModelMeta(type):
    """Register concrete model classes when Python creates them."""

    def __new__(
        mcls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> ModelMeta:
        created_class = super().__new__(
            mcls,
            name,
            bases,
            namespace,
        )

        if name != "BaseModel":
            MODEL_REGISTRY[name] = created_class

        return created_class


class BaseModel(metaclass=ModelMeta):
    """Framework base class; intentionally excluded from the registry."""


class UserModel(BaseModel):
    """Example registered user model."""


class ProductModel(BaseModel):
    """Example registered product model."""


def run_l3_005() -> None:
    """Display classes registered by the metaclass."""
    print("\n=== L3-005: Metaclasses ===")

    for model_name, model_class in MODEL_REGISTRY.items():
        print(f"{model_name}: {model_class}")


# =============================================================================
# L3-006 — __slots__
# =============================================================================

class NormalEmployee:
    """Normal instances store attributes in an instance dictionary."""

    def __init__(self, name: str, salary: int) -> None:
        self.name = name
        self.salary = salary


class SlottedEmployee:
    """Slotted instances allow only predefined attributes."""

    __slots__ = ("name", "salary")

    def __init__(self, name: str, salary: int) -> None:
        self.name = name
        self.salary = salary


def run_l3_006() -> None:
    """Compare a normal instance with a slotted instance."""
    print("\n=== L3-006: __slots__ ===")

    normal_employee = NormalEmployee("Ahmed", 10_000)
    normal_employee.department = "Engineering"
    normal_employee.country = "UAE"

    slotted_employee = SlottedEmployee("Ahmed", 10_000)

    print("Normal employee dictionary:")
    print(normal_employee.__dict__)

    print("Slotted employee:")
    print(slotted_employee.name, slotted_employee.salary)

    print(
        "Slotted employee has __dict__:",
        hasattr(slotted_employee, "__dict__"),
    )


# =============================================================================
# L3-007 — Concurrency Models Compared
# =============================================================================

def l3_007_thread_download(file_name: str) -> None:
    """Simulate blocking I/O for the threading comparison."""
    print(f"[Threading] Starting {file_name}")
    time.sleep(1)
    print(f"[Threading] Finished {file_name}")


def run_l3_007_threading() -> None:
    """Run two blocking I/O tasks with threads."""
    threads = [
        threading.Thread(
            target=l3_007_thread_download,
            args=(file_name,),
        )
        for file_name in ("file_1.pdf", "file_2.pdf")
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("[Threading] All downloads completed")


def l3_007_process_calculation(start: int, end: int) -> None:
    """Perform a CPU-bound calculation in a child process."""
    total = sum(number * number for number in range(start, end))
    print(f"[Multiprocessing] Range {start:,}–{end:,}: {total}")


def run_l3_007_multiprocessing() -> None:
    """Run two CPU-bound tasks in separate processes."""
    processes = [
        multiprocessing.Process(
            target=l3_007_process_calculation,
            args=(0, 300_000),
        ),
        multiprocessing.Process(
            target=l3_007_process_calculation,
            args=(300_000, 600_000),
        ),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("[Multiprocessing] All calculations completed")


async def l3_007_async_download(file_name: str) -> None:
    """Simulate non-blocking I/O for the asyncio comparison."""
    print(f"[Asyncio] Starting {file_name}")
    await asyncio.sleep(1)
    print(f"[Asyncio] Finished {file_name}")


async def run_l3_007_asyncio() -> None:
    """Run three non-blocking I/O tasks concurrently."""
    await asyncio.gather(
        l3_007_async_download("file_1.pdf"),
        l3_007_async_download("file_2.pdf"),
        l3_007_async_download("file_3.pdf"),
    )

    print("[Asyncio] All downloads completed")


def run_l3_007() -> None:
    """Compare threading, multiprocessing, and asyncio."""
    print("\n=== L3-007: Concurrency Models Compared ===")

    print("\n--- Threading ---")
    run_l3_007_threading()

    print("\n--- Multiprocessing ---")
    run_l3_007_multiprocessing()

    print("\n--- Asyncio ---")
    asyncio.run(run_l3_007_asyncio())


# =============================================================================
# L3-008 — Threading
# =============================================================================

L3_008_COUNTER = 0
L3_008_COUNTER_LOCK = threading.Lock()


def l3_008_download(file_name: str) -> str:
    """Simulate a blocking file download."""
    print(f"Starting {file_name}")
    time.sleep(1)
    print(f"Finished {file_name}")
    return f"{file_name} downloaded"


def run_l3_008_basic_threads() -> None:
    """Run two downloads using manually created threads."""
    threads = [
        threading.Thread(
            target=l3_008_download,
            args=(file_name,),
        )
        for file_name in ("manual_file_1.pdf", "manual_file_2.pdf")
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Manual threads completed")


def l3_008_increment_counter() -> None:
    """Safely increment a shared counter."""
    global L3_008_COUNTER

    for _ in range(1_000):
        with L3_008_COUNTER_LOCK:
            current_value = L3_008_COUNTER
            time.sleep(0.00001)
            L3_008_COUNTER = current_value + 1


def run_l3_008_lock_example() -> None:
    """Run two threads that safely modify shared state."""
    global L3_008_COUNTER
    L3_008_COUNTER = 0

    threads = [
        threading.Thread(target=l3_008_increment_counter)
        for _ in range(2)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Expected counter:", 2_000)
    print("Actual counter:", L3_008_COUNTER)


def run_l3_008_thread_pool() -> None:
    """Run several downloads through a reusable thread pool."""
    file_names = [
        "pool_file_1.pdf",
        "pool_file_2.pdf",
        "pool_file_3.pdf",
        "pool_file_4.pdf",
    ]

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(l3_008_download, file_name)
            for file_name in file_names
        ]

        for future in as_completed(futures):
            try:
                print(future.result())
            except Exception as error:
                print("Download failed:", error)

    print("Thread pool completed")


class BankAccount:
    """Bank account that protects withdrawals with a thread lock."""

    def __init__(self, balance: float) -> None:
        self.balance = balance
        self._lock = threading.Lock()

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero")

        thread_name = threading.current_thread().name

        with self._lock:
            if self.balance < amount:
                print(
                    f"{thread_name} failed to withdraw {amount}: "
                    "insufficient balance"
                )
                return

            current_balance = self.balance
            time.sleep(0.1)
            self.balance = current_balance - amount

            print(
                f"{thread_name} withdrew {amount}. "
                f"Remaining balance: {self.balance}"
            )


def run_l3_008_bank_example() -> None:
    """Run two competing withdrawals safely."""
    account = BankAccount(1_000)

    threads = [
        threading.Thread(
            target=account.withdraw,
            args=(700,),
            name="Thread 1",
        ),
        threading.Thread(
            target=account.withdraw,
            args=(500,),
            name="Thread 2",
        ),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Final balance:", account.balance)


def run_l3_008() -> None:
    """Run the complete threading lesson."""
    print("\n=== L3-008: Threading ===")

    print("\n--- Basic Threads ---")
    run_l3_008_basic_threads()

    print("\n--- Lock Example ---")
    run_l3_008_lock_example()

    print("\n--- Thread Pool ---")
    run_l3_008_thread_pool()

    print("\n--- Thread-Safe Bank Withdrawals ---")
    run_l3_008_bank_example()


# =============================================================================
# L3-009 — Multiprocessing
# =============================================================================

def l3_009_calculate_sum(start: int, end: int) -> int:
    """Return the sum of squared numbers in a range."""
    total = 0

    for number in range(start, end):
        total += number * number

    return total


def l3_009_calculate_and_print(start: int, end: int) -> None:
    """Calculate and display a result inside a child process."""
    result = l3_009_calculate_sum(start, end)
    process_name = multiprocessing.current_process().name

    print(
        f"{process_name} completed range "
        f"{start:,} to {end:,}"
    )
    print(f"{process_name} result: {result}")


def run_l3_009_basic_processes() -> None:
    """Run two CPU calculations in separate child processes."""
    processes = [
        multiprocessing.Process(
            target=l3_009_calculate_and_print,
            args=(0, 1_000_000),
            name="Process 1",
        ),
        multiprocessing.Process(
            target=l3_009_calculate_and_print,
            args=(1_000_000, 2_000_000),
            name="Process 2",
        ),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    failed_processes = [
        process.name
        for process in processes
        if process.exitcode != 0
    ]

    if failed_processes:
        raise RuntimeError(
            "The following child processes failed: "
            + ", ".join(failed_processes)
        )

    print("All basic process calculations completed")


# -----------------------------------------------------------------------------
# Queue Example
# -----------------------------------------------------------------------------

def l3_009_calculate_for_queue(
    task_name: str,
    start: int,
    end: int,
    result_queue: multiprocessing.Queue,
) -> None:
    """
    Calculate a result and place it into a multiprocessing queue.

    Each put() adds one separate item to the shared queue.
    """
    result = l3_009_calculate_sum(start, end)

    result_queue.put(
        (task_name, result)
    )


def run_l3_009_queue_example() -> None:
    """Receive separate child-process results through one shared queue."""
    result_queue = multiprocessing.Queue()

    processes = [
        multiprocessing.Process(
            target=l3_009_calculate_for_queue,
            args=(
                "Process 1",
                0,
                1_000_000,
                result_queue,
            ),
            name="Queue Process 1",
        ),
        multiprocessing.Process(
            target=l3_009_calculate_for_queue,
            args=(
                "Process 2",
                1_000_000,
                2_000_000,
                result_queue,
            ),
            name="Queue Process 2",
        ),
    ]

    for process in processes:
        process.start()

    # Each get() removes and returns one separate queue item.
    # Completion order is not guaranteed, so each result includes a task name.
    received_results: dict[str, int] = {}

    for _ in processes:
        task_name, result = result_queue.get()
        received_results[task_name] = result

    for process in processes:
        process.join()

    for task_name, result in received_results.items():
        print(f"{task_name} returned: {result}")

    combined_result = sum(received_results.values())
    print("Combined queue result:", combined_result)

    result_queue.close()
    result_queue.join_thread()


# -----------------------------------------------------------------------------
# Process Pool Example
# -----------------------------------------------------------------------------

def l3_009_square(number: int) -> int:
    """
    Return the square of a number.

    This worker is defined at module level because multiprocessing must be able
    to pickle and import it inside child processes.
    """
    return number * number


def run_l3_009_pool_example() -> None:
    """Distribute similar CPU tasks through a reusable process pool."""
    numbers = [1, 2, 3, 4, 5]

    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(
            l3_009_square,
            numbers,
        )

    print("Pool input:", numbers)
    print("Pool results:", results)


# -----------------------------------------------------------------------------
# Shared Memory and Lock Example
# -----------------------------------------------------------------------------

def l3_009_increment_shared_counter(
    counter,
    lock,
) -> None:
    """Safely increment a value shared between child processes."""
    for _ in range(1_000):
        with lock:
            counter.value += 1


def run_l3_009_shared_value_example() -> None:
    """Demonstrate explicit shared memory and process locking."""
    shared_counter = multiprocessing.Value("i", 0)
    counter_lock = multiprocessing.Lock()

    processes = [
        multiprocessing.Process(
            target=l3_009_increment_shared_counter,
            args=(
                shared_counter,
                counter_lock,
            ),
            name=f"Counter Process {index}",
        )
        for index in range(1, 3)
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("Expected shared counter:", 2_000)
    print("Actual shared counter:", shared_counter.value)

# -----------------------------------------------------------------------------
# Shared Array Example
# -----------------------------------------------------------------------------

def l3_009_update_shared_values(values) -> None:
    """
    Update every value inside a shared multiprocessing array.

    The array exists in shared memory, so changes made by this child
    process are visible to the parent process.
    """

    process_name = multiprocessing.current_process().name

    print(
        f"{process_name} received values:",
        list(values),
    )

    for index in range(len(values)):
        # Multiply each shared value by 2.
        values[index] *= 2

    print(
        f"{process_name} updated values:",
        list(values),
    )


def run_l3_009_shared_array_example() -> None:
    """
    Create a shared integer array and update it in a child process.
    """

    # "i" means signed integer.
    #
    # Unlike a normal Python list, multiprocessing.Array creates
    # values that can be accessed by multiple processes.
    shared_values = multiprocessing.Array(
        "i",
        [1, 2, 3, 4],
    )

    print(
        "Parent process values before update:",
        list(shared_values),
    )

    process = multiprocessing.Process(
        target=l3_009_update_shared_values,
        args=(shared_values,),
        name="Shared Array Process",
    )

    # Start the child process.
    process.start()

    # Wait until the child process finishes updating the array.
    process.join()

    if process.exitcode != 0:
        raise RuntimeError(
            f"{process.name} failed with "
            f"exit code {process.exitcode}"
        )

    # The parent can see the updated values because the array
    # was created in shared memory.
    print(
        "Parent process values after update:",
        list(shared_values),
    )

# -----------------------------------------------------------------------------
# Multiprocessing Manager Example
# -----------------------------------------------------------------------------

def l3_009_add_user(
    users,
    user_id: int,
    name: str,
) -> None:
    """
    Add one user to a dictionary managed by multiprocessing.Manager.

    The managed dictionary is not a normal local dictionary.
    It is a proxy object that allows multiple processes to update
    the same shared dictionary.
    """

    process_name = multiprocessing.current_process().name

    users[user_id] = name

    print(
        f"{process_name} added user "
        f"{user_id}: {name}"
    )


def run_l3_009_manager_example() -> None:
    """
    Create a shared dictionary using multiprocessing.Manager
    and update it from two separate child processes.
    """

    # Manager starts a separate server process that manages
    # shared Python objects such as dictionaries and lists.
    with multiprocessing.Manager() as manager:

        # manager.dict() returns a proxy dictionary.
        #
        # Both child processes can update this same managed object,
        # and the parent process can see the final combined result.
        shared_users = manager.dict()

        process_1 = multiprocessing.Process(
            target=l3_009_add_user,
            args=(
                shared_users,
                1,
                "Ahmed",
            ),
            name="User Process 1",
        )

        process_2 = multiprocessing.Process(
            target=l3_009_add_user,
            args=(
                shared_users,
                2,
                "Lokesh",
            ),
            name="User Process 2",
        )

        process_1.start()
        process_2.start()

        process_1.join()
        process_2.join()

        failed_processes = [
            process.name
            for process in (process_1, process_2)
            if process.exitcode != 0
        ]

        if failed_processes:
            raise RuntimeError(
                "The following processes failed: "
                + ", ".join(failed_processes)
            )

        # Convert the manager proxy dictionary into a normal
        # Python dictionary before printing.
        final_users = dict(shared_users)

        print("Final shared users:", final_users)

# -----------------------------------------------------------------------------
# Pickling-Friendly Worker Example
# -----------------------------------------------------------------------------

def l3_009_power(task: tuple[int, int]) -> int:
    """
    Accept serializable data and return a serializable result.

    Multiprocessing sends arguments and results between processes using
    pickling. Top-level functions and ordinary values are safe choices.
    """
    base, exponent = task
    return base**exponent


def run_l3_009_pickling_example() -> None:
    """Show a pool using pickling-friendly function arguments."""
    tasks = [
        (2, 3),
        (3, 2),
        (5, 2),
    ]

    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(
            l3_009_power,
            tasks,
        )

    print("Pickling-friendly tasks:", tasks)
    print("Pickling-friendly results:", results)


def run_l3_009() -> None:
    """Run the complete L3-009 multiprocessing lesson."""

    print("\n=== L3-009: Multiprocessing ===")

    print("\n--- Basic Processes ---")
    run_l3_009_basic_processes()

    print("\n--- Queue Communication ---")
    run_l3_009_queue_example()

    print("\n--- Process Pool ---")
    run_l3_009_pool_example()

    print("\n--- Shared Value and Lock ---")
    run_l3_009_shared_value_example()

    print("\n--- Shared Array ---")
    run_l3_009_shared_array_example()

    print("\n--- Manager Shared Dictionary ---")
    run_l3_009_manager_example()

    print("\n--- Pickling-Friendly Tasks ---")
    run_l3_009_pickling_example()

# =============================================================================
# L3-010 — AsyncIO Deep Dive
# =============================================================================

# -----------------------------------------------------------------------------
# Basic Coroutine
# -----------------------------------------------------------------------------

async def l3_010_fetch_data(
    source_name: str,
    delay: float,
) -> str:
    """
    Simulate a non-blocking I/O operation.

    While this coroutine is waiting, the event loop can execute
    other ready coroutines.
    """

    print(f"Starting request: {source_name}")

    await asyncio.sleep(delay)

    print(f"Finished request: {source_name}")

    return f"Data received from {source_name}"


async def run_l3_010_basic_coroutine_example() -> None:
    """Await one coroutine and print its result."""

    result = await l3_010_fetch_data(
        source_name="Service A",
        delay=1,
    )

    print("Result:", result)

# -----------------------------------------------------------------------------
# asyncio.gather()
# -----------------------------------------------------------------------------

async def fetch_service(service_name: str, delay: float ) -> str:

    print(f"Starting Service: {service_name}")

    await asyncio.sleep(delay)

    print(f"Finished Service: {service_name}")

    return f"Data Received from {service_name}"

async def run_l3_010_gather() -> None:

    results = await asyncio.gather(

    fetch_service("User Service", 2),
    fetch_service("Payment Service", 1),
    fetch_service("Notification Service", 1.5),

    )

    for result in results:
         print(result)

# -----------------------------------------------------------------------------
# asyncio.create_task()
# -----------------------------------------------------------------------------

async def l3_010_process_file(file_name: str, delay: float ) -> str:

    print(f"Starting File: {file_name}")

    await asyncio.sleep(delay)

    print(f"Finished File: {file_name}")

    return f"{file_name} processed successfully"

async def run_l3_010_create_task() -> None:

    task_1 = asyncio.create_task(

        l3_010_process_file("annual_report.pdf", 2),
        name = "L3-010 Task 1",
    )

    task_2 = asyncio.create_task(

        l3_010_process_file("employee_data.csv", 1),
        name = "L3-010 Task 2",
    )

    print("File-processing tasks scheduled")

    print("Task 1 name:", task_1.get_name())
    print("Task 2 name:", task_2.get_name())

    result_1 = await task_1
    result_2 = await task_2

    print(result_1)
    print(result_2)

# -----------------------------------------------------------------------------
# TaskGroup
# -----------------------------------------------------------------------------

async def run_l3_010_task_group_example() -> None:
    """Run related tasks using structured concurrency."""

    async with asyncio.TaskGroup() as task_group:
        task_1 = task_group.create_task(
            l3_010_fetch_data(
                "TaskGroup Service 1",
                1,
            ),
            name="TaskGroup Task 1",
        )

        task_2 = task_group.create_task(
            l3_010_fetch_data(
                "TaskGroup Service 2",
                1.5,
            ),
            name="TaskGroup Task 2",
        )

    # Leaving the TaskGroup block means all tasks completed.
    print("TaskGroup results:")
    print(task_1.result())
    print(task_2.result())

# -----------------------------------------------------------------------------
# Async Context Manager Challenge
# -----------------------------------------------------------------------------


class L3_010AsyncDatabaseConnection:
    """Simulate an asynchronous database connection."""

    async def __aenter__(
        self,
    ) -> "L3_010AsyncDatabaseConnection":
        """
        Open the asynchronous resource.

        The value returned here is assigned to the variable
        after 'as' in the async-with statement.
        """

        print("Opening database connection...")

        await asyncio.sleep(0.5)

        print("Database connection opened")

        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        exc_traceback,
    ) -> None:
        """
        Close the asynchronous resource.

        This method runs when execution leaves the async-with block,
        including when an exception occurs inside the block.
        """

        print("Closing database connection...")

        await asyncio.sleep(0.5)

        print("Database connection closed")

    async def fetch_users(self) -> list[str]:
        """Fetch simulated user records asynchronously."""

        print("Fetching users from database...")

        await asyncio.sleep(1)

        return [
            "Ahmed",
            "Lokesh",
            "Sara",
        ]


async def run_l3_010_context_manager_challenge() -> None:
    """Use the async database connection safely."""

    async with L3_010AsyncDatabaseConnection() as connection:
        users = await connection.fetch_users()

        for user in users:
            print(user)

# -----------------------------------------------------------------------------
# Async Iterator
# -----------------------------------------------------------------------------

class l3_010AsyncTransactionStream:

    def __init__(self, start_id: int, end_id: int, delay: float) -> None:
        self.current_id = start_id
        self.end_id = end_id
        self.delay = delay

    def __aiter__(self) -> l3_010AsyncTransactionStream:
        return self

    async def __anext__(self) -> int:

        if self.current_id >= self.end_id:
            raise StopAsyncIteration

        await asyncio.sleep(self.delay)

        value_id = self.current_id
        self.current_id += 1

        return value_id

async def run_l3_010_async_iterator_challenge() -> None:

    async for id in l3_010AsyncTransactionStream(start_id=1, end_id=5, delay=0.5):
        print("Received ID's:", id)

# -----------------------------------------------------------------------------
# Blocking Call Moved to a Thread
# -----------------------------------------------------------------------------

def l3_010_blocking_file_operation() -> str:
    """
    Simulate a legacy blocking operation.

    Calling this directly inside a coroutine would block
    the event loop.
    """

    time.sleep(2)

    return "Blocking operation completed"


async def run_l3_010_to_thread_example() -> None:
    """Run blocking I/O without blocking the event loop."""

    result = await asyncio.to_thread(
        l3_010_blocking_file_operation
    )

    print(result)


# -----------------------------------------------------------------------------
# Main L3-010 Async Runner
# -----------------------------------------------------------------------------

async def run_l3_010_async_examples() -> None:
    """Run every asynchronous L3-010 example."""

    print("\n--- Basic Coroutine ---")
    await run_l3_010_basic_coroutine_example()

    print("\n--- Basic asyncio.gather() ---")
    await run_l3_010_gather()

    print("\n--- Basic asyncio.create_task() ---")
    await run_l3_010_create_task()

    print("\n--- Basic TaskGroup Example ---")
    await run_l3_010_task_group_example()

    print("\n--- Basic Context Manager Challenge ---")
    await run_l3_010_context_manager_challenge()

    print("\n--- Basic async Iterator Challenge ---")
    await run_l3_010_async_iterator_challenge()

    print("\n--- Blocking Call Moved to a Thread ---")
    await run_l3_010_to_thread_example()

def run_l3_010() -> None:
    """Create the event loop and run the L3-010 lesson."""

    print("\n=== L3-010: AsyncIO Deep Dive ===")

    asyncio.run(
        run_l3_010_async_examples()
    )

# =============================================================================
# L3-011 — Profiling
# =============================================================================


def l3_011_fast_calculation() -> int:
    """Perform a relatively small calculation."""

    total = 0

    for number in range(100_000):
        total += number

    return total


def l3_011_slow_calculation() -> int:
    """Perform a larger CPU-bound calculation."""

    total = 0

    for number in range(2_000_000):
        total += number * number

    return total


def l3_011_run_cpu_workload() -> None:
    """Run functions with different CPU costs."""

    fast_result = l3_011_fast_calculation()
    slow_result = l3_011_slow_calculation()

    print("Fast result:", fast_result)
    print("Slow result:", slow_result)


def run_l3_011_cprofile_example() -> None:
    """Profile CPU usage with cProfile."""

    profiler = cProfile.Profile()

    profiler.enable()

    l3_011_run_cpu_workload()

    profiler.disable()

    statistics = pstats.Stats(profiler)

    statistics.sort_stats(
        pstats.SortKey.CUMULATIVE
    )

    statistics.print_stats(10)


def l3_011_allocate_memory() -> list[str]:
    """Allocate Python-managed memory."""

    return [
        f"Record {number}"
        for number in range(100_000)
    ]


def l3_011_bytes_to_megabytes(
    number_of_bytes: int,
) -> float:
    """Convert bytes into a readable memory unit."""

    return number_of_bytes / (1024 * 1024)


def run_l3_011_traced_memory_example() -> None:
    """Measure current and peak traced memory."""

    tracemalloc.start()

    records = l3_011_allocate_memory()

    current_memory, peak_memory = (
        tracemalloc.get_traced_memory()
    )

    print(
        "Current traced memory:",
        f"{l3_011_bytes_to_megabytes(current_memory):.2f}",
        "MB",
    )

    print(
        "Peak traced memory:",
        f"{l3_011_bytes_to_megabytes(peak_memory):.2f}",
        "MB",
    )

    tracemalloc.stop()

    print("Records created:", len(records))


def run_l3_011_memory_snapshot_example() -> None:
    """Display the largest traced memory allocations."""

    tracemalloc.start()

    records = l3_011_allocate_memory()

    snapshot = tracemalloc.take_snapshot()

    statistics = snapshot.statistics(
        "lineno"
    )

    print("Top memory allocations:")

    for statistic in statistics[:5]:
        print(statistic)

    tracemalloc.stop()

    print("Records created:", len(records))


def run_l3_011() -> None:
    """Run the complete L3-011 profiling lesson."""

    print("\n=== L3-011: Profiling ===")

    print("\n--- cProfile ---")
    run_l3_011_cprofile_example()

    print("\n--- Traced Memory ---")
    run_l3_011_traced_memory_example()

    print("\n--- Memory Snapshot ---")
    run_l3_011_memory_snapshot_example()

# =============================================================================
# L3-012 — Advanced Typing and Structural Typing
# =============================================================================


@runtime_checkable
class L3_012NotificationSender(Protocol):
    """
    Define the behavior required from a notification sender.

    A class does not need to inherit from this protocol.
    It only needs a compatible send() method.
    """

    def send(
        self,
        recipient: str,
        message: str,
    ) -> bool:
        ...


class L3_012EmailSender:
    """Send a simulated email notification."""

    def send(
        self,
        recipient: str,
        message: str,
    ) -> bool:
        print(
            f"Email sent to {recipient}: {message}"
        )

        return True


class L3_012SMSSender:
    """Send a simulated SMS notification."""

    def send(
        self,
        recipient: str,
        message: str,
    ) -> bool:
        print(
            f"SMS sent to {recipient}: {message}"
        )

        return True


class L3_012InvalidSender:
    """Does not satisfy the notification sender protocol."""

    def deliver(
        self,
        message: str,
    ) -> None:
        print(message)


def l3_012_send_notification(
    sender: L3_012NotificationSender,
    recipient: str,
    message: str,
) -> bool:
    """
    Accept any object that structurally satisfies
    L3_012NotificationSender.
    """

    return sender.send(
        recipient,
        message,
    )


def run_l3_012_protocol_example() -> None:
    """Demonstrate structural typing using Protocol."""

    email_sender = L3_012EmailSender()
    sms_sender = L3_012SMSSender()
    invalid_sender = L3_012InvalidSender()

    l3_012_send_notification(
        sender=email_sender,
        recipient="ahmed@example.com",
        message="Your report is ready",
    )

    l3_012_send_notification(
        sender=sms_sender,
        recipient="+971500000000",
        message="Your OTP is 1234",
    )

    print(
        "Email sender satisfies protocol:",
        isinstance(
            email_sender,
            L3_012NotificationSender,
        ),
    )

    print(
        "SMS sender satisfies protocol:",
        isinstance(
            sms_sender,
            L3_012NotificationSender,
        ),
    )

    print(
        "Invalid sender satisfies protocol:",
        isinstance(
            invalid_sender,
            L3_012NotificationSender,
        ),
    )


def run_l3_012() -> None:
    """Run the complete L3-012 typing lesson."""

    print(
        "\n=== L3-012: Advanced Typing "
        "and Structural Typing ==="
    )

    print("\n--- Protocol Example ---")

    run_l3_012_protocol_example()

# =============================================================================
# Program Entry Point
# =============================================================================

TASK_RUNNERS: dict[str, Callable[[], None]] = {
    "l3-002": run_l3_002,
    "l3-003": run_l3_003,
    "l3-004": run_l3_004,
    "l3-005": run_l3_005,
    "l3-006": run_l3_006,
    "l3-007": run_l3_007,
    "l3-008": run_l3_008,
    "l3-009": run_l3_009,
    "l3-010": run_l3_010,
    "l3-011": run_l3_011,
    "l3-012": run_l3_012,
}


def parse_arguments() -> argparse.Namespace:
    """Read the task name from the command line."""
    parser = argparse.ArgumentParser(
        description="Run one structured L3 Python Internals lesson.",
    )

    parser.add_argument(
        "task",
        choices=[*TASK_RUNNERS, "all"],
        help="Task to run, for example: l3-009",
    )

    return parser.parse_args()


def main() -> None:
    """Run one selected task or every task."""
    arguments = parse_arguments()

    if arguments.task == "all":
        for runner in TASK_RUNNERS.values():
            runner()
        return

    TASK_RUNNERS[arguments.task]()


if __name__ == "__main__":
    # Required for safe multiprocessing on macOS and Windows.
    multiprocessing.freeze_support()
    main()