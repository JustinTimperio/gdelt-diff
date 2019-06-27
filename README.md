# GDELT-Diff
This script is designed to download, convert, and sort GDELT source files automatically. https://www.gdeltproject.org/data.html#rawdatafiles

## Description
To maintain consistency across our datasets, these files are converted upon download from .zip to .gz. 
Due to the large size of the GDELT source files extra care is taken to ensure that as much file proccessing as possible is done in ram.
After a fresh install is performed the script runs automatically every 60 mins, fetching any missing files then exiting. Gdelt-diff.py itself is run via systemd.service and systemd.timer but can be used manually.

## Install Instructions
_NOTE: This script is designed for large servers with a MINIMUM +1TB OS Drive, +10TB of storage, and +250GB of RAM._
Additionally this script assumes you are not a pleb and are using Arch Linux.

1. `sudo mkdir /var/app && sudo chmod 777 /var/app`
2. `cd /var/app && git clone https://github.com/JustinTimperio/gdelt-diff.git`
3. `sudo python3 /var/app/gdelt-diff/core/gdelt_diff-v2.py -i -d`
4. After the download is complete, be sure to start the freshly enabled systemd.timers placed in /etc/systemd.
