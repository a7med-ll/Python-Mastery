from time import perf_counter

#---------------------------------------------------------
# Create The Optimized Version
#---------------------------------------------------------

def l3_018OptimizedCalculation(data: list[int]) -> int:
    """Perform optimized calculation."""

    total = sum(data) ** 2     # --> optimized version formula

    return total  # --> return calculated result

#---------------------------------------------------------
# Run The Optimized Version
#---------------------------------------------------------

def run_l3_018OptimizedVersion() -> None:
    """Run optimized version example."""

    # Create same test data.
    data = list(range(1, 8000))

    # Measure execution time.
    start_time = perf_counter()

    # Call optimized function
    result = l3_018OptimizedCalculation(data)

    # calculate the elapsed time
    elapsed_seconds = perf_counter() - start_time

    # print result
    print(f"Result: {result}")

    # Print execution time.
    print(f"Elapsed time: {elapsed_seconds:.6f} seconds")

#---------------------------------------------------------
# Optimized Program Entry Point
#---------------------------------------------------------

if __name__ == "__main__":
    run_l3_018OptimizedVersion()




