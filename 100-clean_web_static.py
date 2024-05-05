#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.user = "ubuntu"
env.hosts = ["34.229.66.190", "100.26.20.236"]
env.key_filename = '~/alx-server-key'


def do_clean(number=0):
    """
    Deletes out-of-date archives.
    
    Args:
        number: The number of archives to keep (including the most recent).
                Defaults to 0, which keeps only the most recent archive.
    """
    try:
        number = int(number)
    except ValueError:
        print("Please provide a valid number.")
        return

    if number < 0:
        print("Number must be a positive integer.")
        return

    # Local cleanup
    with lcd("versions"):
        local_archives = local("ls -t", capture=True).split("\n")
        if len(local_archives) > number:
            local("rm -f {}".format(" ".join(local_archives[number:])))

    # Remote cleanup
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -t").split("\n")
        if len(remote_archives) > number:
            run("rm -rf {}".format(" ".join(remote_archives[number:])))
