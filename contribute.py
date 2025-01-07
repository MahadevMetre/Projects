#!/usr/bin/env python
import argparse
import os
from datetime import datetime, timedelta
from random import randint, choice
from subprocess import Popen
import sys


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    start_date = datetime(2022, 6, 3)
    end_date = datetime(2025, 1, 7)
    directory = "repository-" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email

    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]

    os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])

    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    # Simulate contributions
    for day in date_range(start_date, end_date):
        if should_contribute():
            num_commits = randint(0, 5)
            for _ in range(num_commits):
                commit_time = day + timedelta(hours=randint(9, 17), minutes=randint(0, 59))
                contribute(commit_time)

    if repository is not None:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation ' +
          '\x1b[6;30;42mcompleted successfully\x1b[0m!')


def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    Popen(commands).wait()


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def date_range(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)


def should_contribute():
    # Skip some days to simulate a real contributor
    return choice([True] * 7 + [False] * 3)


def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="""A link to an empty non-initialized remote git
                        repository. If specified, the script pushes the changes
                        to the repository. The link is accepted in SSH or HTTPS
                        format. For example: git@github.com:user/repo.git or
                        https://github.com/user/repo.git""")
    parser.add_argument('-un', '--user_name', type=str, required=False,
                        help="""Overrides user.name git config.
                        If not specified, the global config is used.""")
    parser.add_argument('-ue', '--user_email', type=str, required=False,
                        help="""Overrides user.email git config.
                        If not specified, the global config is used.""")
    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()
