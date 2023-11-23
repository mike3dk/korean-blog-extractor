import traceback

import yaml

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


def main2():
    urls = {
    # url = "https://blog.naver.com/odoomi/222248896354"
    # url = "https://likewind.net/1487"
    "https://blog.naver.com/ssamssam48/222070461955",
    "https://chakeun.tistory.com/1060",
    # url = "https://blog.daum.net/yoji88/3124"
    "https://chitsol.com/entry/meta_quest3_review/"  # wordpress rss
    }

    for url in urls:
        ph = PostHandler(url)
        ph.extract()
        info = ph.blog_info
        tags, images = ph.post_tags_images
        print(vars(ph))
        print("info=")
        print(info)
        print("tags=")
        for tag in tags:
            print(tag)
        print("images=")
        for image in images:
            print(image)


if __name__ == "__main__":
    main2()
