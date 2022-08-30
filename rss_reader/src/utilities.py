#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import re
from datetime import datetime

import requests

from .rss_reader_errors import URLNotFoundError, IncorrectURLError, InvalidURLError, InvalidNewsDateError


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


def _convert_space_to_underscore(input_str: str) -> str:
    """
    Replace space to underscore

    :param str input_str: string for transformation
    :return: string after transformation
    """
    return input_str.replace(' ', '_')


def _sanitize_filename(input_str: str) -> str:
    """
    Remove the special characters from the string. Keep spaces

    :param str input_str: string for transformation
    :return: string without special characters
    """
    return re.sub(r'[^a-zA-Z0-9\u0400-\u04FF]', " ", input_str)


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


def get_formatted_date_to_pdf(date_str: str) -> str:
    """
    Returnn formatted date string

    :param str date_str: the string in yyyymmdd
    :return: the string in yyyy-mm-dd
    """
    return date_str[:4] + '-' + date_str[4:6] + '-' + date_str[6:]
