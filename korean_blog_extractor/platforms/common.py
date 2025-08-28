import httpx
from bs4 import BeautifulSoup


def fetch_soup(url: str) -> BeautifulSoup:
    """Fetch a URL and return a BeautifulSoup object."""
    try:
        with httpx.Client(timeout=30) as client:  # 30 second timeout
            page = client.get(url)
            page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
    except (httpx.RequestError, Exception) as e:
        raise RuntimeError(f"Failed to fetch or parse URL {url}: {e}")
