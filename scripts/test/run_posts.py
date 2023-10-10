import yaml
import traceback

from korean_blog_extractor import BlogChartHandler, PostHandler


def main():
    with open("scripts/test/expected_posts.yaml") as file:
        expected_list = yaml.safe_load(file)

    for idx, expected in enumerate(expected_list):
        try:
            print(f">>>{idx}: {expected['url']}")

            # figure out platform and guess rss_url
            ph = PostHandler(expected["url"])
            print(ph.platform)
            print(ph.rss_url)

            # actually visit the site and extract information
            ph.extract()
            info = ph.blog_info
            tags, images = ph.post_tags_images
            print(info)
            print(tags)
            for img in images[:3]:
                print(img)

            assert info == expected["info"]
            assert tags == expected["tags"]
            assert images == expected["images"]

            print(">>> all good!!!")
        except Exception as err:
            print(f"An exception occurred: {err}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
