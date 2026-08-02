from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class L3_015BatchTask:
    """Represent one batch-processing task."""

    batch_id: int  # --> batch id int
    numbers: tuple[int, ...]  # --> an immutable tuple containing integers.

@dataclass(frozen=True, slots=True)
class L3_015BatchResult:
    """Represent the result of processing one batch."""

    batch_id: int
    process_id: int
    item_count: int
    total:  int | None  # --> int or none
    minimum:  int | None # --> int or none
    maximum:  int | None # --> int or none
    elapsed_seconds: float
    error:  str | None  # --> str or none


    @property
    def is_successful(self) -> bool:
        """Return whether batch processing succeeded."""

        if self.error is None:
            return True  # --> return true if error is none that means it is successful
        else:
            return False  # --> if contains error return False 


