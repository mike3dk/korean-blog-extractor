import logging
import urllib
from enum import Enum

import feedparser

from korean_blog_extractor.platforms.naver import (
    naver_func_blog_info,
    naver_func_tags_images,
)
from korean_blog_extractor.platforms.tistory import (
    tistory_func_blog_info,
    tistory_func_tags_images,
)
from korean_blog_extractor.platforms.wordpress import (
    wordpress_func_blog_info,
    wordpress_func_tags_images,
)
from korean_blog_extractor.utils import url_exist


class Platform(str, Enum):
    NAVER = 1
    TISTORY = 2  # daum is now using Tistory
    EGLOOS = 3  # now deprecated but
    WORDPRESS = 4


func_dict_blog_info = {
    Platform.NAVER: naver_func_blog_info,
    Platform.TISTORY: tistory_func_blog_info,
    Platform.WORDPRESS: wordpress_func_blog_info,
}

func_dict_tags_images = {
    Platform.NAVER: naver_func_tags_images,
    Platform.TISTORY: tistory_func_tags_images,
    Platform.WORDPRESS: wordpress_func_tags_images,
}


class PostHandler:
    def __init__(self, url):
        self.url = url
        self._rss_url = None
        self.valid = url_exist(self.url)
        self._blog_info = {}
        self._tags = set()
        self._images = set()

        self.__guess_rss_url()

    def __guess_rss_url(self):
        parsed = urllib.parse.urlparse(self.url)

        parts = parsed.path.split("/")
        path_parts = [part for part in parts if part]

        if "naver" in parsed.netloc:
            name = path_parts[0]
            self._platform = Platform.NAVER
            self._rss_url = f"{parsed.scheme}://rss.{parsed.netloc}/{name}.xml"
            return

        if "tistory" in parsed.netloc:
            self._platform = Platform.TISTORY
            self._rss_url = f"{parsed.scheme}://{parsed.netloc}/rss"
            return

        if "blog.me" in parsed.netloc:
            name = path_parts[0]
            self._platform = Platform.NAVER
            self._rss_url = f"https://rss.blog.naver.com/{name}.xml"
            return

        url_wp_base = f"{parsed.scheme}://{parsed.netloc}"
        url_wp_admin = f"{url_wp_base}/wp-admin"
        if url_exist(url_wp_admin):
            self._platform = Platform.WORDPRESS
            self._rss_url = f"{url_wp_base}/feed"
            return

        # if paltform is still unknown
        self._rss_url = f"https://{parsed.netloc}/rss"
        parsed = feedparser.parse(self.rss_url)

        if "generator" in parsed.feed:
            generator = parsed.feed.generator.upper()
            if 'WORDPRESS' in generator:
                self._platform = Platform.WORDPRESS
                # Update RSS URL to use /feed for WordPress  
                url_parsed = urllib.parse.urlparse(self.url)
                url_wp_base = f"{url_parsed.scheme}://{url_parsed.netloc}"
                self._rss_url = f"{url_wp_base}/feed"
                return
            elif 'TISTORY' in generator:
                self._platform = Platform.TISTORY
                return
            elif 'NAVER' in generator:
                self._platform = Platform.NAVER
                return

        self._platform = None

    def extract(self):
        if not self.valid:
            logging.warning(f"Cannot connect to {self.url}")
            return

        self.parsed_feed = feedparser.parse(self.rss_url)

        func1 = func_dict_blog_info[self._platform]
        self._blog_info = func1(self)

        func2 = func_dict_tags_images[self._platform]
        self._tags, self._images = func2(self)

    @property
    def platform(self):
        return self._platform

    @property
    def rss_url(self):
        return self._rss_url

    @property
    def blog_info(self):
        return self._blog_info

    @property
    def post_tags_images(self):
        return self._tags, self._images
