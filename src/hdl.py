# Heise downloader (hdl)
from urllib.request import urlopen
from bs4 import BeautifulSoup
from src import helpers

url = 'https://www.heise.de'


def get_page(url):
    response = urlopen(url)
    webContent = response.read()

    return webContent


def extract_article_links(content):
    """Tries to exctract links to articles and returns them in a list"""
    soup = BeautifulSoup(content, 'html.parser')
    article_links = {}

    for link in soup.find_all('a'):
        lhref = link.get('href')
        if "/newsticker/meldung/" in lhref:
            article_id = lhref[-12:-5]
            if helpers.is_valid_article_id(article_id):
                article_links[article_id] = lhref

    return article_links


# links = extract_article_links(str(get_page(url)))
# print(links)
