import requests
from bs4 import BeautifulSoup


def fetch_soup(url: str) -> BeautifulSoup:
    """Fetch a URL and return a BeautifulSoup object."""
    try:
        page = requests.get(url, timeout=30)  # 30 second timeout
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
    except (requests.RequestException, Exception) as e:
        raise RuntimeError(f"Failed to fetch or parse URL {url}: {e}")
