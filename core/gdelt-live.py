import io
import os
import paf
import zipfile
import requests
import argparse


def gdelt_live(lang):
    last_eng = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'
    last_trans = 'http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt'
    old_fetch = '/tmp/gdelt-live/prev-' + lang + '.txt'
    dl_path = '/tmp/gdelt-live/' + lang

    # Downloading Most Recent File List
    if 'english' == lang:
        dl = requests.get(last_eng)
    elif 'translation' == lang:
        dl = requests.get(last_trans)

    # Get File and Filter URLs
    status = (lang.upper() + ' Stream Status: ' + str(dl)[1:-1])
    print('-'*len(status))
    paf.prBold(status)
    print('-'*len(status))
    urls = {''.join(x.split(' ')[2:]) for x in dl.text.split('\n')[:-1]}

    # Compare and Diff
    if os.path.exists(old_fetch):
        old = paf.read_file(old_fetch, 'set')
        new = set(urls.difference(old))
        rm = set(old.difference(urls))

        if len(new) == 0:
            paf.prSuccess(lang.upper() + ' Live Files are Already Up-to-Date!')
            return
        else:
            # Remove Old Files
            for x in rm:
                os.remove(dl_path + '/' + ''.join(x.split('/')[-1][:-4]))

    else:
        # Setup If First Run
        if not os.path.exists(dl_path):
            os.makedirs(dl_path)
        new = urls

    # Download URLs
    for url in new:
        try:
            print('Downloading: ' + ''.join(url.split('/')[-1]))
            resp = requests.get(url)
            print('Decompressing: ' + ''.join(url.split('/')[-1]))
            with zipfile.ZipFile(io.BytesIO(resp.content), 'r') as csvzip:
                csvzip.extractall(dl_path)

        except Exception:
            print("404: " + url)

    # Export Final Results
    paf.export_iterable(old_fetch, urls)


####################
# Argument Parser
##################

parser = argparse.ArgumentParser(description="Fetch the Most Recent Files in the Gdelt into /tmp/gdelt-live. Without an Argument this Script Fetchs Both the English and Translation Stream.")
parser.add_argument("-t", "--translation", action='store_true', help="Download Only the Most Recent Files in the Translation Stream.")
parser.add_argument("-e", "--english", action='store_true', help="Download Only the Most Recent Files in the English Stream.")
arguments = parser.parse_args()

if arguments.translation:
    gdelt_live('translation')
elif arguments.english:
    gdelt_live('english')
else:
    gdelt_live('english')
    print('')
    gdelt_live('translation')
