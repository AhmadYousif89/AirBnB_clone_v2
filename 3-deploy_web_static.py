#!/usr/bin/python3
"""
Fabric script that creates and uploads an archive to the web servers
Usage: fab -f 3-deploy_web_static.py deploy -i ssh_private_key
"""

from datetime import datetime
from os.path import exists, join
from fabric.api import env, local, put, run, runs_once

env.user = 'ubuntu'
env.hosts = ['34.224.62.175', '54.157.181.100']

src_folder = 'web_static'
dest_folder = 'versions'


@runs_once
def do_pack():
    """making an archive on web_static folder"""
    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S")
    archive_name = f'{src_folder}_{timestamp}.tgz'
    save_path = join(dest_folder, archive_name)
    try:
        local(f'mkdir -p {dest_folder}')
        local(f'tar -cvzf {save_path} {src_folder}')
        return archive_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Uploads an archive to the web servers"""
    archive_fullpath = f'{dest_folder}/{archive_path}'
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
        print("Failed to create the archive")
        return False
    return do_deploy(archive_path)
