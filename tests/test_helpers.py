# Testing helpers.py
import unittest
from src import helpers


class TestHelpers(unittest.TestCase):

    def test_is_valid_article_id_with_number(self):
        self.assertTrue(helpers.is_valid_article_id("1234567"))

    def test_is_valid_article_id_with_invalid_input(self):
        self.assertFalse(helpers.is_valid_article_id("peter"))
        self.assertFalse(helpers.is_valid_article_id("-123456"))
        self.assertFalse(helpers.is_valid_article_id("12345"))
        self.assertFalse(helpers.is_valid_article_id("12345678"))
        self.assertFalse(helpers.is_valid_article_id("1.23456"))
        self.assertFalse(helpers.is_valid_article_id("a123456"))
