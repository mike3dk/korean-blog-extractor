from unittest.mock import MagicMock


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
        "korean_blog_extractor.platforms.common.httpx.Client.get", side_effect=side_effect
    )

    theme = "게임"
    bch = BlogChartHandler([theme])
    assert bch.all_themes.get(theme) == url2

    expected = [
        "https://blog.naver.com/soary81",
        "https://blog.naver.com/2pnn",
        "https://blog.naver.com/anisaver",
        "https://blog.naver.com/ddihw",
        "https://blog.naver.com/hypoid613",
        "https://blog.naver.com/sun0799dh",
        "https://blog.naver.com/jjang986",
        "https://blog.naver.com/sweetk2ss",
        "https://blog.naver.com/cowai",
        "https://blog.naver.com/rdal89",
    ]
    assert bch.ranks.get(theme) == expected
