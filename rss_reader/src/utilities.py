#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import json
import os
import re
from datetime import datetime

import requests

from src import file_processing_utilities
from src.rss_reader_errors import URLNotFoundError, IncorrectURLError, InvalidURLError, InvalidNewsDateError


def _get_current_time() -> datetime:
    """
    Get current time

    :return: current time
    """
    return datetime.now()


def get_formatted_current_date_for_log() -> str:
    """
    Get the formatted current date and time for log

    :return: formatted current date and time "%d/%m/%Y %H:%M:%S"
    """
    now = _get_current_time()
    # dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")


def check_feed_url(url: str) -> None:
    """
    Validation an RSS feed URL

    :param str url: an RSS-feed URL
    :return: raise an error in case of present
    """
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        raise URLNotFoundError
    except requests.exceptions.InvalidURL:
        raise InvalidURLError
    except requests.exceptions.RequestException:
        raise IncorrectURLError


def validate_news_date_argument(input_data: str) -> None:
    """
    Validation of the input date. The date should be in 'yyyymmdd' format

    :param str input_data: the CLI arg - input date
    :return: raise an error in case of present
    """
    format_yyyymmdd = '%Y%m%d'
    try:
        datetime.strptime(input_data, format_yyyymmdd)
    except ValueError:
        raise InvalidNewsDateError


def search_and_print_news_2(news_folder: str, date: str) -> None:
    news_file_extension = '*.json'
    news_files_names = file_processing_utilities.gen_find(news_file_extension, news_folder)
    files = file_processing_utilities.gen_opener(news_files_names)
    for news_json in files:
        data = json.load(news_json)
        print("********************************************************************")
        print("File name:", news_json.name)
        for post in data['posts']:
            if any([True for k, v in post.items() if v == date]):
                print("********************************************************************")
                for k, v in post.items():
                    print(k, v)


def search_and_print_news(news_folder: str, date: str) -> None:
    """
    Search and print news by a particular date from the cache

    :param str news_folder: path to cached news
    :param str date: date to search
    :return: None
    """
    for filename in os.listdir(news_folder):
        news_json = os.path.join(news_folder, filename)
        # checking if it is a file
        if os.path.isfile(news_json):
            data = _read_json_from_file(news_json)
            print("********************************************************************")
            print("File name:", news_json)
            for post in data['posts']:
                if any([True for k, v in post.items() if v == date]):
                    print("********************************************************************")
                    for k, v in post.items():
                        print(k, v)


def _read_json_from_file(path_to_file: str) -> dict:
    """
    Read from the file and deserialization of JSON

    :param str path_to_file: path to JSON
    :return: dictionary
    """
    with open(path_to_file, 'r', encoding="utf-8") as f:
        json_dict = json.load(f)
    return json_dict


def write_json_to_file(news_folder: str, data: dict) -> None:
    """
    Save data as a JSON to file

    :param str news_folder: path to JSON
    :param dict data: dictionary
    :return: None
    """
    file_name = get_file_name(news_folder, data)
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_file_name(news_folder: str, data: dict) -> str:
    """
    Return full file name

    :param str news_folder: folder to save
    :param dict data: RSS news
    :return: full file name
    """
    file_extension = '.json'
    feed_name = _convert_space_to_underscore(_clean_filename(data['Blog title']))
    return os.path.join(news_folder, _set_file_name(feed_name) + file_extension)


def _clean_filename(input_str: str) -> str:
    """
    Remove the special characters from the string. Keep spaces

    :param str input_str: string for transformation
    :return: string without special characters
    """
    return re.sub(r"[^a-zA-Z0-9\u0400-\u04FF]", " ", input_str)


def _convert_space_to_underscore(input_str: str) -> str:
    """
    Replace space to underscore

    :param str input_str: string for transformation
    :return: string after transformation
    """
    return input_str.replace(' ', '_')


def _set_file_name(input_str: str) -> str:
    """
    Make the file name as 'feed_name-current_date'

    :param str input_str: the feed name
    :return: file name
    """
    return "".join([input_str, "-", _get_formatted_current_date_for_file_name()])


def _get_formatted_current_date_for_file_name() -> str:
    """
    Get the formatted current date and time for a filename

    :return: formatted current date and time "%Y%m%d"
    """
    now = _get_current_time()
    # yyyymmdd
    return now.strftime("%Y%m%d")


def is_dir_exists(dir_path: str) -> bool:
    """
    Check if the folder exists

    :param dir_path: path to a folder
    :return: True/False
    """
    return os.path.isdir(dir_path)


def is_file_exists(file_path: str) -> bool:
    """
    Check if the file exists

    :param str file_path: path to a file
    :return: True/False
    """
    return os.path.isfile(file_path)


def create_news_folder(dir_path: str) -> None:
    """
    Create the news folder

    :param str dir_path: the folder name
    :return: None
    """
    os.makedirs(dir_path)
