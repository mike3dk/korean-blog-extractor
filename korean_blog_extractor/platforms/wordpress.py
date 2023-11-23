import feedparser
from bs4 import BeautifulSoup


def wordpress_func_blog_info(ph):
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
    else:
        info["generator"] = "WORDPRESS"

    return info


def wordpress_func_tags_images(ph):
    found = [post for post in ph.parsed_feed.entries if post.link == ph.url]

    if not found:
        return {}, {}

    post = found[0]
    tags = {clean_tag(tag.get("term")) for tag in post.tags}
    soup = BeautifulSoup(post.content[0].value, "html.parser")
    images = {img.get("src") for img in soup.select("img")}

    return tags, images


def clean_tag(tag_text):
    return tag_text.replace("#", "")
