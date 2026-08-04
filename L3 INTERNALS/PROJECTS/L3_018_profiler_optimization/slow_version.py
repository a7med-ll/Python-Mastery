from time import perf_counter

#---------------------------------------------------------
# Create The Slow Version
#---------------------------------------------------------

def l3_018SlowCalculation(data: list[int]) -> int:    # --> takes list of integer as input
    """Perform intentionally slow calculation."""

    total = 0

    for number in data:                  # --> outer loop: x
        for value in data:               # --> inner loop: x
            total += number * value      # --> total 0(x^2),  This gives us a clear optimization later

    return total                         # --> return the total value

#---------------------------------------------------------
# Run The Slow Version
#---------------------------------------------------------

def run_l3_018SlowVersion() -> None:
    """Run slow version example."""

    # Create test data.
    data = list(range(1,8000))    # --> list large enough to show the slowdown

    # Record start time.
    start_time = perf_counter()

    # Run slow calculation.
    result = l3_018SlowCalculation(data)

    # Calculate elapsed time.
    elapsed_seconds = perf_counter() - start_time

    # print result
    print(f"Result: {result}")

    # Print execution time.
    print(f"Elapsed time: {elapsed_seconds:.6f} seconds")

#---------------------------------------------------------
# Slow Version Entry Point
#---------------------------------------------------------

if __name__ == "__main__":
    run_l3_018SlowVersion()