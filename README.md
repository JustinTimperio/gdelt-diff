# GDELT-Diff
  
## Abstract
This small tool is designed to automate the download, orginization, and storage of [GDELT source files](https://www.gdeltproject.org/data.html#rawdatafiles). GDELT-Diff includes a deamon that runs every 60 mins fetching any new or missing files and sorts them into folders for easy storage. Additionally, an extremely lightweight tool is provided to maintain a copy of only the streams most recent files in /tmp/gdelt-live. This is targeted for anyone doing real-time analysis of the GDELT and doesn't require a full copy of the source files.

## What is the GDELT?
The GDELT Project is the largest, most comprehensive, and highest resolution open database of human society ever created. Just the 2015 data alone records nearly three quarters of a trillion emotional snapshots and more than 1.5 billion location references, while its total archives span more than 215 years, making it one of the largest open-access spatio-temporal datasets in existance and pushing the boundaries of "big data" study of global human society. Advanced users and those with unique use cases can download the entire underlying event and graph datasets in CSV format. Deep technical knowledge and extensive experience working with large datasets is required to make use of these datasets, with the 2015 GKG alone requiring more than 2.5TB.
To learn more about the GDELT and the records that make up its database, check out the [offical documentaion page](https://www.gdeltproject.org/data.html#documentation).
  
## Install Instructions  
_NOTE: This utlity is designed for large servers with a MINIMUM +1TB OS Drive, +30TB of storage, and +64GB of RAM. Also please consider how many files you need to sync before running._  
  
1. If you have a pre-existing directory of GDELT files, YOU MUST ensure that files are organized into folders by Year and Month(`/path/to/stream/2015/05/`) While it is possible for this utility to process, download and organize the entire stream, it will take a very long time depending on your internet.
2. Install GDELT-Diff along with its dependencies: `curl rawurlhere | sudo bash`
3. To start a full sync after install: `sudo gdelt-diff -full`
4. To maintain a live copy of the most recent files: `sudo gdelt-diff -enable_live` 


## CLI-Tool
When using the utlity manually simply stop the systemd.timers and call gdelt-diff-v2.py manually:

```
sudo gdelt-diff -full_diff
```

To uninstall the utility:
_(This will NOT remove the files you have downloaded)_
```
sudo gdelt-diff -remove

```

To sync only one stream use:

```
sudo gdelt-diff -english
```
OR
```
sudo gdelt-diff -translation
```

To force a fetch of all 404'd urls use:

```
sudo gdelt-diff -retry
```

To see all options and flags:

```
sudo gdelt-diff -help
```
