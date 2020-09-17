#! /usr/bin/env python3
import os
import re
import math
import datetime as dt


############
# Assorted Functions
######

def replace_spaces(lst, replacement='-'):
    '''
    Replaces spaces with the defined replacement string
    for every occurance and every string in a list.
    '''
    return {s.strip().replace(' ', replacement) for s in lst}


def date_to_today(year, month, day):
    '''
    Returns a list of dates between input date and today.
    '''
    start_date = dt.date(year, month, day)
    end_date = dt.date.today() - dt.timedelta(days=1)
    delta = abs((start_date - dt.date.today()).days)
    date_list = [str(end_date - dt.timedelta(days=x)) for x in range(0, delta)]
    return date_list


def max_threads(thread_target):
    '''
    Returns the max number of threads availble for a target process.
    '''
    cores = os.cpu_count()
    if cores >= thread_target:
        return thread_target
    else:
        return cores


def convert_size(size_bytes):
    '''
    Convert raw byte value into human readable format.
    '''
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, i)
    size = round(size_bytes / power, 2)
    return "{} {}".format(size, size_name[i])


def read_between(start, end, iterable, re_flag=False):
    '''
    Returns list of lines found between two strings/values.
    If re_flag is False, direct string comparison will be used.
    If re_flag is True, regex will be used to find start and end strings.
    '''
    lines = list()
    flag = None

    if re_flag is False:
        for line in iterable:
            if line is start:
                flag = True
            elif line is end:
                flag = False
            elif flag is None or flag is False:
                pass
            elif flag is True:
                lines.append(line)
        return lines

    elif re_flag is True:
        for line in iterable:
            if re.findall(re.escape(start.lower()), line.lower()):
                flag = True
            elif re.findall(re.escape(end.lower()), line.lower()):
                flag = False
            elif flag is None or flag is False:
                pass
            elif flag is True:
                lines.append(line)
        return lines
