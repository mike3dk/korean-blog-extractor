def replace_http(url):
    if "http://" in url:
        return url.replace("http://", "https://")
