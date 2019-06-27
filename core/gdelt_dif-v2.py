#### Download, convert, and sort gdelt source files automatically
## This script requires: gnu rsync, gnu parallel, linux unzip, gnu gzip, linux touch, python wget, python requests 
import requests, re, shutil, wget, argparse
from global_defuns import *

###############
## Defs and Vars
###########
base_dir = '/var/app/gdelt-dif'
ram_dir = '/tmp/gdelt-dif'

def load_from_disk(file_path):
    if not os.path.exists(file_path): 
        try: shutil.copyfile(base_dir + str(file_path)[4:], file_path) 
        except IOError: sys.exit('Critical Error Restoring ' + file_path + ' from the disk!')

##############
def gdelt_dif(lang, fzf_force=False):
###########
### Install dependinces and build app
########
    def install_packages():
        pacman_install('rsync parallel unzip gzip')
        pip_install('wget requests')
        os.system('sudo cp ' + base_dir + '/core/daemons/* /etc/systemd/system/')
        os.system('sudo systemctl daemon-reload && sudo systemctl enable gdelt-dif.timer gdelt-live.timer')

    def fresh_install():
        homedir = input('Enter the FULL Path of the Existing ' + lang.upper() + ' Gdelt Repo (IE:/mnt/lt-mem/gdelt-v2/' + lang + '-stream):') 
        mkdir(base_dir, 'u')
        ## export path for stream
        with open(base_dir + '/path-' + lang + '.txt', 'w') as f:
            f.write(homedir)
        mkdir(base_dir + '/' + lang + '-dl', 'u')
        touch(base_dir + '/404-' + lang + '.txt', 'u')
        ## search file system
        print('Searching Through File System...')
        fs = {os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(homedir)) for f in fn} 
        fs = {path.replace(homedir,'') for path in fs}
        fs = {path[9:-2] for path in fs}
        fs = {"http://data.gdeltproject.org/gdeltv2/" + path + "zip" for path in fs}
        export_list(base_dir + '/master-' + lang + '-previous.txt', fs) 

    ## wait for user input if /var/tmp/gdelt-dif is missing
    if not os.path.exists(base_dir + '/' + lang + '-dl'):
        fresh = input('Persistence Files for ' + lang.upper() + ' are Missing! Do You Want to Perform a Fresh Install? (y/n):')
        if fresh.lower() in ['y','yes']: 
            fresh_install()
            print('Starting Fresh Install....')
        else:
            return

#############
### Start Core Dif Process
#########
    ## restore all files to /tmp if missing
    mkdir(ram_dir, 'u')
    mkdir(ram_dir + '/' + lang + '-dl', 'u')
    load_from_disk(ram_dir + '/master-' + lang + '-previous.txt')
    load_from_disk(ram_dir + '/404-' + lang + '.txt')
    load_from_disk(ram_dir + '/path-' + lang + '.txt')
    ## download most recent masterfilelist.txt
    ltmem = open(ram_dir + '/path-' + lang + '.txt').read()
    if lang in 'english': 
        dln = requests.get('http://data.gdeltproject.org/gdeltv2/masterfilelist.txt')
    else: 
        dln = requests.get('http://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt')
    print(lang.upper() + ' Stream Status:', dln)
    ## remove junk strings from list
    rxhttp = re.compile("http*")
    dln = list(filter(rxhttp.match,(dln.text.split())))
    ## compare to previous dif
    dlp = read_list(ram_dir + '/master-' + lang + '-previous.txt') 
    dif = set(dln).difference(dlp)

#############
### Download Gdelt Files
#########
    def fetch():
        fzfnew = set()
        ## main download function
        for url in dif:
            try: wget.download(url,fetch_path) ## Download File URL
            except: fzfnew.add(url) ## Or add to the 404 list on any error
        export_list('/tmp/gdelt-dif/master-' + lang + '-previous.txt', dln)
        export_list(base_dir + '/master-' + lang + '-previous.txt', dln)
        #####
        if fzf_force == True or len(fzfnew) >= 1:
            ## retry any 404's 
            print('\nRetrying Previous 404\'s...') 
            fzfold = read_list('/tmp/gdelt-dif/404-' + lang + '.txt')
            fzf = fzfold|fzfnew ## combine any old 404's with any new 404's
            for url in fzf:
                try: wget.download(url,fetch_path)
                except: fzfnew.add(url)
            print(len(fzfnew),'Total Files 404\'d')
            export_list('/tmp/gdelt-dif/404-' + lang + '.txt', fzfnew) 
            export_list(base_dir + '/404-' + lang + '.txt', fzfnew) 
            
#############
### Convert Gdelt Source Files from .zip to .gz
#########
    def convert():
        print('\nUnzipping Files...')
        try: os.system('cd ' + fetch_path + ' && parallel unzip -qq ::: * && find . -iname "*.zip" -delete')
        except: print('Unable to Decompress Files!') 
        print('Compressing Files to .gz...')
        try: os.system('cd ' + fetch_path + ' && parallel gzip ::: *')
        except: print('Unable to Compress Files!') 

#############
## Sort Download Source Files into Folders
#########
    def sort():
        dlfs = {os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(fetch_path)) for f in fn} 
        if len(dlfs) == 0:
            return  ## exit function if no files are found
        if lang in 'translation':
            offset = 12
        else: offset = 0
        gkgs = set()
        for url in dif:
            if len(url) == 63 + offset:
                gkgs.add(url)
        ## make year dirs
        years = {"/" + path[37:-22 - offset] for path in gkgs}
        for year in years:
            if not os.path.exists(ltmem + year):
                os.makedirs(ltmem + year)
        ## make month dirs
        months = {"/" + path[37:-22 - offset] + "/" + path[41:-20 - offset] for path in gkgs} 
        for month in months:
            if not os.path.exists(str(ltmem) + month):
                os.makedirs(str(ltmem) + month)
        ## move files to ltmem
        print("Moving Files...")
        for fil in dlfs:
            if len(fil) == len(fetch_path) + 26 + offset:
                os.system("rsync --remove-source-files " + fil + " " + ltmem + "/" + fil[len(fetch_path)+1:-21 - offset] + "/" + fil[len(fetch_path)+5:-19 - offset])
            elif len(fil) == len(fetch_path) + 29 + offset:
                os.system("rsync --remove-source-files " + fil + " " + ltmem + "/" + fil[len(fetch_path)+1:-24 - offset] + "/" + fil[len(fetch_path)+5:-22 - offset])
            elif len(fil) == len(fetch_path) + 31 + offset:
                os.system("rsync --remove-source-files " + fil + " " + ltmem + "/" + fil[len(fetch_path)+1:-26 - offset] + "/" + fil[len(fetch_path)+5:-24 - offset])
            else:
                print(str(len(fil)) + '=str_length :  File Name NOT Formated Correctly!')
 
###############
## Control Flow
###############
    print(str(len(dif)))
    if len(dif) > 10000:
        large_yn = input('More than 10k Files Are Missing! Do You Still Want to Continue? (y/n):')
        if large_yn.lower() in ['y','yes']: 
            fetch_path = str(base_dir + '/' + lang + '-dl/')
            print('This May Take a While! Starting Download...')
        else: sys.exit('Update Canceled!')
    elif 10000 > len(dif) >= 1:
        fetch_path = str(ram_dir + "/" + lang + '-dl/')
    elif len(dif) == 0:
        print('Source Files Up to Date!')
        return
    fetch()
    convert()
    sort()
    print(lang.upper() + ' Dif Complete!')

###############

def remove_data():
    rm_dir('/tmp/gdelt-dif', 'r')
    rm_dir(base_dir + '/english-dl', 'r')
    rm_dir(base_dir + '/translation-dl', 'r')
    app_files = {base_dir + '/404-english.txt', base_dir + '/404-translation.txt', base_dir + '/master-english-previous.txt', base_dir + '/master-translation-previous.txt', base_dir + '/path-english.txt', base_dir + '/path-translation.txt'}
    for file_path in app_files:
        rm_dir(file_path, 'r')
    sys.exit('All Files Removed!')

###############

parser = argparse.ArgumentParser(description="This script is used to automatically maintain a repository for the Gdelt Project. This script requires: gnu rsync, gnu parallel, linux unzip, gnu gzip, linux touch, linux find, python wget, python requests. Delete /var/tmp/gdelt-dif & /tmp/gdelt-dif to force a fresh install.")
parser.add_argument("-d", "--dif", action='store_true', help="Dif and Download BOTH Gdelt Streams.")
parser.add_argument("-de", "--dif_english", action='store_true', help="Dif and Download the Entire Gdelt English Stream.")
parser.add_argument("-dt", "--dif_translation", action='store_true', help="Dif and Download the Entire Gdelt Translation Stream.")
parser.add_argument("-r", "--retry", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in BOTH Streams.")
parser.add_argument("-re", "--retry_english", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in English Stream.")
parser.add_argument("-rt", "--retry_translation", action='store_true', help="Force a 404-Retry on All Missing or Dead Files in Translation Stream.")
parser.add_argument("-rm", "--remove", action='store_true', help="Remove All Persistence Files. AKA-Uninstall")
parser.add_argument("-i", "--install", action='store_true', help="Install All Needed Packages.")
arguments = parser.parse_args()
##
if arguments.install:
    install_packages()
if arguments.dif:
    gdelt_dif('english')
    print('------------------')
    gdelt_dif('translation')
elif arguments.dif_english:
    gdelt_dif('english')
elif arguments.dif_translation:
    gdelt_dif('translation')
##
elif arguments.retry:
    gdelt_dif('english')
    print('------------------')
    gdelt_dif('translation')
elif arguments.retry_english:
    retry('english')
elif arguments.retry_translation:
    retry('translation')
##
elif arguments.remove:
    remove_data()
else:
    print('Missing Argument! Use --help to See All Arguments.')
