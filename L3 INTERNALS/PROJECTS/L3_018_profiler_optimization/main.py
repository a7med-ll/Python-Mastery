from time import perf_counter

from slow_version import l3_018SlowCalculation
from optimized_version import l3_018OptimizedCalculation


#---------------------------------------------------------
# Profiler Optimization Demo
#---------------------------------------------------------

def run_l3_018ProfilerOptimization() -> None:
    """Run profiler optimization case study."""

    # Create same test data for both versions.
    data = list(range(1, 8000))


    #---------------------------------------------------------
    # Run Slow Version
    #---------------------------------------------------------

    print("SLOW VERSION")

    # Record slow version start time.
    start_time = perf_counter()

    # Run slow calculation.
    slow_result = l3_018SlowCalculation(data)

    # Calculate slow version elapsed time.
    slow_elapsed_seconds = perf_counter() - start_time

    # Print slow version result.
    print(f"Result: {slow_result}")

    # Print slow version execution time.
    print(f"Elapsed time: {slow_elapsed_seconds:.6f} seconds")


    #---------------------------------------------------------
    # Run Optimized Version
    #---------------------------------------------------------

    print("\nOPTIMIZED VERSION")

    # Record optimized version start time.
    start_time = perf_counter()

    # Run optimized calculation.
    optimized_result = l3_018OptimizedCalculation(data)

    # Calculate optimized version elapsed time.
    optimized_elapsed_seconds = perf_counter() - start_time

    # Print optimized version result.
    print(f"Result: {optimized_result}")

    # Print optimized version execution time.
    print(f"Elapsed time: {optimized_elapsed_seconds:.6f} seconds")


    #---------------------------------------------------------
    # Compare Results
    #---------------------------------------------------------

    print("\nCOMPARISON")

    # Verify both versions produce the same result.
    if slow_result == optimized_result:
        print("Results are identical")  # --> optimization did not change the output.
    else:
        print("Results are different")  # --> optimization changed the output.


#---------------------------------------------------------
# Program Entry Point
#---------------------------------------------------------

def main() -> None:
    """Program entry point."""

    run_l3_018ProfilerOptimization()


if __name__ == "__main__":
    main()