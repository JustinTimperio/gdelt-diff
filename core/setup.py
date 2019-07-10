#### Setup scripts for gdelt_diff
from global_defuns import *

###############

def install_packages():
    os_name = os_distro() 
    pip_install('wget requests')
    pacman_install('rsync parallel unzip gzip')
    if 'arch' in os_name.lower():
        pacman('rsync parallel unzip gzip')
    elif 'debian' or 'ubuntu' in os_name.lower():
        apt('rsync parallel unzip gzip')
    elif 'fedora' or 'redhat' in os_name.lower():
        yum('rsync parallel unzip gzip')
    else: 
        sys.exit('Automated package installs for ' + os_name + ' are not yet supported.')
    
    ## copy deamon files into /etc/systemd 
    os.system('sudo cp ' + base_dir + '/core/daemons/* /etc/systemd/system/')
    os.system('sudo systemctl daemon-reload && sudo systemctl enable gdelt-diff.timer gdelt-live.timer')

###############

def remove_data():
    rm_dir(ram_dir, 'r')
    rm_dir(base_dir + '/english-dl', 'r')
    rm_dir(base_dir + '/translation-dl', 'r')
    app_files = {base_dir + '/404-english.txt', base_dir + '/404-translation.txt', base_dir + '/master-english-previous.txt', base_dir + '/master-translation-previous.txt', base_dir + '/path-english.txt', base_dir + '/path-translation.txt'}
    for file_path in app_files:
        rm_dir(file_path, 'r')
    sys.exit('All Files Removed!')

###############
