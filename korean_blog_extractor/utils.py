import urllib


def replace_http(url):
    if "http://" in url:
        return url.replace("http://", "https://")


def url_exist(url):
    try:
        resp = urllib.request.urlopen(url)
    except urllib.error.URLError:
        return False
    else:
        return True
