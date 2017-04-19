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
        print("mock opener")
        return mock_response(req)


class TestHDL(unittest.TestCase):

    def setUp(self):
        my_opener = urllib.request.build_opener(MyHTTPHandler)
        urllib.request.install_opener(my_opener)

    def test_get_start_page(self):
        url = "http://example.com"
        response = urllib.request.urlopen(url)

        self.assertEqual(hdl.get_start_page(url), response.read())

    def test_extract_article_links(self):
        pass
