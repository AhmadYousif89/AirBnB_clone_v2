#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers
"""

import os
from os.path import exists
from fabric.api import put, run, env

env.hosts = ['34.224.62.175', '54.84.8.54']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False

    filename = os.path.basename(archive_path)
    tmp_tar = f"/tmp/{filename}"
    name, _ = os.path.splitext(filename)
    new_folder = f"/data/web_static/releases/{name}"
    try:
        put(archive_path, tmp_tar)
        run(f"mkdir -p {new_folder}")
        run(f"tar -xzf {tmp_tar} -C {new_folder}")
        run(f"rm {tmp_tar}")
        run(f"mv {new_folder}/web_static/* {new_folder}/")
        run(f"rm -rf {new_folder}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {new_folder} /data/web_static/current")
        return True
    except Exception:
        return False
