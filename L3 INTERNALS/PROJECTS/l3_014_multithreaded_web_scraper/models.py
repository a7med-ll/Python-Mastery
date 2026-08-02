from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class L3_014ScrapeResult:
    """Represent the result of scraping one URL."""

    url: str
    status_code: int | None
    title: str | None
    elapsed_seconds: float
    error: str | None

    @property
    def is_successful(self) -> bool:
        """Return whether the URL was scraped successfully."""
        return (
            self.error is None
            and self.status_code is not None
            and 200 <= self.status_code < 400
        )