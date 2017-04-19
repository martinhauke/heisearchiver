# Heise downloader (hdl)
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
from src import helpers


cwd = os.path.dirname(__file__)
print(cwd)
archive_path = os.path.join(cwd, '../archive/')
print(archive_path)
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


def get_articles(article_links):
    for article_id, href in article_links.items():
        soup = BeautifulSoup(get_page(url+href))
        print("==== " + article_id + "====")
        with open(archive_path + article_id, 'w') as f:
            f.write(soup.prettify())
        for article in soup.find_all(attrs={"data-article-type": "meldung"}):
            print("article found")


links = extract_article_links(str(get_page(url)))
get_articles(links)
# print(links)
