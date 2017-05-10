from bs4 import BeautifulSoup
from datetime import datetime


class Parser():

    def __init__(self, content):
        self.soup = BeautifulSoup(content, 'html.parser')

    def prettify(self):
        """Returns a prettified version of the original input"""
        return self.soup.prettify()

    def extract_year(self):
        """Returns the publication year of the article"""
        date = self.extract_date()
        return date.year

    def extract_date(self):
        """Returns the publication date of the article"""
        date_string = self.soup.find_all("meta", {"name": "date"})
        print(date_string)
        return datetime.strptime(date_string[0].attrs['content'],
                                 "%Y-%m-%dT%H:%M:%S")
