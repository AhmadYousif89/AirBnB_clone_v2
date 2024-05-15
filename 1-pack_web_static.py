#!/usr/bin/python3
"""
Fabric script to genereate tgz archive
Usage: fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """Creates a new archive of the web_static folder"""
    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S")
    src_folder = 'web_static'
    dest_folder = 'versions'
    archive_name = f'{src_folder}_{timestamp}.tgz'
    save_path = f'{dest_folder}/{archive_name}'
    try:
        local(f'mkdir -p {dest_folder}')
        local(f'tar -cvzf {save_path} {src_folder}')
        return archive_name
    except Exception:
        return None
