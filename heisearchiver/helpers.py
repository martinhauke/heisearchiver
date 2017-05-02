import os
from bs4 import BeautifulSoup


def is_valid_article_id(string):
    """Returns true, if the article id appears to be valid"""
    return len(string) >= 4 and len(string) <= 7 and string.isdigit()


def check_for_attributes_with_multiple_values(path_to_archive, attributes,
                                              tag=None):
    """This method is just for checking if articles with multiple values for

    a specific attribute exist"""

    for filename in os.listdir(path_to_archive):
        with open(path_to_archive + filename, 'rb') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            values = soup.find_all(tag, attributes)
            values = values[0].attrs['content']

            print(values)
            if ',' in values or '/' in values:
                print("Multiple values found: " + values)
