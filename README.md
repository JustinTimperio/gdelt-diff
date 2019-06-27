# gdelt-dif
This script is designed to download, convert, and sort Gdelt source files automatically. https://www.gdeltproject.org/data.html#rawdatafiles

To maintain consistency across our data sets, these files are converted upon download from .zip to .gz 
Due to the large size of the GDELT source files extra care is taken to ensure that as much file proccessing as possible is done in ram.
After a fresh install is performed the script runs automatically every 60 mins, fetching any missing files then exiting. Gdelt-dif.py itself is run via systemd.service and systemd.timer but can be used manually.

_Install Instruction_
NOTE: This script is designed for large servers with a MINIMUM +1TB OS Drive, +10TB of storage, and +250GB of RAM.
`sudo mkdir /var/app`
`cd /var/app && git clone https://github.com/JustinTimperio/gdelt-dif.git`
`sudo python3 /var/app/gdelt-dif/core/gdelt_dif-v2.py -i`
