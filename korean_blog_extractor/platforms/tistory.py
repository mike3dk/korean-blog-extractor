from typing import Dict, Set, Tuple, Any, Optional


from korean_blog_extractor.platforms.common import fetch_soup


def tistory_func_blog_info(ph: Any) -> Dict[str, str]:
    """Extract blog information from Tistory feed."""
    parsed = ph.parsed_feed
    info = {
        "name": parsed.feed.title,
        "url": parsed.feed.link,
        "rss_url": ph.rss_url,
        "description": parsed.feed.description,
    }
    if "generator" in parsed.feed:
        info["generator"] = parsed.feed.generator
    return info


def clean_image(url: Optional[str]) -> Optional[str]:
    """Clean and normalize image URL."""
    if not url:
        return url
    # Remove query parameters that might cause issues
    if "?" in url:
        url = url.split("?")[0]
    return url.strip()


def clean_tag(tag_text: Optional[str]) -> Optional[str]:
    """Clean and normalize tag text."""
    if not tag_text:
        return tag_text
    return tag_text.strip().lower()


def tistory_func_tags_images(ph: Any) -> Tuple[Set[str], Set[str]]:
    """Extract tags and images from Tistory post."""
    url = ph.url
    soup = fetch_soup(url)

    # Try multiple content area selectors
    main = (
        soup.select_one("div.area_view_content")
        or soup.select_one("div.article_content")
        or soup.select_one("div.article-view")
    )
    images = (
        {clean_image(img.get("src")) for img in main.select("img")} if main else set()
    )

    # Try multiple tag area selectors
    tag_area = soup.select_one("div.tag_content") or soup.select_one("div.article-tag")
    tags = (
        {clean_tag(tag.text) for tag in tag_area.select("a[rel='tag']")}
        if tag_area
        else set()
    )

    return tags, images
