# Testing hdl.py
import unittest
from src import hdl
from io import StringIO
import urllib.request


def mock_response(req):
    if req.get_full_url() == "http://example.com":
        resp = urllib.request.addinfourl(StringIO("mock file"),
                                         "mock message",
                                         req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp


class MyHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return mock_response(req)


class TestHDL(unittest.TestCase):

    def setUp(self):
        my_opener = urllib.request.build_opener(MyHTTPHandler)
        urllib.request.install_opener(my_opener)

    def test_get_page(self):
        url = "http://example.com"
        response = urllib.request.urlopen(url)

        self.assertEqual(hdl.get_page(url), response.read())

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
