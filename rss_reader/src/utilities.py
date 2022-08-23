#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import json
import os
from datetime import datetime

import requests

from src.rss_reader_errors import URLNotFoundError, IncorrectURLError, InvalidURLError, InvalidNewsDateError


def get_current_time() -> datetime:
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
    now = get_current_time()
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


def _space_to_underscore(input_str: str) -> str:
    return input_str.replace(' ', '_')


def _get_formatted_current_date_for_file_name() -> str:
    """
    Get the formatted current date and time for a filename

    :return: formatted current date and time "%Y%m%d"
    """
    now = get_current_time()
    # yyyymmdd
    return now.strftime("%Y%m%d")


def _set_file_name(input_str: str) -> str:
    return "".join([input_str, "-", _get_formatted_current_date_for_file_name()])


def get_file_name(news_folder: str, data: dict) -> str:
    file_extension = '.json'
    feed_name = _space_to_underscore(data['Blog title'])
    return os.path.join(news_folder, _set_file_name(feed_name) + file_extension)


def write_json_to_file(news_folder: str, data: dict) -> None:
    file_name = get_file_name(news_folder, data)
    with open(file_name, 'w') as f:
        json.dump(data, f)


def _read_json_from_file(path_to_file: str) -> dict:
    with open(path_to_file, 'r') as f:
        json_dict = json.load(f)
    return json_dict


def search_and_print(news_folder: str, date: str) -> None:
    for filename in os.listdir(news_folder):
        news_json = os.path.join(news_folder, filename)
        # checking if it is a file
        if os.path.isfile(news_json):
            data = _read_json_from_file(news_json)
            for post in data['posts']:
                if any([True for k, v in post.items() if v == date]):
                    print("Found")
                    print("********************************************************************")
                    for k, v in post.items():
                        print(k, v)


def is_dir_exists(dir_path: str) -> bool:
    return os.path.isdir(dir_path)


def is_file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)


def create_news_folder(dir_path: str) -> None:
    os.makedirs(dir_path)
