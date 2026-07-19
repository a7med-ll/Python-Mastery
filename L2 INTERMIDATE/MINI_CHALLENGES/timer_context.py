import time
import logging
from types import TracebackType
from typing import Type


# Show INFO-level logs in a simple format
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


class Timer:
    """Context manager that measures and logs code execution time."""

    def __init__(self, name: str) -> None:
        # Name used in the log message
        self.name = name

        # Stores the time when the block starts
        self.start_time: float | None = None

    def __enter__(self) -> "Timer":
        # Called automatically when entering the with block
        self.start_time = time.perf_counter()

        # Allows: with Timer(...) as timer
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        # Ensure __enter__ started the timer
        if self.start_time is None:
            raise RuntimeError("Timer was not started")

        # Called automatically when leaving the with block
        end_time = time.perf_counter()

        # Calculate elapsed time in seconds
        duration = end_time - self.start_time

        # Log the measured duration
        logging.info(
            "%s completed in %.4f seconds",
            self.name,
            duration,
        )

        # False means exceptions are not hidden
        return False


if __name__ == "__main__":
    # Measure everything inside this block
    with Timer("Example task"):
        time.sleep(2)