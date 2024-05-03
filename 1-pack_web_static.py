#!/usr/bin/python3
"""
Fabric script to genereate tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""
from fabric import task
from datetime import datetime


@task
def do_pack(c):
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        # Get the current date and time
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the versions folder if it doesn't exist
        c.run("mkdir -p versions")

        # Generate the archive file name
        archive_name = "web_static_{}.tgz".format(timestamp)

        # Create the .tgz archive from the web_static folder
        c.run("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the path to the archive if it's generated successfully
        return "versions/{}".format(archive_name)

    except Exception as e:
        print(e)
        return None
