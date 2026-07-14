import requests
import time
import functools


def retry(max_retries: int = 3, delay: int = 1):

    def decorator(func):
        # functools.wraps keeps the original function's name/docstring
        # intact, instead of wrapper() overwriting them
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # try up to max_retries times before giving up
            for attempt in range(1, max_retries + 1):
                try:
                    # attempt to run the real function (e.g. fetch_page)
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")

                    # if this was the LAST allowed attempt, stop retrying
                    # and re-raise the error so the caller knows it failed
                    if attempt == max_retries:
                        raise

                    # otherwise, wait a bit before trying again
                    time.sleep(delay)

        return wrapper

    return decorator


# @retry wraps fetch_page so that if the request fails,
# it automatically retries up to 3 times, waiting 1 second between tries
@retry(max_retries=3, delay=1)
def fetch_page(page_number):
    # CHANGED URL: pointing at a made-up endpoint that doesn't exist,
    # to intentionally trigger failures and test the retry logic
    response = requests.get(f"https://jsonplaceholder.typicode.com/invalid-endpoint/{page_number}")

    # raise_for_status() turns a bad HTTP status (like 404) into
    # an actual Python exception - this is what @retry catches
    response.raise_for_status()

    # if we get here, the request succeeded - return the JSON data
    return response.json()


def scrape_pages(total_pages):

    for page in range(1, total_pages + 1):
        try:
            # try to fetch this page (this itself retries 3 times internally)
            result = fetch_page(page)
            yield result  # hand this page's data to whoever is looping over us

        except Exception as e:
            # if fetch_page failed even after all its retries,
            # don't crash the whole scrape - just note the failure
            # and continue on to the next page
            print(f"Skipping page {page}, all retries failed: {e}")
            yield {"page": page, "error": True}

