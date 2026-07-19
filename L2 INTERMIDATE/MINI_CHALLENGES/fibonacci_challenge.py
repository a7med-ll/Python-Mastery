from collections.abc import Iterable, Iterator


def fibonacci() -> Iterator[int]:
    """Generate Fibonacci numbers forever."""
    first = 0
    second = 1

    while True:
        # Produce current Fibonacci number
        yield first

        # Move to next Fibonacci pair
        first, second = second, first + second


def filter_even(numbers: Iterable[int]) -> Iterator[int]:
    """Yield only even numbers."""
    for number in numbers:
        # Keep only numbers divisible by 2
        if number % 2 == 0:
            yield number


def square_numbers(numbers: Iterable[int]) -> Iterator[int]:
    """Yield the square of each number."""
    for number in numbers:
        # Transform each number
        yield number ** 2


def take(numbers: Iterable[int], count: int) -> Iterator[int]:
    """Yield only the requested number of items."""
    if count < 0:
        raise ValueError("count cannot be negative")

    for index, number in enumerate(numbers):
        # Stop after reaching the limit
        if index >= count:
            return

        yield number


if __name__ == "__main__":
    fibonacci_numbers = fibonacci()

    # Build generator pipeline
    even_numbers = filter_even(fibonacci_numbers)
    squared_numbers = square_numbers(even_numbers)

    # Prevent infinite execution
    first_five = take(squared_numbers, 5)

    print(list(first_five))