#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import json
import sys
import time

import feedparser

from src import utilities
from src.rss_reader_errors import *


class RSSReader:
    """The class is responsible for getting, transforming, and printing an RSS-feed topics"""

    _rss_feed_url = ""
    _JSON_mode = False
    _verbose_mode = False
    _limit = 0
    _date = ""
    _news_folder = 'news'
    _rss_feed = None

    def __init__(self, url, is_JSON_needed=False, is_verbose=False, limit=0, date="") -> None:
        """
        The class constructor

        :param str url: an RSS-feed URL
        :param bool is_JSON_needed: Print result as JSON in stdout
        :param bool is_verbose: Outputs verbose status messages
        :param int limit: Limit news topics if this parameter provided
        """
        self._rss_feed_url = url
        self._JSON_mode = is_JSON_needed
        self._verbose_mode = is_verbose
        self._limit = limit
        self._date = date

    def show_rss(self) -> None:
        """
        Print the RSS-feed topics. The only function is available for external use.

        :return: None
        """
        self._print_log_message("Program started")

        self._search_historical_data(self._date)

        self._print_log_message("Getting RSS-feed")
        try:
            self._rss_feed = self._get_feed(self._rss_feed_url)
        except URLNotFoundError as err:
            print("The URL not found. Check the URL and try again", str(err))
            sys.exit(1)
        except InvalidURLError as err:
            print("The invalid URL was provided. Check the URL and try again", str(err))
            sys.exit(1)
        except IncorrectURLError as err:
            print("The incorrect URL was provided. Check the URL and try again", str(err))
            sys.exit(1)

        self._print_log_message("Getting posts")
        try:
            data = self._get_posts_details()
        except RSSParsingError as err:
            print("RSS feed parsing error occurred", str(err))
            sys.exit(1)

        if self._JSON_mode:
            self._print_log_message("JSON mode on")
            self._show_rss_as_json(data)
        else:
            self._print_log_message("Plain text mode on")
            self._show_rss_as_plain_text(data)

        self._save_historical_data(data)

        self._print_log_message("Program ended")

    def _print_log_message(self, message: str) -> None:
        """
        If verbose mode is on print a message in stdout

        :param str message: A message to print
        :return: None
        """
        if self._verbose_mode:
            print(message, utilities.get_formatted_current_date_for_log())

    def _search_historical_data(self, date: str) -> None:
        """
        Search and print news by a particular date from the cache

        :param str date: the CLI arg - input date
        :return: None
        """
        if date is not None:
            try:
                utilities.validate_news_date_argument(self._date)
            except InvalidNewsDateError as err:
                print("The invalid date. The date should be in 'yyyymmdd' format", str(err))
                sys.exit(1)
            if utilities.is_dir_exists(self._news_folder):
                self._print_log_message("Searching news...")
                utilities.search_and_print_news(self._news_folder, self._date)
            else:
                self._print_log_message("News folder not found")
        else:
            self._print_log_message("Date for searching was not provided")

    def _get_feed(self, url):
        """
        Get the RSS feed from the RSS-feed URL

        :param str url: an RSS-feed URL
        :return: an RSS-feed object
        """
        utilities.check_feed_url(url)
        return feedparser.parse(url)

    def _get_posts_details(self) -> dict:
        """
        Get a formatted dictionary of RSS feed topics

        :return: formatted dict
        """
        posts_details = {"Blog title": self._get_feed_name(), "Blog link": self._get_feed_link(),
                         "posts": self._get_posts_list()}
        return posts_details

    def _get_feed_name(self) -> str:
        """
        Return the RSS-feed name

        :return: str the RSS-feed name
        """
        self._print_log_message("Getting the feed name")
        try:
            feed_name = self._rss_feed.feed.title
        except AttributeError:
            raise RSSParsingError
        return feed_name

    def _get_feed_link(self) -> str:
        """
        Return the RSS-feed link

        :return: str the RSS-feed link
        """
        self._print_log_message("Getting the feed link")
        try:
            feed_link = self._rss_feed.feed.link
        except AttributeError:
            raise RSSParsingError
        return feed_link

    def _get_posts_list(self) -> list:
        """
        Get the posts list from the RSS-feed

        :return: a list of posts
        """
        posts_list = []
        self._print_log_message("Getting the posts list")
        for post in self._rss_feed.entries:
            if post.title in [x['title'] for x in posts_list]:
                pass
            else:
                temp_post = self._get_post(post)
                posts_list.append(temp_post)

        return posts_list

    def _get_post(self, entry) -> dict:
        """
        Get a post from the RSS-feed

        :param entry: an RSS-feed topic object
        :return: a parsed RSS topic dict
        """
        post = dict()
        post['title'] = entry.title
        post['date'] = time.strftime('%Y%m%d', entry.published_parsed)
        post['link'] = entry.link
        post['links'] = [link.href for link in entry.links]

        return post

    def _show_rss_as_json(self, data) -> None:
        """
        Print results in JSON

        :param data: a formatted dictionary of RSS feed topics
        :return: None
        """
        if self._is_print_all():
            self._print_log_message("Printing all posts as a JSON")
            print(json.dumps(data, ensure_ascii=False, indent=4))
        else:
            self._print_log_message("Printing limited posts as a JSON")
            self._limited_print(data)

    def _is_print_all(self) -> bool:
        """
        If `--limit` is not specified or `--limit` is larger than feed size then user should get all available news.

        :return: bool
        """
        feed_length = self._get_feed_length()
        if self._limit == 0 or self._limit > feed_length:
            return True

    def _get_feed_length(self) -> int:
        """
        Return the RSS-feed topics count

        :return: int the RSS-feed topics count
        """
        self._print_log_message("Getting the feed length")
        return len(self._rss_feed.entries)

    def _limited_print(self, data) -> None:
        """
        Limit news topics

        :param data: a formatted dictionary of RSS feed topics
        :return: None
        """
        limit = 0
        for post in data['posts']:
            print("********************************************************************")
            for k, v in post.items():
                print(k, v)
            limit += 1
            if limit == self._limit:
                break

    def _show_rss_as_plain_text(self, data) -> None:
        """
        Print results in human-readable format

        :param data: a formatted dictionary of RSS feed topics
        :return: None
        """
        if self._is_print_all():
            self._print_log_message("Printing all posts as a plain text")
            print(data)
        else:
            self._print_log_message("Printing limited posts as a plain text")
            self._limited_print(data)

    def _save_historical_data(self, data) -> None:
        """
        Save the RSS news

        :param data: a formatted dictionary of RSS feed topics
        :return: None
        """
        if not utilities.is_dir_exists(self._news_folder):
            self._print_log_message("News folder not found. Creating...")
            utilities.create_news_folder(self._news_folder)
            self._print_log_message("News folder created successfully")
        file_name = utilities.get_file_name(self._news_folder, data)
        if not utilities.is_file_exists(file_name):
            self._print_log_message("File " + file_name + " not found. Caching...")
            utilities.write_json_to_file(self._news_folder, data)
            self._print_log_message("News saved successfully")
        else:
            self._print_log_message("File " + file_name + " found. No need to cache")
