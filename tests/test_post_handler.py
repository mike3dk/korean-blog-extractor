from unittest.mock import MagicMock

import feedparser
import pytest
import yaml

from korean_blog_extractor.post_handler import Platform, PostHandler
from tests.util import file_loader

with open("scripts/test/expected_posts.yaml") as file:
    expected_list = yaml.safe_load(file)


@pytest.mark.parametrize(
    ["input_url", "expected"],
    [
        pytest.param(
            expected_list[0]["url"],
            {
                "platform": Platform.NAVER,
                "rss_url": expected_list[0]["info"]["rss_url"],
                "info": expected_list[0]["info"],
                "images": expected_list[0]["images"],
                "tags": expected_list[0]["tags"],
            },
        ),
        pytest.param(
            expected_list[1]["url"],
            {
                "platform": Platform.TISTORY,
                "rss_url": expected_list[1]["info"]["rss_url"],
                "info": expected_list[1]["info"],
                "images": expected_list[1]["images"],
                "tags": expected_list[1]["tags"],
            },
        ),
        pytest.param(
            expected_list[2]["url"],
            {
                "platform": Platform.WORDPRESS,
                "rss_url": expected_list[2]["info"]["rss_url"],
                "info": expected_list[2]["info"],
                "images": expected_list[2]["images"],
                "tags": expected_list[2]["tags"],
            },
        ),
    ],
)
def test_post_handler(mocker, input_url, expected):
    def mock():
        mock_naver = feedparser.parse("tests/data/rss_naver.xml")
        mock_tistory = feedparser.parse("tests/data/rss_tistory.xml")
        mock_wordpress = feedparser.parse("tests/data/rss_wordpress.xml")

        if expected["platform"] == Platform.NAVER:
            mocker.patch(
                "korean_blog_extractor.post_handler.feedparser.parse",
                return_value=mock_naver,
            )
        elif expected["platform"] == Platform.TISTORY:
            mocker.patch(
                "korean_blog_extractor.post_handler.feedparser.parse",
                return_value=mock_tistory,
            )
        elif expected["platform"] == Platform.WORDPRESS:
            mocker.patch(
                "korean_blog_extractor.post_handler.feedparser.parse",
                return_value=mock_wordpress,
            )

        def side_effect2(url, timeout):
            if url == "https://m.blog.naver.com/mike3dk/223983671419":
                return MagicMock(content=file_loader("tests/data/post_naver.html"))
            if url == "https://mike3dk.tistory.com/1":
                return MagicMock(content=file_loader("tests/data/post_tistory.html"))
            if (
                url
                == "https://mike7dk.wordpress.com/2025/08/25/cities-with-most-michelin-restaurants/"
            ):
                return MagicMock(content=file_loader("tests/data/post_wordpress.html"))

            raise ValueError(f"Unsupported URL: {url}")

        mocker.patch(
            "korean_blog_extractor.platforms.common.requests.get",
            side_effect=side_effect2,
        )
        mocker.patch("korean_blog_extractor.post_handler.url_exist", return_value=True)

    mock()

    ph = PostHandler(input_url)
    assert ph.platform == expected["platform"]
    assert ph.rss_url == expected["rss_url"]

    ph.extract()
    tags, images = ph.post_tags_images
    assert ph.blog_info == expected["info"]
    assert tags == set(expected["tags"])
    assert images == set(expected["images"])
