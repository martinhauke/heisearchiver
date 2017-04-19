# Heise downloader (hdl)
import os
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
from src import helpers


cwd = os.path.dirname(__file__)
print(cwd)
ARCHIVE_PATH = os.path.join(cwd, '../archive/')
print(ARCHIVE_PATH)
BASE_URL = 'https://www.heise.de/'
# https://www.heise.de/newsticker/archiv/?jahr=2017;woche=3
URL = 'https://www.heise.de/newsticker'
ARCHIVE_BASE_URL = 'https://www.heise.de/newsticker/archiv/'


def get_page(url):
    try:
        response = urlopen(url)
        webContent = response.read()
    except urllib.error.HTTPError as e:
        print(e.code)
        return None

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


def get_articles(article_links, path=ARCHIVE_PATH):
    for article_id, href in article_links.items():
        print("article id: " + article_id + " link: " + href)
        if os.path.isfile(path + article_id):
            print("file exists -> skipping")
            continue
        soup = BeautifulSoup(get_page(BASE_URL+href), "html.parser")
        with open(ARCHIVE_PATH + article_id, 'wb') as f:
            f.write(soup.prettify().encode("utf-8"))
        for article in soup.find_all(attrs={"data-article-type": "meldung"}):
            print("article downloaded")


def fetch_archive():
    WEEKS = 52
    YEARS = ['2016', '2015', '2014']

    for year in YEARS:
        archive_path = ARCHIVE_PATH + str(year) + "/"
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)
        for week in range(WEEKS):
            archive_url = ARCHIVE_BASE_URL
            archive_url += "?jahr=" + str(year) + ";woche=" + str(week)

            extract_url = str(get_page(archive_url))

            if extract_url:
                links = extract_article_links(extract_url)
                print("=== retrieving articles ["
                      + year + " week " + str(week) + "] ===")
                get_articles(links, path=archive_path)

    return 0


def main():
    fetch_archive()
    # links = extract_article_links(str(get_page(URL)))
    # get_articles(links)
    # print(links)


if __name__ == "__main__":
    main()
