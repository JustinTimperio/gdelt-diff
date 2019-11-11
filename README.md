# GDELT-Diff - _Alpha_  
This script is designed to download, convert, and sort GDELT source files automatically into a user-specified path. https://www.gdeltproject.org/data.html#rawdatafiles  
  
## Description  
To maintain consistency across my personal datasets, these files are converted upon download from .zip to .gz. Due to the large size of the GDELT source files extra care is taken to ensure that as much file processing as possible is done in ram.  
After a fresh install is performed the script runs automatically every 60 mins, fetching any missing files, converting them from .zip to .gz, then finally sorting them into folders in long-term storage. gdelt-diff-v2.py itself is run via systemd.service and systemd.timer but can be used manually. Additionally, an extremely small and fast script is provided to maintain a copy of the streams' most recent files in /tmp/gdelt-live.  
  
## Install Instructions  
_NOTE: This script is designed for large servers with a MINIMUM +1TB OS Drive, +10TB of storage, and +128GB of RAM. Please consider how many files you need to sync before running._  
  
1. Ensure that you have a pre-existing directory of GDELT files placed in folders organized by Year then Month. (/2009/05/) While it is possible for the diff process to download and organize the entire stream, it is NOT advised due to the tremendous disk size required for the os drive. It is possible though to update well over 200k files including missing files anywhere in the stream.  
2. `sudo mkdir /var/app && sudo chmod 777 /var/app`  
3. `cd /var/app && git clone https://github.com/JustinTimperio/gdelt-diff.git`  
4. `sudo python3 /var/app/gdelt-diff/core/gdelt_diff-v2.py -i -d`  
5. After the download is complete, be sure to start the freshly enabled systemd.timers placed in /etc/systemd.  
`sudo systemctl start gdelt-diff.timer gdelt-live.timer`  
  

## CLI-Tool
When using the script manually simply stop the systemd.timers and call gdelt-diff-v2.py manually:

`sudo python3 /var/app/gdelt-diff/core/gdelt-diff-v2.py -d`

To unistall the app use:

`sudo python3 /var/app/gdelt-diff/core/gdelt-diff-v2.py -remove`

To sync only one stream use:

`sudo python3 /var/app/gdelt-diff/core/gdelt-diff-v2.py -diff_english`
or
`sudo python3 /var/app/gdelt-diff/core/gdelt-diff-v2.py -diff_translation`

To force a fetch of all 404'ed urls use:

`sudo python3 /var/app/gdelt-diff/core/gdelt-diff-v2.py -retry`

To see all options and usage use:

`sudo python3 /var/app/gdelt-diff/core/gdelt-diff-v2.py -help`


				
If you experience any issues or bugs please submit an issue. Thanks!
