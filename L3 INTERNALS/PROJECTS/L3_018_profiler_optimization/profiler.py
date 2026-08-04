import cProfile
import pstats

from slow_version import l3_018SlowCalculation

#---------------------------------------------------------
# Find the BottleNeck
#---------------------------------------------------------

def l3_018ProfileSlowCalculation() -> None:
    """Profile the slow calculation."""

    # Create test data.
    data = list(range(1, 8000))         # --> the same input size as your slow version

    # Run cProfile.
    profiler = cProfile.Profile()

    # Enable the profiler
    profiler.enable()

    # Run the target Function
    l3_018SlowCalculation(data)

    # Disable the Profiler
    profiler.disable()

    # Display profiling results.
    stats = pstats.Stats(profiler)

    stats.sort_stats("cumulative")      # --> cumulative means show the functions that consumed most total time
    stats.print_stats()

#---------------------------------------------------------
# Program Entry Point
#---------------------------------------------------------

if __name__ == "__main__":
    l3_018ProfileSlowCalculation()
