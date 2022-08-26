#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import fnmatch
import json
import os

from src.rss_reader_errors import NewsNotFoundError
from src.utilities import _convert_space_to_underscore, _sanitize_filename, _set_file_name


def gen_find(filepattern, top: str):
    """
    Find all filenames in a directory tree that match a shell wildcard pattern

    :param str filepattern: a shell wildcard pattern for files
    :param str top: directory name
    :return:
    """
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepattern):
            yield os.path.join(path, name)


def gen_opener(filenames):
    """
    Open a sequence of filenames one at a time producing a file object.
    The file os closed immediately when proceeding to the next iteration.

    :param filenames:
    :return:
    """
    for filename in filenames:
        f = open(filename, 'r', encoding="utf-8")
        yield f
        f.close()


def search_and_print_news(news_folder: str, date: str) -> None:
    news_file_extension = '*.json'
    news_files_names = gen_find(news_file_extension, news_folder)
    files = gen_opener(news_files_names)
    is_found = False
    print("********************************************************************")
    print("Search results:")
    for news_json in files:
        data = json.load(news_json)
        print("********************************************************************")
        print("File name:", news_json.name)
        for post in data['posts']:
            if any([True for k, v in post.items() if v == date]):
                is_found = True
                print("********************************************************************")
                for k, v in post.items():
                    print(k, v)
    if not is_found:
        raise NewsNotFoundError


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


def create_news_folder(dir_path: str) -> None:
    """
    Create the news folder

    :param str dir_path: the folder name
    :return: None
    """
    os.makedirs(dir_path)


def is_file_exists(file_path: str) -> bool:
    """
    Check if the file exists

    :param str file_path: path to a file
    :return: True/False
    """
    return os.path.isfile(file_path)


def is_dir_exists(dir_path: str) -> bool:
    """
    Check if the folder exists

    :param dir_path: path to a folder
    :return: True/False
    """
    return os.path.isdir(dir_path)


def get_file_name(news_folder: str, data: dict) -> str:
    """
    Return full file name

    :param str news_folder: folder to save
    :param dict data: RSS news
    :return: full file name
    """
    file_extension = '.json'
    feed_name = _convert_space_to_underscore(_sanitize_filename(data['Blog title']))
    return os.path.join(news_folder, _set_file_name(feed_name) + file_extension)
