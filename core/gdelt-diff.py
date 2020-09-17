#! /usr/bin/env python3
import os
import sys
import paf
import argparse
import requests


##################
# Defs and Vars
################

config = {
    'base': '/opt/gdelt-diff',
    'user_config': '/etc/gdelt-diff/config',
    'english': 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt',
    'translation': 'http://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt'
    }


def fresh_install(lang, uc, config):
    '''
    '''
    if uc[lang + '_path'] == '/path/here':
        paf.prWarning('Your Config File Has Not Been Setup for the ' + lang + ' Stream!')
        sys.exit('Edit the File ' + config['config_file'] + ' and Re-Run Your Command!')

    paf.prWorking('Scanning File System...')
    files = paf.basenames(paf.find_files(uc[lang + '_path']))
    files = {"http://data.gdeltproject.org/gdeltv2/" + f for f in files}
    paf.export_iterable(config['base'] + '/prev-' + lang + '.txt', files)
    paf.export_iterable(config['base'] + '/404-' + lang + '.txt', [])


def fetch(url_list, storage_path):
    '''
    '''
    fzf_new = set()
    folders = {str('/' + f[:4] + '/' + f[4:6] + '/') for f in paf.basenames(url_list)}

    for x in folders:
        if not os.path.exists(storage_path + x[-1:]):
            os.makedirs(storage_path + x[-1:])

    for url in paf.progress_bar(url_list, 'Downloading ' + str(len(url_list)) + 'Files'):
        try:
            f = requests.get(url)
        except Exception:
            fzf_new.add(url)
            continue

        fname = paf.basename(url)
        folder = str('/' + f[:4] + '/' + f[4:6] + '/')
        with open(storage_path + folder + fname, 'wb') as csv:
            csv.write(f.content)

    return fzf_new


def retry(lang, config):
    '''
    '''
    fzf_path = config['base'] + '/404-' + lang + '.txt'
    fzf = fetch(paf.read_file(fzf_path))
    paf.export_iterable(fzf_path, fzf)


def gdelt_diff(lang, config):
    '''
    '''
    # Load User Config
    mandatory = ['english_path', 'translation_path']
    optional = []
    uc = paf.read_config(config['user_config'], mandatory, optional)

    # Download Most Recent masterfilelist.txt
    if 'english' == lang:
        dln = requests.get(config['english'])
    elif 'translation' == lang:
        dln = requests.get(config['translation'])

    # Get File, Filter URLs
    status = (lang.upper() + ' Stream Status: ' + str(dln)[1:-1])
    print('-'*len(status))
    paf.prBold(status)
    print('-'*len(status))
    dlc = {''.join(x.split(' ')[2:]) for x in dln.text.split('\n')[:-1]}
    dlp_path = config['base'] + '/prev-' + lang + '.txt'
    fzf_path = config['base'] + '/404-' + lang + '.txt'

    # Run Install If Fresh Run
    if not os.path.exists(dlp_path):
        fresh_install(lang, uc, config)

    # Compare Previous Run
    dlp = paf.read_file(dlp_path)
    diff = set(dlc).difference(dlp)

    # Download Files Into Place
    if diff > 10000:
        if paf.yn_frame(str(len(diff)) + ' Files Are Missing! Do You Still Want to Continue?') is True:
            print('This May Take a While! Starting Download...')
        else:
            sys.exit()
    if diff > 0:
        fzf = fetch(diff, uc[lang + '_path'])
        for x in paf.read_file(fzf_path):
            fzf.add(x)
        paf.export_iterable(fzf_path, fzf)
    else:
        paf.prSucess('All Files Are Up To Date!')


parser = argparse.ArgumentParser(description="This tool is used to automatically maintain a repository of source files for the GDELT Project.")
parser.add_argument("-d", "--diff", action='store_true', help="diff and Download BOTH Gdelt Streams.")
parser.add_argument("-r", "--retry", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in BOTH Streams.")
parser.add_argument("-de", "--diff_english", action='store_true', help="diff and Download the Entire Gdelt English Stream.")
parser.add_argument("-dt", "--diff_translation", action='store_true', help="diff and Download the Entire Gdelt Translation Stream.")
parser.add_argument("-re", "--retry_english", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in English Stream.")
parser.add_argument("-rt", "--retry_translation", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in Translation Stream.")
arguments = parser.parse_args()


if arguments.diff:
    gdelt_diff('english')
    print('')
    gdelt_diff('translation')

elif arguments.diff_english:
    gdelt_diff('english')

elif arguments.diff_translation:
    gdelt_diff('translation')

if arguments.retry:
    gdelt_diff('english')
    print('')
    gdelt_diff('translation')

elif arguments.retry_english:
    retry('english')

elif arguments.retry_translation:
    retry('translation')

else:
    print('Missing Argument! Use --help to See All Arguments.')
