# Heise downloader
import os
import sys
import getopt
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
from io import StringIO
from heisearchiver import helpers
from heisearchiver.config import ARCHIVE_PATH, BASE_URL, ARCHIVE_BASE_URL, cwd


def print_paths():
    """Prints the current path settings"""
    print("Current directory: " + cwd)
    print("Path to local Archive: " + ARCHIVE_PATH)
    print("Base URL: " + BASE_URL)
    # print("URL for link extraction: " + URL)
    print("URL to the archive: " + ARCHIVE_BASE_URL)


def get_page(url):
    """Gets the content of the specified URL"""
    try:
        response = urlopen(url)
        webContent = response.read()
    except urllib.error.HTTPError as e:
        print(e.code)
        return None
    except ValueError as e:
        print("Invalid URL")
        return None

    return webContent


def extract_article_links(content):
    """Tries to exctract links to articles and returns them in a list"""
    article_links = {}
    if content:
        soup = BeautifulSoup(content, 'html.parser')

        for link in soup.find_all('a'):
            lhref = link.get('href')
            if "/meldung/" in lhref:
                article_id_starts_at = lhref.rfind('-') + 1
                article_id_ends_at = lhref.rfind('.')
                article_id = lhref[article_id_starts_at:article_id_ends_at]
                if helpers.is_valid_article_id(article_id):
                    article_links[article_id] = lhref

    return article_links


def write_article_to_file(content, outfile=StringIO()):
    """Writes content to a file"""
    outfile.write(content)


def get_articles(article_links, local_archive_path=ARCHIVE_PATH):
    """Downloads and saves articles in an archive"""
    for article_id, href in article_links.items():
        print("article id: " + article_id + " link: " + href)
        if os.path.isfile(local_archive_path + article_id):
            print("*** file already exists -> skipping")
            continue
        content = get_page(BASE_URL+href)
        if not content:
            print("[ERROR]: Page not found")
            continue
        soup = BeautifulSoup(content, "html.parser")
        with open(local_archive_path + article_id, 'wb') as f:
            write_article_to_file(soup.prettify().encode("utf-8"), f)
            print("article saved to ..." + f.name[-15:])
        # for article in soup.find_all(attrs={"data-article-type": "meldung"}):
        #    print("article downloaded")


def fetch_archive(years):
    WEEKS = 52

    for year in years:
        archive_path = ARCHIVE_PATH + str(year) + "/"
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)
        for week in range(1, WEEKS + 1):
            archive_url = ARCHIVE_BASE_URL
            archive_url += "?jahr=" + str(year) + ";woche=" + str(week)

            extract_url = str(get_page(archive_url))

            if extract_url:
                links = extract_article_links(extract_url)
                print("=== retrieving articles ["
                      + year + " week " + str(week) + "] ===")
                get_articles(links, local_archive_path=archive_path)

    return 0


def main(argv):
    print_paths()
    years = ['2017', '2016', '2015', '2014', '2013', '2012', '2011']
    try:
        opts, args = getopt.getopt(argv, "hty:", ["years="])
    except getopt.GetoptError:
        print('Usage: python heisearchiver.downloader [-y <years>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: python heisearchiver.downloader [-y <years>]')
            sys.exit()
        elif opt in ("-y", "--years"):
            years = arg.split(',')
        elif opt in "-t":
            helpers.check_for_attributes_with_multiple_values(
                ARCHIVE_PATH + "/2017/",
                attributes={"name": "publisher"},
                tag="meta")
            sys.exit(0)

    fetch_archive(years)
    # links = extract_article_links(str(get_page(URL)))
    # get_articles(links)
    # print(links)


if __name__ == "__main__":
    main(sys.argv[1:])
