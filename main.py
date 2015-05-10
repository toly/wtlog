#!/usr/bin/env python
__author__ = 'toly'
"""
    Format log file:
        timestamp1  project_path1   branch1
        timestamp1  project_path2   branch2
        timestamp2  project_path1   branch3
"""

import os
import time
import commands
from collections import defaultdict
from datetime import datetime
from argparse import ArgumentParser, ArgumentTypeError


HOME_DIR = os.path.expanduser('~')
APP_DIR = os.path.join(HOME_DIR, '.wtlog')
CONFIG = os.path.join(APP_DIR, 'projects.conf')
LOG_FORMAT = '{timestamp}\t{project_path}\t{branch}\n'


def create_arg_parser():

    def valid_date(s):
        try:
            return datetime.strptime(s, "%Y.%m.%d")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise ArgumentTypeError(msg)

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
    lines.sort()
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


class WorkTimeLog(object):

    def __init__(self, date=None):
        self.date = date or datetime.now()

    @property
    def log_path_file(self):
        log_directory = os.path.join(APP_DIR, self.date.strftime('%Y/%m'))
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        return os.path.join(APP_DIR, self.date.strftime('%Y/%m/%d')) + '.log'

    def write_log(self):
        results = {}
        for project_path in get_projects():
            get_branch_command = 'cd %s && git rev-parse --abbrev-ref HEAD' % project_path
            status, branch = commands.getstatusoutput(get_branch_command)
            if status == 0:
                results[project_path] = branch

        time_hash = str(time.time())
        with open(self.log_path_file, 'a+') as f:
            for project_path in get_projects():
                log_params = dict(
                    timestamp=time_hash,
                    project_path=project_path,
                    branch=results[project_path]
                )
                log_line = LOG_FORMAT.format(**log_params)
                f.write(log_line)

    def read_log(self):
        with open(self.log_path_file) as f:
            log_lines = f.readlines()
        log_lines = map(lambda x: x.strip(), log_lines)

        projects_dict = defaultdict(dict)
        for line in log_lines:
            try:
                timestamp, project_path, branch = line.split('\t')
            except ValueError:
                continue
            timestamp = float(timestamp)
            projects_dict[timestamp][project_path] = branch

        return projects_dict


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    if args.init:
        make_app_dirs()
        add_projects()
        # todo: update crontab
        return

    if args.log:
        wt_log = WorkTimeLog()
        wt_log.write_log()
        return

    if args.report:
        wt_log = WorkTimeLog(date=args.date)
        log_data = wt_log.read_log()
        # make and print report
        return

    arg_parser.print_help()

if __name__ == '__main__':
    main()