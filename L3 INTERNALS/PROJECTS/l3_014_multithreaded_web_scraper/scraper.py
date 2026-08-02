from threading import Lock
from models import L3_014ScrapeResult
from html.parser import HTMLParser
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from collections.abc import Iterable

from concurrent.futures import (
    FIRST_COMPLETED,
    Future,
    ThreadPoolExecutor,
    wait,
)
from concurrent.futures import Future

#-----------------------------------------------------
# thread-safe result store
#-----------------------------------------------------

class L3_014ThreadSafeResultStore:
    """Store scrapper results safely between worker threads"""

    def __init__(self) -> None:

        self._lock = Lock()
        self._scraper_results: list[L3_014ScrapeResult] = []

    def add_result(self, scraper_result: L3_014ScrapeResult) -> None:
        """Add one result safely"""

        with self._lock:
            self._scraper_results.append(scraper_result)

    def get_results(self) -> list[L3_014ScrapeResult]:
        """Return a safe copy of all stored scrapper results"""

        with self._lock:
            return self._scraper_results.copy()  # --> Return a new list rather than the original internal list.

#-----------------------------------------------------
# HTML Title Parser
#-----------------------------------------------------

class L3_014TitleParser(HTMLParser):
    """Extract the title from an HTML document."""

    def __init__(self) -> None:
        super().__init__()

        # Track whether the parser is currently inside a title tag.
        self._inside_title = False

        # Store separate pieces of title text.
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]],) -> None:
        """Handle an opening HTML tag."""

        if tag.lower() == "title":
            self._inside_title = True

    def handle_data(self, data: str) -> None:
        """Handle text found inside the HTML."""

        if self._inside_title:
            self._title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        """Handle a closing HTML tag."""

        if tag.lower() == "title":
            self._inside_title = False

    def get_title(self) -> str | None:
        """Return the cleaned page title."""

        title = "".join(self._title_parts).strip()
        return title or None

#-----------------------------------------------------
# Fetch One URL
#-----------------------------------------------------

def l3_014FetchPage(url: str, timeout: float, ) -> L3_014ScrapeResult:
    """Fetch one URL and return its scraping result."""

    # Record the starting time.
    start_time = perf_counter()

    try:

        request = Request(   # --> Create the request
            url,
            headers={"User-Agent": "L3-014-Python-Web-Scraper/1.0"},
        )

        with urlopen(request, timeout=timeout) as response:  # --> Open the URL

            status_code = response.status
            response_body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"

        # Decode the response
        html = response_body.decode(charset, errors="replace") # --> errors="replace" prevents one invalid byte from terminating the entire scrape.

        # Extract the title
        parser = L3_014TitleParser()
        parser.feed(html)
        title = parser.get_title()

        # close the parser afterward
        parser.close()

        # Calculate elapsed time
        elapsed_seconds = perf_counter() - start_time

        return L3_014ScrapeResult(
            url=url,
            status_code=status_code,
            title=title,
            elapsed_seconds=elapsed_seconds,
            error=None,
        )

    except HTTPError as error:

        # HTTPError can still contain a status code such as 404 or 500
        elapsed_seconds = perf_counter() - start_time

        return L3_014ScrapeResult(
            url=url,
            status_code=error.code,
            title=None,
            elapsed_seconds=elapsed_seconds,
            error=str(error),
        )

    except URLError as error:

        # covers connection failures, DNS problems, refused connections, and some timeout cases.
        elapsed_seconds = perf_counter() - start_time

        return L3_014ScrapeResult(
            url=url,
            status_code=None,
            title=None,
            elapsed_seconds=elapsed_seconds,
            error=str(error.reason),
        )

    except Exception as error:

        # Unexpected exception
        elapsed_seconds = perf_counter() - start_time

        return L3_014ScrapeResult(
            url=url,
            status_code=None,
            title=None,
            elapsed_seconds=elapsed_seconds,
            error=f"{type(error).__name__}: {error}",
        )

# -----------------------------------------------------
# Scrape Multiple URLs
# -----------------------------------------------------

def l3_014ScrapeUrls(
    urls: Iterable[str],
    max_workers: int,
    max_pending_tasks: int,
    timeout: float,
) -> list[L3_014ScrapeResult]:
    """Scrape multiple URLs using a bounded thread pool."""

    # Validate max_workers.
    if max_workers <= 0:
        raise ValueError(
            f"max_workers must be greater than 0, got {max_workers}"
        )

    # Validate max_pending_tasks.
    if max_pending_tasks <= 0:
        raise ValueError(
            f"max_pending_tasks must be greater than 0, "
            f"got {max_pending_tasks}"
        )

    # Ensure the pending-task limit can fully use all worker threads.
    if max_pending_tasks < max_workers:
        raise ValueError(
            "max_pending_tasks must be greater than or equal to max_workers"
        )

    # Create the thread-safe result store.
    result_store = L3_014ThreadSafeResultStore()

    # Convert URLs into an iterator.
    url_iterator = iter(urls)

    # Create the thread pool.
    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        # Create a set of pending futures.
        pending_futures: set[Future[L3_014ScrapeResult]] = set()

        # Submit up to max_pending_tasks URLs initially.
        for _ in range(max_pending_tasks):
            try:
                # Get one URL from the iterator.
                url = next(url_iterator)

            except StopIteration:
                # Stop when there are no more URLs.
                break

            # Schedule the scraping function in the thread pool.
            future = executor.submit(
                l3_014FetchPage,
                url,
                timeout,
            )

            # Store the returned Future in the pending set.
            pending_futures.add(future)

        # Continue while there are still running or waiting tasks.
        while pending_futures:

            # Wait until at least one future completes.
            completed_futures, pending_futures = wait(
                pending_futures,
                return_when=FIRST_COMPLETED,
            )

            # Process every completed task.
            for completed_future in completed_futures:

                # Get the scraping result from the completed Future.
                scrape_result = completed_future.result()

                # Store the result safely.
                result_store.add_result(scrape_result)

                # Submit one replacement task for the completed task.
                try:
                    # Get the next URL from the iterator.
                    url = next(url_iterator)

                except StopIteration:
                    # No replacement is needed when all URLs are consumed.
                    continue

                # Schedule the replacement task.
                new_future = executor.submit(
                    l3_014FetchPage,
                    url,
                    timeout,
                )

                # Add the replacement Future to the pending set.
                pending_futures.add(new_future)

    # Return a safe copy of all stored results.
    return result_store.get_results()