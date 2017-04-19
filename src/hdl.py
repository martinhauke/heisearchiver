# Heise downloader (hdl)
from urllib.request import urlopen

url = 'https://www.heise.de'


def get_start_page(url):
    response = urlopen(url)
    webContent = response.read()

    return webContent


def extract_article_links(content):
    """Tries to exctract links to articles and returns them in a list"""
    return []
