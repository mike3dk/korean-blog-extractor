from enum import Enum
from urllib.parse import urlparse

import feedparser

from posui.platforms.naver import naver_func_blog_info, naver_func_tags_images
from posui.platforms.tistory import tistory_func_blog_info, tistory_func_tags_images
from posui.platforms.egloos import egloos_func_blog_info, egloos_func_tags_images


class Platform(Enum):
    NAVER = 1
    TISTORY = 2  # daum is now using Tistory
    EGLOOS = 3


func_dict_blog_info = {
    Platform.NAVER: naver_func_blog_info,
    Platform.TISTORY: tistory_func_blog_info,
    Platform.EGLOOS: egloos_func_blog_info,
}

func_dict_tags_images = {
    Platform.NAVER: naver_func_tags_images,
    Platform.TISTORY: tistory_func_tags_images,
    Platform.EGLOOS: egloos_func_tags_images,
}


class PostHandler:
    def __init__(self, url):
        self._url = url
        self._rss_url = self.__guess_rss_url(url)

        func1 = func_dict_blog_info[self._platform]
        self._blog_info = func1(self._rss_url)

        func2 = func_dict_tags_images[self._platform]
        self._tags, self._images = func2(url)

    @property
    def blog_info(self):
        return self._blog_info

    @property
    def post_tags_images(self):
        return self._tags, self._images

    @property
    def rss_url(self):
        return self._rss_url

    def __guess_rss_url(self, url):
        parsed = urlparse(url)
        parts = parsed.path.split("/")
        path_parts = [part for part in parts if part]

        if "naver" in parsed.netloc:
            name = path_parts[0]
            self._platform = Platform.NAVER
            return f"{parsed.scheme}://rss.{parsed.netloc}/{name}.xml"

        if "tistory" in parsed.netloc:
            self._platform = Platform.TISTORY
            return f"{parsed.scheme}://{parsed.netloc}/rss"

        if "egloos" in parsed.netloc:
            name = parsed.netloc.split(".")[0]
            self._platform = Platform.EGLOOS
            return f"http://rss.egloos.com/blog/{name}"

        if "blog.me" in parsed.netloc:
            return f"http://rss.blog.naver.com/{name}.xml"

        return f"http://{parsed.netloc}/rss"
