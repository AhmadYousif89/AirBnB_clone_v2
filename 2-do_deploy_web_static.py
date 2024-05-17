#!/usr/bin/python3
"""
Fabric script that uploads an archive to the web servers
execute:
    fab -f 2-do_deploy_web_static.py do_pack:archive_path=<path> -i <ssh_key>
"""

import os
from fabric.api import put, run, env

env.user = 'ubuntu'
env.hosts = ['34.224.62.175', '54.157.181.100']


def do_deploy(archive_path):
    """Uploads an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    archive_fullname = archive_path.split('/')[-1]
    archive_tmp_path = f"/tmp/{archive_fullname}"
    archive_name = archive_fullname.split('.')[0]
    release_path = f"/data/web_static/releases/{archive_name}"

    try:
        put(archive_path, archive_tmp_path)
        # ex: /data/web_static/releases/web_static_20240505004540
        run(f"mkdir -p {release_path}")
        unpack = f'\
            tar -xzf {archive_tmp_path} -C {release_path} --strip-components=1'
        run(unpack)
        run(f"rm {archive_tmp_path}")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -sf {release_path} /data/web_static/current")
        return True
    except Exception:
        return False
