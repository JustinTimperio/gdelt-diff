#! /usr/bin/env python3
import os


#######################
# Native Loading Bar
#####################

def progress_bar(iterable, prefix='Progress', suffix='Complete', fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
        iteration   - Required  : current iteration (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    decimals = 1
    length = os.get_terminal_size()[0] - (len(prefix) + len(suffix) + 15)

    # Progress Bar Printing Function
    def print_bar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    # Initial Call
    print_bar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        print_bar(i + 1)
    # Print New Line on Complete
    print()


###############################
# Application Print Commands
#############################

def prError(text):
    print("\u001b[31;1m{}\033[00m" .format(text))

def prSuccess(text):
    print("\u001b[32;1m{}\033[00m" .format(text))

def prWarning(text):
    print("\u001b[33;1m{}\033[0m" .format(text))

def prBold(text):
    print("\u001b[37;1m{}\u001b[0m" .format(text))

def prChanged(text):
    print("\u001b[35m{}\033[00m" .format(text))

def prRemoved(text):
    print("\033[31m{}\033[00m" .format(text))

def prAdded(text):
    print("\033[94m{}\033[00m" .format(text))
