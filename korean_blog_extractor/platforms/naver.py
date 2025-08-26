import re
from urllib.parse import urlparse

from korean_blog_extractor.platforms.common import fetch_soup


def naver_func_blog_info(ph):
    parsed = ph.parsed_feed
    info = {
        "name": parsed.feed.title,
        "url": parsed.feed.link,
        "rss_url": ph.rss_url,
        "description": parsed.feed.description,
    }
    if "image" in parsed.feed:
        info["image"] = parsed.feed.image.href
    if "generator" in parsed.feed:
        info["generator"] = parsed.feed.generator

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


def naver_func_tags_images(ph):
    web_url = ph.url
    url = mobile_url(web_url)

    soup = fetch_soup(url)

    main = soup.select_one("div.se-main-container")
    images = (
        {clean_image(img.get("src")) for img in main.select("img")} if main else set()
    )

    # Try to get tags from HTML first (old method)
    tag_area = soup.select_one("div#blog_fe_post_tag")
    tags = set()

    if tag_area:
        li_tags = tag_area.select("li")
        if li_tags:
            tags = {clean_tag(tag.text) for tag in li_tags}

    # If no tags found from HTML, try JavaScript variables (new method)
    if not tags:
        html_content = str(soup)

        # Look for gsTagName variable
        tag_match = re.search(r"var gsTagName = \"([^\"]*)\";", html_content)
        if tag_match:
            tag_string = tag_match.group(1)
            if tag_string:
                tags = {tag.strip() for tag in tag_string.split(",")}

    return tags, images
