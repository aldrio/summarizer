from functools import lru_cache
from bs4 import BeautifulSoup
import favicon
import requests


@lru_cache(maxsize=128)
def fetch_page(url):
    """
    Fetches a beautiful soup page from a url
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    # Download page
    res = requests.get(url, timeout=5, stream=True, headers=headers)

    if res.status_code != 200:
        raise Exception(f"bad response from website {res.status_code}")
    if not res.headers["content-type"].startswith("text/html"):
        raise Exception("bad content-type")

    maxsize = 5000000  # 5mb
    content = ""
    for chunk in res.iter_content(chunk_size=2048, decode_unicode=True):
        content += chunk
        if len(content) > maxsize:
            res.close()
            raise Exception("response from website too large")

    return BeautifulSoup(content, "html.parser")


def get_page_title(page):
    """
    Gets the title of the page from the BeautifulSoup page
    """
    og_title = page.find(name="meta", property="og:title")
    if og_title is not None:
        return og_title.get("content")

    tw_title = page.find(name="meta", property="twitter:title")
    if tw_title is not None:
        return tw_title.get("content")

    h1_title = page.find(name="h1")
    if h1_title is not None:
        return h1_title.get_text()

    title = page.find("title")
    if title is not None:
        return title.get_text()

    return None


def get_image(page):
    """
    Gets an image from the BeautifulSoup page
    """
    og_image = page.find(name="meta", property="og:image")
    if og_image is not None:
        return og_image.get("content")

    tw_image = page.find(name="meta", property="twitter:image")
    if tw_image is not None:
        return tw_image.get("content")

    image = page.find(name="img")
    if image is not None:
        return image.get("src")

    return None


@lru_cache(maxsize=128)
def get_icon(url):
    icons = favicon.get(url)
    if icons:
        # sort by icons with 'favicon' in the url
        def sort(icon):
            return "favicon" in icon.url

        icons = sorted(icons, key=sort, reverse=True)
        return icons[0].url

    return None
