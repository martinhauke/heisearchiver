# Testing hdl.py
import os
import unittest
from heisearchiver import hdl
from io import StringIO
import urllib.request
from heisearchiver.config import BASE_URL, PATH_FOR_TEST_FILES
from bs4 import BeautifulSoup


def mock_response(req):
    print("URL: " + req.get_full_url())
    if req.get_full_url() == "http://example.com":
        resp = urllib.request.addinfourl(StringIO("mock file"),
                                         "mock message",
                                         req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp
    elif req.get_full_url() == BASE_URL + "article-123456.html":
        message = """<html>
        <body>
        <article>This is an article</article>
        </body>
        </html>"""
        resp = urllib.request.addinfourl(StringIO(message),
                                         "mock message",
                                         req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp
    elif req.get_full_url() == BASE_URL + "article-123457.html":
        message = """<html>
        <body>
        <article>This is another article</article>
        </body>
        </html>"""
        resp = urllib.request.addinfourl(StringIO(message),
                                         "mock message",
                                         req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp
    else:
        resp = urllib.request.addinfourl(StringIO("mock file"),
                                         "mock message",
                                         req.get_full_url())
        resp.code = 404
        resp.msg = "Not found"
        return resp


class MyHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        print("http")
        return mock_response(req)


class MyHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        print("https")
        return mock_response(req)


class TestHDL(unittest.TestCase):

    def setUp(self):
        my_opener = urllib.request.build_opener(MyHTTPHandler, MyHTTPSHandler)
        urllib.request.install_opener(my_opener)
        if not os.path.exists(PATH_FOR_TEST_FILES):
            os.makedirs(PATH_FOR_TEST_FILES)

    def test_get_page(self):
        url = "http://example.com"
        response = urllib.request.urlopen(url)

        self.assertEqual(hdl.get_page(url), response.read())

    def test_get_page_with_invalid_url(self):
        url = "thisisnotavalidurl"

        self.assertIsNone(hdl.get_page(url))

    def test_get_page_that_does_not_exist(self):
        self.assertIsNone(hdl.get_page("http://notapage.com"))

    def test_extract_article_links(self):
        content = """
        <html>
        <head></head>
        <body>
            <a href='/should-be-ignored'>ignore me</a>
            <a href='/newsticker/meldung/article-name-1234567.html'>
                find me once
            </a>
            <a href='/newsticker/meldung/article-name-1234567.html'>
                find me once
            </a>
            <a href='/newsticker/meldung/article-name-1234568.html'>
                find me, too
            </a>
            <a href='/newsticker/meldung/wrong-format.html'>
                this link is wrong
            </a>
            <a href='/newsticker/should-be-ignored'>ignore me</a>
        </body>
        </html>
        """
        valid_links = {
            '1234567': '/newsticker/meldung/article-name-1234567.html',
            '1234568': '/newsticker/meldung/article-name-1234568.html'}

        self.assertDictEqual(hdl.extract_article_links(content), valid_links)

    def test_get_articles(self):
        article_links = {
            '123456': "article-123456.html",
            '123457': "article-123457.html",
        }

        hdl.get_articles(article_links, local_archive_path=PATH_FOR_TEST_FILES)

        for article_id, href in article_links.items():
            path_to_file = PATH_FOR_TEST_FILES + article_id
            with open(path_to_file, 'r') as f:
                response = urllib.request.urlopen(BASE_URL + href)
                soup = BeautifulSoup(response.read(), "html.parser")
                self.assertEqual(soup.prettify(), f.read())
            os.remove(path_to_file)

    def test_write_article_to_file(self):
        content = "this ist a test;\nthis is a test on the next level"
        mockfile = StringIO()
        hdl.write_article_to_file(content, outfile=mockfile)
        self.assertEqual(content, mockfile.getvalue())
