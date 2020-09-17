#! /usr/bin/env python3
import os
import sys
import hashlib
import multiprocessing


############
# File System Commands
######


def scan_dir(path):
    '''
    Non-recursively return a tuple of files and directories in a path.
    '''
    dirs = set()
    files = set()
    for x in os.scandir(path):
        if x.is_dir():
            dirs.add(x.path)
        elif x.is_file():
            files.add(x.path)

    return(files, dirs)


def find_subdirs(path):
    '''
    Recursively return a list of directories in a path(s).
    This seems to be the fastest implementation possible.
    '''
    # Allow For Single Path or Multiple
    if type(path) is str:
        paths = set()
        paths.add(path)
    elif type(path) is set or list:
        paths = path
    else:
        sys.exit('Error: Invalid Path Input!')

    subfolders = set()
    for x in paths:
        for f in os.scandir(path):
            if f.is_dir():
                subfolders.add(f.path)

    for path in set(subfolders):
        subfolders.update(find_subdirs(path))

    return subfolders


def find_files(path):
    '''
    Scans a path(s) recursivly and return a list of files.
    This seems to be the fastest implementation possible.
    '''
    # Allow For Single Path or Multiple
    if type(path) is str:
        paths = set()
        paths.add(path)
    elif type(path) is set or list:
        paths = path
    else:
        sys.exit('Error: Invalid Path Input!')

    files = set()
    dirs = set()

    for x in paths:
        z = scan_dir(x)
        files.update(z[0])
        dirs.update(z[1])

    for d in set(dirs):
        files.update(find_files(d))

    return files


def size_of_files(file_list):
    '''
    Returns byte sum of files in a list.
    '''
    size = 0
    for f in file_list:
        try:
            size += os.path.getsize(f)
        except Exception:
            OSError

    return size


############
# File Commands
######


def export_iterable(file_path, iterable):
    '''
    Export iterable to a file with each entry on a new line.
    '''
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'w') as f:
        for i in iterable:
            f.write("%s\n" % i)


def read_file(file_path, typ='list'):
    '''
    Reads file into set or list.
    '''
    if typ.lower() == 'list':
        fl = list(open(file_path).read().splitlines())
    elif typ.lower() == 'set':
        fl = set(open(file_path).read().splitlines())
    else:
        sys.exit('Error: Type Must be List/Set!')

    return fl


############
# Checksum Functions
######


def checksum_file(file_path):
    '''
    Checksums a file using hashlib.md5(). Reads the file in 250MB chunks.
    Checksum is slow as fuck on anything larger than 5GB so they are ignored.
    Returns a tuple with tuple[0] == path and tuple[1] == checksum.
    '''
    if not os.path.exists(file_path):
        return (file_path, 'MISSING!')
    else:
        try:
            size = os.path.getsize(file_path)
        except Exception:
            return (file_path, 'UNREADABLE!')

    if size == 0:
        return (file_path, '0')

    elif size > 5368709120:
        return (file_path, 'TOO LARGE!')

    else:
        with open(file_path, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(268435456)
                if not data:
                    break
                m.update(data)
            return (file_path, str(m.hexdigest()))


def checksum_files(paths, threads=os.cpu_count()):
    '''
    Checksum all files in paths using mp.pool then return results.
    Returns a set of tuples with paths and checksums.
    '''
    with multiprocessing.Pool(threads) as pool:
        sums = (pool.imap(checksum_file, paths))

    return sums
