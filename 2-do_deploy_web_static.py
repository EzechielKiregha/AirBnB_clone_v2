#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import *
from fabric.contrib.files import sed

# env.user = "ubuntu"
env.hosts = ["34.229.66.190", "100.26.20.236"]
# env.key_filename = '~/alx-server-key'
# env.port = '22'


@task
def resetup_ssh():
    """
    Resetup SSH on the server to allow password authentication and root login.

    Returns:
        True if the SSH resetup was successful, False otherwise.
    """
    # Install openssh-server if not already installed
    result = sudo('apt-get update && apt-get install -y openssh-server')
    if result.failed:
        return False

    # Backup existing sshd_config
    result = sudo('cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak')
    if result.failed:
        return False

    # Update sshd_config to allow password authentication and root login
    result = sudo('sed -i.bak -r -e \'s/PasswordAuthentication '
                  'no/PasswordAuthentication yes/g\' '
                  '"$(echo /etc/ssh/sshd_config)"')
    if result.failed:
        return False
    result = sudo('sed -i.bak -r -e \'s/PermitRootLogin '
                  'no/PermitRootLogin yes/g\' '
                  '"$(echo /etc/ssh/sshd_config)"')
    if result.failed:
        return False

    # Restart ssh service
    result = sudo('systemctl restart sshd')
    if result.failed:
        return False

    return True


@task
def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    Args:
        archive_path: Path to the archive to deploy.
    Returns:
        True if all operations were successful, False otherwise.
    """
    if resetup_ssh():
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
    else:
        return False
