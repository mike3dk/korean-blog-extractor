# Korean Blog Extractor

`korean-blog-extractor` is a python package to extract blog information, tags and images from most Korean blog platforms.
It supports collecting information from Naver blog and Tistory.
Also it extracts top blogger rankings by categories from [blog chart](https://www.blogchart.co.kr).

## Installation
```
pip install git+https://github.com/mike3dk/korean-blog-extractor
```

## Blog Post Usage
```
url = 'https://blog.naver.com/songsong14/222993193146'

ph = PostHandler(url)
print(ph.blog_info)

# will retrun
{
    'title': '스웨트러너 블로그',
    'url': 'https://blog.naver.com/songsong14',
    'rss_url': 'https://rss.blog.naver.com/songsong14.xml',
    'description': '"애니정보 & 리뷰 블로그"',
    'image': 'https://blogpfthumb-phinf.pstatic.net/20161005_164/songsong14_1475630067178Lb0AM_GIF/59203351_mobGif.gif?type=m2'
}

tags, images = ph.post_tags_images
print(tags, images)

# will return
[] [
    'https://postfiles.pstatic.net/MjAyMzAxMjVfMjgy/MDAxNjc0NTg1NTMxNTAz.5g4j7NnZ4pixLqCIeM3Ll6yH4Lx1_YAKnFBYERPl7F8g.mprO29rGTasLdS2630QV6xK7zIXkPIuKVKYwJ_qqdrsg.PNG.songsong14%EB%A6%AC%EB%B7%B0%EC%8B%9C%EC%9E%911.png?',
    'https://blogpfthumb-phinf.pstatic.net/20161005_164/songsong14_1475630067178Lb0AM_GIF/59203351_mobGif.gif?']
```

## BlogChart Usage
```
themes = ["게임"]
bch = BlogChartHandler(themes)
print(bch.ranks)

# will return
{
    '게임': [
        'http://blog.naver.com/sun0799dh',
        'http://blog.naver.com/soary81',
        'http://blog.naver.com/jjang986',
        'http://blog.naver.com/hypoid613',
        'http://blog.naver.com/anisaver',
        'http://blog.naver.com/2pnn',
        'http://blog.naver.com/whaudrlekd',
        'http://blog.naver.com/sweetk2ss',
        'http://blog.naver.com/meniereman',
        'http://blog.naver.com/playmyworld'
    ]
}
```