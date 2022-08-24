#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
import fnmatch
import os


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
