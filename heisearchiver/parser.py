from bs4 import BeautifulSoup
from datetime import datetime


class Parser():

    def __init__(self, content):
        self.soup = BeautifulSoup(content, 'html.parser')

    def prettify(self):
        return self.soup.prettify()

    def extract_year(self):
        date = self.extract_date()
        return date.year

    def extract_date(self):
        date_string = self.soup.find_all("meta", {"name": "date"})
        print(date_string)
        return datetime.strptime(date_string[0].attrs['content'],
                                 "%Y-%m-%dT%H:%M:%S")
