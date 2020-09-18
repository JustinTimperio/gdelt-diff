# GDELT-Diff
  
## Abstract
This small tool is designed to automate the download, orginization, and storage of [GDELT source files](https://www.gdeltproject.org/data.html#rawdatafiles). GDELT-Diff includes a deamon that runs every 60 mins fetching any new or missing files and sorts them into folders for easy storage. Additionally, an extremely lightweight tool is provided to maintain a copy of only the streams most recent files in /tmp/gdelt-live. This is for anyone doing real-time analysis of the GDELT and doesn't require a full copy of the source files.

## What is the GDELT?
The GDELT Project is the largest, most comprehensive, and highest resolution open database of human society ever created. Just the 2015 data alone records nearly three quarters of a trillion emotional snapshots and more than 1.5 billion location references, while its total archives span more than 215 years, making it one of the largest open-access spatio-temporal datasets in existance and pushing the boundaries of "big data" study of global human society. Advanced users and those with unique use cases can download the entire underlying event and graph datasets in CSV format. Deep technical knowledge and extensive experience working with large datasets is required to make use of these datasets, with the GKG alone requiring more than 2.5TB of storage compressed.

To learn more about the GDELT and the records that make up its database, check out the [offical documentaion page](https://www.gdeltproject.org/data.html#documentation).
  
## Install Instructions  
_NOTE: This utlity is designed for large servers with a MINIMUM +100GB OS Drive, +10TB of storage, and +32GB of RAM. Also please consider how many files you need to sync before running._  
  
1. If you have a pre-existing directory of GDELT files, **YOU MUST** ensure that files are organized into folders by stream, year and month(`/path/stream/2015/05/`) 
2. Install GDELT-Diff:
```
curl https://raw.githubusercontent.com/JustinTimperio/gdelt-diff/master/build/install.sh | bash
```
3. Edit Your User Config File With The Paths You Wish to Use:
```
sudo vi /etc/gdelt-diff/config
```
4. Manually Run GDELT-Diff to Ensure Everything is Setup:
```
sudo gdelt-diff -d
```
5. Enable Automatic Downloads With:
```
sudo systemctl enable gdelt-diff.timer
```
6. Enable Automatic Live Downloads With:
```
sudo systemctl enable gdelt-live.timer
```

## Uninstall GDELT-Diff:
**This will NOT remove the files you have downloaded**
```
sudo /opt/gdelt-diff/build/remove.sh
```

## CLI-Tool
When using the utlity manually simply stop the systemd.timers and call gdelt-diff manually:
```
sudo gdelt-diff --diff
```

To sync only one stream use:
```
sudo gdelt-diff --diff_english
```
OR
```
sudo gdelt-diff --diff_translation
```

To force a fetch of  404'd URLs use:
```
sudo gdelt-diff --retry
```

To refresh the database of synced files:
```
sudo gdelt-diff --refresh_database
```

To see all options and flags:
```
sudo gdelt-diff -help
```
