#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to the web servers
"""

from datetime import datetime
from os.path import exists, isdir
from fabric.api import env, local, put, run

env.hosts = ['34.224.62.175', '54.84.8.54']


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {file_name} web_static")
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run(f'mkdir -p {path}{no_ext}/')
        run(f'tar -xzf /tmp/{file_n} -C {path}{ no_ext}/')
        run(f'rm /tmp/{file_n}')
        run(f'mv {path}{ no_ext}/web_static/* {path}{ no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
