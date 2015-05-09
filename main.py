#!/usr/bin/env python
__author__ = 'toly'

import os
import commands
from datetime import datetime
from argparse import ArgumentParser, ArgumentTypeError


HOME_DIR = os.path.expanduser('~')
APP_DIR = os.path.join(HOME_DIR, '.wtlog')
CONFIG = os.path.join(APP_DIR, 'projects.conf')


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y.%m.%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise ArgumentTypeError(msg)


def create_arg_parser():
    parser = ArgumentParser(prog='wtlog')
    parser.add_argument('-i', '--init', action="store_true",
                        help="Init WTLog:\n 1. make dirs\n 2. find projects (.git/)\n 3. update crontab")
    parser.add_argument('-l', '--log', action="store_true",
                        help="Logging state of project dirs")
    parser.add_argument('-r', '--report', action="store_true",
                        help="Output report")
    parser.add_argument('-d', '--date', type=valid_date)
    return parser


def get_projects():
    with open(CONFIG) as f:
        lines = f.readlines()
    lines = map(lambda x: x.strip(), lines)
    lines = filter(None, lines)
    return lines


def make_app_dirs():
    if not os.path.exists(APP_DIR):
        os.mkdir(APP_DIR)


def add_projects():
    project_path = True
    projects = list()
    while project_path:
        project_path = raw_input('Add project path: ')
        if project_path:
            if os.path.exists(project_path):
                if os.path.isdir(project_path):
                    projects.append(project_path)
                else:
                    print 'Error: Project path must be a directory: %s' % project_path
            else:
                print 'Error: Project path must be exists: %s' % project_path

    with open(CONFIG, 'w') as f:
        for project_path in projects:
            f.write(project_path + '\n')


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    if args.init:
        make_app_dirs()
        add_projects()
        # update crontab
        return

    if args.log:
        # write log
        return

    if args.report:
        report_date = args.date or datetime.now()
        # make and print report
        return

    arg_parser.print_help()

if __name__ == '__main__':
    main()