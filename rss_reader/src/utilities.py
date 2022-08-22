#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
from datetime import datetime

import requests

from src.rss_reader_errors import URLNotFoundError, IncorrectURLError, InvalidURLError


def get_current_date() -> str:
    """
    Get the current date and time

    :return: formatted current date and time "%d/%m/%Y %H:%M:%S"
    """
    now = datetime.now()
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
