#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from src.rss_reader_errors import RSSParsingError
from src.rss_reader_impl import RSSReader
from src.utilities import get_current_date


class TestRSSReader(TestCase):

    def setUp(self) -> None:
        self.rss_reader_full = RSSReader("https://news.yahoo.com/rss/", False, False, 0)
        self.rss_reader_verbose = RSSReader("https://news.yahoo.com/rss/", False, True, 0)
        self.rss_reader_limit = RSSReader("https://news.yahoo.com/rss/", False, False, 3)

    def test_get_feed_name(self):
        rss_feed = self.rss_reader_full._get_feed(self.rss_reader_full._rss_feed_url)
        self.assertEqual(self.rss_reader_full._get_feed_name(rss_feed), "Yahoo News - Latest News & Headlines")

    def test_get_feed_wrong_name(self):
        rss_feed = self.rss_reader_full._get_feed(self.rss_reader_full._rss_feed_url)
        self.assertNotEqual(self.rss_reader_full._get_feed_name(rss_feed), "Test_name")

    def test_get_feed_link(self):
        rss_feed = self.rss_reader_full._get_feed(self.rss_reader_full._rss_feed_url)
        self.assertEqual(self.rss_reader_full._get_feed_link(rss_feed), "https://www.yahoo.com/news")

    def test_get_feed_wrong_link(self):
        rss_feed = self.rss_reader_full._get_feed(self.rss_reader_full._rss_feed_url)
        self.assertNotEqual(self.rss_reader_full._get_feed_link(rss_feed), "Test_link")

    def test_print_all_true(self):
        self.assertTrue(self.rss_reader_full._is_print_all())

    def test_print_all_false(self):
        self.assertFalse(self.rss_reader_limit._is_print_all())

    def test_get_feed_length(self):
        rss_feed = self.rss_reader_full._get_feed(self.rss_reader_full._rss_feed_url)
        self.assertEqual(self.rss_reader_full._get_feed_length(rss_feed), 50)

    def test_get_feed_length_wrong(self):
        rss_feed = self.rss_reader_full._get_feed(self.rss_reader_full._rss_feed_url)
        self.assertNotEqual(self.rss_reader_full._get_feed_length(rss_feed), 1)

    def test_print_log_message(self):
        with patch('sys.stdout', new=StringIO()) as mock_out:
            self.rss_reader_verbose._print_log_message("Test message")
            self.assertEqual(mock_out.getvalue(), "Test message " + get_current_date() + "\n")

    def test_not_print_log_message(self):
        with patch('sys.stdout', new=StringIO()) as mock_out:
            self.rss_reader_full._print_log_message("Test message")
            self.assertEqual(mock_out.getvalue(), "")

    def test_posts_detail(self):
        rss_feed = self.rss_reader_full._get_feed(self.rss_reader_full._rss_feed_url)
        data = self.rss_reader_full._get_posts_details(rss_feed)
        self.assertEqual(data['Blog title'], "Yahoo News - Latest News & Headlines")
        self.assertEqual(data['Blog link'], "https://www.yahoo.com/news")

    def test_test_get_feed_name_exception(self):
        test_object = "Test"
        with self.assertRaises(RSSParsingError):
            self.rss_reader_full._get_feed_name(test_object)

    def test_test_get_feed_link_exception(self):
        test_object = "Test"
        with self.assertRaises(RSSParsingError):
            self.rss_reader_full._get_feed_link(test_object)


if __name__ == '__main__':
    unittest.main()
