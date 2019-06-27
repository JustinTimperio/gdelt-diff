#### Keep a copy of the most recent gdelt source files in /tmp)
## This script requires: gnu parallel, linux unzip, gnu gzip, pip wget, pip requests 
import requests, re, shutil, wget, os, sys, argparse
###############

def install_gdelt_live():
    from global_defuns import pacman_install
    from global_defuns import pip_install
    pacman_install('parallel unzip gzip')
    pip_install('wget requests shutil re argparse')

def gdelt_live(lang):
    ## downloading most recent file list
    if 'english' in lang:
        dln = requests.get('http://data.gdeltproject.org/gdeltv2/lastupdate.txt')
    else:
        dln = requests.get('http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt')
    print(lang.upper() + ' Stream Status:', dln)
    ## sorting out urls from list
    rx = re.compile("http*")
    dln = list(filter(rx.match,(dln.text.split())))

    def compare_previous():
        dlp = list(open('/tmp/gdelt-live/previous-' + lang + '.txt').read().splitlines()) 
        dif = set(dln).difference(dlp)
        if len(dif) > 1:
            fetch()
        else: print(lang.upper() + ' Live Files are Already Up-to-Date!')

    def fetch():
        ## downloading and cleaning dir for new files
        if os.path.exists('/tmp/gdelt-live/' + lang + '-dl'):
            shutil.rmtree('/tmp/gdelt-live/' + lang + '-dl')
        os.makedirs('/tmp/gdelt-live/' + lang + '-dl')
        for url in dln:
            try: wget.download(url, '/tmp/gdelt-live/' + lang + '-dl')
            except: print("URL 404\'d : " + url)
        print('\nDecompressing...')
        os.system('cd /tmp/gdelt-live/' + lang + '-dl && find . -iname "*.zip" | parallel unzip && find . -iname "*.zip" -delete')
        if os.path.exists('/tmp/gdelt-live/previous-' + lang + '.txt'):
            os.remove('/tmp/gdelt-live/previous-' + lang + '.txt')
        with open('/tmp/gdelt-live/previous-' + lang + '.txt', 'w') as f:
            for url in dln:
                f.write("%s\n" % url)
        print(lang.upper() + ' Live Update Complete!')

    if not os.path.exists('/tmp/gdelt-live'):
        os.makedirs('/tmp/gdelt-live')
    if os.path.exists('/tmp/gdelt-live/previous-' + lang + '.txt'):
        compare_previous()
    else: fetch()

###############

parser = argparse.ArgumentParser(description="Fetch the Most Recent Files in the Gdelt into /tmp/gdelt-live. Without an Argument this Script Fetchs Both the English and Translation Stream.")
parser.add_argument("-t", "--translation", action='store_true', help="Download Only the Most Recent Files in the Translation Stream.")
parser.add_argument("-e", "--english", action='store_true', help="Download Only the Most Recent Files in the English Stream.")
parser.add_argument("-i", "--install", action='store_true', help="Install All Packages and Tools Needed for gdelt_live.py")
arguments = parser.parse_args()

if arguments.install:
    install_gdelt_live()
elif arguments.translation:
    gdelt_live('translation') 
elif arguments.english:
    gdelt_live('english') 
else:
    gdelt_live('english')
    print('-----------------------')
    gdelt_live('translation')
