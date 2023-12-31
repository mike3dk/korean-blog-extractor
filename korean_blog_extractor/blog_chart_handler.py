import re
from urllib.parse import urlparse

import feedparser

from korean_blog_extractor.platforms.common import fetch_soup
from korean_blog_extractor.utils import replace_http


class BlogChartHandler:
    def __init__(self, themes):
        self._all_themes = self.__generate_themes_list()
        self._themes = themes
        self._ranks = self.__find_ranks(self._themes)

    @property
    def ranks(self):
        return self._ranks

    @property
    def all_themes(self):
        return self._all_themes

    @property
    def all_theme_names(self):
        return self._all_themes.keys()

    def __generate_themes_list(self):
        all_themes = {}
        URL = "https://www.blogchart.co.kr/chart/theme_list"
        soup = fetch_soup(URL)
        area = soup.select_one("table.Category_list_table")
        found = area.select("a")

        for row in found:
            theme = row.text
            url = self.__convert_link(row)
            if theme in all_themes and all_themes[theme] != url:
                raise ValueError(
                    f"Something went wrong: url={url}, theme={theme}, all_themes[theme]={all_themes[theme]}"
                )

            all_themes[theme] = url

        return all_themes

    def __find_ranks(self, themes):
        ranks = {}
        for theme in themes:
            if theme not in self._all_themes.keys():
                continue

            url = self._all_themes.get(theme)
            ranks[theme] = self.__ranks(url)

        return ranks

    def __ranks(self, url):
        soup = fetch_soup(url)

        list_area = soup.select_one("div.all_category")
        ranks = [row.get("href") for row in list_area.select("a")] if list_area else []

        # make sure all urls start with https
        ranks = [replace_http(rank) for rank in ranks]

        return ranks

    def __convert_link(self, tag):
        # text = "goCate("ZGxxdWMkMkFwbl40IS4+Ympna2tjLHFvXjcgMysgMi8tPyAxQQ=="); return false;"
        # return "https://www.blogchart.co.kr/chart/theme_list?theme=ZGxxdWMkMkFwbl40IS4+Ympna2tjLHFvXjcgMysgMi8tPyAxQQ=="
        text = tag.get("onclick")
        mo = re.search(r"\"(.*)\"", text)
        if mo:
            theme_name = mo[1]
            return f"https://www.blogchart.co.kr/chart/theme_list?theme={theme_name}"

        return None
