from urllib.parse import urlparse

import feedparser

from korean_blog_extractor.platforms.common import fetch_soup


def naver_func_blog_info(rss_url):
    parsed = feedparser.parse(rss_url)
    info = {
        "name": parsed.feed.title,
        "url": parsed.feed.link,
        "rss_url": rss_url,
        "description": parsed.feed.description,
    }
    if "image" in parsed.feed:
        info["image"] = parsed.feed.image.href
    return info


def mobile_url(web_url):
    parsed = urlparse(web_url)
    return f"{parsed.scheme}://m.{parsed.netloc}{parsed.path}"


def clean_image(url):
    parsed = urlparse(url)
    server = (
        "postfiles.pstatic.net"
        if parsed.netloc == "mblogthumb-phinf.pstatic.net"
        else parsed.netloc
    )
    query = "type=w966" if parsed.query == "type=w80_blur" else ""
    cleaned = f"{parsed.scheme}://{server}{parsed.path}?{query}"
    return cleaned


def clean_tag(tag_text):
    return tag_text.replace("#", "")


def naver_func_tags_images(web_url):
    url = mobile_url(web_url)

    soup = fetch_soup(url)

    main = soup.select_one("div.post_ct")
    images = (
        {clean_image(img.get("src")) for img in main.select("img")} if main else set()
    )

    tag_area = soup.select_one("div.post_tag")
    tags = (
        {clean_tag(tag.text) for tag in tag_area.select("span")} if tag_area else set()
    )

    return tags, images
