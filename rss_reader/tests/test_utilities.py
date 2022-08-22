#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import unittest
from unittest import TestCase

from src.rss_reader_errors import URLNotFoundError, InvalidURLError, IncorrectURLError
from src.utilities import check_feed_url


class TestUtilities(TestCase):
    def test_bad_url_exception_1(self):
        with self.assertRaises(URLNotFoundError):
            check_feed_url("https://news.yahoo.ua")

    def test_bad_url_exception_2(self):
        with self.assertRaises(InvalidURLError):
            check_feed_url("https://")

    def test_bad_url_exception_3(self):
        with self.assertRaises(IncorrectURLError):
            check_feed_url("abc")


if __name__ == '__main__':
    unittest.main()
