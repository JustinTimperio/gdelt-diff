# GDELT-Diff
This script is designed to download, convert, and sort GDELT source files automatically into a user specified path. https://www.gdeltproject.org/data.html#rawdatafiles

## Description
To maintain consistency across our datasets, these files are converted upon download from .zip to .gz. 
Due to the large size of the GDELT source files extra care is taken to ensure that as much file proccessing as possible is done in ram.
After a fresh install is performed the script runs automatically every 60 mins, fetching any missing files then exiting. Gdelt-diff.py itself is run via systemd.service and systemd.timer but can be used manually.
Additionally an extreamly small and fast script is provided to maintain a copy of the streams most recent files in /tmp/gdelt-live.

## Install Instructions
_NOTE: This script is designed for large servers with a MINIMUM +1TB OS Drive, +10TB of storage, and +250GB of RAM._
Additionally this script assumes you are not a pleb and are using Arch Linux.

1. Ensure that you have a pre-existing directory of GDELT files placed in folders orginized by Year then Month. (/2009/05/) While it is possible for the diff process to download and orginize the entire stream, it is NOT advised due to the tremedous disksize required for the os drive. It is possible though to update well over 200k files including any missing files.
2. `sudo mkdir /var/app && sudo chmod 777 /var/app`
3. `cd /var/app && git clone https://github.com/JustinTimperio/gdelt-diff.git`
4. `sudo python3 /var/app/gdelt-diff/core/gdelt_diff-v2.py -i -d`
5. After the download is complete, be sure to start the freshly enabled systemd.timers placed in /etc/systemd.
5. `sudo systemctl start gdelt-diff.timer gdelt-live.timer`
