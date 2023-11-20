from unittest.mock import MagicMock

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
            "https://blog.naver.com/ssamssam48/222070461955",
            {
                "platform": Platform.NAVER,
                "rss_url": expected_list[0]["info"]["rss_url"],
                "info": expected_list[0]["info"],
                "images": expected_list[0]["images"],
                "tags": expected_list[0]["tags"],
            },
        ),
        pytest.param(
            "https://chakeun.tistory.com/1060",
            {
                "platform": Platform.TISTORY,
                "rss_url": expected_list[1]["info"]["rss_url"],
                "info": expected_list[1]["info"],
                "images": expected_list[1]["images"],
                "tags": expected_list[1]["tags"],
            },
        ),
    ],
)
def test_post_handler(mocker, input_url, expected):
    info_naver = expected_list[0]["info"]
    mock_naver = MagicMock(
        feed=MagicMock(
            title=info_naver["name"],
            link=info_naver["url"],
            rss_url=info_naver["rss_url"],
            description=info_naver["description"],
            image=MagicMock(href=info_naver["image"]),
        )
    )
    info_tistory = expected_list[1]["info"]
    mock_tistory = MagicMock(
        feed=MagicMock(
            title=info_tistory["name"],
            link=info_tistory["url"],
            description=info_tistory["description"],
        )
    )

    if expected["platform"] == Platform.NAVER:
        mocker.patch(
            "korean_blog_extractor.platforms.naver.feedparser.parse",
            return_value=mock_naver,
        )
    elif expected["platform"] == Platform.TISTORY:
        mocker.patch(
            "korean_blog_extractor.platforms.tistory.feedparser.parse",
            return_value=mock_tistory,
        )

    def side_effect2(url, timeout):
        if url == "https://m.blog.naver.com/ssamssam48/222070461955":
            return MagicMock(content=file_loader("tests/data/post_naver.html"))
        if url == "https://chakeun.tistory.com/1060":
            return MagicMock(content=file_loader("tests/data/post_tistory.html"))

        raise ValueError("Unsupported URL")

    mocker.patch(
        "korean_blog_extractor.platforms.common.requests.get", side_effect=side_effect2
    )

    ph = PostHandler(input_url)
    assert ph.platform == expected["platform"]
    assert ph.rss_url == expected["rss_url"]

    ph.extract()
    tags, images = ph.post_tags_images
    assert ph.blog_info == expected["info"]
    assert tags == set(expected["tags"])
    assert images == set(expected["images"])
