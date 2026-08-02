from os import getpid
from time import perf_counter
from models import L3_015BatchResult, L3_015BatchTask
from collections.abc import Iterable
from multiprocessing import Pool

#-----------------------------------------------------
# worker that processes one batch
#-----------------------------------------------------

def l3_015ProcessBatch(task: L3_015BatchTask, ) -> L3_015BatchResult:
    """Process one batch inside a worker process."""

    start_time = perf_counter()  # --> Record the start time.
    process_id = getpid()        # --> Get the current process ID.

    try:

        if not task.numbers:  # --> Reject an empty batch.
            raise ValueError("Batch cannot be empty")

        # Calculate:
        item_count = len(task.numbers)  # --> item count so we use len
        total = sum(task.numbers)       # --> total so we use sum
        minimum = min(task.numbers)     # --> min so we use min func
        maximum = max(task.numbers)     # --> max so we use max func

        elapsed_seconds = perf_counter() - start_time   # --> calculate it by taking a second timestamp after the work finishes and subtracting the start timestamp.

        # Return a successful L3_015BatchResult

        result: L3_015BatchResult = L3_015BatchResult(

            batch_id=task.batch_id,
            process_id=process_id,
            item_count=item_count,
            total=total,
            minimum=minimum,
            maximum=maximum,
            elapsed_seconds=elapsed_seconds,
            error=None,
        )

        return result


    except Exception as error:
        # Calculate how long processing took before failing.
        elapsed_seconds = perf_counter() - start_time

        # Return a failed batch result.
        return L3_015BatchResult(
            batch_id=task.batch_id,
            process_id=process_id,
            item_count=len(task.numbers),
            total=None,
            minimum=None,
            maximum=None,
            elapsed_seconds=elapsed_seconds,
            error=f"{type(error).__name__}: {error}",
        )

#-----------------------------------------------------
# Multiprocessing Pool Function
#-----------------------------------------------------

def l3_015ProcessBatches(tasks: Iterable[L3_015BatchTask], process_count: int, chunk_size: int) -> list[L3_015BatchResult]:
    """Process multiple batches using a process pool."""

    # Validate process_count
    if process_count <= 0:
        raise ValueError("Process count must be greater than 0")

    # Validate chunk_size.
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than 0")

    # Convert tasks into a list
    tasks_collection = list(tasks)

    # If there are no tasks, return an empty list
    if not tasks_collection:
        return []

    # Create the pool using process_count
    with Pool(processes=process_count) as pool:

        results = pool.map(
            l3_015ProcessBatch,  # --> applies l3_015ProcessBatch to every task
            tasks_collection,    # --> preserves input order
            chunksize=chunk_size,  # --> accepts chunksize
        )

    # Return results after the pool closes
    return results