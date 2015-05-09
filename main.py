#!/usr/bin/env python
__author__ = 'toly'

from datetime import datetime
from argparse import ArgumentParser, ArgumentTypeError


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y.%m.%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise ArgumentTypeError(msg)


def create_arg_parser():
    parser = ArgumentParser()
    parser.add_argument('-i', '--init', action="store_true",
                        help="Init WTLog:\n 1. make dirs\n 2. find projects (.git/)\n 3. update crontab")
    parser.add_argument('-l', '--log', action="store_true",
                        help="Logging state of project dirs")
    parser.add_argument('-r', '--report', action="store_true",
                        help="Output report")
    parser.add_argument('-d', '--date', type=valid_date)
    return parser


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()


if __name__ == '__main__':
    main()