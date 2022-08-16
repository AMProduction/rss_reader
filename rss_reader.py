#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.

import argparse

from src.rss_reader_impl import RSSReader

# adding CLI arguments
parser = argparse.ArgumentParser(prog='RSS reader', description='Pure Python command-line RSS reader.',
                                 epilog='Enjoy the program!')
parser.add_argument('url', type=str, help='RSS feed URL')
parser.add_argument('--version',
                    action='version',
                    version='%(prog)s v.1.0',
                    help='Print version info and exits')
parser.add_argument('-j',
                    '--json',
                    action='store_true',
                    help='Print result as JSON in stdout')
parser.add_argument('--verbose',
                    action='store_true',
                    help='Outputs verbose status messages')
parser.add_argument('--limit',
                    action='store',
                    type=int,
                    help='Limit news topics if this parameter provided')
# parsing CLI arguments
args = parser.parse_args()


# check and initial defining optional arguments
def check_is_JSON_needed(arguments) -> bool:
    return arguments.json


def check_is_verbose(arguments) -> bool:
    return arguments.verbose


def set_limit(arguments) -> int:
    if arguments.limit is not None and arguments.limit >= 0:
        return arguments.limit
    else:
        return 0


if __name__ == '__main__':
    rss_reader = RSSReader(args.url, check_is_JSON_needed(args), check_is_verbose(args), set_limit(args))
    rss_reader.show_rss()
