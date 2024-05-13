#!/usr/bin/python3
"""
Deletes out-of-date archives
fab -f 100-clean_web_static.py do_clean:number=2
    -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import run, cd, lcd, local, env

env.hosts = ['54.84.8.54', '34.224.62.175']


def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number (int): The number of archives to keep.
    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)
    archives_path = "versions"
    archives = sorted(os.listdir(archives_path))
    [archives.pop() for i in range(number)]
    with lcd(archives_path):
        [local(f"rm ./{archive}") for archive in archives]

    releases_path = "/data/web_static/releases"
    with cd(releases_path):
        archives = run("ls -tr").split()
        archives = [archive for archive in archives if "web_static_" in archive]
        [archives.pop() for i in range(number)]
        [run(f"rm -rf ./{archive}") for archive in archives]
