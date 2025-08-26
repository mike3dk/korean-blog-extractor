import urllib
from typing import Optional


def replace_http(url: str) -> str:
    """Replace http:// with https:// in URL."""
    if "http://" in url:
        return url.replace("http://", "https://")
    return url


def url_exist(url: str) -> bool:
    """Check if a URL exists and is accessible."""
    try:
        resp = urllib.request.urlopen(url, timeout=10)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return False
    else:
        return True
