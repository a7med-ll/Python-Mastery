from models import L3_014ScrapeResult
from scraper import l3_014ScrapeUrls


def l3_014PrintResult(result: L3_014ScrapeResult) -> None:
    """Print one scraping result."""

    # Print success details.
    if result.is_successful:
        print("SUCCESS")
        print(f"URL: {result.url}")
        print(f"Status code: {result.status_code}")
        print(f"Title: {result.title or 'No title'}")
        print(f"Elapsed time: {result.elapsed_seconds:.3f} seconds")

    # Print failure details.
    else:
        status_code = (
            result.status_code
            if result.status_code is not None
            else "N/A"
        )

        print("FAILED")
        print(f"URL: {result.url}")
        print(f"Status code: {status_code}")
        print(f"Error: {result.error or 'Unknown error'}")
        print(f"Elapsed time: {result.elapsed_seconds:.3f} seconds")

    # Separate each result visually.
    print("-" * 50)


def run_l3_014WebScraper() -> None:
    """Run the multi-threaded web scraper example."""

    # Create a list of test URLs.
    urls = [
        "https://example.com",
        "https://www.python.org",
        "https://docs.python.org/3/",
        "https://httpbin.org/status/404",
        "https://invalid-domain-example.test",
    ]

    #  Configure worker count, pending-task limit, and timeout.
    max_workers = 3
    max_pending_tasks = 5
    timeout = 5.0

    #  Call l3_014ScrapeUrls().
    results = l3_014ScrapeUrls(
        urls=urls,
        max_workers=max_workers,
        max_pending_tasks=max_pending_tasks,
        timeout=timeout,
    )

    # Print every result
    for result in results:
        l3_014PrintResult(result)

    #  Print a final summary.
    successful_count = sum(
        1 for result in results if result.is_successful
    )

    failed_count = len(results) - successful_count

    print("SCRAPING SUMMARY")
    print(f"Total URLs: {len(results)}")
    print(f"Successful: {successful_count}")
    print(f"Failed: {failed_count}")


def main() -> None:
    """Run the program."""
    run_l3_014WebScraper()


if __name__ == "__main__":
    main()