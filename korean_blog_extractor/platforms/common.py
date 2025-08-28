import time

import httpx
from bs4 import BeautifulSoup


def fetch_soup(
    url: str, max_retries: int = 3, retry_delay: float = 1.0
) -> BeautifulSoup:
    """Fetch a URL and return a BeautifulSoup object with retry logic."""
    last_exception = None

    for attempt in range(max_retries):
        try:
            with httpx.Client(timeout=30) as client:  # 30 second timeout
                page = client.get(url)
                page.raise_for_status()
            soup = BeautifulSoup(page.content, "html.parser")
            return soup
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            last_exception = e
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
            continue
        except Exception as e:
            # For non-HTTP errors, don't retry
            raise RuntimeError(f"Failed to fetch or parse URL {url}: {e}")

    # If we get here, all retries failed
    raise RuntimeError(
        f"Failed to fetch URL {url} after {max_retries} attempts: {last_exception}"
    )
