from models import L3_015BatchResult, L3_015BatchTask
from processor import l3_015ProcessBatches


def l3_015PrintResult(result: L3_015BatchResult) -> None:
    """Print one batch-processing result."""

    # Print success details.
    if result.is_successful:
        print("SUCCESS")
        print(f"Batch ID: {result.batch_id}")                         # --> batch ID
        print(f"Process ID: {result.process_id}")                     # --> process ID
        print(f"Item Count: {result.item_count}")                     # --> item count
        print(f"Total : {result.total}")                         # --> total
        print(f"Minimum : {result.minimum}")                          # --> minimum
        print(f"Maximum : {result.maximum}")                          # --> maximum
        print(f"Elapsed time: {result.elapsed_seconds:.6f} seconds")  # --> elapsed seconds with six decimal places

    # Print failure details.
    else:
        print("FAILED")                                               # --> FAILED
        print(f"Batch ID: {result.batch_id}")                         # --> batch ID
        print(f"Process ID: {result.process_id}")                     # --> process ID
        print(f"Item Count: {result.item_count}")                     # --> item count
        print(f"Error: {result.error or 'Unknown error'}")            # --> error
        print(f"Elapsed time: {result.elapsed_seconds:.6f} seconds")  # --> elapsed seconds with six decimal places

    # Separate each result visually.
    print("-" * 50)


# running the batch processor
def run_l3_015BatchProcessor() -> None:
    """Run the multi-process batch processor example."""

    # Create several batch tasks.
    tasks = [
        L3_015BatchTask(
            batch_id=1,
            numbers=(10, 20, 30, 40),
        ),
        L3_015BatchTask(
            batch_id=2,
            numbers=(5, 15, 25),
        ),
        L3_015BatchTask(
            batch_id=3,
            numbers=(-10, -5, 0, 5, 10),
        ),
        L3_015BatchTask(
            batch_id=4,
            numbers=(100, 200, 300, 400, 500),
        ),
        L3_015BatchTask(
            batch_id=5,
            numbers=(),
        ),
    ]

    # Configure process count and chunk size.
    process_count = 2
    chunk_size = 1

    # Process all batches.
    results = l3_015ProcessBatches(
        tasks=tasks,
        process_count=process_count,
        chunk_size=chunk_size,
    )

    # Print every result.
    for result in results:
        l3_015PrintResult(result)

    # Calculate successful and failed counts.
    successful_count = sum(
        1 for result in results if result.is_successful
    )

    failed_count = len(results) - successful_count

    # Print the final summary.
    print("BATCH PROCESSING SUMMARY")
    print(f"Total batches: {len(results)}")
    print(f"Successful: {successful_count}")
    print(f"Failed: {failed_count}")

def main() -> None:
    """Run the program."""
    run_l3_015BatchProcessor()


if __name__ == "__main__":
    main()
