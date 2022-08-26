#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import unittest
from unittest import TestCase

from src.rss_reader_errors import URLNotFoundError, InvalidURLError, IncorrectURLError, InvalidNewsDateError
from src.utilities import check_feed_url, validate_news_date_argument, _convert_space_to_underscore, _sanitize_filename


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

    def test_date_validation_exception(self):
        with self.assertRaises(InvalidNewsDateError):
            validate_news_date_argument("26-08-2022")

    def test_convert_space_to_underscore(self):
        self.assertEqual(_convert_space_to_underscore("Test test test"), "Test_test_test")

    def test_sanitize_filename(self):
        self.assertEqual(_sanitize_filename("Test!23&%test.)test&&?"), "Test 23  test  test   ")


if __name__ == '__main__':
    unittest.main()
