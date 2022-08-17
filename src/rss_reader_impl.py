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

    def __init__(self, url, is_JSON_needed=False, is_verbose=False, limit=0) -> None:
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

    def show_rss(self) -> None:
        """
        Print the RSS-feed topics. The only function is available for external use.

        :return: None
        """
        self._print_log_message("Program started")

        self._print_log_message("Getting RSS-feed")
        try:
            rss_feed = self._get_feed(self._rss_feed_url)
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
            data = self._get_posts_details(rss_feed)
        except RSSParsingError as err:
            print("RSS feed parsing error occurred", str(err))
            sys.exit(1)

        if self._JSON_mode:
            self._print_log_message("JSON mode on")
            self._show_rss_as_json(data)
        else:
            self._print_log_message("Plain text mode on")
            self._show_rss_as_plain_text(data)

        self._print_log_message("Program ended")

    def _print_log_message(self, message: str) -> None:
        """
        If verbose mode is on print a message in stdout

        :param str message: A message to print
        :return: None
        """
        if self._verbose_mode:
            print(message, utilities.get_current_date())

    def _get_feed(self, url):
        """
        Get the RSS feed from the RSS-feed URL

        :param str url: an RSS-feed URL
        :return: an RSS-feed object
        """
        utilities.check_feed_url(url)
        return feedparser.parse(url)

    def _get_posts_details(self, rss_feed) -> dict:
        """
        Get a formatted dictionary of RSS feed topics

        :param rss_feed: an RSS-feed object
        :return: formatted dict
        """
        posts_details = {"Blog title": self._get_feed_name(rss_feed), "Blog link": self._get_feed_link(rss_feed),
                         "posts": self._get_posts_list()}
        return posts_details

    def _get_feed_name(self, rss_feed) -> str:
        """
        Return the RSS-feed name

        :param rss_feed: an RSS-feed object
        :return: str the RSS-feed name
        """
        self._print_log_message("Getting the feed name")
        try:
            feed_name = rss_feed.feed.title
        except AttributeError:
            raise RSSParsingError
        return feed_name

    def _get_feed_link(self, rss_feed) -> str:
        """
        Return the RSS-feed link

        :param rss_feed: an RSS-feed object
        :return: str the RSS-feed link
        """
        self._print_log_message("Getting the feed link")
        try:
            feed_link = rss_feed.feed.link
        except AttributeError:
            raise RSSParsingError
        return feed_link

    def _get_posts_list(self) -> list:
        """
        Get the posts list from the RSS-feed

        :return: a list of posts
        """
        posts_list = []
        posts = self._get_feed(self._rss_feed_url)
        self._print_log_message("Getting the posts list")
        for post in posts.entries:
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
        self._print_log_message("Getting a post")
        post['title'] = entry.title
        post['date'] = time.strftime('%Y-%m-%d', entry.published_parsed)
        post['link'] = entry.link
        post['links'] = [link.href for link in entry.links]

        return post

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

    def _show_rss_as_json(self, data) -> None:
        """
        Print results in JSON

        :param data: a formatted dictionary of RSS feed topics
        :return: None
        """
        if self._is_print_all():
            self._print_log_message("Printing all posts as a JSON")
            print(json.dumps(data, indent=2))
        else:
            self._print_log_message("Printing limited posts as a JSON")
            self._limited_print(data)

    def _is_print_all(self) -> bool:
        """
        If `--limit` is not specified or `--limit` is larger than feed size then user should get all available news.

        :return: bool
        """
        rss_feed = self._get_feed(self._rss_feed_url)
        feed_length = self._get_feed_length(rss_feed)
        if self._limit == 0 or self._limit > feed_length:
            return True

    def _get_feed_length(self, rss_feed) -> int:
        """
        Return the RSS-feed topics count

        :param rss_feed: an RSS-feed object
        :return: int the RSS-feed topics count
        """
        self._print_log_message("Getting the feed length")
        return len(rss_feed.entries)

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
