#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import shutil
import unittest
from unittest import TestCase

from src import file_processing_utilities
from src.pdf_processor import save_data_to_pdf
from src.rss_reader_impl import RSSReader


class TestPDFProcessor(TestCase):
    news_pdf_folder = 'news_pdf'

    def tearDown(self) -> None:
        shutil.rmtree(self.news_pdf_folder)

    def test_save_data_to_pdf(self):
        self.rss_reader_object = RSSReader("https://news.yahoo.com/rss/", to_pdf=True, limit=3)
        rss_feed = self.rss_reader_object._get_feed(self.rss_reader_object._rss_feed_url)
        data = self.rss_reader_object._get_posts_details(rss_feed)
        save_data_to_pdf(data, self.rss_reader_object._limit)
        file_name = file_processing_utilities.get_file_name(self.news_pdf_folder, data, '.pdf')
        self.assertTrue(file_processing_utilities.is_file_exists(file_name))


if __name__ == '__main__':
    unittest.main()
