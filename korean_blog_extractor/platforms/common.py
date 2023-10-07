import requests
from bs4 import BeautifulSoup


def fetch_soup(url):
    page = requests.get(url, timeout=300)  # 300 millisec timeout
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
