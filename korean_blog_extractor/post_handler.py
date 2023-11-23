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


class Platform(str, Enum):
    NAVER = 1
    TISTORY = 2  # daum is now using Tistory
    EGLOOS = 3  # now deprecated but


func_dict_blog_info = {
    Platform.NAVER: naver_func_blog_info,
    Platform.TISTORY: tistory_func_blog_info,
}

func_dict_tags_images = {
    Platform.NAVER: naver_func_tags_images,
    Platform.TISTORY: tistory_func_tags_images,
}


class PostHandler:
    def __init__(self, url):
        self._url = url
        self.valid = False
        self.__check_valid()
        self._blog_info = {}
        self._tags = set()
        self._images = set()
        self._rss_url = None
        self._platform = None

        self.__guess_rss_url()
        self.__guess_platform()

    def extract(self):
        if not self.valid:
            print(f"Cannot connect to {self._url}")
            return

        func1 = func_dict_blog_info[self._platform]
        self._blog_info = func1(self._rss_url)

        func2 = func_dict_tags_images[self._platform]
        self._tags, self._images = func2(self._url)

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

    def __check_valid(self):
        try:
            resp = urllib.request.urlopen(self._url)
        except urllib.error.URLError:
            self.valid = False
        else:
            self.valid = True

    def __guess_rss_url(self):
        parsed = urllib.parse.urlparse(self._url)

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
            self._platform = Platform.NAVER
            self._rss_url = f"https://rss.blog.naver.com/{name}.xml"
            return

        self._rss_url = f"https://{parsed.netloc}/rss"

    def __guess_platform(self):
        if not self.valid:
            return

        if self._platform is None:
            parsed = feedparser.parse(self.rss_url)
            self._platform = Platform[parsed.feed.generator.upper()]
