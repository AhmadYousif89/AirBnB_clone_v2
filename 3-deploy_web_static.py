#!/usr/bin/python3
"""
Fabric script that creates and uploads an archive to the web servers
execute: fab -f 2-do_deploy_web_static.py -i <ssh_key>
"""

from os.path import exists
from datetime import datetime
from fabric.api import env, local, put, run

env.user = 'ubuntu'
env.hosts = ['34.224.62.175', '54.84.8.54']


def do_pack():
    """making an archive on web_static folder"""
    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S")
    archive_name = f'web_static_{timestamp}.tgz'
    try:
        local('mkdir -p versions')
        local(f'tar -cvzf versions/{archive_name} web_static')
        return archive_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Uploads an archive to the web servers"""
    archive_fullpath = f'versions/{archive_path}'
    if not exists(archive_fullpath):
        return False

    archive_name = archive_path.split('.')[0]  # web_static_20240505004540
    archive_tmp_path = f"/tmp/{archive_path}"
    release_path = f"/data/web_static/releases/{archive_name}"

    try:
        put(archive_fullpath, archive_tmp_path)
        run(f"mkdir -p {release_path}")
        unpack_archive = f'\
            tar -xzf {archive_tmp_path} -C {release_path} --strip-components=1'
        run(unpack_archive)
        run(f"rm {archive_tmp_path}")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -sf {release_path} /data/web_static/current")
        return True
    except Exception:
        return False


def deploy():
    """creates and deploy a new web_static release to the web servers"""
    archive_path = do_pack()  # web_static_20240505004540.tgz
    if archive_path is None:
        return False
    return do_deploy(archive_path)
