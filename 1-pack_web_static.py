#!/usr/bin/python3
"""
Fabric script to genereate tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """Creates a new archive of the web_static folder"""
    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S")
    archive_name = f'web_static_{timestamp}.tgz'
    try:
        local('mkdir -p versions')
        local(f'tar -cvzf versions/{archive_name} web_static')
        return archive_name
    except Exception:
        return None
