#!/usr/bin/python3
# Write a Fabric script that generates a .tgz archive
# from the contents of the web_static folder of
# your AirBnB Clone repo, using the function do_pack.

import os
from datetime import datetime
from fabric.api import *

env.user = "ubuntu"
env.hosts = ["34.229.66.190", "100.26.20.236"]
env.key_filename = '~/alx-server-key'
env.port = '22'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns:
        Path to the archive if successful, None otherwise.
    """
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )

    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

    if local(f"tar -cvzf {file} web_static").failed is True:
        return None

    return file


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    Args:
        archive_path: Path to the archive to deploy.
    Returns:
        True if all operations were successful, False otherwise.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    result = run("mv /data/web_static/releases/{}/web_static/* "
                 "/data/web_static/releases/{}/".format(name, name))
    if result.failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
