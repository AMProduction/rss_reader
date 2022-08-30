#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.

import argparse

from src.rss_reader_impl import RSSReader

# adding CLI arguments
parser = argparse.ArgumentParser(prog='RSS reader', description='Pure Python command-line RSS reader.',
                                 epilog='Enjoy the program!')
parser.add_argument('--url',
                    action='store',
                    type=str,
                    help='RSS feed URL')
parser.add_argument('--version',
                    action='version',
                    version='%(prog)s v.4.0',
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
parser.add_argument('--date',
                    action='store',
                    type=str,
                    help='The date getting news from local storage')
parser.add_argument('--to_pdf',
                    action='store_true',
                    help='Save results as PDF file')
parser.add_argument('--to_html',
                    action='store_true',
                    help='Save results as HTML file')
# parsing CLI arguments
args = parser.parse_args()


# check and initial defining optional arguments
def set_url(arguments) -> str:
    return arguments.url


def check_is_JSON_needed(arguments) -> bool:
    return arguments.json


def check_is_verbose(arguments) -> bool:
    return arguments.verbose


def set_limit(arguments) -> int:
    if arguments.limit is not None and arguments.limit >= 0:
        return arguments.limit
    else:
        return 0


def set_date(arguments) -> str:
    return arguments.date


def set_pdf(arguments) -> bool:
    return arguments.to_pdf


def set_html(arguments) -> bool:
    return arguments.to_html


def main():
    rss_reader = RSSReader(set_url(args), check_is_JSON_needed(args), check_is_verbose(args), set_limit(args),
                           set_date(args), set_pdf(args), set_html(args))
    rss_reader.show_rss()


if __name__ == '__main__':
    main()
