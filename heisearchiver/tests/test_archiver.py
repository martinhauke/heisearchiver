# Testing heisedownloader.archiver.py
import unittest
import os
from heisearchiver import archiver
from heisearchiver.config import PATH_FOR_TEST_FILES


class TestArchiver(unittest.TestCase):

    def test_write_article_to_file(self):
        content = "this ist a test;\nthis is a test on the next level"
        filename = PATH_FOR_TEST_FILES + "testfile"
        archiver.write_article_to_file(content, filename)
        with open(filename, 'r') as f:
            self.assertEqual(content, f.read())
        os.remove(filename)

    def test_save_article(self):
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

        archiver.save_article(article_id='21234', content=content,
                              path=PATH_FOR_TEST_FILES)

        with open(PATH_FOR_TEST_FILES + "/2017/21234", 'r') as f:
            self.assertEqual(content.split(), f.read().split())
        os.remove(PATH_FOR_TEST_FILES + "/2017/21234")
