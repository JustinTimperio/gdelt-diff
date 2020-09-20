#! /usr/bin/env python3
import os
import sys
import paf
import argparse
import requests


config = {
    'base': '/opt/gdelt-diff',
    'user_config': '/etc/gdelt-diff/config',
    'english': 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt',
    'translation': 'http://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt'
    }


###################
# Core Functions
#################

def print_stream_status(lang, url):
    status = requests.get(url, stream=True)
    status = (lang.upper() + ' Stream Status: ' + str(status)[1:-1])
    print('-'*len(status))
    paf.prBold(status)
    print('-'*len(status))


def fresh_install(lang, uc, config):
    if uc[lang + '_path'] == '/path/here':
        paf.prWarning('Your Config File Has Not Been Setup for the ' + lang.upper() + ' Stream!')
        sys.exit('Edit the File ' + config['user_config'] + ' and Re-Run Your Command!')

    if not os.path.exists(uc[lang + '_path']):
        os.makedirs(uc[lang + '_path'])

    paf.prWarning('Scanning File System...')
    files = paf.basenames(paf.find_files(uc[lang + '_path']))
    files = {"http://data.gdeltproject.org/gdeltv2/" + f for f in files}
    paf.export_iterable(config['base'] + '/prev-' + lang + '.txt', files)
    paf.export_iterable(config['base'] + '/404-' + lang + '.txt', [])


def fetch(url_list, storage_path):
    fzf_new = set()
    folders = set()
    for f in paf.basenames(url_list):
        if f:
            folders.add(str('/' + f[:4] + '/' + f[4:6]))

    for x in folders:
        if not os.path.exists(storage_path + x):
            os.makedirs(storage_path + x)

    for url in paf.progress_bar(url_list, 'Downloading ' + str(len(url_list)) + ' Files'):
        try:
            f = requests.get(url)
        except Exception:
            fzf_new.add(url)
            continue

        fname = paf.basename(url)
        folder = str('/' + fname[:4] + '/' + fname[4:6] + '/')
        with open(storage_path + folder + fname, 'wb') as csv:
            csv.write(f.content)

    return fzf_new


def retry(lang, uc, config):
    fzf_path = config['base'] + '/404-' + lang + '.txt'
    fzf = fetch(paf.read_file(fzf_path), uc[lang + '_path'])
    paf.export_iterable(fzf_path, fzf)


def gdelt_diff(lang, uc, config):
    dlp_path = config['base'] + '/prev-' + lang + '.txt'
    fzf_path = config['base'] + '/404-' + lang + '.txt'

    # Download and Filter URLs
    url = config[lang]
    print_stream_status(lang, url)
    paf.prBold('Downloading ' + lang.upper() + ' Stream Inventory File...')
    dln = requests.get(url)
    dlc = {''.join(x.split(' ')[2:]) for x in dln.text.split('\n')[:-1]}

    # Filter URL Based On Start Date
    if uc['start_date'] != 'all':
        d = uc['start_date'].split('/')
        days = {dt.replace('-', '') for dt in paf.date_to_today(int(d[0]), int(d[1]), int(d[2]))}
        filtered = set()
        for x in dlc:
            if paf.basename(x)[:8] in days:
                filtered.add(x)
        dlc = filtered

    # Run Install If Fresh Run
    if not os.path.exists(dlp_path):
        fresh_install(lang, uc, config)

    # Compare Previous Run
    dlp = paf.read_file(dlp_path)
    diff = set(dlc).difference(dlp)

    # Download Files Into Place
    if len(diff) > 10000:
        if paf.yn_frame(str(len(diff)) + ' Files Are Missing! Do You Still Want to Continue?') is True:
            print('This May Take a While! Starting Download...')
        else:
            sys.exit()
    if len(diff) > 0:
        fzf = fetch(diff, uc[lang + '_path'])
        paf.export_iterable(dlp_path, dlc)
        for x in paf.read_file(fzf_path):
            fzf.add(x)
        paf.export_iterable(fzf_path, fzf)
    else:
        paf.prSuccess('All Files Are Up To Date!')


####################
# Parse Arguments
##################

parser = argparse.ArgumentParser(description="This tool is used to automatically maintain a repository of source files for the GDELT Project.")
parser.add_argument("-d", "--diff", action='store_true', help="Diff and Download BOTH GDELT Streams.")
parser.add_argument("-r", "--retry", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in BOTH Streams.")
parser.add_argument("-de", "--diff_english", action='store_true', help="Diff and Download the Entire GDELT English Stream.")
parser.add_argument("-dt", "--diff_translation", action='store_true', help="Diff and Download the Entire GDELT Translation Stream.")
parser.add_argument("-re", "--retry_english", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in English Stream.")
parser.add_argument("-rt", "--retry_translation", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in Translation Stream.")
parser.add_argument("-rd", "--refresh_database", action='store_true', help="Update The Database of Synced Files For Both Streams.")
args = parser.parse_args()


######################
# Setup Environment
####################

if paf.am_i_root() is False:
    sys.exit('Critical Error: This Command Must Be Run As Root!')
mandatory = ['english_path', 'translation_path', 'start_date']
optional = []
user_config = paf.read_config(config['user_config'], mandatory, optional)


#################
# Control Flow
###############

if args.diff:
    gdelt_diff('english', user_config, config)
    print('')
    gdelt_diff('translation', user_config, config)

elif args.diff_english:
    gdelt_diff('english', user_config, config)

elif args.diff_translation:
    gdelt_diff('translation', user_config, config)

if args.retry:
    gdelt_diff('english', user_config, config)
    print('')
    gdelt_diff('translation', user_config, config)

elif args.retry_english:
    retry('english', user_config, config)

elif args.retry_translation:
    retry('translation', user_config, config)

if args.refresh_database:
    if os.path.exists(config['base'] + '/prev-english.txt'):
        fresh_install('english', user_config, config)
        print('Updated English Database!')
    if os.path.exists(config['base'] + '/prev-translation.txt'):
        fresh_install('translation', user_config, config)
        print('Updated Translation Database!')
