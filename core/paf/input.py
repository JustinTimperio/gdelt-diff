#! /usr/bin/env python3
import re


def yn_frame(prompt):
    '''
    Generic Y/N input frame. Returns True for Yes, False for No.
    User can input `exit` or `quit` to return False.
    '''
    while True:
        yn = input('\033[1m' + prompt + ' (y/n):' + '\033[0m')
        if yn.lower().strip() in ['y', 'yes']:
            return True
        elif yn.lower().strip() in ['no', 'n']:
            return False
        elif yn.lower().strip() in ['quit', 'exit']:
            return None
        else:
            print('Please Respond With Yes/No! (`exit` or `quit` to Return)')


def multi_choice_frame(options):
    '''
    Lets a user select between arbitrary number of input selections.
    Returns value the user selects.
    User can input `exit` or `quit` to return False.
    '''
    c_list = list(options)
    counter = 1
    while True:
        for o in c_list:
            print('(' + str(counter) + ') ' + o)
            counter += 1
        ans = input('\033[1m' + 'Enter Your Selection With an INT: ' + '\033[0m').strip()

        if re.findall(r'^([1-9]|0[1-9]|[1-9][0-9]|[1-9][1-9][0-9])$', ans) and int(ans) < counter:
            return c_list[int(ans) - 1]
        elif ans.lower() == 'quit' or ans.lower() == 'exit':
            return None
        else:
            counter = 1
            print('Invalid: Please Select a Validate Integer! (`exit` or `quit` to Return)')
