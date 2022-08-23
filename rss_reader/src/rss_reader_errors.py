#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.

class RSSReaderErrors(Exception):
    pass


class RSSParsingError(RSSReaderErrors):
    pass


class URLNotFoundError(RSSReaderErrors):
    pass


class InvalidURLError(RSSReaderErrors):
    pass


class IncorrectURLError(RSSReaderErrors):
    pass


class InvalidNewsDateError(RSSReaderErrors):
    pass
