import yaml

from korean_blog_extractor import PostHandler, BlogChartHandler


def main():
    with open("scripts/test/expected_posts.yaml") as file:
        expected_list = yaml.safe_load(file)

    for idx, expected in enumerate(expected_list):
        try:
            print(f">>>{idx}: {expected['url']}")

            ph = PostHandler(expected["url"])

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
        except AssertionError as err:
            print(err)


if __name__ == "__main__":
    main()
