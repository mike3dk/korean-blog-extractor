from bs4 import BeautifulSoup

from korean_blog_extractor.platforms.common import fetch_soup


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
    # Get tags from the actual HTML page using rel="tag" links
    soup = fetch_soup(ph.url)
    tags = set()

    # Method 2: Look for rel="tag" links but filter out categories
    tag_links = soup.select('a[rel="tag"]')
    for link in tag_links:
        href = link.get("href", "")
        text = link.get_text().strip()
        # Only include links that go to /tag/ URLs, not /category/ URLs
        if "/tag/" in href and text:
            tags.add(clean_tag(text))

    # Get images from RSS content
    found = [post for post in ph.parsed_feed.entries if post.link == ph.url]
    if found:
        post = found[0]
        soup_content = BeautifulSoup(post.content[0].value, "html.parser")
        images = {
            img.get("src") for img in soup_content.select("img") if img.get("src")
        }
    else:
        images = set()

    return tags, images


def clean_tag(tag_text):
    return tag_text.replace("#", "")
