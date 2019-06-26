# gdelt-dif
This script is designed to download, convert, and sort Gdelt source files automatically. https://www.gdeltproject.org/data.html#rawdatafiles

To maintain consistency across our data sets, these files are converted upon download from .zip to .gz 
Due to the large size of the GDELT source files extra care is taken to ensure that as much file proccessing as possible is done in ram.
NOTE: This script is designed for large servers with a MINIMUM of +1TB OS Drive, +10TB of storage, and +250GB of RAM.
This script is designed to be 100% automated after a fresh install is performed. The script is run via systemd.service and systemd.timer but can be used manually.
