# Tests for parser.py
import unittest
from datetime import datetime
from heisearchiver.parser import Parser


class TestParser(unittest.TestCase):

    content = """<html>
    <head>
    <meta content="2017-01-06T19:00:00" name="date"/>
    </head>
    <body>
    <article>
    <h1>
    Test save_article
    </h1>
    <p>
    This is an article
    </p>
    </article>
    </body>
    </html>"""

    def setUp(self):
        self.parser = Parser(self.content)

    def test_extract_year(self):
        self.assertEqual(self.parser.extract_year(), 2017)

    def test_extract_date(self):
        date = datetime.strptime("2017-01-06T19:00:00",
                                 "%Y-%m-%dT%H:%M:%S")
        self.assertEqual(self.parser.extract_date(), date)
