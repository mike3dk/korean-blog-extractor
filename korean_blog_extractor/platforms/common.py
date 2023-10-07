import requests
from bs4 import BeautifulSoup


def fetch_soup(url):
    # requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "@SECLEVEL=1"
    page = requests.get(url, timeout=300)  # 300 sec timeout
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
