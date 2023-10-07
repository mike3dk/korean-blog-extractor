import re
from urllib.parse import urlparse

import feedparser

from posui.platforms.common import fetch_soup


class BlogChartHandler:
    def __init__(self, themes):
        self._all_themes = self.__generate_themes_list()
        self._themes = themes
        self._ranks = self.__find_ranks(self._themes)

    @property
    def ranks(self):
        return self._ranks

    @property
    def all_theme_names(self):
        return self._all_themes.keys()

    def __generate_themes_list(self):
        all_themes = {}

        # URL = "https://www.blogchart.co.kr/chart/theme"
        # soup = fetch_soup(URL)
        # found = soup.select("ul.theme_list li a")
        # for row in found:
        #     theme = row.select_one("p").text
        #     url = row.get("href")
        #     all_themes[theme] = url

        URL2 = "https://www.blogchart.co.kr/chart/theme_list"

        soup = fetch_soup(URL2)
        area = soup.select_one("table.Category_list_table")
        found = area.select("a")
        for row in found:
            theme = row.text
            url = self.__convert_link(row)
            if theme in all_themes and all_themes[theme] != url:
                breakpoint()

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
        ranks = (
            [row.get("href") for row in list_area.select("table tr td a")]
            if list_area
            else []
        )

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
