#! /usr/bin/env python3
import os
from .file import read_file


def distro_name():
    '''
    Returns distrbution information from /etc/os-release.
    '''
    release = read_file('/etc/os-release')
    version = 'none'

    for line in release:
        if line.startswith('ID='):
            name = line[3:].replace('"', '')
        elif line.startswith('VERSION_ID='):
            version = line[11:].replace('"', '')

    return (name, version)


############
# Linux System Package Commands
######

def pacman(package, arg='-S'):
    os.system("sudo pacman " + arg + " " + package)


def yum(package, arg='install'):
    os.system("sudo yum " + arg + " " + package)


def apt(package, arg='install'):
    os.system("sudo apt-get " + arg + " " + package)


def zypper(package, arg='install'):
    os.system("sudo zypper " + arg + " " + package)


def pip_install(packages, arg='install'):
    os.system("sudo pip " + arg + " " + packages)


def yay_install(packages, arg='-S'):
    os.system("yay " + arg + packages)
