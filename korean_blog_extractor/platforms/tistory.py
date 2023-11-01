from urllib.parse import urlparse

import feedparser

from korean_blog_extractor.platforms.common import fetch_soup


def tistory_func_blog_info(rss_url):
    parsed = feedparser.parse(rss_url)
    info = {
        "title": parsed.feed.title,
        "url": parsed.feed.link,
        "rss_url": rss_url,
        "description": parsed.feed.description,
    }
    return info


def clean_image(url):
    return url


def clean_tag(tag_text):
    return tag_text


def tistory_func_tags_images(url):
    soup = fetch_soup(url)

    main = soup.select_one("div.article-view")
    images = (
        {clean_image(img.get("src")) for img in main.select("img")} if main else set()
    )

    tag_area = soup.select_one("div.article-tag")
    tags = (
        {clean_tag(tag.text) for tag in tag_area.select("a[rel='tag']")}
        if tag_area
        else set()
    )

    return tags, images
