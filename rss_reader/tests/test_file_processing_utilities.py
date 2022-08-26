#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import os
import shutil
import unittest
from unittest import TestCase
from src.file_processing_utilities import is_file_exists, is_dir_exists, create_news_folder


class TestFileProcessingUtilities(TestCase):
    test_directory_name = "Test_directory"
    test_file_name = "test.txt"

    def setUp(self) -> None:
        os.mkdir(self.test_directory_name)
        with open(os.path.join(self.test_directory_name, self.test_file_name), 'w') as fp:
            fp.write('This is a new line')

    def tearDown(self) -> None:
        shutil.rmtree(self.test_directory_name)

    def test_is_file_exists(self):
        self.assertTrue(is_file_exists(os.path.join(self.test_directory_name, self.test_file_name)))

    def test_is_dir_exists(self):
        self.assertTrue(is_dir_exists(self.test_directory_name))

    def test_create_news_folder(self):
        expected_dir_path = os.path.join(self.test_directory_name, "Test_2")
        create_news_folder(expected_dir_path)
        self.assertTrue(os.path.isdir(expected_dir_path))


if __name__ == '__main__':
    unittest.main()
