#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
from datetime import datetime


def get_current_date() -> str:
    """
    Get the current date and time

    :return: formatted current date and time "%d/%m/%Y %H:%M:%S"
    """
    now = datetime.now()
    # dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")
