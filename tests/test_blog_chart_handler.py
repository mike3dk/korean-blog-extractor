from unittest.mock import MagicMock
from bs4 import BeautifulSoup

from korean_blog_extractor.blog_chart_handler import BlogChartHandler
from tests.util import file_loader


def test_blog_chart_handler(mocker):
    url1 = "https://www.blogchart.co.kr/chart/theme_list"
    html1 = file_loader("tests/data/blogchart_theme_list.html")
    html2 = file_loader("tests/data/blogchart_theme_list_game.html")

    def side_effect(url, max_retries=3, retry_delay=1.0):
        if url == url1:
            return BeautifulSoup(html1, "html.parser")
        elif "theme=" in url:  # Any theme-specific URL
            return BeautifulSoup(html2, "html.parser")
        else:
            raise ValueError("Unsupported URL")

    # Mock the fetch_soup function directly
    mocker.patch(
        "korean_blog_extractor.platforms.common.fetch_soup", 
        side_effect=side_effect
    )

    theme = "게임"
    bch = BlogChartHandler([theme])
    
    # Check that the theme exists and has a valid URL
    theme_url = bch.all_themes.get(theme)
    assert theme_url is not None
    assert theme_url.startswith("https://www.blogchart.co.kr/chart/theme_list?theme=")
    assert len(theme_url) > 50  # Basic sanity check

    expected = [
        "https://blog.naver.com/rdal89",
        "https://blog.naver.com/jjang986",
        "https://blog.naver.com/ddihw",
        "https://blog.naver.com/soary81",
        "https://blog.naver.com/anisaver",
        "https://blog.naver.com/zeimer",
        "https://blog.naver.com/obama8775",
        "https://blog.naver.com/h1hc",
        "https://blog.naver.com/jina3421",
        "https://blog.naver.com/hypoid613",
    ]
    assert bch.ranks.get(theme) == expected
