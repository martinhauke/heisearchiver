import os
from bs4 import BeautifulSoup


def is_valid_article_id(string):
    """Returns true, if the article id appears to be valid"""
    return len(string) >= 4 and len(string) <= 7 and string.isdigit()


def check_for_articles_with_multiple_authors(path_to_archive):
    """This method is just for checking if articles with multiple authors

    exist"""

    for filename in os.listdir(path_to_archive):
        with open(path_to_archive + filename, 'rb') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            authors = soup.find_all("meta", {"name": "author"})
            authors = authors[0].attrs['content']
            if ',' in authors or '/' in authors:
                print("Multiple authors found: " + authors)
