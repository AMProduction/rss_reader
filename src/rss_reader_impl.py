#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import json
import time

import feedparser


class RSSReader:
    _rss_feed_url = ""
    _JSON_mode = False
    _verbose_mode = False
    _limit = 0

    def __init__(self, url, is_JSON_needed=False, is_verbose=False, limit=0) -> None:
        self._rss_feed_url = url
        self._JSON_mode = is_JSON_needed
        self._verbose_mode = is_verbose
        self._limit = limit

    def show_rss(self) -> None:
        rss_feed = self._get_feed(self._rss_feed_url)
        data = self._get_posts_details(rss_feed)
        if self._JSON_mode:
            self._show_rss_as_json(data)
        else:
            self._show_rss_as_plain_text(data)

    def _get_feed(self, url):
        return feedparser.parse(url)

    def _get_posts_details(self, rss_feed) -> dict:
        posts_details = {"Blog title": self._get_feed_name(rss_feed), "Blog link": self._get_feed_link(rss_feed),
                         "posts": self._get_posts_list(rss_feed)}
        return posts_details

    def _get_posts_list(self, rss_feed) -> list:
        post_list = []
        posts = self._get_feed(self._rss_feed_url)
        for post in posts.entries:
            if post.title in [x['title'] for x in post_list]:
                pass
            else:
                temp_post = self._get_post(post)
                post_list.append(temp_post)

        return post_list

    def _get_post(self, entry) -> dict:
        post = dict()
        try:
            post['title'] = entry.title
            post['date'] = time.strftime('%Y-%m-%d', entry.published_parsed)
            post['link'] = entry.link
            post['links'] = [link.href for link in entry.links]
        except:
            pass

        return post

    def _get_feed_name(self, rss_feed) -> str:
        return rss_feed.feed.title

    def _get_feed_link(self, rss_feed) -> str:
        return rss_feed.feed.link

    def _show_rss_as_plain_text(self, data) -> None:
        if self._is_print_all():
            print(data)
        else:
            self._limited_print(data)

    def _show_rss_as_json(self, data) -> None:
        if self._is_print_all():
            print(json.dumps(data, indent=2))
        else:
            self._limited_print(data)

    def _is_print_all(self) -> bool:
        rss_feed = self._get_feed(self._rss_feed_url)
        feed_length = self._get_feed_length(rss_feed)
        if self._limit == 0 or self._limit > feed_length:
            return True
        else:
            return False

    def _get_feed_length(self, rss_feed) -> int:
        return len(rss_feed.entries)

    def _limited_print(self, data) -> None:
        limit = 0
        for post in data['posts']:
            print("********************************************************************")
            for k, v in post.items():
                print(k, v)
            limit += 1
            if limit == self._limit:
                break
