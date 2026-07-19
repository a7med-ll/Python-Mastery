import time
from functools import wraps
from typing import Callable, TypeVar, ParamSpec


P = ParamSpec("P")  # Function argument types
R = TypeVar("R")    # Function return type


def retry(times: int = 3, delay: float = 1.0):
    # Validate retry settings
    if times < 1:
        raise ValueError("times must be at least 1")

    if delay < 0:
        raise ValueError("delay cannot be negative")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            current_delay = delay  # Initial delay

            for attempt in range(times):
                try:
                    # Run the function
                    return func(*args, **kwargs)

                except Exception:
                    # Raise after the final attempt
                    if attempt == times - 1:
                        raise

                    # Wait before retrying
                    time.sleep(current_delay)

                    # Double the delay
                    current_delay *= 2

            # Safety fallback
            raise RuntimeError("Unexpected retry state")

        return wrapper

    return decorator


call_count = 0


@retry(times=3, delay=1)
def unstable_operation(name: str) -> str:
    global call_count
    call_count += 1

    # Fail on the first two calls
    if call_count < 3:
        raise ConnectionError("Temporary failure")

    return f"Operation completed for {name}"


if __name__ == "__main__":
    result = unstable_operation("Ahmed")
    print(result)