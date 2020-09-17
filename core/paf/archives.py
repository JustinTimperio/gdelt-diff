#! /usr/bin/env python3
import os
import gzip
import shutil
import tarfile
from .file import find_files


############
# Core Archive Functions
######

def gz_c(path, rm=False):
    with open(path, 'rb') as f:
        with gzip.open(path + '.gz', 'wb') as gz:
            shutil.copyfileobj(f, gz)
    if rm is True:
        os.remove(path)
    elif rm is False:
        pass


def gz_d(path, rm=False):
    with gzip.open(path, 'rb') as gz:
        with open(path[:-3], 'wb') as f:
            shutil.copyfileobj(gz, f)
    if rm is True:
        os.remove(path)
    elif rm is False:
        pass


def tar_dir(path, rm=False):
    with tarfile.open(path + '.tar', 'w') as tar:
        for f in find_files(path):
            tar.add(f, f[len(path):])
    if rm is True:
        shutil.rmtree(path)
    elif rm is False:
        pass


def untar_dir(path, rm=False):
    with tarfile.open(path, 'r:') as tar:
        tar.extractall(path[:-4])
    if rm is True:
        os.remove(path)
    elif rm is False:
        pass
