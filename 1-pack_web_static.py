#!/usr/bin/python3
# Write a Fabric script that generates a .tgz archive
# from the contents of the web_static folder of
# your AirBnB Clone repo, using the function do_pack.

import os
from datetime import datetime
from fabric.api import local


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
