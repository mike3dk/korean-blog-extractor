from unittest.mock import MagicMock

import pytest

from korean_blog_extractor.blog_chart_handler import BlogChartHandler
from tests.util import file_loader


def test_blog_chart_handler(mocker):
    url1 = "https://www.blogchart.co.kr/chart/theme_list"
    html1 = file_loader("tests/data/blogchart_theme_list.html")

    url2 = "https://www.blogchart.co.kr/chart/theme_list?theme=ZnVhbmkvaiAyP1wlMT5oZmxwWWRoJDFEYFNcXmtjMg=="
    html2 = file_loader("tests/data/blogchart_theme_list_game.html")

    def side_effect(url, timeout):
        if url == url1:
            return MagicMock(content=html1)
        if url == url2:
            return MagicMock(content=html2)

        raise ValueError("Unsupported URL")

    mocker.patch(
        "korean_blog_extractor.platforms.common.requests.get", side_effect=side_effect
    )

    theme = "게임"
    bch = BlogChartHandler([theme])
    assert bch.all_themes.get(theme) == url2

    expected = [
        "http://blog.naver.com/soary81",
        "http://blog.naver.com/2pnn",
        "http://blog.naver.com/anisaver",
        "http://blog.naver.com/ddihw",
        "http://blog.naver.com/hypoid613",
        "http://blog.naver.com/sun0799dh",
        "http://blog.naver.com/jjang986",
        "http://blog.naver.com/sweetk2ss",
        "http://blog.naver.com/cowai",
        "http://blog.naver.com/rdal89",
    ]
    assert bch.ranks.get(theme) == expected
