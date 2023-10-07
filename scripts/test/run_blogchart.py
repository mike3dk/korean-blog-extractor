import yaml

from korean_blog_extractor import BlogChartHandler


def main():
    with open("scripts/test/expected_blog_chart.yaml") as file:
        expected_list = yaml.safe_load(file)

    themes = ["국내여행", "해외여행", "방송/연예"]
    bch = BlogChartHandler(themes)

    for idx, expected in enumerate(expected_list):
        try:
            theme = expected["theme"]
            print(f">>>{idx} {theme}")
            actual = bch.ranks.get(theme)

            if not actual:
                continue

            for row in actual:
                print(row)

            print(">>> all good!!!")
        except AssertionError as err:
            print(err)


if __name__ == "__main__":
    main()
