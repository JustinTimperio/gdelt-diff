#! /usr/bin/env python3
import re
import os
import sys
from .file import read_file


############
# Linux System Commands
######

def am_i_root():
    '''
    Checks if python was run with sudo or as root.
    Returns True if root and False if userspace.
    '''
    if os.getuid() == 0:
        return True
    else:
        return False


def list_normal_users():
    '''
    Get info about every normal users.
    '''
    usr_list = set()

    for x in read_file('/etc/login.defs'):
        if x.startswith('UID_MIN'):
            min_uid = int(x.split('\t')[-1].strip())
        if x.startswith('UID_MAX'):
            max_uid = int(x.split('\t')[-1].strip())
    usr_range = range(min_uid, max_uid + 1)

    for x in read_file('/etc/passwd'):
        entry = tuple(x.split(':'))
        if int(entry[2]) in usr_range:
            usr_list.add(entry)

    return usr_list


############
# File System Commands
######

def rm_file(file_path, sudo):
    '''
    Uses os.system() to remove files using standard *nix commands.
    The main advatage over os submodule is support for sudo.
    '''
    if sudo is True:
        if os.path.exists(file_path):
            os.system('sudo rm ' + file_path)
    elif sudo is False:
        if os.path.exists(file_path):
            os.system('rm ' + file_path)
    else:
        sys.exit('Error: Sudo Must be True/False!')


def mk_dir(dir_path, sudo):
    '''
    Uses os.system() to make a directory using standard *nix commands.
    The main advatage over os submodule is support for sudo.
    '''
    if sudo is True:
        if not os.path.exists(dir_path):
            os.system("sudo mkdir " + dir_path)
    elif sudo is False:
        if not os.path.exists(dir_path):
            os.system("mkdir " + dir_path)
    else:
        sys.exit('Error: Sudo Must be True/False!')


def rm_dir(dir_path, sudo):
    '''
    Uses os.system() to remove a directory using standard *nix commands.
    The main advatage over os submodule is support for sudo.
    '''
    if sudo is True:
        if os.path.exists(dir_path):
            os.system('sudo rm -r ' + dir_path)
    elif sudo is False:
        if os.path.exists(dir_path):
            os.system('rm -r ' + dir_path)
    else:
        sys.exit('Error: Sudo Must be True/False!')


def basename(path):
    '''
    Provides faster file name trim than os.basename()
    '''
    return path.split('/')[-1]


def basenames(file_list):
    '''
    Returns a list of unique file names. Will remove duplicates names.
    Provides faster file name trim than looping with os.basename()
    '''
    return {p.split('/')[-1] for p in file_list}


############
# Terminal
######

def escape_bash_input(astr):
    '''
    Uses regex subsitution to safely escape bash input.
    '''
    return re.sub("(!| |\$|#|&|\"|\'|\(|\)|\||<|>|`|\\\|;)", r"\\\1", astr)


def sed_uncomment_line(pattern, file_path, sudo):
    '''
    Uncomments lines using sed. This can safely be run over a file multiple
    times without adverse effects. This is ungodly helpful when modifing
    linux config files.
    '''
    if sudo is True:
        os.system("sudo sed -e'/" + pattern + "/s/^#//g' -i " + file_path)
    elif sudo is False:
        os.system("sed -e'/" + pattern + "/s/^#//g' -i " + file_path)
    else:
        sys.exit('Error: Sudo Must be True/False!')


def sed_comment_line(pattern, file_path, sudo):
    '''
    Comments lines using sed. This can safely be run over a file multiple
    times without adverse effects. This is ungodly helpful when modifing
    linux config files.
    '''
    if sudo is True:
        os.system("sudo sed -e'/" + pattern + "/s/^#*/#/g' -i " + file_path)
    elif sudo is False:
        os.system("sed -e'/" + pattern + "/s/^#*/#/g' -i " + file_path)
    else:
        sys.exit('Error: Sudo Must be True/False!')


############
# File and Folder Permissions
######

def get_permissions(basedir, typ):
    '''
    For some reason python has no simple inbuilt way to get file or folder permissions
    without changing the permission. This is gross but it works.
    Returns set of tuples in format (dir_path, permissions, owner, group)
    '''
    temp_file = '/tmp/get_perms.txt'

    # Fetch Folder Permissions
    if typ == 'files':
        os.system('find ' + escape_bash_input(basedir) + ' -type f -exec ls -d -l */ {} + > ' + temp_file)
    elif typ == 'folders':
        os.system('find ' + escape_bash_input(basedir) + ' -type d -exec ls -d -l */ {} + > ' + temp_file)
    else:
        sys.exit('Error: Type Must Be `Files` or `Folders`!')

    raw_perms = read_file(temp_file)
    rm_file(temp_file, sudo=False)

    # Parse Perms
    perms = set()
    for x in raw_perms:
        s = x.split(' ')
        s = ' '.join([x for x in s if x != '']).split(' ', 8)
        s = (s[8].replace("'", "").strip(), s[0].strip(), s[2].strip(), s[3].strip())
        if s[0].startswith('/'):
            perms.add(s)

    return perms


def perm_to_num(symbolic):
    '''
    Convert symbolic permission notation to numeric notation.
    '''
    perms = {
            '---': '0',
            '--x': '1',
            '-w-': '2',
            '-wx': '3',
            'r--': '4',
            'r-x': '5',
            'rw-': '6',
            'rwx': '7'
        }

    # Trim Lead If It Exists
    if len(symbolic) == 10:
        symbolic = symbolic[1:]

    # Parse Symbolic to Numeric
    x = (symbolic[:-6], symbolic[3:-3], symbolic[6:])
    numeric = perms[x[0]] + perms[x[1]] + perms[x[2]]
    return numeric
