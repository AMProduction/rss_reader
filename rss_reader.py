#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.

import argparse

# parsing CLI arguments
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

args = parser.parse_args()

if __name__ == '__main__':
    print(vars(args))
